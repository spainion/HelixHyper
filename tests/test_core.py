from hyperhelix.core import HyperHelix
from hyperhelix.node import Node


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
