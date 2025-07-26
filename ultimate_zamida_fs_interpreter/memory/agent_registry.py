"""Simple SQLite‑backed registry of available agents.

The registry stores agent names in a SQLite database.  It exposes
methods to register new agents and list existing ones.  The file is
created with an empty table if it does not exist.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class AgentRegistry:
    """SQLite registry for agent names."""

    def __init__(self, path: str) -> None:
        self.path = path
        # Ensure the database and table exist
        self._ensure_db()

    def _ensure_db(self) -> None:
        p = Path(self.path)
        p.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS agents (name TEXT PRIMARY KEY)"
            )
            conn.commit()
        finally:
            conn.close()

    def register(self, name: str) -> None:
        """Register an agent by name if it has not been registered."""
        conn = sqlite3.connect(self.path)
        try:
            conn.execute("INSERT OR IGNORE INTO agents (name) VALUES (?)", (name,))
            conn.commit()
        finally:
            conn.close()

    def list_agents(self) -> list[str]:
        """Return all registered agent names."""
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.execute("SELECT name FROM agents")
            rows = cur.fetchall()
            return [row[0] for row in rows]
        finally:
            conn.close()