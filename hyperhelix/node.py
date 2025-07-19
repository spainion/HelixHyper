from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List

import logging

logger = logging.getLogger(__name__)

@dataclass
class NodeMetadata:
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    importance: float = 0.0
    permanence: float = 0.0
    perception_history: List[str] = field(default_factory=list)


@dataclass
class Node:
    id: str
    payload: Any
    tags: List[str] = field(default_factory=list)
    layer: int = 0
    strand: str = "default"
    edges: Dict[str, float] = field(default_factory=dict)
    metadata: NodeMetadata = field(default_factory=NodeMetadata)
    execute_fn: Callable[[Any], Any] | None = None

    def execute(self) -> Any:
        logger.debug("Executing node %s", self.id)
        if self.execute_fn:
            try:
                result = self.execute_fn(self.payload)
                logger.info("Node %s executed successfully", self.id)
                return result
            except Exception as exc:  # pragma: no cover - actual error path
                logger.exception("Execution failed for node %s", self.id)
                raise
        return None
