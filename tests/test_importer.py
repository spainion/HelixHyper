from hyperhelix.core import HyperHelix
from hyperhelix.importer import merge_memory_graph
from ultimate_zamida_fs_interpreter.memory.memory_graph import MemoryGraph


def test_merge_memory_graph():
    g = MemoryGraph()
    n1 = g.add_node("foo")
    n2 = g.add_node("bar")
    g.link_nodes(n1.id, "ref", n2.id)

    hh = HyperHelix()
    merge_memory_graph(g, hh)

    assert set(hh.nodes.keys()) == {n1.id, n2.id}
    assert n2.id in hh.nodes[n1.id].edges

