from __future__ import annotations

from pathlib import Path
from types import ModuleType
import importlib.util

from ..core import HyperHelix
from ..node import Node


def scan_repository(graph: HyperHelix, base_path: str) -> None:
    """Add all Python files under ``base_path`` to the graph."""
    root = Path(base_path)
    for file in root.rglob("*.py"):
        content = file.read_text()
        node_id = f"file:{file.relative_to(root)}"
        graph.add_node(Node(id=node_id, payload={"path": str(file), "content": content}))


def load_module_from_node(graph: HyperHelix, node_id: str) -> ModuleType:
    """Load a Python module from the node's stored source code."""
    data = graph.nodes[node_id].payload
    source = data.get("content", "")
    spec = importlib.util.spec_from_loader(node_id, loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(source, module.__dict__)
    return module
