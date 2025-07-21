from __future__ import annotations

from ..core import HyperHelix


def graph_summary(graph: HyperHelix, limit: int = 5) -> str:
    """Return a short text summary of the graph state."""
    nodes = list(graph.nodes)[:limit]
    summary = f"The graph contains {len(graph.nodes)} nodes."
    if nodes:
        summary += f" Sample nodes: {', '.join(nodes)}."
    return summary
