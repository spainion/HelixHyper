# API Routers Guidelines

- Keep endpoints minimal and focused on graph operations.
- Use `Depends(get_graph)` to access the shared graph.
- Return Pydantic models for consistency across routes.
- Add tests in `tests/` when introducing new endpoints.
