# Build and Deployment Instructions

Follow these steps to work with the full HelixHyper system:

1. Clone the repository and install dependencies with `pip install -r requirements.txt` before starting any service or container.
2. Adjust configuration in `config/` as needed, particularly `logging.yaml` for log levels and file locations.
   Logs are written to `hyperhelix.log` with errors duplicated in `errors.log`.
3. Run `pytest -q` to ensure the codebase imports and tests pass.
   Set `USE_REAL_LLM=1` to disable test patches or use `scripts/test_with_llm.sh`.
4. Use the CLI or API components to interact with the graph. The API exposes endpoints for creating nodes and edges, listing nodes and edges (globally or per node), deleting nodes and edges, executing nodes, walking the graph, and listing available OpenRouter models. HuggingFace completions are also supported via the `/suggest` endpoint. A `/autosuggest` endpoint can generate follow-up tasks for a node using an LLM.
   Additional CLI helpers let you fetch GitHub issues (`issues`) and send quick LLM prompts (`codex`). Graph-aware agents can be created with the OpenAI Agents SDK in `hyperhelix.agents.openai_agent`. Agents can list nodes, create new ones and connect them via chat commands. The helper `enable_auto_suggest` binds automatic suggestions in code.
5. Build the included `Dockerfile` to run everything in a container if desired.

Supply a persistence adapter when constructing `HyperHelix` if you need to
store nodes and edges across sessions.

Keep documentation up to date as new modules are added.

Configuration files include:
- `default.yaml` for runtime settings like strand counts.
- `persistence.yaml` for database connection details.
Update these along with `logging.yaml` when deploying to new environments.
For LLM integration set provider API keys (e.g. `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `HUGGINGFACE_API_TOKEN`) in the environment before running the application. Local models require the `transformers` package.
Each package directory may also contain an `AGENTS.md` with specialized instructions.
