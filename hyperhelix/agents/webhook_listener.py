from __future__ import annotations

from ..core import HyperHelix
from ..node import Node


def process_webhook(graph: HyperHelix, payload: dict) -> None:
    node_id = payload.get("id", "webhook")
    graph.add_node(Node(id=node_id, payload=payload))
