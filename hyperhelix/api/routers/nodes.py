from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..schemas import NodeIn, NodeOut
from ..dependencies import get_graph
from ...core import HyperHelix
from ...node import Node

router = APIRouter()


@router.post('/nodes', response_model=NodeOut)
def create_node(node: NodeIn, graph: HyperHelix = Depends(get_graph)) -> NodeOut:
    if node.id in graph.nodes:
        raise HTTPException(status_code=400, detail='Node exists')
    g_node = Node(id=node.id, payload=node.payload)
    graph.add_node(g_node)
    return NodeOut(id=g_node.id, payload=g_node.payload)


@router.get('/nodes/{node_id}', response_model=NodeOut)
def get_node(node_id: str, graph: HyperHelix = Depends(get_graph)) -> NodeOut:
    try:
        node = graph.nodes[node_id]
    except KeyError:
        raise HTTPException(status_code=404, detail='Not found')
    return NodeOut(id=node.id, payload=node.payload)
