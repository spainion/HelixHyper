from __future__ import annotations

import threading
import time

from ..core import HyperHelix
from ..analytics.importance import compute_importance
from ..analytics.permanence import compute_permanence


def run_periodically(graph: HyperHelix, interval: float) -> threading.Thread:
    """Periodically recompute node metrics."""

    def _worker() -> None:
        while True:
            time.sleep(interval)
            for node in graph.nodes.values():
                node.metadata.importance = compute_importance(node, graph.nodes.values())
                node.metadata.permanence = compute_permanence(node)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return t
