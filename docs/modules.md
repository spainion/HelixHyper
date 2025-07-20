# Module Guide

- **config/** – configuration files for runtime tuning, logging and persistence.
- **hyperhelix/** – core engine and subpackages for analytics, evolution, execution and more.
- **hyperhelix/api/** – FastAPI server exposing REST routes.
- **hyperhelix/cli/** – command-line interface helpers.
- **hyperhelix/core.py** – graph container with `add_node`, `add_edge`, `spiral_walk` and `shortest_path`.
- **persistence adapters** – implement `save_node`, `load_node`, `save_edge` and
  `load_edges` for automatic storage when supplied to `HyperHelix`.
- **hyperhelix/evolution/** – event-driven and periodic engines that update node metrics.
- **hyperhelix/agents/code_scanner.py** – scans directories and stores Python source in the graph.
- **hyperhelix/agents/llm.py** – wrappers for OpenAI and OpenRouter chat models.
- **hyperhelix/api/routers/scan.py** – endpoint to index directories via `/scan`.
- **frontend/** – example React + Three.js client.
- **tests/** – unit tests covering the system.

Start the API from the command line with `python -m hyperhelix.cli.commands serve`.
Use `python -m hyperhelix.cli.commands scan .` to index a directory.
