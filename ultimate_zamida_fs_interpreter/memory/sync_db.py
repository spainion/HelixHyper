"""Synchronous context database with file locking.

This module provides a simple advisory file lock and a context
manager for loading and saving a :class:`MemoryGraph` while holding
the lock.  It is intended for multi‑process use where multiple
processes might read or write the same graph file concurrently.
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .memory_graph import MemoryGraph
from .persistence import load, save


@contextmanager
def file_lock(lock_path: str, timeout: float = 5.0, poll_interval: float = 0.05) -> Iterator[None]:
    """Acquire an exclusive lock file, waiting up to ``timeout`` seconds.

    The function attempts to create a lock file atomically using
    ``os.O_CREAT | os.O_EXCL``.  If the file already exists it
    repeatedly sleeps for ``poll_interval`` seconds until the file is
    removed or the timeout is exceeded, in which case a
    ``TimeoutError`` is raised.  The lock file is deleted when
    leaving the context.
    """
    lock_file = Path(lock_path)
    start = time.time()
    while True:
        try:
            fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            if time.time() - start > timeout:
                raise TimeoutError(f"Timeout acquiring lock: {lock_path}")
            time.sleep(poll_interval)
    try:
        yield
    finally:
        # Remove the lock file if it still exists
        try:
            if lock_file.exists():
                os.unlink(str(lock_file))
        except Exception:
            pass


class SyncContextDB:
    """A file‑backed graph with synchronised access using a lock file."""

    def __init__(self, graph_path: str, lock_path: str) -> None:
        self.graph_path = str(graph_path)
        self.lock_path = str(lock_path)
        # ensure initial graph exists
        p = Path(self.graph_path)
        if not p.exists():
            # create an empty graph and save it
            save(MemoryGraph(), self.graph_path)
        # placeholder for loaded graph
        self.graph: MemoryGraph | None = None

    @contextmanager
    def locked(self, reload: bool = False) -> Iterator["SyncContextDB"]:
        """Context manager that loads and saves the graph while holding the lock.

        Upon entering the context the graph is loaded from disk into
        ``self.graph``.  On exit the graph is saved back to disk.
        Setting ``reload=True`` reloads the graph from disk after
        saving, which allows a caller to see the merged changes from
        multiple processes.
        """
        with file_lock(self.lock_path):
            # load the current graph
            self.graph = load(self.graph_path)
            try:
                yield self
            finally:
                # save the graph back to disk
                assert self.graph is not None
                save(self.graph, self.graph_path)
                if reload:
                    # reload from disk to merge concurrent changes
                    self.graph = load(self.graph_path)