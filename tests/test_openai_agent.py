import os
import pytest

from hyperhelix.core import HyperHelix
from hyperhelix.agents.openai_agent import create_graph_agent, run_graph_agent


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set; skipping openai agent test",
)
def test_graph_agent_runs():
    g = HyperHelix()
    agent = create_graph_agent(g)
    out = run_graph_agent(agent, "Hello")
    assert isinstance(out, str)
