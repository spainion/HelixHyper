# Module Guide

- **config/** – configuration files for runtime tuning, logging and persistence.
- **hyperhelix/** – core engine and subpackages for analytics, evolution, execution and more.
- **hyperhelix/api/** – FastAPI server exposing REST routes.
- **hyperhelix/cli/** – command-line interface helpers.
- **hyperhelix/evolution/** – event-driven and periodic engines that update node metrics.
- **hyperhelix/agents/code_scanner.py** – scans directories and stores Python source in the graph.
- **hyperhelix/agents/llm.py** – wrappers for OpenAI and OpenRouter chat models.
- **frontend/** – example React + Three.js client.
- **tests/** – unit tests covering the system.

Start the API from the command line with `python -m hyperhelix.cli.commands serve`.
