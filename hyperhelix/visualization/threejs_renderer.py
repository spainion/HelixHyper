from __future__ import annotations

from ..node import Node


def node_to_json(node: Node) -> dict:
    return {"id": node.id, "payload": node.payload}
