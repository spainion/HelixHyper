# HelixHyper

HelixHyper orchestrates code analysis, task management and execution through a multi-layered graph structure.
HelixHyper provides a minimal implementation alongside documentation and configuration. The layout below outlines the complete system as it grows.

## Getting Started
Clone the repository and install all dependencies before running any commands.

```bash
git clone <repo-url> && cd HelixHyper
pip install -r requirements.txt
python -m pytest -q
```

Start the API once tests pass:

```bash
uvicorn hyperhelix.api.main:app --reload
```

You can also run the server via the CLI command:

```bash
python -m hyperhelix.cli.commands serve
```

Alternatively build and run the provided Dockerfile:

```bash
docker build -t helixhyper .
docker run -p 8000:8000 helixhyper
```

## Development Workflow
Follow these practices when contributing to ensure consistent builds and clear logs:

1. Install dependencies with `pip install -r requirements.txt` and set any required keys such as `OPENAI_API_KEY` in your environment.
2. Run `pytest -q` to verify all modules import and tests succeed before committing.
3. Configure logging via `config/logging.yaml`; runtime output goes to `hyperhelix.log` and errors to `errors.log`.
4. Avoid leaving `TODO` comments in the code—track outstanding work in documentation or the issue tracker.

## API Usage
With the server running you can create nodes and edges via HTTP:

```bash
curl -X POST http://localhost:8000/nodes -H 'Content-Type: application/json' \
     -d '{"id": "a", "payload": {"foo": "bar"}}'

curl -X POST http://localhost:8000/edges -H 'Content-Type: application/json' \
     -d '{"a": "a", "b": "b"}'

curl http://localhost:8000/walk/a?depth=1
```
```
hyperhelix_system/
├── README.md
├── LICENSE
├── setup.py
├── requirements.txt
├── config/
│   ├── default.yaml             # all tunables (strands, thresholds, DB URIs…)
│   ├── logging.yaml             # Python logging config
│   └── persistence.yaml         # adapters (Neo4j, Qdrant, SQLAlchemy)
├── hyperhelix/                  # core engine
│   ├── __init__.py
│   ├── node.py                  # Node class (+payload, tags, layer, strand, edges, metadata)
│   ├── edge.py                  # Edge helper (bidirectional connect, weight updates)
│   ├── metadata.py              # metadata fields & perception_history logic
│   ├── core.py                  # HyperHelix class (add_node, add_edge, spiral_walk)
│   ├── analytics/               # self-analysis
│   │   ├── __init__.py
│   │   ├── importance.py        # compute_importance(node, all_nodes)
│   │   └── permanence.py        # compute_permanence(node)
│   ├── evolution/               # auto-evolution engines
│   │   ├── __init__.py
│   │   ├── evented_engine.py    # Event-driven (hooks → prune/weave/adjust)
│   │   └── continuous_engine.py # optional interval fallback
│   ├── execution/               # execution & agent hooks
│   │   ├── __init__.py
│   │   ├── executor.py          # Node.execute() wrapper
│   │   └── hook_manager.py      # bind_recursion_to_task, on_insert/update hooks
│   ├── tasks/                   # project & team orchestration
│   │   ├── __init__.py
│   │   ├── task.py              # Task node definitions (due, priority, assigned_to)
│   │   ├── task_manager.py      # create_task(), assign_task()
│   │   └── sprint_planner.py    # sprint_plan()
│   ├── persistence/             # storage adapters
│   │   ├── __init__.py
│   │   ├── base_adapter.py      # interface (save_node, load_node, save_edge…)
│   │   ├── neo4j_adapter.py     # graph DB backing store
│   │   ├── qdrant_adapter.py    # vector DB for embeddings
│   │   └── sqlalchemy_adapter.py# relational fallback
│   ├── api/                     # FastAPI REST & GraphQL
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI()/include routers, CORS, auth
│   │   ├── dependencies.py      # JWT/OAuth2 stubs
│   │   ├── schemas.py           # Pydantic models (NodeIn, NodeOut, EdgeIn…)
│   │   └── routers/
│   │       ├── nodes.py         # POST /nodes, GET /nodes/{id}
│   │       ├── edges.py         # POST /edges
│   │       ├── walk.py          # GET /walk/{start_id}
│   │       └── bloom.py         # POST /autobloom/{node_id}
│   ├── cli/                     # command-line interface
│   │   ├── __init__.py
│   │   └── commands.py          # click-based commands (init, load, dump, serve)
│   ├── visualization/           # 3D layout & rendering helpers
│   │   ├── __init__.py
│   │   ├── coords_generator.py  # helix_coords(node, idx, total, …)
│   │   └── threejs_renderer.py  # JSON export for Three.js front-end
│   └── agents/                  # LLM/chatbot integrations & webhooks
│       ├── __init__.py
│       ├── chat_adapter.py      # ChatMessage → Graph operations
│       └── webhook_listener.py  # HTTP hook into CI/CD, code-commit events
├── frontend/                    # React + Three.js UI
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx              # root component
│       ├── GraphView.jsx        # canvas + renderer
│       └── services/
│           └── hyperhelix_api.js# Axios calls to backend
├── tests/                       # full unit & integration coverage
│   ├── test_node.py
│   ├── test_core.py
│   ├── test_importance.py
│   ├── test_permanence.py
│   ├── test_evented_engine.py
│   ├── test_continuous_engine.py
│   ├── test_executor.py
│   ├── test_tasks.py
│   ├── test_persistence.py
│   ├── test_api.py
│   └── test_cli.py
└── docs/                        # full documentation & tutorials
    ├── architecture.md          # high-level system overview
    ├── modules.md               # deep dive per module
    └── tutorials/
        ├── quick_start.md
        ├── team_orchestration.md
        └── advanced_evolution.md
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
The engine also provides event hooks. `evented_engine.on_insert` is registered automatically and recalculates importance and permanence whenever a node is added. You can register custom callbacks with `register_insert_hook` or `register_update_hook` to persist data or trigger other tasks.

## LLM Integration
Use the helpers in `hyperhelix.agents.llm` to connect to popular language models such as OpenAI. Chat messages can be processed with `handle_chat_message`, which stores the conversation in the graph and records any model replies. Set provider keys like `OPENAI_API_KEY` in the environment so integrations work correctly.

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
