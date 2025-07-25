# Quick Start

1. Install dependencies with `pip install -r requirements.txt`.
2. Run `pytest -q` to confirm the environment is healthy.
3. Launch the API using `uvicorn hyperhelix.api.main:app --reload`.
4. Use the provided HTTP routes to create nodes and edges.
5. Retrieve existing nodes with `curl http://localhost:8000/nodes`.
6. List created edges with `curl http://localhost:8000/edges`.
7. Get edges for a node with `curl http://localhost:8000/edges/<id>`.
8. Delete an edge with `curl -X DELETE http://localhost:8000/edges/<a>/<b>` and expect `{"status": "deleted"}` in the response.
9. Delete a node with `curl -X DELETE http://localhost:8000/nodes/<id>` and expect `{"status": "deleted"}` in the response.
10. Get a quick graph summary with `curl http://localhost:8000/summary`.
11. Execute a node with `curl -X POST http://localhost:8000/nodes/<id>/execute` and receive the updated node back.
12. Request code suggestions with `curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"openai"}'` (includes a graph summary automatically).
13. Use OpenRouter with `curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"openrouter"}'`.
14. List OpenRouter models with `curl http://localhost:8000/models/openrouter`.
15. Use HuggingFace with `curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"huggingface"}'`.
16. Use a local model with `curl -X POST http://localhost:8000/suggest -d '{"prompt":"Hello","provider":"local"}'`.
17. List HuggingFace models with `curl http://localhost:8000/models/huggingface?q=gpt2`.
18. List GitHub issues with `python -m hyperhelix.cli.commands issues owner/repo`.
19. Get an LLM reply using `python -m hyperhelix.cli.commands codex "Hello"`.
20. Stream a response with `python -m hyperhelix.cli.commands codex "Hi" --stream --model openai/gpt-4o`.
