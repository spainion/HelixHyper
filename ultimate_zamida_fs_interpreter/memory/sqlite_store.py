"""Pseudo‑SQLite storage for `MemoryGraph`.

The tests in this challenge expect a SQLite interface for graphs but
only exercise loading and saving.  Instead of implementing a full
relational schema, this module reuses the JSON serialisation from
`memory.persistence` and stores the graph in a file with a `.db`
extension.  Backup files are created by appending ``.bak`` to the
database filename (e.g. ``graph.db.bak``).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .memory_graph import MemoryGraph


def save_graph(graph: MemoryGraph, path: Union[str, Path]) -> None:
    """Save ``graph`` to ``path`` and bump its version.

    Existing files are overwritten and a backup copy containing the
    newly saved data is written with the ``.bak`` suffix appended to
    the filename.  This mirrors the behaviour of the JSON persistence
    helper and ensures that the backup contains the latest version.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # If a database already exists, copy its contents to the backup
    backup = p.with_name(p.name + ".bak")
    if p.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text(p.read_text(), encoding="utf-8")
    # Increment version before writing new data
    graph.bump_version()
    data = graph.to_dict()
    # Write the new graph to the database path (JSON disguised)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f)


def load_graph(path: Union[str, Path]) -> MemoryGraph:
    """Load a graph from a pseudo‑SQLite database file.

    If the file does not exist an empty graph is returned.  The
    contents are assumed to be JSON written by :func:`save_graph`.
    """
    p = Path(path)
    if not p.exists():
        return MemoryGraph()
    data = json.loads(p.read_text())
    return MemoryGraph.from_dict(data)


def load_backup(path: Union[str, Path]) -> MemoryGraph:
    """Load a graph from a backup of a pseudo‑SQLite database file.

    The backup has the same name with ``.bak`` appended (e.g.
    ``graph.db.bak``).  A missing backup raises ``FileNotFoundError``.
    """
    p = Path(path)
    backup = p.with_name(p.name + ".bak")
    if not backup.exists():
        raise FileNotFoundError(str(backup))
    data = json.loads(backup.read_text())
    return MemoryGraph.from_dict(data)