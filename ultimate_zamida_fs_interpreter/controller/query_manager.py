"""Minimal query manager for routing commands in the CLI tests."""

from __future__ import annotations

from typing import Any


class QueryManager:
    """Container for a graph, a GPT connector, a task manager and an execution manager."""

    def __init__(self, graph: Any, gpt_connector: Any, task_manager: Any, executor: Any) -> None:
        self.graph = graph
        self.gpt_connector = gpt_connector
        self.task_manager = task_manager
        self.executor = executor