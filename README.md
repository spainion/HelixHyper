# HelixHyper

HelixHyper is a conceptual blueprint for a self-evolving AI context engine. It orchestrates code analysis, task management and execution through a multi-layered graph structure. While the current repository contains only documentation, the following layout describes the intended modules and their roles.

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

## Logging and Error Management
All modules use Python's `logging` package configured via `config/logging.yaml`. Errors should raise specific exceptions and be logged with context. Avoid TODO markers in production code—track open tasks in issue trackers or documentation instead.

## Contribution Guidelines
- Follow the structure above when adding modules.
- Keep logging consistent and avoid bare `except` clauses.
- Update documentation whenever functionality changes.
- Run available tests before submitting pull requests.

For repository-specific instructions see [AGENTS.md](AGENTS.md).

