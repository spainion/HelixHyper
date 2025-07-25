from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from ..schemas import NodeIn, NodeOut
from ..dependencies import get_graph
from ...core import HyperHelix
from ...node import Node
from ...execution.executor import execute_node

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/nodes', response_model=NodeOut)
def create_node(node: NodeIn, graph: HyperHelix = Depends(get_graph)) -> NodeOut:
    if node.id in graph.nodes:
        logger.error("Create node failed duplicate id %s", node.id)
        raise HTTPException(status_code=400, detail='Node exists')
    g_node = Node(id=node.id, payload=node.payload)
    graph.add_node(g_node)
    return NodeOut(id=g_node.id, payload=g_node.payload)


@router.get('/nodes/{node_id}', response_model=NodeOut)
def get_node(node_id: str, graph: HyperHelix = Depends(get_graph)) -> NodeOut:
    try:
        node = graph.nodes[node_id]
    except KeyError:
        logger.error("Node %s not found", node_id)
        raise HTTPException(status_code=404, detail='Not found')
    return NodeOut(id=node.id, payload=node.payload)


@router.delete('/nodes/{node_id}')
def delete_node(node_id: str, graph: HyperHelix = Depends(get_graph)) -> dict[str, str]:
    """Remove a node from the graph."""
    if node_id not in graph.nodes:
        logger.error("Node %s not found", node_id)
        raise HTTPException(status_code=404, detail='Not found')
    graph.remove_node(node_id)
    return {"status": "deleted"}


@router.get('/nodes', response_model=List[NodeOut])
def list_nodes(graph: HyperHelix = Depends(get_graph)) -> list[NodeOut]:
    """Return all nodes in the graph sorted by identifier."""
    nodes = [NodeOut(id=n.id, payload=n.payload) for n in graph.nodes.values()]
    return sorted(nodes, key=lambda n: n.id)


@router.post('/nodes/{node_id}/execute', response_model=NodeOut)
def execute_node_endpoint(node_id: str, graph: HyperHelix = Depends(get_graph)) -> NodeOut:
    """Execute the given node and trigger update hooks."""
    if node_id not in graph.nodes:
        logger.error("Node %s not found", node_id)
        raise HTTPException(status_code=404, detail='Not found')
    execute_node(graph, node_id)
    node = graph.nodes[node_id]
    return NodeOut(id=node.id, payload=node.payload)
