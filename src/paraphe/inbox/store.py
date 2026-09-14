"""Store location and SQLite card payload for the Inbox."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

STORE_DIR_NAME = "paraphe"
STORE_FILENAME = "inbox.sqlite"
STORE_MODE = 0o600
DATA_DIR_MODE = 0o700
# The location earlier releases used, and the one an existing deployment still
# configures. Resolving somewhere else while this one holds a store refuses
# rather than starting a second, empty store.
LEGACY_STORE_PATH = Path("/var/lib/paraphe/inbox.sqlite")


def default_data_dir() -> Path:
    """The platform's per-user data directory for this product."""
    base = os.environ.get("XDG_DATA_HOME")
    if base and base.strip():
        return Path(base).expanduser() / STORE_DIR_NAME
    return Path.home() / ".local" / "share" / STORE_DIR_NAME


def default_store_path() -> Path:
    return default_data_dir() / STORE_FILENAME


def store_exists(path: Path) -> bool:
    """True when a store file is there. An unreadable path has no store to strand."""
    try:
        return path.is_file()
    except OSError:
        return False


def _setup_error(message: str) -> Exception:
    from .config import SetupError

    return SetupError(message)


class Store:
    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path else default_store_path()
        self._conn: sqlite3.Connection | None = None

    @classmethod
    def prepare(cls, path: Path | str) -> Path:
        target = Path(path)
        parent = target.parent
        if not parent.exists():
            try:
                parent.mkdir(parents=True, exist_ok=True, mode=DATA_DIR_MODE)
                os.chmod(parent, DATA_DIR_MODE)
            except OSError as exc:
                raise _setup_error(f"data directory is not usable: {parent}") from exc
        try:
            target.touch(exist_ok=True)
            target.chmod(STORE_MODE)
        except OSError as exc:
            raise _setup_error(f"store file is not usable: {target}") from exc
        return target

    def open(self) -> None:
        self.prepare(self.path)
        # ponytail: serialized sqlite, split connections if writers contend
        conn = sqlite3.connect(str(self.path), check_same_thread=False)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS cards ("
            "request_id TEXT PRIMARY KEY, "
            "payload TEXT NOT NULL)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notifications ("
            "external_id TEXT PRIMARY KEY)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS durable_state ("
            "key TEXT PRIMARY KEY, "
            "value TEXT NOT NULL)"
        )
        conn.commit()
        self._conn = conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def load_cards(self) -> list[dict[str, Any]]:
        if self._conn is None:
            raise RuntimeError("store is not open")
        rows = self._conn.execute("SELECT payload FROM cards").fetchall()
        return [json.loads(row[0]) for row in rows]

    def save_card(self, payload: dict[str, Any]) -> None:
        if self._conn is None:
            raise RuntimeError("store is not open")
        self._conn.execute(
            "INSERT OR REPLACE INTO cards (request_id, payload) VALUES (?, ?)",
            (payload["request_id"], json.dumps(payload)),
        )
        self._conn.commit()

    def load_notification_ids(self) -> list[str]:
        if self._conn is None:
            raise RuntimeError("store is not open")
        rows = self._conn.execute("SELECT external_id FROM notifications").fetchall()
        return [str(row[0]) for row in rows]

    def save_notification_id(self, external_id: str) -> None:
        if self._conn is None:
            raise RuntimeError("store is not open")
        self._conn.execute(
            "INSERT OR REPLACE INTO notifications (external_id) VALUES (?)",
            (external_id,),
        )
        self._conn.commit()

    def delete_notification_id(self, external_id: str) -> None:
        if self._conn is None:
            raise RuntimeError("store is not open")
        self._conn.execute(
            "DELETE FROM notifications WHERE external_id = ?",
            (external_id,),
        )
        self._conn.commit()

    def load_telegram_next_offset(self) -> int | None:
        if self._conn is None:
            raise RuntimeError("store is not open")
        row = self._conn.execute(
            "SELECT value FROM durable_state WHERE key = ?",
            ("telegram_next_offset",),
        ).fetchone()
        if row is None:
            return None
        try:
            offset = int(row[0])
        except (TypeError, ValueError):
            raise RuntimeError("telegram next offset is invalid") from None
        if offset < 0:
            raise RuntimeError("telegram next offset is invalid")
        return offset

    def save_telegram_next_offset(self, offset: int) -> None:
        if self._conn is None:
            raise RuntimeError("store is not open")
        if offset < 0:
            raise RuntimeError("telegram next offset is invalid")
        self._conn.execute(
            "INSERT OR REPLACE INTO durable_state (key, value) VALUES (?, ?)",
            ("telegram_next_offset", str(offset)),
        )
        self._conn.commit()
