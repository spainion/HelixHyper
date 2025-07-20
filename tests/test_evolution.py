import pytest
from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.execution.executor import execute_node
from hyperhelix.evolution import evented_engine


def test_weave_by_tag_on_insert():
    g = HyperHelix()
    g.add_node(Node(id="a", payload=None, tags=["x"]))
    g.add_node(Node(id="b", payload=None, tags=["x"]))
    # event hook registered automatically
    assert "b" in g.nodes["a"].edges


def test_prune_missing_edges():
    g = HyperHelix()
    a = Node(id="a", payload=None)
    b = Node(id="b", payload=None)
    g.add_node(a)
    g.add_node(b)
    g.add_edge("a", "b")
    del g.nodes["b"]
    evented_engine.prune_missing_edges(g)
    assert "b" not in a.edges


def test_execute_updates_hooks_and_history():
    g = HyperHelix()
    n = Node(id="x", payload=1, execute_fn=lambda p: p + 1)
    g.add_node(n)
    execute_node(g, "x")
    assert n.metadata.perception_history == ["2"]

