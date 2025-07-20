from __future__ import annotations

from ..core import HyperHelix


def on_insert(graph: HyperHelix, node_id: str) -> None:
    """Example hook triggered when a node is inserted."""
    # A real implementation could prune or weave the graph here.
    _ = graph.nodes.get(node_id)
