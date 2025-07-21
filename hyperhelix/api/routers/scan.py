from __future__ import annotations

from fastapi import APIRouter, Depends, Body

from ..dependencies import get_graph
from ...core import HyperHelix
from ...agents.code_scanner import scan_repository

router = APIRouter()

@router.post('/scan')
def scan_repo(path: str = Body(..., embed=True), graph: HyperHelix = Depends(get_graph)) -> dict[str, int]:
    """Scan a directory and store Python files as nodes."""
    scan_repository(graph, path)
    return {"total_nodes": len(graph.nodes)}
