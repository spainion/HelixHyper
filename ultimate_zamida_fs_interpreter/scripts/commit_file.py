"""Commit a file to a GitHub repository using the GitHubAgent.

This script either takes raw content via the ``content`` parameter or
reads it from a source file given by ``source``.  The path within
the repository and the commit message are required positional
arguments.  Environment variables ``GITHUB_REPO`` and
``GITHUB_TOKEN`` configure the repository and authentication.
"""

from __future__ import annotations

import base64
import os
from typing import Optional

from agents.github_agent import GitHubAgent


def run(path: str, message: str, *, content: Optional[str] = None, source: Optional[str] = None) -> None:
    """Create or update a file in a GitHub repository.

    :param path: destination path inside the repository
    :param message: commit message
    :param content: optional raw string content
    :param source: optional filesystem path to read content from
    """
    agent = GitHubAgent()
    if content is None and source is not None:
        data = open(source, "rb").read()
        # treat bytes as UTF‑8 if possible
        try:
            content = data.decode()
        except Exception:
            # fall back to base64 encoded string of bytes
            content = base64.b64encode(data).decode()
    elif content is None:
        content = ""
    # Use the GitHubAgent to commit the file
    agent.commit_file(path, message, content)