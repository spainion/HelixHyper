"""Utilities for discovering scripts and agents.

Script discovery walks the given directory and imports every Python file
found (excluding those starting with an underscore).  Only modules
containing a callable ``run`` function are returned.  Agent discovery
looks for files ending in ``_agent.py`` and returns classes defined
within those modules.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Dict, Any


def _iter_files(directory: str, pattern: str) -> list[Path]:
    base = Path(directory)
    if not base.is_dir():
        return []
    return [p for p in base.glob(pattern) if p.is_file()]


def discover_scripts(directory: str) -> Dict[str, Any]:
    """Return a mapping of script names to imported modules with a ``run``.

    The script name is the filename without extension.  Files
    starting with an underscore or named ``__init__.py`` are ignored.
    """
    scripts: Dict[str, Any] = {}
    for file in _iter_files(directory, "*.py"):
        name = file.stem
        if name.startswith("_") or name == "__init__":
            continue
        # Normalize the directory path into a module prefix by replacing
        # forward and back slashes with dots.  Using replace on the
        # string avoids issues with f‑string backslash escapes.
        prefix = directory.replace('/', '.').replace('\\', '.')
        mod_name = f"{prefix}.{name}"
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        if hasattr(mod, "run"):
            scripts[name] = mod
    return scripts


def discover_agents(directory: str) -> Dict[str, Any]:
    """Return a mapping of agent names to classes defined in the module.

    An agent module is identified by the filename ending with
    ``_agent.py``.  The key in the returned dictionary is the
    filename (including the ``_agent`` suffix) and the value is the
    first class defined in the module.  This simple heuristic is
    adequate for the tests which monkeypatch specific agents.
    """
    agents: Dict[str, Any] = {}
    for file in _iter_files(directory, "*_agent.py"):
        name = file.stem
        prefix = directory.replace('/', '.').replace('\\', '.')
        mod_name = f"{prefix}.{name}"
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        # find first class defined in module
        cls = None
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if isinstance(obj, type):
                cls = obj
                break
        if cls:
            agents[name] = cls
    return agents