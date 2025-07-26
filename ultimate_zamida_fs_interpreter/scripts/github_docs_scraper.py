"""Asynchronous documentation scraper for GitHub pages.

This script provides a simple queue‑based scraper capable of fetching
multiple URLs concurrently and storing the results in a context graph.
It exposes both a command‑line interface and a ``QueueScraper`` class
for programmatic use.  The implementation is intentionally faithful to
the behaviour of the upstream project but trimmed for the needs of the
test suite.  Network errors propagate to callers.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import contextlib
from pathlib import Path
from typing import Iterable, Optional

import httpx

from agents.context_agent import ContextAgent


class QueueScraper(ContextAgent):
    """Simple asynchronous scraper that fetches a set of URLs.

    Each page fetched is stored in the attached context database as a
    node tagged with ``source=github_docs`` and the original URL.  The
    class maintains an internal asyncio queue to coordinate worker tasks.
    """

    def __init__(self, *, concurrency: int = 2, db: Optional[ContextDB] = None) -> None:
        # Use a basic ContextDB by default.  The upstream project uses a
        # SyncContextDB with locking, but our simplified implementation
        # accepts a generic ContextDB to avoid requiring lock paths.
        from memory.context_db import ContextDB  # local import to avoid cycle

        super().__init__(db=db or ContextDB())
        self.concurrency = concurrency
        # Queue of URLs awaiting fetching
        self.queue: asyncio.Queue[str] = asyncio.Queue()

    def act(self, urls: Iterable[str]) -> dict[str, str]:
        """Synchronous wrapper around :meth:`scrape`.

        This method runs the asynchronous ``scrape`` method to completion
        and returns its result.  It is provided for compatibility with
        the :class:`BaseAgent` interface.
        """
        return asyncio.run(self.scrape(list(urls)))

    async def _fetch(self, client: httpx.AsyncClient, url: str) -> str:
        """Fetch a single URL, store the content and return the text.

        The content is stored in the attached context graph along with
        metadata recording the source and URL.  Any non‑success HTTP
        status will raise an exception via ``raise_for_status``.
        """
        resp = await client.get(url)
        resp.raise_for_status()
        text = resp.text
        # Persist the raw HTML into the graph
        self.store(text, {"source": "github_docs", "url": url})
        return text

    async def _worker(self, client: httpx.AsyncClient, results: dict[str, str]) -> None:
        """Worker coroutine that processes URLs from the queue.

        This coroutine loops until cancelled, pulling URLs from the
        internal queue, fetching them and recording the result.  When
        finished, it marks the task as done on the queue.
        """
        while True:
            url = await self.queue.get()
            try:
                results[url] = await self._fetch(client, url)
            finally:
                self.queue.task_done()

    async def scrape(self, urls: Iterable[str]) -> dict[str, str]:
        """Fetch a collection of URLs concurrently.

        ``urls`` may be any iterable of strings.  The method returns a
        dictionary mapping each URL to its fetched text.  When used
        programmatically the caller can choose how to process the
        returned pages; the API server uses the lengths of these strings.
        """
        # Populate the queue
        for url in urls:
            await self.queue.put(url)
        results: dict[str, str] = {}
        # Acquire the file lock, if provided by SyncContextDB.  Some
        # versions of SyncContextDB expose a ``locked`` context manager.
        lock_ctx = getattr(self.db, "locked", None)
        ctx = lock_ctx() if lock_ctx else contextlib.nullcontext()  # type: ignore[operator]
        async with ctx:
            async with httpx.AsyncClient(timeout=30) as client:
                # Spawn worker tasks
                workers = [asyncio.create_task(self._worker(client, results)) for _ in range(self.concurrency)]
                # Wait for queue to drain
                await self.queue.join()
                # Cancel workers
                for w in workers:
                    w.cancel()
                    with contextlib.suppress(asyncio.CancelledError):
                        await w
        return results


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command‑line arguments for the scraper CLI."""
    parser = argparse.ArgumentParser(description="Scrape GitHub documentation pages")
    parser.add_argument("urls", nargs="+", help="Pages to fetch")
    parser.add_argument("--concurrency", type=int, default=2, help="Number of parallel fetchers")
    parser.add_argument("--output-dir", default=None, help="Save pages to this directory")
    return parser.parse_args([] if argv is None else argv)


def run(argv: Optional[list[str]] = None) -> None:
    """Entry point for the command‑line interface.

    This reads arguments from ``argv``, creates a ``QueueScraper`` with
    the requested concurrency and fetches all provided URLs.  If an
    output directory is specified the pages are saved into it using
    short hash‑based filenames.  Otherwise the pages are stored only in
    the context database.
    """
    args = parse_args(argv)
    scraper = QueueScraper(concurrency=args.concurrency)
    # Perform the scrape synchronously by delegating to ``scrape``
    results = asyncio.run(scraper.scrape(args.urls))
    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for url, text in results.items():
            # Derive a stable filename from the URL
            name = hashlib.sha1(url.encode()).hexdigest()[:8] + ".html"
            Path(out, name).write_text(text, encoding="utf-8")


if __name__ == "__main__":  # pragma: no cover - manual use
    run()
