"""Console destination: the card is printed where the owner is looking.

The same two-method contract the tap adapter implements, with no network call
and no external service, so a first run can exercise the whole loop locally.
"""

from __future__ import annotations

from typing import Any, Callable

ANSWER_PATH = "/answer"


class ConsoleDestination:
    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 0,
        write: Callable[[str], None] = print,
        answer_path: str = ANSWER_PATH,
    ) -> None:
        self.host = host
        self.port = port
        self.write = write
        self.answer_path = answer_path

    def notify(self, payload: dict[str, Any]) -> None:
        if payload.get("kind") == "notify":
            self.write(f"[paraphe] {payload.get('title', '')}: {payload.get('message') or ''}")
            return
        request_id = str(payload.get("request_id") or "")
        version = payload.get("version")
        if not request_id or version is None:
            return
        lines = [
            f"[paraphe] card {request_id} (version {version}) is waiting for you",
            f"  kind: {payload.get('kind')}   risk: {payload.get('risk')}   priority: {payload.get('priority')}",
        ]
        for label, key in (("title", "title"), ("question", "question"), ("details", "details"), ("context", "context")):
            value = payload.get(key)
            if value:
                lines.append(f"  {label}: {value}")
        choices = payload.get("choices") or []
        if choices:
            lines.append(f"  choices: {', '.join(str(choice) for choice in choices)}")
        if payload.get("recommendation"):
            lines.append(f"  recommendation: {payload['recommendation']}")
        if payload.get("consequence"):
            lines.append(f"  if ignored: {payload['consequence']}")
        lines.append(
            "  answer with: curl -s -X POST "
            f"http://{self.host}:{self.port}{self.answer_path} "
            '-H "Authorization: Bearer $PARAPHE_OWNER_ANSWER_TOKEN" '
            f'--data \'{{"request_id": "{request_id}", "version": {version}, "choice": "<your answer>"}}\''
        )
        self.write("\n".join(lines))

    def edit_and_strip(self, card_id: str, version: int) -> None:
        self.write(f"[paraphe] card {card_id} (version {version}) closed")
