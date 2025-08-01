from hyperhelix.node import Node


def test_node_execute():
    called = {}

    def run(payload):
        called['result'] = payload
        return payload

    n = Node(id='1', payload={'a': 1}, execute_fn=run)
    result = n.execute()
    assert result == {'a': 1}
    assert called['result'] == {'a': 1}
    assert n.metadata.updated >= n.metadata.created

def test_node_execute_no_fn():
    n = Node(id='2', payload=None)
    assert n.execute() is None
