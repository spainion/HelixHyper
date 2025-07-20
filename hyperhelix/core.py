from __future__ import annotations

from collections import deque
from typing import Dict, Generator

import logging

from .node import Node
from .edge import connect

logger = logging.getLogger(__name__)


class HyperHelix:
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}

    def add_node(self, node: Node) -> None:
        logger.debug("Adding node %s", node.id)
        self.nodes[node.id] = node

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
