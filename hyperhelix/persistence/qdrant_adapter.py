from __future__ import annotations

from .base_adapter import BaseAdapter


class QdrantAdapter(BaseAdapter):
    def __init__(self) -> None:
        self._store: dict[str, dict] = {}
        self._edges: dict[str, dict[str, float]] = {}

    def save_node(self, node_id: str, payload: dict) -> None:
        self._store[node_id] = payload

    def load_node(self, node_id: str) -> dict:
        return self._store[node_id]

    def save_edge(self, a: str, b: str, weight: float) -> None:
        self._edges.setdefault(a, {})[b] = weight
        self._edges.setdefault(b, {})[a] = weight

    def load_edges(self, node_id: str) -> dict[str, float]:
        return self._edges.get(node_id, {})
