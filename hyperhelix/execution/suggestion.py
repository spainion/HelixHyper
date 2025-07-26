from __future__ import annotations

import logging

from .hook_manager import bind_recursion_with_node
from ..core import HyperHelix
from ..agents.context import graph_summary
from ..agents.llm import OpenAIChatModel
from ..tasks.task import Task
from ..tasks import task_manager

logger = logging.getLogger(__name__)


def auto_suggest(graph: HyperHelix, node_id: str) -> None:
    """Create a follow-up task using an LLM suggestion."""
    node = graph.nodes[node_id]
    messages = [
        {"role": "system", "content": "You are a code-review agent."},
        {
            "role": "user",
            "content": f"{graph_summary(graph)}\nAnalyze node {node_id}: {node.payload}",
        },
    ]
    try:
        model = OpenAIChatModel()
        suggestion = model.generate_response(messages)
    except Exception:
        logger.exception("Suggestion generation failed")
        return
    task = Task(id=f"suggest-{node_id}", description=suggestion)
    task_manager.create_task(graph, task)


def enable_auto_suggest(graph: HyperHelix) -> None:
    """Bind automatic suggestions to node insertion."""
    bind_recursion_with_node(graph, auto_suggest)
