from __future__ import annotations

"""Integration with the OpenAI Agents SDK."""

from agents import Agent, Runner, function_tool
from agents.memory import SQLiteSession, Session

from ..core import HyperHelix
from ..node import Node
from .context import graph_summary
from ..execution.suggestion import auto_suggest


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

    @function_tool
    def autosuggest(node_id: str, provider: str = "openai", model: str | None = None) -> list[str]:
        """Generate follow-up tasks for ``node_id`` and return their descriptions."""
        tasks = auto_suggest(graph, node_id, provider=provider, model=model)
        return [t.description for t in tasks]

    inst = instructions or "You are a helpful assistant for graph operations."
    return Agent(
        name=name,
        instructions=inst,
        tools=[summary, list_nodes, add_node, connect_nodes, autosuggest],
    )


def run_graph_agent(agent: Agent, prompt: str, *, session: Session | None = None) -> str:
    """Send ``prompt`` to ``agent`` and return its final output."""
    result = Runner.run_sync(agent, prompt, session=session)
    return result.final_output


def create_session(session_id: str = "graph") -> Session:
    """Return a SQLite-backed session for conversation history."""
    return SQLiteSession(session_id)
