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

You can index a directory into the running graph with:

```bash
python -m hyperhelix.cli.commands scan .
```

The scanner parses ``import`` statements and links files in the graph,
creating edges for modules that depend on one another.

List open GitHub issues with:

```bash
python -m hyperhelix.cli.commands issues owner/repo
```

Quickly get an LLM response using:

```bash
python -m hyperhelix.cli.commands codex "Hello" --provider openrouter
python -m hyperhelix.cli.commands codex "Hello" --provider local
python -m hyperhelix.cli.commands codex "Hi" --provider openrouter --model openai/gpt-4o --stream
# the codex command also sends a graph summary as context
python -m hyperhelix.cli.commands models --provider openrouter
python -m hyperhelix.cli.commands models --provider huggingface --query gpt2
python -m hyperhelix.cli.commands export graph.json
```

Create a graph-aware OpenAI agent using the Agents SDK:

```python
from hyperhelix.core import HyperHelix
from hyperhelix.agents.openai_agent import (
    create_graph_agent,
    run_graph_agent,
    run_graph_agent_async,
    create_session,
)

g = HyperHelix()
agent = create_graph_agent(g)
session = create_session()
response = run_graph_agent(agent, "Summarize the graph", session=session)
print(response)

# Or run asynchronously
import asyncio
asyncio.run(run_graph_agent_async(agent, "Summarize the graph", session=session))

# Agents can also modify the graph:
run_graph_agent(agent, "add_node id=test payload='demo'")
run_graph_agent(agent, "connect_nodes a=test b=other", session=session)
# have the agent generate follow-up tasks
run_graph_agent(agent, "autosuggest node_id=test", session=session)
```
Commands read provider keys such as `OPENAI_API_KEY`, `OPENROUTER_API_KEY` and
`HUGGINGFACE_API_TOKEN` from the environment using
`hyperhelix.utils.get_api_key()`.

The `HyperHelix` graph accepts a persistence adapter for automatically storing
nodes and edges. Instantiate it with an adapter such as `Neo4jAdapter` to
persist connections as they are created.

Alternatively build and run the provided Dockerfile:

```bash
docker build -t helixhyper .
docker run -p 8000:8000 helixhyper
```

Or use Docker Compose:

```bash
docker-compose up api
```

For development with full tooling (pytest, git, editors), use the development container:

```bash
docker build -f Dockerfile.dev -t helixhyper-dev .
docker run -it -p 8000:8000 -v $(pwd):/app helixhyper-dev

# Or with Docker Compose
docker-compose up dev
```

See `docs/docker.md` for detailed Docker documentation and `docs/dev-container-quickref.md` for a quick reference guide.

## Development Workflow
Follow these practices when contributing to ensure consistent builds and clear logs:

1. Install dependencies with `pip install -r requirements.txt` and set any required keys such as `OPENAI_API_KEY` or `OPENROUTER_API_KEY` in your environment.
2. Run `pytest -q` to verify all modules import and tests succeed before committing.
   Use `scripts/test_with_llm.sh` to run tests against live LLMs by setting `USE_REAL_LLM=1` automatically.
   Integration tests that call OpenAI or OpenRouter are automatically skipped if
   the corresponding `OPENAI_API_KEY` or `OPENROUTER_API_KEY` variables are not
   present.
3. Configure logging via `config/logging.yaml`; runtime output goes to `hyperhelix.log` and errors to `errors.log`.
4. Avoid leaving `TODO` comments in the code—track outstanding work in documentation or the issue tracker.

## API Usage
With the server running you can create nodes and edges via HTTP:

```bash
curl -X POST http://localhost:8000/nodes -H 'Content-Type: application/json' \
     -d '{"id": "a", "payload": {"foo": "bar"}}'

curl -X POST http://localhost:8000/edges -H 'Content-Type: application/json' \
     -d '{"a": "a", "b": "b"}'

curl http://localhost:8000/nodes

curl http://localhost:8000/edges

curl http://localhost:8000/edges/a
# [{"a": "a", "b": "b", "weight": 1.0}]

# delete an edge
curl -X DELETE http://localhost:8000/edges/a/b
# {"status": "deleted"}
# deleting a missing edge returns 404

# delete a node
curl -X DELETE http://localhost:8000/nodes/a
# {"status": "deleted"}
All edges referencing the node will be dropped.

curl http://localhost:8000/walk/a?depth=1

# get a graph summary
curl http://localhost:8000/summary

# execute nodes
curl -X POST http://localhost:8000/nodes/a/execute
# returns updated node data

# index project source
curl -X POST http://localhost:8000/scan -d 'path=.'

# manage tasks
curl -X POST http://localhost:8000/tasks -H 'Content-Type: application/json' \
     -d '{"id":"t1","description":"demo"}'
curl -X POST http://localhost:8000/tasks/t1/assign -d 'user=alice'
curl http://localhost:8000/tasks
curl http://localhost:8000/tasks/plan

# get code suggestions (the server automatically sends a graph summary)
curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"openai"}'
# use OpenRouter
curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"openrouter"}'
curl http://localhost:8000/models/openrouter
# use HuggingFace
curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"huggingface"}'
# use a local Transformers model
curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"local"}'
curl http://localhost:8000/models/huggingface?q=gpt2
curl -X POST http://localhost:8000/chat -d '{"prompt":"Hello"}'
# includes a graph summary automatically
# have the server generate follow-up tasks for a node
curl -X POST http://localhost:8000/autosuggest -d '{"node_id":"my-node"}'
# or do the same in code
python - <<'PY'
from hyperhelix.core import HyperHelix
from hyperhelix.execution import enable_auto_suggest
from hyperhelix.node import Node

g = HyperHelix()
enable_auto_suggest(g)
g.add_node(Node(id="x", payload="print('hi')"))
PY
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
│   ├── core.py                  # HyperHelix class (add_node, add_edge, spiral_walk, shortest_path)
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
│   │       ├── nodes.py         # POST /nodes, GET /nodes/{id}, GET /nodes, DELETE /nodes/{id}, POST /nodes/{id}/execute
│   │       ├── edges.py         # POST /edges, DELETE /edges/{a}/{b}, GET /edges, GET /edges/{id}
│   │       ├── walk.py          # GET /walk/{start_id}
│   │       ├── bloom.py         # POST /autobloom/{node_id}
│   │       ├── scan.py          # POST /scan
│   │       ├── tasks.py         # POST /tasks
│   │       ├── suggest.py       # POST /suggest
│   │       ├── models.py        # GET /models/openrouter
│   │       ├── summary.py       # GET /summary
│   │       ├── export.py        # GET /export
│   │       └── chat.py          # POST /chat
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
├── ultimate_zamida_fs_interpreter/        # lightweight graph & CLI helpers
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
- **hyperhelix/core.py** provides the `HyperHelix` graph with thread-safe `add_node`, `add_edge`, `spiral_walk` and `shortest_path` operations.
- **HyperHelix** can be initialized with a persistence adapter so new nodes and
  connections are saved automatically.
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
Use the helpers in `hyperhelix.agents.llm` to connect to popular language models such as OpenAI. Chat messages can be processed with `handle_chat_message`, which stores the conversation in the graph and records any model replies. Set provider keys like `OPENAI_API_KEY`, `OPENROUTER_API_KEY` and `HUGGINGFACE_API_TOKEN` in the environment so integrations work correctly. When `OPENAI_API_KEY` isn’t present a fallback value of ``"test"`` is used so development can proceed without a real key. The convenience function `hyperhelix.utils.get_api_key("OPENROUTER_API_KEY")` retrieves keys with a warning if they are missing.

### Calling OpenAI directly

```
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What’s in this image?","image":"data:image/png;base64,....."}],"temperature":0.7,"stream":true}'
```

### Streaming with OpenRouter

```python
import json
import requests

question = "How would you build the tallest building ever?"
headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
payload = {"model": "openai/gpt-4o", "messages": [{"role": "user", "content": question}], "stream": True}
buffer = ""
with requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, stream=True) as r:
    for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
        buffer += chunk
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
    print(json.loads(data)["choices"][0]["delta"].get("content", ""), end="")
```

`OpenRouterChatModel` also provides a `stream_response()` method that returns the
complete text from a streamed response.

Use `list_openrouter_models()` to retrieve available models from the service:

```python
from hyperhelix.agents.llm import list_openrouter_models
models = list_openrouter_models()
print(models)
```
The helper reads `OPENROUTER_API_KEY` from the environment when available.
Alternatively, call `GET /models/openrouter` to fetch the list via the API:

```bash
curl http://localhost:8000/models/openrouter
```

### Using the HuggingFace Inference API

```python
from hyperhelix.agents.llm import HuggingFaceChatModel
model = HuggingFaceChatModel()
resp = model.generate_response([{'role': 'user', 'content': 'Hello'}])
print(resp)
```
The model reads `HUGGINGFACE_API_TOKEN` from the environment when present.

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
- Self-heals by pruning broken edges and weaving new nodes by shared tags
- Records execution results in each node's perception history
- Quickly queries context with `find_nodes_by_tag` and integrates responses from popular LLMs

This is the full system—every file, class and function—powering a zero-bloat, infinitely weaving digital brain.
