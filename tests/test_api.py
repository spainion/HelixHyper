from fastapi.testclient import TestClient
import os
import pytest
from hyperhelix.api.main import app
from hyperhelix.core import HyperHelix
from hyperhelix.node import Node

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_graph():
    app.state.graph = HyperHelix()


def test_create_and_get_node():
    resp = client.post('/nodes', json={'id': 'a', 'payload': {'foo': 'bar'}})
    assert resp.status_code == 200
    data = resp.json()
    assert data['id'] == 'a'
    resp = client.get('/nodes/a')
    assert resp.status_code == 200
    assert resp.json()['payload'] == {'foo': 'bar'}


def test_create_edge_and_walk():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    client.post('/nodes', json={'id': 'b', 'payload': {}})
    resp = client.post('/edges', json={'a': 'a', 'b': 'b'})
    assert resp.status_code == 200
    walk = client.get('/walk/a', params={'depth': 1})
    assert walk.status_code == 200
    ids = {n['id'] for n in walk.json()}
    assert ids == {'a', 'b'}

def test_scan_endpoint(tmp_path):
    app.state.graph = HyperHelix()
    f = tmp_path / "a.py"
    f.write_text("x=1")
    resp = client.post('/scan', json={'path': str(tmp_path)})
    assert resp.status_code == 200
    assert f"file:{f.name}" in app.state.graph.nodes

def test_root_endpoint():
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}


def test_duplicate_node_error():
    client.post('/nodes', json={'id': 'x', 'payload': {}})
    resp = client.post('/nodes', json={'id': 'x', 'payload': {}})
    assert resp.status_code == 400


def test_edge_missing_node():
    resp = client.post('/edges', json={'a': 'x', 'b': 'y'})
    assert resp.status_code == 404


def test_walk_missing_start():
    resp = client.get('/walk/missing')
    assert resp.status_code == 404

def test_autobloom():
    client.post('/nodes', json={'id': 'orig', 'payload': {}})
    resp = client.post('/autobloom/orig')
    assert resp.status_code == 200
    assert 'bloom:orig' in app.state.graph.nodes


def test_get_missing_node():
    resp = client.get('/nodes/none')
    assert resp.status_code == 404


def test_delete_node():
    client.post('/nodes', json={'id': 'z', 'payload': {}})
    resp = client.delete('/nodes/z')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'deleted'
    assert 'z' not in app.state.graph.nodes


def test_list_nodes():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    client.post('/nodes', json={'id': 'b', 'payload': {}})
    resp = client.get('/nodes')
    assert resp.status_code == 200
    ids = {n['id'] for n in resp.json()}
    assert ids == {'a', 'b'}


def test_list_edges():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    client.post('/nodes', json={'id': 'b', 'payload': {}})
    client.post('/edges', json={'a': 'a', 'b': 'b', 'weight': 2.0})
    resp = client.get('/edges')
    assert resp.status_code == 200
    edges = {(e['a'], e['b'], e['weight']) for e in resp.json()}
    assert edges == {('a', 'b', 2.0)}


def test_delete_edge():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    client.post('/nodes', json={'id': 'b', 'payload': {}})
    client.post('/edges', json={'a': 'a', 'b': 'b'})
    resp = client.delete('/edges/a/b')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'deleted'
    assert 'b' not in app.state.graph.nodes['a'].edges


def test_delete_missing_edge():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    client.post('/nodes', json={'id': 'b', 'payload': {}})
    resp = client.delete('/edges/a/b')
    assert resp.status_code == 404


def test_list_node_edges():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    client.post('/nodes', json={'id': 'b', 'payload': {}})
    client.post('/edges', json={'a': 'a', 'b': 'b'})
    resp = client.get('/edges/a')
    assert resp.status_code == 200
    assert resp.json() == [{'a': 'a', 'b': 'b', 'weight': 1.0}]


def test_list_edges_missing_node():
    resp = client.get('/edges/missing')
    assert resp.status_code == 404


def test_summary_endpoint():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    resp = client.get('/summary')
    assert resp.status_code == 200
    data = resp.json()['summary']
    assert '1' in data


def test_execute_node_endpoint():
    called = {}
    app.state.graph.add_node(Node(id='x', payload=None, execute_fn=lambda _: called.setdefault('x', True)))
    resp = client.post('/nodes/x/execute')
    assert resp.status_code == 200
    assert called.get('x') is True
    data = resp.json()
    assert data['id'] == 'x'


def test_export_endpoint():
    client.post('/nodes', json={'id': 'a', 'payload': {}})
    client.post('/nodes', json={'id': 'b', 'payload': {}})
    client.post('/edges', json={'a': 'a', 'b': 'b'})
    resp = client.get('/export')
    assert resp.status_code == 200
    data = resp.json()
    ids = {n['id'] for n in data['nodes']}
    assert {'a', 'b'} <= ids
    assert any(e['a'] == 'a' and e['b'] == 'b' for e in data['edges'])


def test_chat_endpoint(monkeypatch):
    captured = {}

    def fake_generate(self, msgs):
        captured['messages'] = msgs
        return 'ok'

    monkeypatch.setattr(
        'hyperhelix.api.routers.chat.OpenAIChatModel.generate_response',
        fake_generate,
    )
    resp = client.post('/chat', json={'prompt': 'hi', 'provider': 'openai'})
    assert resp.status_code == 200
    assert resp.json() == {'response': 'ok'}
    assert captured['messages'][0]['role'] == 'system'


def test_task_endpoints():
    resp = client.post('/tasks', json={'id': 't1', 'description': 'demo'})
    assert resp.status_code == 200
    resp = client.post('/tasks/t1/assign', json={'user': 'bob'})
    assert resp.status_code == 200
    listing = client.get('/tasks')
    assert listing.status_code == 200
    assert listing.json()[0]['id'] == 't1'
    plan = client.get('/tasks/plan')
    assert plan.status_code == 200
    assert plan.json() == ['t1']


@pytest.mark.skipif(
    not os.getenv('OPENAI_API_KEY'),
    reason='OPENAI_API_KEY not set; skipping live integration test',
)
def test_suggest_endpoint():
    resp = client.post('/suggest', json={'prompt': 'Hello', 'provider': 'openai'})
    assert resp.status_code == 200
    assert 'response' in resp.json()


@pytest.mark.skipif(
    not os.getenv('OPENROUTER_API_KEY'),
    reason='OPENROUTER_API_KEY not set; skipping live integration test',
)
def test_suggest_endpoint_openrouter():
    resp = client.post('/suggest', json={'prompt': 'Hello', 'provider': 'openrouter'})
    assert resp.status_code == 200
    assert 'response' in resp.json()


@pytest.mark.skipif(
    not os.getenv('HUGGINGFACE_API_TOKEN'),
    reason='HUGGINGFACE_API_TOKEN not set; skipping live integration test',
)
def test_suggest_endpoint_huggingface():
    resp = client.post('/suggest', json={'prompt': 'Hello', 'provider': 'huggingface'})
    assert resp.status_code == 200
    assert 'response' in resp.json()


@pytest.mark.skipif(
    not os.getenv('OPENROUTER_API_KEY'),
    reason='OPENROUTER_API_KEY not set; skipping live integration test',
)
def test_list_openrouter_models_endpoint():
    resp = client.get('/models/openrouter')
    assert resp.status_code == 200
    assert isinstance(resp.json(), list) and resp.json()


def test_list_huggingface_models_endpoint(monkeypatch):
    monkeypatch.setattr(
        'hyperhelix.api.routers.models.list_huggingface_models',
        lambda search='gpt2', limit=5: ['model-a', 'model-b'],
    )
    resp = client.get('/models/huggingface?q=gpt2')
    assert resp.status_code == 200
    assert resp.json() == ['model-a', 'model-b']


def test_suggest_includes_context(capture_openai):
    resp = client.post('/suggest', json={'prompt': 'hi', 'provider': 'openai'})
    assert resp.status_code == 200
    if capture_openai is not None:
        assert capture_openai['messages'][0]['role'] == 'system'


def test_suggest_includes_context_hf(capture_huggingface):
    resp = client.post('/suggest', json={'prompt': 'hi', 'provider': 'huggingface'})
    assert resp.status_code == 200
    if capture_huggingface is not None:
        assert capture_huggingface['messages'][0]['role'] == 'system'


def test_suggest_includes_context_local(capture_local):
    resp = client.post('/suggest', json={'prompt': 'hi', 'provider': 'local'})
    assert resp.status_code == 200
    if capture_local is not None:
        assert capture_local['messages'][0]['role'] == 'system'

