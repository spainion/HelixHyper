from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get('/walk/{start_id}')
def walk_graph(start_id: str) -> dict[str, str]:
    return {"start": start_id}
