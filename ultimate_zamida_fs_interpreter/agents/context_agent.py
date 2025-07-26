"""Agent that maintains a persistent context database.

This module defines a ``ContextAgent`` class which extends the basic
``BaseAgent`` to provide an attached :class:`~memory.context_db.ContextDB`.
Agents derived from ``ContextAgent`` can store content in a persistent
graph and optionally log changes.  The implementation here mirrors the
behaviour of the upstream repository sufficiently for the test suite,
keeping things intentionally simple.
"""

from __future__ import annotations

from typing import Optional

from .base_agent import BaseAgent
from ..memory.context_db import ContextDB


class ContextAgent(BaseAgent):
    """Base class for agents that operate over a :class:`ContextDB`.

    A ``ContextAgent`` owns a context database used to persist data
    across actions.  Subclasses can call :meth:`store` to add content
    into the underlying graph and optionally record log entries.  If no
    database is provided one will be created automatically, taking
    configuration from environment variables (see ``ContextDB``).
    """

    def __init__(self, db: Optional[ContextDB] = None) -> None:
        # Initialize with the provided database or create a new one.
        self.db: ContextDB = db or ContextDB()

    def store(self, content: str, metadata: Optional[dict] = None) -> str:
        """Store ``content`` in the graph with optional ``metadata``.

        The content is added as a new node in the database's graph.  If
        a change log is configured on the database, an entry is also
        recorded.  The newly created node's identifier is returned.
        """
        # Add the node to the graph
        node = self.db.graph.add_node(content, metadata)
        # Record in change log if configured
        if getattr(self.db, "change_log", None):
            self.db.change_log.log(f"store:{node.id}", category="agent")
        return node.id
