from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import get_graph
from ...core import HyperHelix
from ...node import Node

router = APIRouter()


@router.post('/autobloom/{node_id}')
def auto_bloom(node_id: str, graph: HyperHelix = Depends(get_graph)) -> dict[str, str]:
    graph.add_node(Node(id=f"bloom:{node_id}", payload={"source": node_id}))
    return {"node": node_id}
