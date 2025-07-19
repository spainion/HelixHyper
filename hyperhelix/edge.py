from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def connect(node_a, node_b, weight: float = 1.0) -> None:
    """Create a bidirectional edge between two nodes."""
    node_a.edges[node_b.id] = weight
    node_b.edges[node_a.id] = weight
    logger.debug("Connected %s <-> %s with weight %s", node_a.id, node_b.id, weight)
