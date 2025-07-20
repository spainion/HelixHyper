from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
import logging
from typing import List

from ..schemas import NodeOut
from ..dependencies import get_graph
from ...core import HyperHelix

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/walk/{start_id}', response_model=List[NodeOut])
def walk_graph(start_id: str, depth: int = 1, graph: HyperHelix = Depends(get_graph)) -> list[NodeOut]:
    try:
        nodes = list(graph.spiral_walk(start_id, depth))
    except KeyError:
        logger.error("Start node %s not found", start_id)
        raise HTTPException(status_code=404, detail='Start node not found')
    return [NodeOut(id=n.id, payload=n.payload) for n in nodes]
