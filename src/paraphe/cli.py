"""The shell-side half of the return path: ``paraphe ask`` and ``paraphe wait``.

A runner without tool bindings creates a card and prints its request id, then
backgrounds ``paraphe wait``; the owner's tap ends the wait and the runner
reads the answer from the command's stdout. It speaks the same Streamable
HTTP surface every other client speaks, and it is standard library only.
"""

from __future__ import annotations

import json
import os
import sys
import time
import tomllib
import urllib.error
import urllib.request
import uuid
from typing import TextIO

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8787

WINDOW_SECONDS = 60.0
REQUEST_TIMEOUT = WINDOW_SECONDS + 30.0
TRANSPORT_ATTEMPTS = 20
TRANSPORT_BACKOFF_SECONDS = 3.0

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NOT_ANSWERABLE = 3
EXIT_UNKNOWN = 4

UNKNOWN_REQUEST_ERROR = "unknown request_id"

CLI_USAGE = """\
paraphe ask QUESTION [options]      create a card and print the request id
  --context TEXT      extra context for the owner
  --choice TEXT       one choice (repeatable, up to 4)
  --external-id ID    the caller's stable key (default: generated)
  --agent-name NAME   which agent asks
  --url URL           service endpoint (default: PARAPHE_MCP_URL, then
                      http://PARAPHE_MCP_HOST:PARAPHE_MCP_PORT/mcp)

paraphe wait REQUEST_ID [--url URL]
  blocks until the card is answered or can no longer be answered, then
  prints the answered envelope as JSON. Exit 0 answered, 3 expired or not
  answerable, 4 unknown request id.

The create bearer comes from PARAPHE_MCP_CREATE_BEARER, or from
mcp_create_bearer in the configured file (PARAPHE_CONFIG_PATH, or
./paraphe.toml). A secret is never passed on the command line.
"""


class CliError(Exception):
    """The command cannot proceed: missing setup, unreachable service."""


class ToolError(Exception):
    """The service refused the tool call."""


def _endpoint(explicit: str | None) -> str:
    if explicit and explicit.strip():
        return explicit.strip()
    url = os.environ.get("PARAPHE_MCP_URL")
    if url and url.strip():
        return url.strip()
    host = os.environ.get("PARAPHE_MCP_HOST") or DEFAULT_HOST
    port = os.environ.get("PARAPHE_MCP_PORT") or str(DEFAULT_PORT)
    return f"http://{host}:{port}/mcp"


def _bearer() -> str | None:
    token = os.environ.get("PARAPHE_MCP_CREATE_BEARER")
    if token and token.strip():
        return token.strip()
    path = os.environ.get("PARAPHE_CONFIG_PATH") or "paraphe.toml"
    try:
        with open(path, "rb") as handle:
            data = tomllib.load(handle)
    except (OSError, ValueError):
        return None
    value = data.get("mcp_create_bearer") if isinstance(data, dict) else None
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _call(url: str, bearer: str, tool: str, arguments: dict[str, object]) -> object:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise CliError(f"the service refused the call (HTTP {exc.code})") from None
    except (urllib.error.URLError, OSError, ValueError):
        raise CliError("the service is unreachable") from None
    if not isinstance(body, dict):
        raise CliError("the service returned an invalid response")
    result = body.get("result")
    if not isinstance(result, dict):
        error = body.get("error")
        message = error.get("message") if isinstance(error, dict) else None
        raise CliError(str(message or "the service returned an invalid response"))
    content = result.get("content") or []
    text = content[0].get("text") if content and isinstance(content[0], dict) else None
    if result.get("isError"):
        raise ToolError(str(text or "tool error"))
    if text is None:
        raise CliError("the service returned an invalid response")
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        raise CliError("the service returned an invalid response") from None


def ask(
    question: str,
    *,
    context: str | None = None,
    choices: list[str] | None = None,
    external_id: str | None = None,
    agent_name: str | None = None,
    url: str | None = None,
    out: TextIO | None = None,
    err: TextIO | None = None,
) -> int:
    out = sys.stdout if out is None else out
    err = sys.stderr if err is None else err
    bearer = _bearer()
    if not bearer:
        print(
            "paraphe: no create bearer: set PARAPHE_MCP_CREATE_BEARER or mcp_create_bearer",
            file=err,
        )
        return EXIT_ERROR
    arguments: dict[str, object] = {
        "question": question,
        "external_id": external_id or f"cli-{uuid.uuid4().hex}",
    }
    if context:
        arguments["context"] = context
    if choices:
        arguments["choices"] = choices
    if agent_name:
        arguments["agent_name"] = agent_name
    try:
        created = _call(_endpoint(url), bearer, "ask_question", arguments)
    except (CliError, ToolError) as exc:
        print(f"paraphe: {exc}", file=err)
        return EXIT_ERROR
    if not isinstance(created, dict) or not created.get("request_id"):
        print("paraphe: the service returned an invalid response", file=err)
        return EXIT_ERROR
    print(created["request_id"], file=out)
    return EXIT_OK


def wait_for_answer(
    request_id: str,
    *,
    url: str | None = None,
    window: float = WINDOW_SECONDS,
    out: TextIO | None = None,
    err: TextIO | None = None,
) -> int:
    out = sys.stdout if out is None else out
    err = sys.stderr if err is None else err
    bearer = _bearer()
    if not bearer:
        print(
            "paraphe: no create bearer: set PARAPHE_MCP_CREATE_BEARER or mcp_create_bearer",
            file=err,
        )
        return EXIT_ERROR
    endpoint = _endpoint(url)
    window = max(0.0, min(float(window), WINDOW_SECONDS))
    failures = 0
    while True:
        try:
            envelope = _call(
                endpoint,
                bearer,
                "get_response",
                {"request_id": request_id, "wait_seconds": window},
            )
            failures = 0
        except CliError as exc:
            failures += 1
            if failures >= TRANSPORT_ATTEMPTS:
                print(f"paraphe: {exc}", file=err)
                return EXIT_ERROR
            time.sleep(TRANSPORT_BACKOFF_SECONDS)
            continue
        except ToolError as exc:
            print(f"paraphe: {exc}", file=err)
            if UNKNOWN_REQUEST_ERROR in str(exc):
                return EXIT_UNKNOWN
            return EXIT_ERROR
        if not isinstance(envelope, dict):
            print("paraphe: the service returned an invalid response", file=err)
            return EXIT_ERROR
        status = envelope.get("status")
        if status in ("answered", "acknowledged"):
            print(json.dumps(envelope), file=out)
            return EXIT_OK
        if status in ("expired", "cancelled"):
            print(f"paraphe: the card is {status}", file=err)
            return EXIT_NOT_ANSWERABLE
        # Anything else is still open: hold another bounded window.


def _parse_options(
    args: list[str], allowed: set[str], repeatable: set[str]
) -> tuple[dict[str, list[str]], list[str]]:
    values: dict[str, list[str]] = {}
    positionals: list[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        if token.startswith("--"):
            name = token[2:]
            if name not in allowed and name not in repeatable:
                raise CliError(f"unknown option --{name}")
            if index + 1 >= len(args):
                raise CliError(f"--{name} needs a value")
            values.setdefault(name, []).append(args[index + 1])
            index += 2
        else:
            positionals.append(token)
            index += 1
    return values, positionals


def main(argv: list[str]) -> int:
    args = list(argv)
    if not args or args[0] in {"-h", "--help", "help"}:
        print(CLI_USAGE, end="")
        return EXIT_OK
    command = args[0]
    rest = args[1:]
    if "--help" in rest or "-h" in rest:
        print(CLI_USAGE, end="")
        return EXIT_OK
    try:
        if command == "ask":
            options, positionals = _parse_options(
                rest,
                {"context", "external-id", "agent-name", "url"},
                {"choice"},
            )
            if len(positionals) != 1:
                raise CliError("ask needs exactly one QUESTION")
            return ask(
                positionals[0],
                context=(options.get("context") or [None])[0],
                choices=options.get("choice"),
                external_id=(options.get("external-id") or [None])[0],
                agent_name=(options.get("agent-name") or [None])[0],
                url=(options.get("url") or [None])[0],
            )
        if command == "wait":
            options, positionals = _parse_options(rest, {"url"}, set())
            if len(positionals) != 1:
                raise CliError("wait needs exactly one REQUEST_ID")
            return wait_for_answer(
                positionals[0],
                url=(options.get("url") or [None])[0],
            )
    except CliError as exc:
        print(f"paraphe: {exc}", file=sys.stderr)
        return EXIT_ERROR
    print(f"paraphe: unknown command {command!r}", file=sys.stderr)
    return EXIT_ERROR
