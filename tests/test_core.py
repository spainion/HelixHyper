from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
import pytest


def test_add_and_walk():
    graph = HyperHelix()
    a = Node(id='a', payload=None)
    b = Node(id='b', payload=None)
    graph.add_node(a)
    graph.add_node(b)
    graph.add_edge('a', 'b')

    nodes = list(graph.spiral_walk('a', depth=1))
    ids = {n.id for n in nodes}
    assert ids == {'a', 'b'}


def test_add_edge_missing_node():
    graph = HyperHelix()
    graph.add_node(Node(id='a', payload=None))
    with pytest.raises(KeyError):
        graph.add_edge('a', 'missing')


def test_spiral_walk_missing_start():
    graph = HyperHelix()
    with pytest.raises(KeyError):
        list(graph.spiral_walk('missing'))
