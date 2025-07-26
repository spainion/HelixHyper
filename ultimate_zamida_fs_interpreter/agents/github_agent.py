"""Minimal GitHub API client used in commit and API tests."""

from __future__ import annotations

import base64
import os
import requests
from typing import List, Dict


class GitHubAgent:
    """Wrapper around a small subset of the GitHub API.

    The agent reads the repository name and token from the
    ``GITHUB_REPO`` and ``GITHUB_TOKEN`` environment variables unless
    provided explicitly.
    """

    def __init__(self, repo: str | None = None, token: str | None = None) -> None:
        self.repo = repo or os.environ.get("GITHUB_REPO")
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com/repos"
        # expose the requests module via an instance attribute so tests can
        # monkeypatch ``agents.github_agent.requests`` and have it take effect
        from . import github_agent as gh_module  # type: ignore
        # assign the module attribute rather than the imported name to
        # respect monkeypatching of gh_module.requests
        self.requests = getattr(gh_module, "requests")

    @property
    def _auth_headers(self) -> Dict[str, str]:
        if not self.token:
            return {}
        return {"Authorization": f"token {self.token}"}

    def list_commits(self, limit: int = 10) -> List[Dict[str, str]]:
        """Return a list of recent commit identifiers and messages.

        The returned dictionaries contain ``sha`` and ``message`` keys.  A
        real implementation would page through the API; this stub
        simply returns an empty list if the repository is unknown.
        """
        if not self.repo:
            return []
        url = f"{self.base_url}/{self.repo}/commits"
        params = {"per_page": limit}
        # Use the instance's requests attribute to allow monkeypatching
        resp = self.requests.get(url, headers=self._auth_headers, params=params, timeout=5)
        resp.raise_for_status()
        commits = []
        for item in resp.json():
            commits.append({"sha": item["sha"], "message": item["commit"]["message"]})
        return commits

    def commit_file(self, path: str, message: str, content: str) -> dict:
        """Create or update a file in the repository.

        The content is sent as base64‑encoded UTF‑8 bytes.  If the file
        already exists the current SHA is included to update it.
        """
        if not self.repo:
            raise ValueError("Missing repository name")
        url = f"{self.base_url}/{self.repo}/contents/{path}"
        # get current SHA if present
        # get current SHA if present using instance requests
        resp = self.requests.get(url, headers=self._auth_headers, timeout=5)
        sha = None
        if resp.status_code == 200:
            try:
                sha = resp.json().get("sha")
            except Exception:
                sha = None
        encoded = base64.b64encode(content.encode()).decode()
        data = {"message": message, "content": encoded}
        if sha:
            data["sha"] = sha
        resp = self.requests.put(url, headers=self._auth_headers, json=data, timeout=5)
        resp.raise_for_status()
        return resp.json()