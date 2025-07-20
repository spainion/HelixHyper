import pytest

from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.execution.executor import execute_node


def test_execute_node_error():
    g = HyperHelix()
    def bad(_: None):
        raise ValueError('boom')
    g.add_node(Node(id='x', payload=None, execute_fn=bad))
    with pytest.raises(ValueError):
        execute_node(g, 'x')
