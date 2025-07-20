from __future__ import annotations

from typing import Callable

from ..core import HyperHelix


def bind_recursion_to_task(graph: HyperHelix, task: Callable[[], None]) -> None:
    """Register a callback to be executed during graph evolution."""
    # Simplified hook registration
    task()
