from __future__ import annotations

from ..core import HyperHelix


def sprint_plan(graph: HyperHelix) -> list[str]:
    """Return a simple ordered list of task IDs."""
    return list(graph.nodes.keys())
