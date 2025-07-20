from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: str
    description: str
    due: Optional[datetime] = None
    priority: int = 0
    assigned_to: Optional[str] = None
