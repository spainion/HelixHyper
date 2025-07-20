from __future__ import annotations

from ..core import HyperHelix
from ..node import Node
from .llm import BaseChatModel


def handle_chat_message(graph: HyperHelix, message: str, model: BaseChatModel | None = None) -> None:
    """Store a chat message and optionally generate a reply using an LLM."""
    node = Node(id=message, payload={"msg": message})
    graph.add_node(node)
    if model:
        response = model.generate_response([
            {"role": "user", "content": message},
        ])
        graph.add_node(Node(id=f"response:{message}", payload={"msg": response}))
