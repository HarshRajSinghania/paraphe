"""Fail-closed setup for the Inbox."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from . import store as _store

DEFAULT_TTL_SECONDS = 14400
FLOOR_TTL_SECONDS = 900
MAX_TTL_SECONDS = 2_592_000

ENV_BOT_TOKEN = "PARAPHE_BOT_TOKEN"
ENV_OWNER_ID = "PARAPHE_OWNER_TELEGRAM_ID"
ENV_DEFAULT_TTL = "PARAPHE_DEFAULT_TTL_SECONDS"
ENV_FLOOR_TTL = "PARAPHE_FLOOR_TTL_SECONDS"
ENV_MCP_BEARER = "PARAPHE_MCP_CREATE_BEARER"
ENV_STORE_PATH = "PARAPHE_STORE_PATH"
ENV_ANSWER_TOKEN = "PARAPHE_OWNER_ANSWER_TOKEN"

_UNSET = object()


class SetupError(Exception):
    """Start refused because required setup is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    owner_telegram_id: int | None
    default_ttl_seconds: int
    floor_ttl_seconds: int
    bot_token: str
    mcp_create_bearer: str
    owner_answer_token: str
    store_path: Path

    def __repr__(self) -> str:
        return (
            f"Settings(owner_telegram_id={self.owner_telegram_id!r}, "
            f"default_ttl_seconds={self.default_ttl_seconds!r}, "
            f"floor_ttl_seconds={self.floor_ttl_seconds!r})"
        )


def _strip(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _env(environ: Mapping[str, str], key: str) -> object:
    if key not in environ:
        return _UNSET
    stripped = _strip(environ[key])
    if stripped is None:
        return _UNSET
    return stripped


def _pick(file_val: object, env_val: object) -> object:
    if env_val is _UNSET:
        return file_val
    return env_val


def _read_file(config_path: Path | str | None) -> dict:
    if config_path is None:
        return {}
    path = Path(config_path)
    if not path.is_file():
        return {}
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise SetupError("config file is invalid") from exc
    if not isinstance(data, dict):
        raise SetupError("config file is invalid")
    return data


def _parse_int(name: str, raw: object, *, default: int | None = None) -> int:
    if raw is None or raw == "":
        if default is None:
            raise SetupError(f"{name} is required")
        return default
    if isinstance(raw, bool):
        raise SetupError(f"{name} is invalid")
    if isinstance(raw, int):
        return raw
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError):
        raise SetupError(f"{name} is invalid") from None


def _parse_ttl(name: str, value: int) -> int:
    if value < FLOOR_TTL_SECONDS:
        raise SetupError(f"{name} is below floor")
    if value > MAX_TTL_SECONDS:
        raise SetupError(f"{name} is above max")
    return value


def resolve_store_path(configured: object) -> Path:
    """Resolve the data location once, so the checked path is the opened path.

    An explicit location is honoured. The default refuses when a store exists at
    the location earlier releases used, so an upgrade never silently starts a
    second, empty store.
    """
    text = _strip(configured)
    if text:
        return Path(text).expanduser()
    target = _store.default_store_path()
    legacy = _store.LEGACY_STORE_PATH
    if not _store.store_exists(target) and _store.store_exists(legacy):
        raise SetupError(
            f"no store at {target}; a store exists at {legacy}. "
            f"Set store_path to {legacy} to keep using it, or start from an empty location."
        )
    return target


def load_settings(
    config_path: Path | str | None = None,
    environ: Mapping[str, str] | None = None,
) -> Settings:
    environ = {} if environ is None else environ
    data = _read_file(config_path)

    token = _strip(_pick(data.get("bot_token"), _env(environ, ENV_BOT_TOKEN)))
    owner_raw = _pick(data.get("owner_telegram_id"), _env(environ, ENV_OWNER_ID))
    bearer = _strip(_pick(data.get("mcp_create_bearer"), _env(environ, ENV_MCP_BEARER)))
    default_raw = _pick(data.get("default_ttl_seconds"), _env(environ, ENV_DEFAULT_TTL))
    floor_raw = _pick(data.get("floor_ttl_seconds"), _env(environ, ENV_FLOOR_TTL))
    store_raw = _pick(data.get("store_path"), _env(environ, ENV_STORE_PATH))

    if not bearer:
        raise SetupError("mcp create bearer is required")

    # The phone destination is the bot token's presence. Without it the run is
    # local: the console destination prints the card and the owner answers
    # through the answer path, which then becomes the only owner identity.
    answer_token = _strip(_pick(data.get("owner_answer_token"), _env(environ, ENV_ANSWER_TOKEN))) or ""
    if answer_token and answer_token == bearer:
        raise SetupError("the answer credential must differ from the create credential")

    owner_id: int | None = None
    if token:
        owner_id = _parse_int("owner telegram id", owner_raw)
        if owner_id <= 0:
            raise SetupError("owner telegram id is invalid")
    elif not answer_token:
        raise SetupError(
            "no phone destination is configured and there is no answer credential: "
            "set owner_answer_token to answer decisions locally"
        )
    default_ttl = _parse_ttl(
        "default ttl",
        _parse_int("default ttl", default_raw, default=DEFAULT_TTL_SECONDS),
    )
    floor_ttl = _parse_ttl(
        "floor ttl",
        _parse_int("floor ttl", floor_raw, default=FLOOR_TTL_SECONDS),
    )
    if default_ttl < floor_ttl:
        raise SetupError("default ttl is below floor")
    return Settings(
        owner_telegram_id=owner_id,
        default_ttl_seconds=default_ttl,
        floor_ttl_seconds=floor_ttl,
        bot_token=token,
        mcp_create_bearer=bearer,
        owner_answer_token=answer_token,
        store_path=resolve_store_path(store_raw),
    )
