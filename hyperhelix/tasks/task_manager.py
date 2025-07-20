from __future__ import annotations

from ..core import HyperHelix
from ..node import Node
from .task import Task


def create_task(graph: HyperHelix, task: Task) -> None:
    node = Node(id=task.id, payload=task)
    graph.add_node(node)


def assign_task(graph: HyperHelix, task_id: str, user: str) -> None:
    node = graph.nodes[task_id]
    if isinstance(node.payload, Task):
        node.payload.assigned_to = user
