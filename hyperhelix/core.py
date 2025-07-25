from __future__ import annotations

from collections import deque
from heapq import heappop, heappush
from typing import Callable, Dict, Generator, List

import logging

from .node import Node
from .edge import connect
from .persistence.base_adapter import BaseAdapter

logger = logging.getLogger(__name__)


class HyperHelix:
    def __init__(self, adapter: "BaseAdapter" | None = None) -> None:
        self.nodes: Dict[str, Node] = {}
        self._insert_hooks: List[Callable[[HyperHelix, str], None]] = []
        self._update_hooks: List[Callable[[HyperHelix, str], None]] = []
        self.adapter = adapter

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
        if self.adapter:
            self.adapter.save_node(node.id, node.payload)
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
        if self.adapter:
            self.adapter.save_edge(a, b, weight)

    def remove_edge(self, a: str, b: str) -> None:
        """Remove an edge between two nodes."""
        logger.debug("Removing edge %s <-> %s", a, b)
        if a not in self.nodes or b not in self.nodes:
            missing = a if a not in self.nodes else b
            logger.error("Edge removal failed missing node %s", missing)
            raise KeyError(missing)
        self.nodes[a].edges.pop(b, None)
        self.nodes[b].edges.pop(a, None)
        if self.adapter and hasattr(self.adapter, "remove_edge"):
            self.adapter.remove_edge(a, b)

    def remove_node(self, node_id: str) -> None:
        """Remove a node and any edges referencing it."""
        logger.debug("Removing node %s", node_id)
        if node_id not in self.nodes:
            logger.error("Node %s not found", node_id)
            raise KeyError(node_id)
        for other in self.nodes.values():
            other.edges.pop(node_id, None)
        del self.nodes[node_id]

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

    def shortest_path(self, start_id: str, end_id: str) -> List[str]:
        """Return the shortest weighted path between two nodes."""
        logger.debug("Shortest path %s -> %s", start_id, end_id)
        if start_id not in self.nodes or end_id not in self.nodes:
            logger.error("Start or end node missing: %s %s", start_id, end_id)
            raise KeyError(start_id if start_id not in self.nodes else end_id)

        distances: Dict[str, float] = {start_id: 0.0}
        prev: Dict[str, str | None] = {start_id: None}
        queue: List[tuple[float, str]] = [(0.0, start_id)]

        while queue:
            dist, current = heappop(queue)
            if current == end_id:
                break
            for neighbor, weight in self.nodes[current].edges.items():
                new_dist = dist + weight
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    prev[neighbor] = current
                    heappush(queue, (new_dist, neighbor))

        if end_id not in prev:
            return []

        path = []
        node = end_id
        while node is not None:
            path.append(node)
            node = prev.get(node)
        return list(reversed(path))
