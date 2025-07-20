from __future__ import annotations

from typing import Iterable

from ..node import Node


def compute_importance(node: Node, all_nodes: Iterable[Node]) -> float:
    """Compute node importance based on degree."""
    return float(len(node.edges))
