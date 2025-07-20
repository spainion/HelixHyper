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


def test_shortest_path():
    g = HyperHelix()
    g.add_node(Node(id='a', payload=None))
    g.add_node(Node(id='b', payload=None))
    g.add_node(Node(id='c', payload=None))
    g.add_edge('a', 'b', 1)
    g.add_edge('b', 'c', 2)
    g.add_edge('a', 'c', 5)

    assert g.shortest_path('a', 'c') == ['a', 'b', 'c']

    with pytest.raises(KeyError):
        g.shortest_path('missing', 'c')
