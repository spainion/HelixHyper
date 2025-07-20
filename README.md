# HelixHyper

HelixHyper orchestrates code analysis, task management and execution through a multi-layered graph structure.
HelixHyper provides a minimal implementation alongside documentation and configuration. The layout below outlines the complete system as it grows.

## Getting Started
Install dependencies and run the small test suite to verify the environment:

```bash
pip install -r requirements.txt
python -m pytest -q
```
```
hyperhelix_system/
├── README.md
├── LICENSE
├── setup.py
├── requirements.txt
├── config/
│   ├── default.yaml
│   ├── logging.yaml
│   └── persistence.yaml
├── hyperhelix/
│   ├── __init__.py
│   ├── node.py
│   ├── edge.py
│   ├── metadata.py
│   ├── core.py
│   ├── analytics/
│   │   ├── importance.py
│   │   └── permanence.py
│   ├── evolution/
│   │   ├── evented_engine.py
│   │   └── continuous_engine.py
│   ├── execution/
│   │   ├── executor.py
│   │   └── hook_manager.py
│   ├── tasks/
│   │   ├── task.py
│   │   ├── task_manager.py
│   │   └── sprint_planner.py
│   ├── persistence/
│   │   ├── base_adapter.py
│   │   ├── neo4j_adapter.py
│   │   ├── qdrant_adapter.py
│   │   └── sqlalchemy_adapter.py
│   ├── api/
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       ├── nodes.py
│   │       ├── edges.py
│   │       ├── walk.py
│   │       └── bloom.py
│   ├── cli/
│   │   └── commands.py
│   ├── visualization/
│   │   ├── coords_generator.py
│   │   └── threejs_renderer.py
│   └── agents/
│       ├── chat_adapter.py
│       └── webhook_listener.py
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── GraphView.jsx
│       └── services/
│           └── hyperhelix_api.js
├── tests/
├── docs/
```

## Module Responsibilities
The directories above form a cohesive system:
- **config/** holds runtime constants, logging and persistence settings.
- **hyperhelix/node.py** defines node fields (id, payload, tags, layer, strand, edges) and metadata (creation time, updates, importance, permanence, perception history) along with execution helpers.
- **hyperhelix/core.py** provides the `HyperHelix` graph with thread-safe `add_node`, `add_edge` and `spiral_walk` operations.
- **analytics/** recalculates node importance and permanence on demand.
- **evolution/evented_engine.py** reacts instantly to insert/update hooks, pruning or weaving without polling.
- **execution/** bridges external callables (builds, tests, deploys) into graph execution and auto-bloom hooks.
- **tasks/** manages project tasks through graph-driven `create_task`, `assign_task` and `sprint_plan` helpers.
- **persistence/** stores nodes and edges via pluggable adapters for Neo4j, Qdrant or SQLAlchemy.
- **api/** exposes operations over REST and GraphQL using Pydantic schemas and optional auth stubs.
- **cli/** offers local commands to initialise, import, export and serve the system.
- **visualization/** generates 3D coordinates for Three.js rendering.
 - **agents/** integrates chat interfaces and webhook events directly into the graph and provides helpers for LLM integrations.
- **frontend/** is a reference React application to browse and edit the graph.
- **tests/** keep all modules verified.
- **docs/** provide architecture details and tutorials.

## Logging and Error Management
Python's `logging` package is configured through `config/logging.yaml`. Logs are emitted to the console and stored in `hyperhelix.log`, while errors are also written to `errors.log`. Tune log levels in that file to match the environment. When handling exceptions, log the failure with context and either re-raise or return a meaningful error to callers. Avoid TODO markers in committed code—track outstanding work in issue trackers or documentation.
The graph core validates nodes when creating edges and logs an error if a referenced node is missing. `spiral_walk` checks the starting node ID and raises `KeyError` when absent. Each node updates its `metadata.updated` timestamp whenever `execute()` runs so event timing stays accurate.

## LLM Integration
Use the helpers in `hyperhelix.agents.llm` to connect to popular language models such as OpenAI. Chat messages can be processed with `handle_chat_message`, which stores the conversation in the graph and records any model replies. API keys are read from environment variables.

## Contribution Guidelines
- Follow the structure above when adding modules.
- Keep logging consistent and avoid bare `except` clauses.
- Update documentation whenever functionality changes.
- Run available tests before submitting pull requests.

For repository-specific instructions see [AGENTS.md](AGENTS.md).
Detailed build and deployment guidance lives in [docs/AGENTS.md](docs/AGENTS.md).
Each major module also provides its own `AGENTS.md` with focused guidelines.


With this in place, your **Living Hyper-Helix**:
- Loads & persists a spherical, self-evolving graph
- Evolves instantly on every insert/update
- Self-analyzes importance, permanence and perception shifts
- Executes real-world code and tasks from nodes
- Orchestrates entire software projects and teams
- Renders in 3D, responds to chat and webhook events
- Scales from a single developer to global micro-services
- Quickly queries context with `find_nodes_by_tag` and integrates responses from popular LLMs

This is the full system—every file, class and function—powering a zero-bloat, infinitely weaving digital brain.
