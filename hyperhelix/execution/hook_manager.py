from __future__ import annotations

from typing import Callable

from ..core import HyperHelix


def bind_recursion_to_task(graph: HyperHelix, task: Callable[[], None]) -> None:
    """Invoke ``task`` whenever a node is inserted."""

    def _hook(_: HyperHelix, __: str) -> None:
        task()

    graph.register_insert_hook(_hook)


def bind_recursion_with_node(
    graph: HyperHelix, task: Callable[[HyperHelix, str], None]
) -> None:
    """Invoke ``task`` with the graph and node id whenever a node is inserted."""

    def _hook(g: HyperHelix, node_id: str) -> None:
        task(g, node_id)

    graph.register_insert_hook(_hook)
