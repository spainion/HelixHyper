from __future__ import annotations

from ..core import HyperHelix
from ..node import Node
from ..edge import connect
from ..analytics.importance import compute_importance
from ..analytics.permanence import compute_permanence


def on_insert(graph: HyperHelix, node_id: str) -> None:
    """Update metrics when a node is inserted."""
    node = graph.nodes[node_id]
    _update_metrics(graph, node)
    weave_by_tag(graph, node_id)
    prune_missing_edges(graph)


def on_update(graph: HyperHelix, node_id: str) -> None:
    """Update metrics when a node changes."""
    node = graph.nodes[node_id]
    _update_metrics(graph, node)
    prune_missing_edges(graph)


def _update_metrics(graph: HyperHelix, node: "Node") -> None:
    node.metadata.importance = compute_importance(node, graph.nodes.values())
    node.metadata.permanence = compute_permanence(node)


def weave_by_tag(graph: HyperHelix, node_id: str) -> None:
    """Connect new node to existing nodes sharing tags."""
    node = graph.nodes[node_id]
    for tag in node.tags:
        for other in graph.find_nodes_by_tag(tag):
            if other.id != node.id and other.id not in node.edges:
                connect(node, other)


def prune_missing_edges(graph: HyperHelix) -> None:
    """Remove edges pointing to nonexistent nodes."""
    for node in list(graph.nodes.values()):
        for neighbor_id in list(node.edges.keys()):
            if neighbor_id not in graph.nodes:
                del node.edges[neighbor_id]

