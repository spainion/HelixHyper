from ultimate_zamida_fs_interpreter.memory.memory_graph import MemoryGraph
from ultimate_zamida_fs_interpreter.memory import persistence


def test_memory_graph_version_and_persistence(tmp_path):
    g = MemoryGraph()
    g.add_node("hello")
    path = tmp_path / "g.json"
    persistence.save(g, path)
    assert g.version == "0.01"
    loaded = persistence.load(path)
    assert len(loaded.nodes) == 1
