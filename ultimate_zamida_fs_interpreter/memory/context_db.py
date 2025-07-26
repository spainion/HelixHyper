"""High level context database combining a graph, change log and agent registry.

The `ContextDB` class bundles together three subsystems used in this
repository: a :class:`MemoryGraph` for storing code, a
`ChangeLog` for recording events, and an `AgentRegistry` for tracking
available agents.  It provides convenience methods to load and save
the graph from a file and to record log entries.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from .memory_graph import MemoryGraph
from .persistence import load, save
from .agent_registry import AgentRegistry
from .change_log import ChangeLog


class ContextDB:
    """Container for a graph, change log and agent registry."""

    def __init__(
        self,
        graph_path: Optional[str] = None,
        log_path: Optional[str] = None,
        registry_path: Optional[str] = None,
    ) -> None:
        # Determine paths from parameters or environment variables
        graph_path = graph_path or os.environ.get("GRAPH_PATH")
        log_path = log_path or os.environ.get("LOG_PATH")
        registry_path = registry_path or os.environ.get("REGISTRY_PATH")
        self.graph_path: Optional[str] = graph_path
        self.log_path: Optional[str] = log_path
        self.registry_path: Optional[str] = registry_path
        # Load or initialise graph
        if self.graph_path:
            self.graph = load(self.graph_path)
        else:
            self.graph = MemoryGraph()
        # Set up change log and registry if paths provided
        self.change_log: Optional[ChangeLog] = (
            ChangeLog(self.log_path) if self.log_path else None
        )
        self.registry: Optional[AgentRegistry] = (
            AgentRegistry(self.registry_path) if self.registry_path else None
        )

    def save_graph(self) -> None:
        """Persist the current graph to its initialised path."""
        if not self.graph_path:
            raise ValueError("graph_path not specified")
        save(self.graph, self.graph_path)

    def log(self, entry: str) -> None:
        """Record an entry in the change log, if one is configured."""
        if self.change_log:
            self.change_log.log(entry)