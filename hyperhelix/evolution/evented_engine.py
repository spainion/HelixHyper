from __future__ import annotations

from ..core import HyperHelix
from ..analytics.importance import compute_importance
from ..analytics.permanence import compute_permanence


def on_insert(graph: HyperHelix, node_id: str) -> None:
    """Update metrics when a node is inserted."""
    node = graph.nodes[node_id]
    node.metadata.importance = compute_importance(node, graph.nodes.values())
    node.metadata.permanence = compute_permanence(node)
