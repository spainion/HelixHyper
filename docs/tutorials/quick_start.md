# Quick Start

1. Install dependencies with `pip install -r requirements.txt`.
2. Run `pytest -q` to confirm the environment is healthy.
3. Launch the API using `uvicorn hyperhelix.api.main:app --reload`.
4. Use the provided HTTP routes to create nodes and edges.
5. Retrieve existing nodes with `curl http://localhost:8000/nodes`.
