import os
import pytest

from hyperhelix.core import HyperHelix
from hyperhelix.agents.openai_agent import (
    create_graph_agent,
    run_graph_agent,
    run_graph_agent_async,
    create_session,
)


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set; skipping openai agent test",
)
def test_graph_agent_runs():
    g = HyperHelix()
    agent = create_graph_agent(g)
    session = create_session()
    out = run_graph_agent(agent, "Hello", session=session)
    assert isinstance(out, str)


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set; skipping openai agent test",
)
@pytest.mark.asyncio
async def test_graph_agent_runs_async():
    g = HyperHelix()
    agent = create_graph_agent(g)
    session = create_session()
    out = await run_graph_agent_async(agent, "Hello", session=session)
    assert isinstance(out, str)


def test_graph_agent_tools():
    g = HyperHelix()
    agent = create_graph_agent(g)
    tool_names = {t.name for t in agent.tools}
    assert {
        "summary",
        "list_nodes",
        "add_node",
        "connect_nodes",
        "autosuggest",
    } <= tool_names
