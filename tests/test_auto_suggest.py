import os
import pytest

from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.execution.suggestion import enable_auto_suggest
from hyperhelix.tasks.task import Task


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set; skipping auto suggest test",
)
def test_auto_suggest_creates_task():
    g = HyperHelix()
    enable_auto_suggest(g)
    g.add_node(Node(id="x", payload="print('hi')"))
    assert "suggest-x" in g.nodes
    assert isinstance(g.nodes["suggest-x"].payload, Task)
