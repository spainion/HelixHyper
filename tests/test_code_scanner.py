from hyperhelix.core import HyperHelix
from hyperhelix.agents.code_scanner import scan_repository, load_module_from_node
import tempfile
from pathlib import Path


def test_scan_and_load():
    graph = HyperHelix()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "mod.py"
        path.write_text("def hello():\n    return 'hi'")
        scan_repository(graph, tmp)
        node_id = f"file:{path.name}"
        mod = load_module_from_node(graph, node_id)
        assert mod.hello() == 'hi'


def test_scan_import_edges():
    graph = HyperHelix()
    with tempfile.TemporaryDirectory() as tmp:
        a = Path(tmp) / "a.py"
        b = Path(tmp) / "b.py"
        a.write_text("import b\n")
        b.write_text("def x():\n    return 1\n")
        scan_repository(graph, tmp)
        node_a = "file:a.py"
        node_b = "file:b.py"
        assert node_b in graph.nodes[node_a].edges
