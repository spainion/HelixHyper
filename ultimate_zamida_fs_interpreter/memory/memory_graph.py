"""In‑memory graph for storing code and related metadata.

This module defines two simple classes: :class:`Node` to represent
individual pieces of data and :class:`MemoryGraph` to manage a
collection of nodes.  Nodes store an identifier, the raw content
string and optional metadata.  Relationships between nodes are
represented via an adjacency mapping on each node (`edges`), where
each key is a relationship name and each value is a set of target
node identifiers.

The graph maintains a version string (`version`) which is bumped
whenever the graph is persisted.  Versions increment by 0.01 each
time `bump_version()` is called.  Serialisation helpers allow graphs
to be converted to and from dictionaries for persistence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass
class Node:
    """Simple node holding content, metadata and outgoing edges."""

    id: str
    content: str
    metadata: dict | None = None
    edges: Dict[str, Set[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class MemoryGraph:
    """A directed graph of :class:`Node` objects with version tracking."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        # version starts at 0.00
        self.version: str = "0.00"

    # Internal helper to generate a new node identifier
    def _next_id(self) -> str:
        return str(len(self.nodes))

    def add_node(self, content: str, metadata: dict | None = None) -> Node:
        """Add a new node with the given content to the graph.

        A numeric string identifier is generated based on the current
        number of nodes in the graph.  The new node is returned.
        """
        node_id = self._next_id()
        node = Node(node_id, content, metadata)
        self.nodes[node_id] = node
        return node

    def link_nodes(self, src_id: str, relation: str, dst_id: str) -> None:
        """Create a directed edge between two existing nodes.

        The edge is stored on the source node under the given relation
        name.  Multiple targets may be associated with the same
        relation; duplicates are silently ignored via the set type.
        """
        src = self.nodes[src_id]
        src.edges.setdefault(relation, set()).add(dst_id)

    def to_dict(self) -> dict:
        """Serialise the graph into a plain dictionary.

        Sets are converted to lists for JSON compatibility.
        """
        return {
            "version": self.version,
            "nodes": {
                nid: {
                    "content": node.content,
                    "metadata": node.metadata,
                    "edges": {rel: list(targets) for rel, targets in node.edges.items()},
                }
                for nid, node in self.nodes.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryGraph":
        """Reconstruct a graph from a serialised dictionary."""
        g = cls()
        g.version = str(data.get("version", "0.00"))
        for nid, ndata in data.get("nodes", {}).items():
            node = Node(nid, ndata.get("content", ""), ndata.get("metadata"), {})
            # convert lists back to sets
            edges_dict = {}
            for rel, ids in ndata.get("edges", {}).items():
                edges_dict[rel] = set(ids)
            node.edges = edges_dict
            g.nodes[nid] = node
        return g

    def bump_version(self) -> None:
        """Increment the graph's version by 0.01.

        The version string is treated as a floating point number and
        formatted with two decimal places.  Invalid values reset to
        0.00 before incrementing.
        """
        try:
            v = float(self.version)
        except Exception:
            v = 0.0
        v += 0.01
        self.version = f"{v:.2f}"