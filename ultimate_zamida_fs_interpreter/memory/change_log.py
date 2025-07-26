"""SQLite change log for recording arbitrary entries.

This class logs textual entries to a SQLite database.  It provides a
generator to iterate over recorded entries in order.  If the log
database does not exist it is created automatically.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class ChangeLog:
    """SQLite‑backed log of string entries."""

    def __init__(self, path: str) -> None:
        self.path = path
        self._ensure()

    def _ensure(self) -> None:
        p = Path(self.path)
        p.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY AUTOINCREMENT, entry TEXT)"
            )
            conn.commit()
        finally:
            conn.close()

    def log(self, entry: str) -> None:
        """Append a new entry to the log."""
        conn = sqlite3.connect(self.path)
        try:
            conn.execute("INSERT INTO log (entry) VALUES (?)", (entry,))
            conn.commit()
        finally:
            conn.close()

    def entries(self):
        """Yield dictionaries for each logged entry in insertion order."""
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.execute("SELECT entry FROM log ORDER BY id")
            for (entry,) in cur.fetchall():
                yield {"entry": entry}
        finally:
            conn.close()