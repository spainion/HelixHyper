from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
import logging

from ..schemas import EdgeIn
from ..dependencies import get_graph
from ...core import HyperHelix

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/edges')
def create_edge(edge: EdgeIn, graph: HyperHelix = Depends(get_graph)) -> dict[str, str]:
    try:
        graph.add_edge(edge.a, edge.b, edge.weight)
    except KeyError as exc:
        logger.error("Create edge failed missing node %s", exc.args[0])
        raise HTTPException(status_code=404, detail=f"Node {exc.args[0]} not found")
    return {"status": "created"}
