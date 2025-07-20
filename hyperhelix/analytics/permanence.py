from __future__ import annotations

from datetime import datetime, timezone

from ..node import Node


def compute_permanence(node: Node) -> float:
    """Simple permanence metric based on age."""
    age = (datetime.now(timezone.utc) - node.metadata.created).total_seconds()
    return age
