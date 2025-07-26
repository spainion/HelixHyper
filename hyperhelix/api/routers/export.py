from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import get_graph
from ...core import HyperHelix
from ...visualization.threejs_renderer import node_to_json

router = APIRouter()


@router.get('/export')
def export_graph(graph: HyperHelix = Depends(get_graph)) -> dict:
    """Return the full graph as a JSON payload."""
    nodes = [node_to_json(n) for n in graph.nodes.values()]
    edges = [
        {'a': a, 'b': b, 'weight': w}
        for a, node in graph.nodes.items()
        for b, w in node.edges.items()
        if a < b
    ]
    return {'nodes': nodes, 'edges': edges}
