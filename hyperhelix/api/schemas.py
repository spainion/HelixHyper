from __future__ import annotations

from datetime import datetime
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


class EdgeOut(BaseModel):
    """Edge representation returned from the API."""

    a: str
    b: str
    weight: float


class TaskIn(BaseModel):
    """Task creation payload."""

    id: str
    description: str
    due: datetime | None = None
    priority: int = 0
    assigned_to: str | None = None


class TaskOut(TaskIn):
    """Task representation returned from the API."""

