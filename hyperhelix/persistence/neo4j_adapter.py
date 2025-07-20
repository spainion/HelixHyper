from __future__ import annotations

from .base_adapter import BaseAdapter


class Neo4jAdapter(BaseAdapter):
    """In-memory stand-in for a Neo4j adapter."""

    def __init__(self) -> None:
        self._store: dict[str, dict] = {}

    def save_node(self, node_id: str, payload: dict) -> None:
        self._store[node_id] = payload

    def load_node(self, node_id: str) -> dict:
        return self._store[node_id]
