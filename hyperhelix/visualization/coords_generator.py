from __future__ import annotations

from typing import Tuple

from ..node import Node


def helix_coords(node: Node, idx: int, total: int) -> Tuple[float, float, float]:
    """Generate simple 3D coordinates."""
    angle = idx * 3.1415 * 2 / max(total, 1)
    return (angle, idx, 0.0)
