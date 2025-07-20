from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post('/edges')
def create_edge() -> dict[str, str]:
    return {"status": "created"}
