from __future__ import annotations

import logging

from ..node import Node

logger = logging.getLogger(__name__)


def execute_node(node: Node) -> None:
    """Execute a node using its stored callable."""
    try:
        node.execute()
    except Exception:
        logger.exception("Node %s execution failed", node.id)
        raise
