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
        node_a = self.nodes[a]
        node_b = self.nodes[b]
        connect(node_a, node_b, weight)

    def spiral_walk(self, start_id: str, depth: int = 1) -> Generator[Node, None, None]:
        logger.debug("Spiral walk from %s depth %d", start_id, depth)
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
