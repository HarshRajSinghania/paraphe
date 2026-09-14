"""Tap claims: owner + live version on an open card, else refuse."""

from __future__ import annotations


class ClaimRefused(Exception):
    """A Telegram callback did not become a Tap."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class NullTelegramPort:
    def edit_and_strip(self, card_id: str, version: int) -> None:
        return None


class FakeTelegramPort:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []
        self.fail = False

    def edit_and_strip(self, card_id: str, version: int) -> None:
        if self.fail:
            raise RuntimeError("edit failed")
        self.calls.append((card_id, version))
