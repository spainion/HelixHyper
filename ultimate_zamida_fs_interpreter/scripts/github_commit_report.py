"""Generate a simple text report of recent commits (stub)."""

from __future__ import annotations

from typing import List

from agents.github_agent import GitHubAgent


def run(argv: List[str]) -> None:
    # Parse options: expects ["--limit", limit, "--output", output]
    limit = 10
    output = None
    it = iter(argv)
    for arg in it:
        if arg == "--limit":
            try:
                limit = int(next(it))
            except StopIteration:
                pass
        elif arg == "--output":
            try:
                output = next(it)
            except StopIteration:
                pass
    agent = GitHubAgent()
    commits = agent.list_commits(limit)
    # Support commit dictionaries that either have a top-level
    # ``message`` key (our GitHubAgent) or a nested ``commit``
    # dictionary with ``message`` (used by tests via DummyAgent).  The
    # tests stub ``GitHubAgent`` to return items with
    # ``{"sha": ..., "commit": {"message": ...}}``
    lines: list[str] = []
    for c in commits:
        msg = c.get("message")
        if msg is None and isinstance(c.get("commit"), dict):
            msg = c["commit"].get("message")
        # Fallback to empty string if no message key is present
        if msg is None:
            msg = ""
        lines.append(f"{c['sha'][:7]} {msg}")
    text = "\n".join(lines)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)