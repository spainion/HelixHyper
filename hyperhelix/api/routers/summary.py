from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import get_graph
from ...core import HyperHelix
from ...agents.context import graph_summary

router = APIRouter()


@router.get('/summary')
def get_summary(graph: HyperHelix = Depends(get_graph)) -> dict[str, str]:
    """Return a short summary of the current graph."""
    return {'summary': graph_summary(graph)}
