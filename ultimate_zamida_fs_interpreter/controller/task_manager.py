"""Simple in‑memory task manager used for CLI operations."""

from __future__ import annotations

from typing import Dict


class TaskManager:
    """Manage a list of tasks with unique identifiers and status flags."""

    def __init__(self, graph) -> None:
        # A reference to the backing graph (unused but kept for parity with tests)
        self.graph = graph
        self.tasks: Dict[str, Dict[str, object]] = {}
        self._counter = 0

    def create(self, description: str) -> str:
        """Create a new task and return its identifier."""
        task_id = str(self._counter)
        self.tasks[task_id] = {"desc": description, "done": False}
        self._counter += 1
        return task_id

    def list_tasks(self) -> str:
        """Return a human‑readable list of tasks and their status."""
        lines: list[str] = []
        for tid, task in self.tasks.items():
            status = "done" if task["done"] else "open"
            lines.append(f"{tid}: {task['desc']} [{status}]")
        return "\n".join(lines)

    def complete(self, task_id: str) -> bool:
        """Mark a task as complete if it exists."""
        if task_id in self.tasks:
            self.tasks[task_id]["done"] = True
            return True
        return False