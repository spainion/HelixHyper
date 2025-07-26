from __future__ import annotations

import logging
import hashlib
from typing import List

from .hook_manager import bind_recursion_with_node
from ..core import HyperHelix
from ..agents.context import graph_summary
from ..agents.llm import (
    OpenAIChatModel,
    OpenRouterChatModel,
    HuggingFaceChatModel,
    TransformersChatModel,
    BaseChatModel,
)
from ..tasks.task import Task
from ..tasks import task_manager
from ..node import Node

logger = logging.getLogger(__name__)


def _select_model(provider: str, model: str | None) -> BaseChatModel:
    """Return a chat model instance for the given provider."""
    if provider == "openai":
        return OpenAIChatModel(model or "gpt-3.5-turbo")
    if provider == "openrouter":
        return OpenRouterChatModel(model or "openai/gpt-4o")
    if provider in {"hf", "huggingface"}:
        return HuggingFaceChatModel(model or "HuggingFaceH4/zephyr-7b-beta")
    if provider in {"local", "transformers"}:
        return TransformersChatModel(model or "sshleifer/tiny-gpt2")
    raise ValueError(f"Unknown provider: {provider}")


def auto_suggest(
    graph: HyperHelix,
    node_id: str,
    *,
    provider: str = "openai",
    model: str | None = None,
) -> List[Task]:
    """Create follow-up tasks from an LLM suggestion."""

    node = graph.nodes[node_id]
    messages = [
        {"role": "system", "content": graph_summary(graph)},
        {
            "role": "user",
            "content": (
                f"Analyze node {node_id}: {node.payload}\n"
                "Return each suggested task on its own line."
            ),
        },
    ]
    try:
        llm = _select_model(provider, model)
        suggestion = llm.generate_response(messages)
    except Exception:
        logger.exception("Suggestion generation failed")
        return []

    tasks: List[Task] = []
    for line in suggestion.splitlines():
        desc = line.lstrip("- ").strip()
        if not desc:
            continue
        task_id = f"suggest-{hashlib.sha1(desc.encode()).hexdigest()[:8]}"
        if task_id in graph.nodes:
            continue
        task = Task(id=task_id, description=desc)
        task_manager.create_task(graph, task)
        tasks.append(task)
    return tasks


def enable_auto_suggest(
    graph: HyperHelix, *, provider: str = "openai", model: str | None = None
) -> None:
    """Bind automatic suggestions to node insertion."""

    def _task(g: HyperHelix, node_id: str, _: Node | None) -> None:
        auto_suggest(g, node_id, provider=provider, model=model)

    bind_recursion_with_node(graph, _task)

