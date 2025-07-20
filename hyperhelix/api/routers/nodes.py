from __future__ import annotations

from fastapi import APIRouter

from ..schemas import NodeIn

router = APIRouter()


@router.post('/nodes')
def create_node(node: NodeIn) -> NodeIn:
    return node
