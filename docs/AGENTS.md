# Build and Deployment Instructions

Follow these steps to work with the full HelixHyper system:

1. Clone the repository and install dependencies with `pip install -r requirements.txt` before starting any service or container.
2. Adjust configuration in `config/` as needed, particularly `logging.yaml` for log levels and file locations.
   Logs are written to `hyperhelix.log` with errors duplicated in `errors.log`.
3. Run `pytest -q` to ensure the codebase imports and tests pass.
4. Use the CLI or API components to interact with the graph. The API exposes endpoints for creating nodes and edges and walking the graph.
5. Build the included `Dockerfile` to run everything in a container if desired.

Keep documentation up to date as new modules are added.

Configuration files include:
- `default.yaml` for runtime settings like strand counts.
- `persistence.yaml` for database connection details.
Update these along with `logging.yaml` when deploying to new environments.
For LLM integration set provider API keys (e.g. `OPENAI_API_KEY`) in the environment before running the application.
Each package directory may also contain an `AGENTS.md` with specialized instructions.
