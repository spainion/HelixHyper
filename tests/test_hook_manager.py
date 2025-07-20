from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.execution import hook_manager


def test_bind_recursion_to_task():
    graph = HyperHelix()
    called = {}
    def task():
        called['x'] = True
    hook_manager.bind_recursion_to_task(graph, task)
    graph.add_node(Node(id='n', payload=None))
    assert called['x'] is True
