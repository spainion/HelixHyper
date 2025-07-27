from __future__ import annotations

from .core import HyperHelix
from .node import Node
from ultimate_zamida_fs_interpreter.memory.memory_graph import MemoryGraph


def merge_memory_graph(mem_graph: MemoryGraph, graph: HyperHelix | None = None) -> HyperHelix:
    """Merge ``mem_graph`` into ``graph`` returning the updated graph."""
    graph = graph or HyperHelix()
    # add nodes
    for mem_node in mem_graph.nodes.values():
        if mem_node.id not in graph.nodes:
            payload = {"content": mem_node.content, "metadata": mem_node.metadata}
            graph.add_node(Node(id=mem_node.id, payload=payload))
    # add edges ignoring relation names
    for src_id, mem_node in mem_graph.nodes.items():
        for targets in mem_node.edges.values():
            for dst_id in targets:
                if src_id in graph.nodes and dst_id in graph.nodes:
                    try:
                        graph.add_edge(src_id, dst_id)
                    except KeyError:
                        pass
    return graph

