from __future__ import annotations

import logging

from ..core import HyperHelix
from ..node import Node

logger = logging.getLogger(__name__)


def execute_node(graph: HyperHelix, node_id: str) -> None:
    """Execute a node and trigger update hooks."""
    node = graph.nodes[node_id]
    try:
        node.execute()
    except Exception:
        logger.exception("Node %s execution failed", node.id)
        raise
    for hook in graph._update_hooks:
        hook(graph, node_id)
