"""Registry for interpreter plugins and execution dispatcher."""

from __future__ import annotations

from typing import Any, Dict


class ExecutionManager:
    """Manage and invoke interpreter plugins by name."""

    def __init__(self) -> None:
        self._plugins: Dict[str, Any] = {}

    def register(self, name: str, plugin: Any) -> None:
        """Register a plugin under a short name."""
        self._plugins[name] = plugin

    def execute(self, name: str, code: str) -> str:
        """Execute code using the named plugin and return its output."""
        if name not in self._plugins:
            raise ValueError(f"Unknown interpreter: {name}")
        plugin = self._plugins[name]
        return plugin.execute(code)