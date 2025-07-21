# Persistence Guidelines
- Implement adapters for Neo4j, Qdrant and SQLAlchemy.
- Adapters must persist both nodes and edges using the BaseAdapter interface.
- Keep database settings in `config/persistence.yaml`.
