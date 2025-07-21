from __future__ import annotations

from pathlib import Path
from types import ModuleType
import importlib.util
import ast

from ..core import HyperHelix
from ..node import Node


def scan_repository(graph: HyperHelix, base_path: str) -> None:
    """Add all Python files under ``base_path`` to the graph.

    Nodes are created for each file and edges link modules that import
    one another based on their ``import`` statements.
    """
    root = Path(base_path)
    mapping: dict[Path, str] = {}

    for file in root.rglob("*.py"):
        content = file.read_text()
        node_id = f"file:{file.relative_to(root)}"
        graph.add_node(Node(id=node_id, payload={"path": str(file), "content": content}))
        mapping[file.relative_to(root)] = node_id

    for rel_path, node_id in mapping.items():
        tree = ast.parse((root / rel_path).read_text())
        for stmt in ast.walk(tree):
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    target_rel = Path(alias.name.replace('.', '/')).with_suffix('.py')
                    target_id = mapping.get(target_rel)
                    if target_id:
                        graph.add_edge(node_id, target_id)
            elif isinstance(stmt, ast.ImportFrom) and stmt.module:
                target_rel = Path(stmt.module.replace('.', '/')).with_suffix('.py')
                target_id = mapping.get(target_rel)
                if target_id:
                    graph.add_edge(node_id, target_id)


def load_module_from_node(graph: HyperHelix, node_id: str) -> ModuleType:
    """Load a Python module from the node's stored source code."""
    data = graph.nodes[node_id].payload
    source = data.get("content", "")
    spec = importlib.util.spec_from_loader(node_id, loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(source, module.__dict__)
    return module
