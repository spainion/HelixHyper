from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post('/autobloom/{node_id}')
def auto_bloom(node_id: str) -> dict[str, str]:
    return {"node": node_id}
