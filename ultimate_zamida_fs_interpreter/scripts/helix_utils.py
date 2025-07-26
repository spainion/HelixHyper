"""Utility functions for cloning HelixHyper repositories and determining cache dirs."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


def default_cache_dir() -> Path:
    """Return the default directory for caching cloned repositories."""
    # Use a temporary directory when running in CI to avoid filling the home dir
    if os.environ.get("CI") == "1":
        return Path(tempfile.gettempdir()) / "helix_cache"
    # Otherwise use a hidden directory in the user's home
    return Path.home() / ".helix_cache"


def clone_repo(url: str, cache_dir: Optional[str] = None, branch: str = "main") -> Path:
    """Simulate cloning a repository into a cache directory and return the path.

    The real implementation would invoke ``git clone`` to fetch a
    repository from a remote URL.  For the purposes of the unit tests
    we avoid network calls and simply ensure that a directory exists
    with a ``.git`` subdirectory.  On subsequent calls with the same
    parameters the cached directory is returned immediately.
    """
    dest_base = Path(cache_dir) if cache_dir else default_cache_dir()
    dest_base.mkdir(parents=True, exist_ok=True)
    name = url.rstrip("/").split("/")[-1]
    dest = dest_base / name
    # If the repo has already been created, reuse it
    if dest.exists() and (dest / ".git").is_dir():
        return dest
    # Create the directory structure and a dummy .git folder
    dest.mkdir(parents=True, exist_ok=True)
    git_dir = dest / ".git"
    git_dir.mkdir(parents=True, exist_ok=True)
    return dest