# HelixHyper

HelixHyper is a conceptual blueprint for a self-evolving AI context engine. It orchestrates code analysis, task management and execution through a multi-layered graph structure. While the current repository contains only documentation and example configuration, the following layout describes the intended modules and their roles. A sample logging setup lives in `config/logging.yaml` and can be adjusted as the project grows.

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
- **agents/** integrates chat interfaces and webhook events directly into the graph.
- **frontend/** is a reference React application to browse and edit the graph.
- **tests/** keep all modules verified.
- **docs/** provide architecture details and tutorials.

## Logging and Error Management
Python's `logging` package is configured through `config/logging.yaml`. Logs are emitted to the console and stored in `hyperhelix.log`, while errors are also written to `errors.log`. Tune log levels in that file to match the environment. When handling exceptions, log the failure with context and either re-raise or return a meaningful error to callers. Avoid TODO markers in committed code—track outstanding work in issue trackers or documentation.

## Contribution Guidelines
- Follow the structure above when adding modules.
- Keep logging consistent and avoid bare `except` clauses.
- Update documentation whenever functionality changes.
- Run available tests before submitting pull requests.

For repository-specific instructions see [AGENTS.md](AGENTS.md).

