from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class NodeMetadata:
    """Metadata about a node's lifecycle."""

    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    importance: float = 0.0
    permanence: float = 0.0
    perception_history: List[str] = field(default_factory=list)
