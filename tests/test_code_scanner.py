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
