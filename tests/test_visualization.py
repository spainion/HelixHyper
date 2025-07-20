from hyperhelix.node import Node
from hyperhelix.visualization.coords_generator import helix_coords
from hyperhelix.visualization.threejs_renderer import node_to_json


def test_visualization_helpers():
    node = Node(id='n', payload={'foo': 'bar'})
    coords = helix_coords(node, 0, 1)
    assert isinstance(coords, tuple) and len(coords) == 3
    data = node_to_json(node)
    assert data == {'id': 'n', 'payload': {'foo': 'bar'}}
