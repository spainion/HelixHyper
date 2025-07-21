from hyperhelix.core import HyperHelix
from hyperhelix.agents import webhook_listener
from hyperhelix.node import Node


def test_process_webhook():
    g = HyperHelix()
    webhook_listener.process_webhook(g, {'id': 'w1', 'msg': 'hi'})
    assert 'w1' in g.nodes and g.nodes['w1'].payload['msg'] == 'hi'
