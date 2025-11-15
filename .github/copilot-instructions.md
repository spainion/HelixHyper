# GitHub Copilot Instructions for HelixHyper

## Project Overview
HyperHelix is a powerful context management system that orchestrates code analysis, task management, and execution through a multi-layered graph structure. The system provides comprehensive context management through graph-based storage, LLM integrations, and metadata-driven perception history.

## Key Architecture Concepts

### Core Components
- **HyperHelix**: Main graph class managing nodes and edges with thread-safe operations
- **Node**: Data structure with id, payload, tags, layer, strand, edges, metadata, and optional execute_fn
- **Edge**: Bidirectional weighted connections between nodes
- **NodeMetadata**: Tracks creation, updates, importance, permanence, and perception_history

### Module Structure
```
hyperhelix/
├── core.py              # HyperHelix class with add_node, add_edge, spiral_walk, shortest_path
├── node.py              # Node dataclass with execution capabilities
├── edge.py              # Edge connection helpers
├── metadata.py          # NodeMetadata for lifecycle tracking
├── utils.py             # API key management with get_api_key()
├── analytics/           # Node importance and permanence calculation
├── evolution/           # Auto-evolution engines (evented and continuous)
├── execution/           # Node execution and hook management
├── tasks/               # Task management and sprint planning
├── persistence/         # Database adapters (Neo4j, Qdrant, SQLAlchemy)
├── api/                 # FastAPI REST endpoints
├── cli/                 # Click-based command-line interface
├── agents/              # LLM integrations and code scanning
└── visualization/       # 3D coordinate generation and rendering
```

## Development Guidelines

### Code Style
- Use Python 3.12+ features and type hints
- Follow dataclass patterns for data structures
- Use `from __future__ import annotations` for forward references
- Log actions at appropriate levels (DEBUG, INFO, ERROR)
- Handle exceptions with context and re-raise when needed

### Logging
- Configure via `config/logging.yaml`
- Logs go to `hyperhelix.log`, errors to `errors.log`
- Use module-level loggers: `logger = logging.getLogger(__name__)`
- Never use bare `except` clauses

### Testing
- Run tests with `pytest -q`
- Use `USE_REAL_LLM=1` or `scripts/test_with_llm.sh` for live LLM tests
- Mock external services (OpenAI, OpenRouter, HuggingFace) in unit tests
- Integration tests skip automatically if API keys not present

### API Keys and Environment
- Access keys via `hyperhelix.utils.get_api_key(name, default=None)`
- Supported keys: `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `HUGGINGFACE_API_TOKEN`
- `GITHUB_TOKEN` for CLI issues command
- Development uses "test" as fallback for missing keys

### Common Patterns

#### Creating a Graph
```python
from hyperhelix.core import HyperHelix
from hyperhelix.node import Node

graph = HyperHelix()  # or with adapter: HyperHelix(adapter=Neo4jAdapter())
node = Node(id="a", payload={"data": "value"}, tags=["example"])
graph.add_node(node)
```

#### Adding Edges
```python
graph.add_edge("a", "b", weight=1.0)  # Creates bidirectional edge
```

#### Traversing the Graph
```python
# Breadth-first walk with depth limit
for node in graph.spiral_walk("start_id", depth=2):
    print(node.id)

# Shortest weighted path
path = graph.shortest_path("start", "end")
```

#### LLM Integration
```python
from hyperhelix.agents.llm import OpenRouterChatModel
from hyperhelix.agents.context import graph_summary
from hyperhelix.utils import get_api_key

model = OpenRouterChatModel(
    model="openai/gpt-4o",
    api_key=get_api_key("OPENROUTER_API_KEY")
)
messages = [
    {"role": "system", "content": graph_summary(graph)},
    {"role": "user", "content": "prompt"}
]
response = model.generate_response(messages)
```

### API Endpoints
- POST `/nodes` - Create node
- GET `/nodes/{id}` - Get node
- GET `/nodes` - List all nodes
- DELETE `/nodes/{id}` - Delete node and its edges
- POST `/nodes/{id}/execute` - Execute node
- POST `/edges` - Create edge
- DELETE `/edges/{a}/{b}` - Delete edge
- GET `/edges` - List all edges
- GET `/edges/{id}` - Get edges for node
- GET `/walk/{start_id}?depth=N` - Traverse graph
- POST `/scan` - Index directory
- POST `/suggest` - Get LLM suggestions
- POST `/chat` - Chat with LLM (includes graph summary)
- GET `/models/{provider}` - List available models
- GET `/summary` - Get graph summary
- GET `/export` - Export graph as JSON

### CLI Commands
```bash
python -m hyperhelix.cli.commands serve          # Start API server
python -m hyperhelix.cli.commands scan .         # Index directory
python -m hyperhelix.cli.commands issues org/repo # List GitHub issues
python -m hyperhelix.cli.commands codex "prompt"  # Quick LLM query
python -m hyperhelix.cli.commands models          # List models
python -m hyperhelix.cli.commands export out.json # Export graph
```

## What NOT to Do
- Don't leave TODO comments in code (use issues or docs)
- Don't commit without running `pytest -q`
- Don't use bare exceptions
- Don't modify working code unnecessarily
- Don't add dependencies without checking security advisories
- Don't hardcode API keys or credentials

## Key Files to Reference
- `README.md` - Getting started and API usage
- `docs/architecture.md` - System architecture overview
- `docs/modules.md` - Module responsibilities
- `config/logging.yaml` - Logging configuration
- `config/default.yaml` - Runtime settings
- `config/persistence.yaml` - Database adapter config
- `AGENTS.md` (in each directory) - Module-specific guidelines

## Persistence Adapters
When suggesting persistence code:
- Implement `BaseAdapter` interface
- Provide `save_node`, `load_node`, `save_edge`, `load_edges` methods
- Pass adapter to `HyperHelix(adapter=...)` for automatic persistence
- Existing adapters: `Neo4jAdapter`, `QdrantAdapter`, `SQLAlchemyAdapter`

## Evolution Engines
- Event-driven (default): `evented_engine.on_insert` registered automatically
- Calculates importance and permanence on node insertion
- Custom hooks via `register_insert_hook` and `register_update_hook`

## When Generating Tests
- Place in `tests/` directory
- Use pytest fixtures from `conftest.py`
- Mock external services
- Test both success and error paths
- Verify logging calls where appropriate
