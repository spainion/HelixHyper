from __future__ import annotations

from typing import Callable

from ..core import HyperHelix


def bind_recursion_to_task(graph: HyperHelix, task: Callable[[], None]) -> None:
    """Invoke ``task`` whenever a node is inserted."""

    def _hook(_: HyperHelix, __: str) -> None:
        task()

    graph.register_insert_hook(_hook)
