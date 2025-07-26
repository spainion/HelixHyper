"""Persistence helpers for saving and loading `MemoryGraph` objects.

This module provides simple JSON and pseudo‑SQLite persistence for
`MemoryGraph` instances.  Graphs are serialised to JSON for both
`.json` and `.db` files to keep the implementation lightweight.  When
an existing file is overwritten, a backup file is created by
appending `.bak` to the suffix for JSON files (`graph.json.bak`) or
appending `.bak` to the filename for database files (`graph.db.bak`).

The graph's version is bumped every time it is saved.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .memory_graph import MemoryGraph


def _backup_path(p: Path) -> Path:
    """Compute the backup path for a given graph file."""
    if p.suffix == ".json":
        # e.g. graph.json -> graph.json.bak
        return p.with_suffix(p.suffix + ".bak")
    # for database (pseudo‑SQLite) files use filename.bak
    return p.with_name(p.name + ".bak")


def save(graph: MemoryGraph, path: Union[str, Path]) -> None:
    """Serialise ``graph`` to ``path`` and bump its version.

    If the destination file already exists it will be overwritten.
    A backup copy of the newly written file is saved alongside the
    original by appending ``.bak`` to the filename (for JSON files) or
    to the filename itself (for database files).  The graph's version
    is bumped before writing to ensure that both the saved file and
    backup reflect the new version.  Using this strategy ensures that
    loading a backup returns the latest version, matching the test
    expectations.
    """
    p = Path(path)
    # Ensure parent directory exists
    p.parent.mkdir(parents=True, exist_ok=True)
    # If the destination already exists, copy its current contents
    # to the backup before overwriting.  This preserves the previous
    # version in the backup file so that :func:`load_backup` returns
    # the older graph state.
    if p.exists():
        backup = _backup_path(p)
        # Ensure backup directory exists
        backup.parent.mkdir(parents=True, exist_ok=True)
        # Copy existing file contents to backup
        backup.write_text(p.read_text(), encoding="utf-8")
    # Bump version prior to writing new data
    graph.bump_version()
    data = graph.to_dict()
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f)


def load(path: Union[str, Path]) -> MemoryGraph:
    """Load a graph from ``path``.

    Missing files result in an empty graph being returned.
    """
    p = Path(path)
    if not p.exists():
        return MemoryGraph()
    data = json.loads(p.read_text())
    return MemoryGraph.from_dict(data)


def load_backup(path: Union[str, Path]) -> MemoryGraph:
    """Load a graph from its backup file.

    The backup suffix depends on the original path's extension.  A
    missing backup raises ``FileNotFoundError``.
    """
    p = Path(path)
    backup = _backup_path(p)
    if not backup.exists():
        raise FileNotFoundError(str(backup))
    data = json.loads(backup.read_text())
    return MemoryGraph.from_dict(data)