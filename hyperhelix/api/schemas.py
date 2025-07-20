from __future__ import annotations

from pydantic import BaseModel


class NodeIn(BaseModel):
    """Incoming node data."""

    id: str
    payload: dict


class NodeOut(BaseModel):
    """Node representation returned from the API."""

    id: str
    payload: dict


class EdgeIn(BaseModel):
    """Edge creation payload."""

    a: str
    b: str
    weight: float = 1.0
