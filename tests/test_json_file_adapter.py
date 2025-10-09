from hyperhelix.persistence.json_file_adapter import JSONFileAdapter


def test_json_file_adapter_roundtrip(tmp_path):
    path = tmp_path / "graph.json"
    adapter = JSONFileAdapter(path)
    adapter.save_node("n1", {"text": "hello"})
    assert adapter.load_node("n1") == {"text": "hello"}
    adapter.save_edge("n1", "n2", 0.7)
    assert adapter.load_edges("n1") == {"n2": 0.7}
    # Ensure data persists across instances
    adapter2 = JSONFileAdapter(path)
    assert adapter2.load_node("n1") == {"text": "hello"}
    assert adapter2.load_edges("n1") == {"n2": 0.7}
