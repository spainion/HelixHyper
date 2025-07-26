from __future__ import annotations

from fastapi import APIRouter, Depends, Body, HTTPException
from typing import List

from ..dependencies import get_graph
from ...core import HyperHelix
from ...execution.suggestion import auto_suggest
from ..schemas import TaskOut

router = APIRouter()

@router.post('/autosuggest', response_model=List[TaskOut])
def autosuggest_endpoint(
    node_id: str = Body(..., embed=True),
    provider: str = Body('openai'),
    model: str | None = Body(None),
    graph: HyperHelix = Depends(get_graph),
) -> List[TaskOut]:
    if node_id not in graph.nodes:
        raise HTTPException(status_code=404, detail='Node not found')
    tasks = auto_suggest(graph, node_id, provider=provider, model=model)
    return [TaskOut(**t.__dict__) for t in tasks]
