from __future__ import annotations

"""Integration with the OpenAI Agents SDK."""

from agents import Agent, Runner, function_tool

from ..core import HyperHelix
from ..node import Node
from .context import graph_summary


def create_graph_agent(graph: HyperHelix, *, name: str = "GraphAssistant", instructions: str | None = None) -> Agent:
    """Return an OpenAI agent configured to inspect ``graph``."""

    @function_tool
    def summary() -> str:
        """Return a one-line summary of the current graph."""
        return graph_summary(graph)

    @function_tool
    def list_nodes() -> list[str]:
        """Return the ids of all nodes in the graph."""
        return list(graph.nodes.keys())

    @function_tool
    def add_node(id: str, payload: str) -> str:
        """Insert a new node and return ``id``."""
        graph.add_node(Node(id=id, payload=payload))
        return id

    @function_tool
    def connect_nodes(a: str, b: str) -> str:
        """Connect two nodes with an edge and return ``a-b``."""
        graph.add_edge(a, b)
        return f"{a}-{b}"

    inst = instructions or "You are a helpful assistant for graph operations."
    return Agent(
        name=name,
        instructions=inst,
        tools=[summary, list_nodes, add_node, connect_nodes],
    )


def run_graph_agent(agent: Agent, prompt: str) -> str:
    """Send ``prompt`` to ``agent`` and return its final output."""
    result = Runner.run_sync(agent, prompt)
    return result.final_output
