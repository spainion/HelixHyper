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
