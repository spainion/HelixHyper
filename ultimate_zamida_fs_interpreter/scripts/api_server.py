"""FastAPI server exposing scraping helpers and GitHub utilities.

This module defines a small HTTP API built with FastAPI.  It
exposes three endpoints used in the test suite:

* ``POST /scrape-docs`` fetches a list of documentation pages using the
  :class:`QueueScraper` defined in :mod:`scripts.github_docs_scraper` and
  returns the length of each fetched document.
* ``GET /commits`` lists the most recent commits in a repository using
  :class:`agents.github_agent.GitHubAgent` and returns truncated SHAs
  along with single‑line commit messages.
* ``GET /todo-list`` runs the ``scripts.list_missing`` CLI and
  returns its output lines as a JSON array.  Query parameters are
  passed through to the underlying script as command‑line options.

The accompanying ``run`` function starts an ASGI server via uvicorn.
"""

from __future__ import annotations

import contextlib
import io

from fastapi import FastAPI
from pydantic import BaseModel

from agents.github_agent import GitHubAgent
import scripts.list_missing as list_missing
from scripts.github_docs_scraper import QueueScraper


# Instantiate a global FastAPI application
app = FastAPI()


class ScrapeRequest(BaseModel):
    """Request body for the ``/scrape-docs`` endpoint."""

    urls: list[str]
    concurrency: int = 2


@app.post("/scrape-docs")
async def scrape_docs(req: ScrapeRequest) -> dict[str, int]:
    """Fetch documentation pages and return their lengths.

    A ``QueueScraper`` is instantiated with the requested concurrency
    level.  The returned dictionary maps each URL to the number of
    characters in the corresponding document.  The actual content
    storage happens in the scraper itself via its base class.
    """
    scraper = QueueScraper(concurrency=req.concurrency)
    results = await scraper.scrape(req.urls)
    # Convert the results to a mapping of URL to content length
    return {u: len(t) for u, t in results.items()}


@app.get("/commits")
def list_commits(limit: int = 10) -> list[dict[str, str]]:
    """Return a list of recent commits with truncated SHAs and messages."""
    agent = GitHubAgent()
    commits = agent.list_commits(limit=limit)
    # Normalise commit objects and extract only the first line of the message
    return [
        {
            "sha": c.get("sha", "")[:7],
            # messages may either be top‑level "message" (our GitHubAgent)
            # or nested under a "commit" dict (tests).  Take the first
            # available value and split on newlines.
            "message": (
                (c.get("message") or c.get("commit", {}).get("message", "")).splitlines()[0]
                if (c.get("message") or c.get("commit", {}).get("message"))
                else ""
            ),
        }
        for c in commits
    ]


@app.get("/todo-list")
def todo_list(root: str | None = None, pattern: str = "TODO") -> list[str]:
    """Run the ``list_missing`` script and return its output lines."""
    opts: list[str] = []
    # Translate query parameters into command‑line options
    if root:
        opts += ["--root", root]
    if pattern:
        opts += ["--pattern", pattern]
    opts += ["--count"]
    # Capture standard output from the script
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        list_missing.run(opts)
    # Split output into lines and filter out empty strings
    return [line for line in buf.getvalue().splitlines() if line]


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Launch the API server using uvicorn."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":  # pragma: no cover - manual use
    run()
