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


def test_bind_recursion_with_node():
    graph = HyperHelix()
    seen = {}

    def task(g: HyperHelix, node_id: str, node: Node | None) -> None:
        seen[node_id] = g is graph and isinstance(node, Node)

    hook_manager.bind_recursion_with_node(graph, task)
    graph.add_node(Node(id='a', payload=None))

    assert seen == {'a': True}
