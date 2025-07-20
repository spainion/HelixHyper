from unittest.mock import patch

from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.evolution import continuous_engine


class DummyThread:
    def __init__(self, target, daemon=None):
        self.target = target
        self.daemon = daemon

    def start(self):
        try:
            self.target()
        except StopIteration:
            pass

    def join(self, timeout=None):
        pass


def test_run_periodically(monkeypatch):
    graph = HyperHelix()
    n = Node(id='a', payload=None)
    graph.add_node(n)
    captured = {}

    def fake_thread(target, daemon=True):
        captured['target'] = target
        return DummyThread(target, daemon)

    def fake_permanence(node):
        node.metadata.permanence = 1.0
        raise StopIteration

    with patch('hyperhelix.evolution.continuous_engine.threading.Thread', fake_thread), \
         patch('hyperhelix.evolution.continuous_engine.time.sleep', lambda x: None), \
         patch('hyperhelix.evolution.continuous_engine.compute_permanence', fake_permanence):
        thread = continuous_engine.run_periodically(graph, 0.0)
        assert isinstance(thread, DummyThread)
        try:
            captured['target']()
        except StopIteration:
            pass
        assert n.metadata.permanence == 1.0
