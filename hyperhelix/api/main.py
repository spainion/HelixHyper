from __future__ import annotations

from fastapi import FastAPI

from ..core import HyperHelix
from .routers import nodes, edges, walk, bloom, scan, tasks, suggest, models

app = FastAPI()
app.state.graph = HyperHelix()
app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(walk.router)
app.include_router(bloom.router)
app.include_router(scan.router)
app.include_router(tasks.router)
app.include_router(suggest.router)
app.include_router(models.router)


@app.get('/')
def read_root() -> dict[str, str]:
    return {"status": "ok"}
