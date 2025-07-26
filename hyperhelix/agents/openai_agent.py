from __future__ import annotations

"""Integration with the OpenAI Agents SDK."""

from agents import Agent, Runner, function_tool

from ..core import HyperHelix
from .context import graph_summary


def create_graph_agent(graph: HyperHelix, *, name: str = "GraphAssistant", instructions: str | None = None) -> Agent:
    """Return an OpenAI agent configured to inspect ``graph``."""

    @function_tool
    def summary() -> str:
        """Return a one-line summary of the current graph."""
        return graph_summary(graph)

    inst = instructions or "You are a helpful assistant for graph operations."
    return Agent(name=name, instructions=inst, tools=[summary])


def run_graph_agent(agent: Agent, prompt: str) -> str:
    """Send ``prompt`` to ``agent`` and return its final output."""
    result = Runner.run_sync(agent, prompt)
    return result.final_output
