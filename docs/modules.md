# Module Guide

- **config/** – configuration files for runtime tuning, logging and persistence.
- **hyperhelix/** – core engine and subpackages for analytics, evolution, execution and more.
- **hyperhelix/api/** – FastAPI server exposing REST routes.
- **hyperhelix/cli/** – command-line interface helpers.
- **hyperhelix/core.py** – graph container with `add_node`, `add_edge`, `remove_edge`, `remove_node`, `spiral_walk` and `shortest_path`.
- **persistence adapters** – implement `save_node`, `load_node`, `save_edge` and
  `load_edges` for automatic storage when supplied to `HyperHelix`.
- **hyperhelix/evolution/** – event-driven and periodic engines that update node metrics.
- **hyperhelix/agents/code_scanner.py** – scans directories, stores Python source and links files via imports.
 - **hyperhelix/agents/llm.py** – wrappers for OpenAI, OpenRouter, HuggingFace and local Transformers chat models.
- **hyperhelix/agents/context.py** – build system prompts from the graph.
- **hyperhelix/api/routers/scan.py** – endpoint to index directories via `/scan`.
- **hyperhelix/api/routers/nodes.py** – create, retrieve, list, delete and execute nodes.
- **hyperhelix/api/routers/edges.py** – create, delete and list edges (global or by node).
- **hyperhelix/api/routers/models.py** – list available OpenRouter or HuggingFace models.
- **hyperhelix/api/routers/summary.py** – return a graph summary via `/summary`.
- **hyperhelix/api/routers/export.py** – dump the entire graph with `/export`.
- **hyperhelix/api/routers/chat.py** – return LLM completions with a graph summary via `/chat`.
- **hyperhelix/api/routers/tasks.py** – CRUD operations for tasks.
- **hyperhelix/api/routers/suggest.py** – get LLM-based code suggestions.
- **hyperhelix/api/routers/autosuggest.py** – generate tasks for a node via `/autosuggest`.
- **hyperhelix/execution/suggestion.py** – create tasks from LLM analysis when nodes are inserted. Supports OpenAI, OpenRouter, HuggingFace and local models.
- `enable_auto_suggest(graph)` binds automatic suggestions to node insertion.
- **hyperhelix/agents/llm.list_openrouter_models** – fetch OpenRouter models.
- **hyperhelix/agents/llm.list_huggingface_models** – fetch HuggingFace models.
- **hyperhelix/agents/openai_agent.py** – build graph-aware agents using the
  OpenAI Agents SDK.
- **frontend/** – example React + Three.js client.
- **tests/** – unit tests covering the system.

Start the API from the command line with `python -m hyperhelix.cli.commands serve`.
Use `python -m hyperhelix.cli.commands scan .` to index a directory.
List GitHub issues with `python -m hyperhelix.cli.commands issues owner/repo`.
Get an LLM reply using `python -m hyperhelix.cli.commands codex "Hi"`.
Specify a model and stream output with `python -m hyperhelix.cli.commands codex "Hi" --model openai/gpt-4o --stream`.
The `codex` command automatically includes a graph summary in the prompt.
List models with `python -m hyperhelix.cli.commands models --provider openrouter`.
Commands read API keys such as `OPENAI_API_KEY`, `OPENROUTER_API_KEY` and `HUGGINGFACE_API_TOKEN` from the environment. Use `hyperhelix.utils.get_api_key()` when accessing keys in your own scripts.
Export the current graph with `python -m hyperhelix.cli.commands export graph.json`.
