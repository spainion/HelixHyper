from hyperhelix.core import HyperHelix
from hyperhelix.node import Node


def test_find_nodes_by_tag():
    g = HyperHelix()
    g.add_node(Node(id="a", payload=None, tags=["x"]))
    g.add_node(Node(id="b", payload=None, tags=["y", "x"]))
    res = g.find_nodes_by_tag("x")
    ids = {n.id for n in res}
    assert ids == {"a", "b"}
