from __future__ import annotations

import threading
import time

from ..core import HyperHelix


def run_periodically(graph: HyperHelix, interval: float) -> threading.Thread:
    """Run a simple evolution pass at a fixed interval."""

    def _worker() -> None:
        while True:
            time.sleep(interval)
            # Placeholder for evolution logic
            _ = len(graph.nodes)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return t
