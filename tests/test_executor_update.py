from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.execution.executor import execute_node


def test_execute_node_triggers_update_hooks():
    g = HyperHelix()
    called = {}
    g.register_update_hook(lambda _g, node_id: called.setdefault('id', node_id))
    g.add_node(Node(id='n', payload=None, execute_fn=lambda x: x))
    execute_node(g, 'n')
    assert called['id'] == 'n'
