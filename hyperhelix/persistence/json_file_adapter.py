from __future__ import annotations

import json
import threading
from pathlib import Path
import logging

from .base_adapter import BaseAdapter


logger = logging.getLogger("hyperhelix")


class JSONFileAdapter(BaseAdapter):
    """Persist nodes and edges to a JSON file.

    The adapter stores a dictionary with ``nodes`` and ``edges`` keys. Nodes map to
    their payloads while edges map a source node to dictionaries of destination
    IDs and weights. Access is guarded by a thread lock so concurrent graph
    operations remain safe.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._lock = threading.Lock()
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                self.data: dict[str, dict] = json.load(f)
        else:
            self.data = {"nodes": {}, "edges": {}}

    def _persist(self) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f)
        logger.debug("Persisted graph to %s", self.path)

    def save_node(self, node_id: str, payload: dict) -> None:
        with self._lock:
            logger.debug("Saving node %s", node_id)
            self.data["nodes"][node_id] = payload
            self._persist()

    def load_node(self, node_id: str) -> dict:
        with self._lock:
            node = self.data["nodes"].get(node_id, {})
            logger.debug("Loaded node %s", node_id)
            return node

    def save_edge(self, a: str, b: str, weight: float) -> None:
        with self._lock:
            logger.debug("Saving edge %s -> %s (weight=%s)", a, b, weight)
            edges = self.data["edges"].setdefault(a, {})
            edges[b] = weight
            self._persist()

    def load_edges(self, node_id: str) -> dict[str, float]:
        with self._lock:
            edges = self.data["edges"].get(node_id, {}).copy()
            logger.debug("Loaded %d edges for %s", len(edges), node_id)
            return edges
