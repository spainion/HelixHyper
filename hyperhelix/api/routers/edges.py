from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from ..schemas import EdgeIn, EdgeOut, StatusOut
from ..dependencies import get_graph
from ...core import HyperHelix

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/edges', response_model=StatusOut)
def create_edge(edge: EdgeIn, graph: HyperHelix = Depends(get_graph)) -> StatusOut:
    try:
        graph.add_edge(edge.a, edge.b, edge.weight)
    except KeyError as exc:
        logger.error("Create edge failed missing node %s", exc.args[0])
        raise HTTPException(status_code=404, detail=f"Node {exc.args[0]} not found")
    return StatusOut(status="created")


@router.delete('/edges/{a}/{b}', response_model=StatusOut)
def delete_edge(a: str, b: str, graph: HyperHelix = Depends(get_graph)) -> StatusOut:
    """Remove an edge from the graph."""
    try:
        graph.remove_edge(a, b)
    except KeyError as exc:
        logger.error("Edge delete failed: %s", exc.args[0])
        raise HTTPException(status_code=404, detail='Not found')
    return StatusOut(status="deleted")


@router.get('/edges', response_model=List[EdgeOut])
def list_edges(graph: HyperHelix = Depends(get_graph)) -> list[EdgeOut]:
    """Return all unique edges in the graph."""
    seen = set()
    edges = []
    for a, node in graph.nodes.items():
        for b, weight in node.edges.items():
            if (b, a) in seen:
                continue
            seen.add((a, b))
            edges.append(EdgeOut(a=a, b=b, weight=weight))
    return sorted(edges, key=lambda e: (e.a, e.b))
