# AI Agent Instructions for HelixHyper

## System Identity
**HyperHelix** is a powerful context management system that orchestrates code analysis, task management, and execution through a multi-layered graph structure.

## Primary Use Cases
1. **Context Management**: Store and retrieve contextual information via graph structure
2. **Code Analysis**: Scan repositories and link files via import dependencies
3. **Task Orchestration**: Manage tasks with priority, assignment, and sprint planning
4. **LLM Integration**: Provide graph context to language models for enhanced responses
5. **Execution Management**: Execute code and track results in node perception history

## Quick Start for AI Agents

### Installation
```bash
pip install -r requirements.txt
python -m pytest -q  # Verify installation
```

### Basic Operations
```python
from hyperhelix.core import HyperHelix
from hyperhelix.node import Node

# Create graph
graph = HyperHelix()

# Add nodes
node = Node(id="task1", payload={"description": "Implement feature"}, tags=["python", "backend"])
graph.add_node(node)

# Connect nodes
graph.add_edge("task1", "task2", weight=1.0)

# Traverse graph
for node in graph.spiral_walk("task1", depth=2):
    process(node)

# Find by tag
python_nodes = graph.find_nodes_by_tag("python")
```

### API Server
```bash
# Start server
uvicorn hyperhelix.api.main:app --reload
# or
python -m hyperhelix.cli.commands serve

# Create node via API
curl -X POST http://localhost:8000/nodes \
  -H 'Content-Type: application/json' \
  -d '{"id": "n1", "payload": {"data": "value"}}'

# Get graph summary
curl http://localhost:8000/summary
```

### LLM Integration Patterns
```python
# OpenRouter (recommended for best models)
from hyperhelix.agents.llm import OpenRouterChatModel
from hyperhelix.agents.context import graph_summary

model = OpenRouterChatModel(model="openai/gpt-4o", api_key="YOUR_KEY")
messages = [
    {"role": "system", "content": graph_summary(graph)},
    {"role": "user", "content": "Analyze this codebase"}
]
response = model.generate_response(messages)

# Streaming responses
response = model.stream_response(messages)  # Returns complete text

# OpenAI
from hyperhelix.agents.llm import OpenAIChatModel
model = OpenAIChatModel(model="gpt-4", api_key="YOUR_KEY")

# HuggingFace
from hyperhelix.agents.llm import HuggingFaceChatModel
model = HuggingFaceChatModel(model="HuggingFaceH4/zephyr-7b-beta", api_key="YOUR_KEY")

# Local Transformers
from hyperhelix.agents.llm import TransformersChatModel
model = TransformersChatModel(model="sshleifer/tiny-gpt2")
```

## Architecture Deep Dive

### Graph Structure
- **Nodes**: Store data with `id`, `payload`, `tags`, `layer`, `strand`, `metadata`
- **Edges**: Bidirectional weighted connections stored in `node.edges` dict
- **Metadata**: Tracks `created`, `updated`, `importance`, `permanence`, `perception_history`

### Core Operations
- `add_node(node)`: Add node to graph, triggers insert hooks
- `add_edge(a, b, weight=1.0)`: Connect two nodes bidirectionally
- `remove_node(node_id)`: Delete node and all its edges
- `remove_edge(a, b)`: Delete edge between nodes
- `find_nodes_by_tag(tag)`: Search nodes by tag
- `spiral_walk(start_id, depth=1)`: BFS traversal with depth limit
- `shortest_path(start_id, end_id)`: Dijkstra's algorithm on weighted edges

### Event Hooks
```python
def my_insert_hook(graph: HyperHelix, node_id: str) -> None:
    node = graph.nodes[node_id]
    # Custom logic on insert
    
graph.register_insert_hook(my_insert_hook)
graph.register_update_hook(my_update_hook)
```

### Persistence
```python
from hyperhelix.persistence.neo4j_adapter import Neo4jAdapter

adapter = Neo4jAdapter(uri="bolt://localhost:7687", user="neo4j", password="password")
graph = HyperHelix(adapter=adapter)
# All add_node and add_edge calls now persist automatically
```

### Code Scanning
```python
from hyperhelix.agents.code_scanner import scan_repository

scan_repository(graph, "/path/to/repo")
# Creates nodes for Python files and links via import statements
```

## Environment Configuration

### Required Variables
- `OPENAI_API_KEY`: For OpenAI chat models
- `OPENROUTER_API_KEY`: For OpenRouter chat models (supports many providers)
- `HUGGINGFACE_API_TOKEN`: For HuggingFace Inference API
- `GITHUB_TOKEN`: For CLI GitHub issues command (optional)

### Configuration Files
- `config/default.yaml`: Runtime settings (strands, thresholds)
- `config/logging.yaml`: Python logging configuration
- `config/persistence.yaml`: Database connection details

## Testing Strategy

### Run Tests
```bash
pytest -q                    # Quick test run
pytest -v                    # Verbose output
pytest --cov=hyperhelix     # Coverage report
USE_REAL_LLM=1 pytest       # Test with real LLM APIs
scripts/test_with_llm.sh    # Convenient wrapper
```

### Writing Tests
- Use pytest fixtures from `tests/conftest.py`
- Mock external services (patch `httpx.post`, `openai.ChatCompletion`, etc.)
- Tests automatically skip if required API keys missing
- Always test error paths

### Test Organization
```
tests/
├── test_core.py           # Graph operations
├── test_node.py           # Node behavior
├── test_api.py            # FastAPI endpoints
├── test_cli_commands.py   # CLI commands
├── test_llm.py            # LLM integrations
├── test_code_scanner.py   # Code scanning
└── ...
```

## CLI Usage Examples

```bash
# Start API server
python -m hyperhelix.cli.commands serve

# Scan a repository
python -m hyperhelix.cli.commands scan /path/to/repo

# List GitHub issues
python -m hyperhelix.cli.commands issues owner/repo

# Quick LLM query with graph context
python -m hyperhelix.cli.commands codex "Explain this codebase" --provider openrouter
python -m hyperhelix.cli.commands codex "Generate tests" --provider openai --model gpt-4
python -m hyperhelix.cli.commands codex "Refactor this" --provider local --stream

# List available models
python -m hyperhelix.cli.commands models --provider openrouter
python -m hyperhelix.cli.commands models --provider huggingface --query gpt2 --limit 10

# Export graph
python -m hyperhelix.cli.commands export graph.json
python -m hyperhelix.cli.commands export -  # Print to stdout
```

## API Reference

### Node Operations
- **POST /nodes**: Create node with `id` and `payload`
- **GET /nodes/{id}**: Retrieve specific node
- **GET /nodes**: List all nodes
- **DELETE /nodes/{id}**: Remove node and edges
- **POST /nodes/{id}/execute**: Execute node's callable

### Edge Operations
- **POST /edges**: Create edge with `a`, `b`, optional `weight`
- **GET /edges**: List all edges
- **GET /edges/{id}**: List edges connected to node
- **DELETE /edges/{a}/{b}**: Remove specific edge

### Graph Operations
- **GET /walk/{start_id}?depth=N**: Traverse from node
- **GET /summary**: Get graph statistics and context
- **GET /export**: Export full graph as JSON

### Analysis Operations
- **POST /scan**: Scan directory, expects `path` parameter
- **POST /autobloom/{node_id}**: Auto-expand node connections

### LLM Operations
- **POST /suggest**: Get code suggestions with graph context
  - Body: `{"prompt": "...", "provider": "openrouter|openai|huggingface|local"}`
- **POST /chat**: Chat with LLM including graph summary
  - Body: `{"prompt": "...", "provider": "openrouter"}`
- **GET /models/{provider}**: List available models
  - Providers: `openrouter`, `huggingface`
  - Query param `q` for HuggingFace search

### Task Operations
- **POST /tasks**: Create task node
- **POST /tasks/{id}/assign**: Assign task to user
- **GET /tasks**: List all tasks
- **GET /tasks/plan**: Get sprint plan

## Common Patterns for AI Agents

### Pattern 1: Context-Aware Code Analysis
```python
from hyperhelix.core import HyperHelix
from hyperhelix.agents.code_scanner import scan_repository
from hyperhelix.agents.context import graph_summary

# Build context from repository
graph = HyperHelix()
scan_repository(graph, ".")

# Use context with LLM
context = graph_summary(graph)
# Feed to your LLM with user query
```

### Pattern 2: Task Dependency Management
```python
from hyperhelix.tasks.task_manager import create_task, assign_task

task1 = create_task(graph, "t1", "Implement API", priority=1)
task2 = create_task(graph, "t2", "Write tests", priority=2)
graph.add_edge("t1", "t2")  # t2 depends on t1

assign_task(graph, "t1", "developer@example.com")
```

### Pattern 3: Execution Tracking
```python
def build_code(payload):
    # Your build logic
    return {"status": "success", "artifacts": ["dist/app.js"]}

node = Node(id="build", payload={"command": "npm run build"}, execute_fn=build_code)
graph.add_node(node)

result = node.execute()  # Executes and stores in perception_history
```

### Pattern 4: Knowledge Graph Integration
```python
# Store architectural decisions
decision = Node(
    id="arch-001",
    payload={"title": "Use FastAPI", "rationale": "..."},
    tags=["architecture", "decision", "api"]
)
graph.add_node(decision)

# Link to related components
graph.add_edge("arch-001", "api-module")
graph.add_edge("arch-001", "auth-service")

# Query later
decisions = graph.find_nodes_by_tag("architecture")
```

## Development Workflow

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Configure Logging**: Edit `config/logging.yaml` if needed
3. **Set API Keys**: Export environment variables for LLM providers
4. **Run Tests**: `pytest -q` to verify setup
5. **Start Development**: Use API or CLI as entry point
6. **Iterate**: Make changes, test frequently, check logs
7. **Document**: Update relevant `AGENTS.md` files in module directories

## Troubleshooting

### Import Errors
- Ensure dependencies installed: `pip install -r requirements.txt`
- Check Python version: Requires 3.12+

### API Key Issues
- Use `hyperhelix.utils.get_api_key()` for environment variables
- Development mode uses "test" as fallback for OpenAI
- Check logs for warnings about missing keys

### Test Failures
- Some tests skip without API keys (expected)
- Use `USE_REAL_LLM=1` for integration tests
- Check `hyperhelix.log` and `errors.log` for details

### Database Connection
- Configure in `config/persistence.yaml`
- Ensure Neo4j/Qdrant running if using those adapters
- SQLAlchemy uses local SQLite by default

## Module-Specific Guidelines

Each module has its own `AGENTS.md` file:
- `/hyperhelix/AGENTS.md` - Core module guidelines
- `/hyperhelix/api/AGENTS.md` - API development
- `/hyperhelix/cli/AGENTS.md` - CLI commands
- `/hyperhelix/agents/AGENTS.md` - LLM integration
- `/hyperhelix/tasks/AGENTS.md` - Task management
- `/hyperhelix/persistence/AGENTS.md` - Database adapters
- `/hyperhelix/analytics/AGENTS.md` - Node metrics
- `/hyperhelix/evolution/AGENTS.md` - Auto-evolution
- `/hyperhelix/execution/AGENTS.md` - Node execution
- `/hyperhelix/visualization/AGENTS.md` - 3D rendering

## Contributing Guidelines

1. Keep directory structure from `README.md`
2. Configure logging via `config/logging.yaml`
3. Remove TODO comments before committing
4. Run `pytest` before each commit
5. Update documentation with new functionality
6. Set LLM provider keys in environment
7. Follow existing code patterns and style

## Integration with GitHub Copilot

This repository is configured for optimal GitHub Copilot experience:
- Comprehensive inline documentation
- Clear type hints throughout
- Consistent naming conventions
- Module-level guidelines in `AGENTS.md` files
- Example usage in docstrings
- Test files demonstrate patterns

## Integration with Codex/ChatGPT

When using with ChatGPT or OpenAI Codex:
1. Reference this file for system overview
2. Check module-specific `AGENTS.md` for detailed guidance
3. Use `docs/architecture.md` for design decisions
4. Refer to `docs/modules.md` for component responsibilities
5. Look at test files for usage examples
6. Review `README.md` for getting started guide

## Key Design Principles

1. **Simplicity**: Minimal abstractions, clear interfaces
2. **Extensibility**: Hook system for custom behavior
3. **Persistence**: Pluggable adapters for any database
4. **Observability**: Comprehensive logging throughout
5. **Context-Aware**: Graph summaries enhance LLM interactions
6. **Type Safety**: Full type hints for better tooling
7. **Testing**: High coverage with mocked external services
8. **Documentation**: Every module has guidelines

## Advanced Topics

### Custom Persistence Adapter
```python
from hyperhelix.persistence.base_adapter import BaseAdapter

class MyAdapter(BaseAdapter):
    def save_node(self, node_id: str, payload: Any) -> None:
        # Your implementation
        pass
    
    def load_node(self, node_id: str) -> Any:
        pass
    
    def save_edge(self, a: str, b: str, weight: float) -> None:
        pass
    
    def load_edges(self, node_id: str) -> list:
        pass
```

### Custom Evolution Engine
```python
from hyperhelix.evolution.evented_engine import on_insert

def custom_evolution(graph: HyperHelix, node_id: str) -> None:
    # Your custom logic
    node = graph.nodes[node_id]
    # Calculate custom metrics
    # Update node properties
    # Link to similar nodes
    
graph.register_insert_hook(custom_evolution)
```

### Custom LLM Provider
```python
from hyperhelix.agents.llm import BaseChatModel

class MyLLMModel(BaseChatModel):
    def generate_response(self, messages: list) -> str:
        # Your implementation
        pass
```

## Resources

- **Main README**: `/README.md`
- **Architecture**: `/docs/architecture.md`
- **Modules Guide**: `/docs/modules.md`
- **Docker Guide**: `/docs/docker.md`
- **Build Instructions**: `/docs/AGENTS.md`
- **Root Guidelines**: `/AGENTS.md`

## Support and Feedback

For issues, feature requests, or questions:
1. Check existing documentation first
2. Review module-specific `AGENTS.md` files
3. Look at test files for examples
4. Consult logs (`hyperhelix.log`, `errors.log`)
5. Open GitHub issue with details

---

**Remember**: HyperHelix is a context management system. Always think in terms of nodes (data), edges (relationships), and context (graph structure + metadata).
