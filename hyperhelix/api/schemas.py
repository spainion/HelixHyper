from __future__ import annotations

from pydantic import BaseModel


class NodeIn(BaseModel):
    id: str
    payload: dict
