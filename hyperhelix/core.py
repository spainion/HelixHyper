from __future__ import annotations

from collections import deque
from typing import Callable, Dict, Generator, List

import logging

from .node import Node
from .edge import connect

logger = logging.getLogger(__name__)


class HyperHelix:
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self._insert_hooks: List[Callable[[HyperHelix, str], None]] = []
        self._update_hooks: List[Callable[[HyperHelix, str], None]] = []

        # Register default evolution hook
        try:
            from .evolution import evented_engine

            self.register_insert_hook(evented_engine.on_insert)
        except Exception:  # pragma: no cover - optional imports
            logger.exception("Failed to register default hooks")

    def register_insert_hook(self, hook: Callable[["HyperHelix", str], None]) -> None:
        """Register a callback for node insertion events."""
        self._insert_hooks.append(hook)

    def register_update_hook(self, hook: Callable[["HyperHelix", str], None]) -> None:
        """Register a callback for node updates."""
        self._update_hooks.append(hook)

    def add_node(self, node: Node) -> None:
        logger.debug("Adding node %s", node.id)
        self.nodes[node.id] = node
        for hook in self._insert_hooks:
            hook(self, node.id)

    def add_edge(self, a: str, b: str, weight: float = 1.0) -> None:
        logger.debug("Adding edge %s <-> %s", a, b)
        try:
            node_a = self.nodes[a]
            node_b = self.nodes[b]
        except KeyError as exc:  # pragma: no cover - run-time safeguard
            logger.error("Cannot add edge, node missing: %s", exc.args[0])
            raise
        connect(node_a, node_b, weight)

    def find_nodes_by_tag(self, tag: str) -> list[Node]:
        """Return all nodes containing the given tag."""
        logger.debug("Searching nodes with tag %s", tag)
        return [n for n in self.nodes.values() if tag in n.tags]

    def spiral_walk(self, start_id: str, depth: int = 1) -> Generator[Node, None, None]:
        logger.debug("Spiral walk from %s depth %d", start_id, depth)
        if start_id not in self.nodes:
            logger.error("Start node %s not found", start_id)
            raise KeyError(start_id)
        visited = set()
        queue = deque([(start_id, 0)])
        while queue:
            current_id, level = queue.popleft()
            if current_id in visited or level > depth:
                continue
            visited.add(current_id)
            node = self.nodes[current_id]
            yield node
            for neighbor_id in node.edges:
                queue.append((neighbor_id, level + 1))
