# Module Guide

- **config/** – configuration files for runtime tuning, logging and persistence.
- **hyperhelix/** – core engine and subpackages for analytics, evolution, execution and more.
- **hyperhelix/api/** – FastAPI server exposing REST routes.
- **hyperhelix/cli/** – command-line interface helpers.
- **hyperhelix/core.py** – graph container with `add_node`, `add_edge`, `remove_node`, `spiral_walk` and `shortest_path`.
- **persistence adapters** – implement `save_node`, `load_node`, `save_edge` and
  `load_edges` for automatic storage when supplied to `HyperHelix`.
- **hyperhelix/evolution/** – event-driven and periodic engines that update node metrics.
- **hyperhelix/agents/code_scanner.py** – scans directories, stores Python source and links files via imports.
- **hyperhelix/agents/llm.py** – wrappers for OpenAI, OpenRouter and HuggingFace chat models.
- **hyperhelix/agents/context.py** – build system prompts from the graph.
- **hyperhelix/api/routers/scan.py** – endpoint to index directories via `/scan`.
- **hyperhelix/api/routers/nodes.py** – create, retrieve, list, delete and execute nodes.
- **hyperhelix/api/routers/edges.py** – create, delete and list edges (global or by node).
- **hyperhelix/api/routers/models.py** – list available OpenRouter models.
- **hyperhelix/api/routers/summary.py** – return a graph summary via `/summary`.
- **hyperhelix/api/routers/tasks.py** – CRUD operations for tasks.
- **hyperhelix/api/routers/suggest.py** – get LLM-based code suggestions.
- **hyperhelix/agents/llm.list_openrouter_models** – fetch available models.
- **frontend/** – example React + Three.js client.
- **tests/** – unit tests covering the system.

Start the API from the command line with `python -m hyperhelix.cli.commands serve`.
Use `python -m hyperhelix.cli.commands scan .` to index a directory.
