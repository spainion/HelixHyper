# Quick Start

1. Install dependencies with `pip install -r requirements.txt`.
2. Run `pytest -q` to confirm the environment is healthy.
3. Launch the API using `uvicorn hyperhelix.api.main:app --reload`.
4. Use the provided HTTP routes to create nodes and edges.
5. Retrieve existing nodes with `curl http://localhost:8000/nodes`.
6. List created edges with `curl http://localhost:8000/edges`.
7. Get a quick graph summary with `curl http://localhost:8000/summary`.
8. Execute a node with `curl -X POST http://localhost:8000/nodes/<id>/execute` and receive the updated node back.
9. Manage tasks:
   - `curl -X POST http://localhost:8000/tasks -d '{"id":"t1","description":"demo"}'`
   - `curl -X POST http://localhost:8000/tasks/t1/assign -d 'user=alice'`
   - `curl http://localhost:8000/tasks/t1`
   - `curl http://localhost:8000/tasks`
   - `curl http://localhost:8000/tasks/plan`
10. Request code suggestions with `curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"openai"}'` (includes a graph summary automatically).
11. Use OpenRouter with `curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"openrouter"}'`.
12. List OpenRouter models with `curl http://localhost:8000/models/openrouter`.
13. These routes return a `503` error unless `OPENAI_API_KEY` or `OPENROUTER_API_KEY` is set in the environment.
14. Provider failures result in a `502` status code.
