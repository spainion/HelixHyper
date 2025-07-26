"""Print basic diagnostic information about available scripts and agents."""

from __future__ import annotations

from controller.agent_factory import discover_scripts, discover_agents
from gpt.connector import GPTConnector


def run() -> None:
    """List script and agent names and issue a simple GPT query."""
    scripts = discover_scripts("scripts")
    agents = discover_agents("agents")
    print("Scripts:", ", ".join(sorted(scripts.keys())))
    print("Agents:", ", ".join(sorted(agents.keys())))
    gpt = GPTConnector()
    # call the connector; tests monkeypatch query()
    resp = gpt.query("ping")
    print(resp)