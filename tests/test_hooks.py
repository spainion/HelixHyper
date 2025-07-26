from hyperhelix.core import HyperHelix
from hyperhelix.node import Node


def test_register_insert_hook_called():
    graph = HyperHelix()
    called = {}

    def hook(g: HyperHelix, node_id: str) -> None:
        called['id'] = node_id

    graph.register_insert_hook(hook)
    graph.add_node(Node(id='x', payload=None))
    assert called['id'] == 'x'


def test_evented_engine_updates_metadata():
    graph = HyperHelix()
    graph.add_node(Node(id='a', payload=None))
    assert graph.nodes['a'].metadata.permanence > 0


def test_insert_hook_exception_does_not_stop_others():
    graph = HyperHelix()
    executed = []

    def failing_hook(g: HyperHelix, node_id: str) -> None:
        executed.append('fail')
        raise RuntimeError('boom')

    def good_hook(g: HyperHelix, node_id: str) -> None:
        executed.append('good')

    graph.register_insert_hook(failing_hook)
    graph.register_insert_hook(good_hook)
    graph.add_node(Node(id='t', payload=None))

    assert executed == ['fail', 'good']
