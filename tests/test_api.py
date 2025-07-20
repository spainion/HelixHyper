from fastapi.testclient import TestClient
import pytest
from hyperhelix.api.main import app
from hyperhelix.core import HyperHelix

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
