from hyperhelix.persistence.neo4j_adapter import Neo4jAdapter
from hyperhelix.persistence.qdrant_adapter import QdrantAdapter
from hyperhelix.persistence.sqlalchemy_adapter import SQLAlchemyAdapter


def test_adapters_save_and_load():
    for Adapter in (Neo4jAdapter, QdrantAdapter, SQLAlchemyAdapter):
        store = Adapter()
        store.save_node('a', {'x': 1})
        assert store.load_node('a') == {'x': 1}
        store.save_edge('a', 'b', 2.0)
        assert store.load_edges('a')['b'] == 2.0
