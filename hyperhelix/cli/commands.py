from __future__ import annotations

import click


@click.group()
def cli() -> None:
    """Command-line interface entry point."""


@cli.command()
def serve() -> None:
    """Run the HTTP API using Uvicorn."""
    import uvicorn

    uvicorn.run("hyperhelix.api.main:app", host="0.0.0.0", port=8000)


@cli.command()
@click.argument("path", default=".")
def scan(path: str) -> None:
    """Scan a directory and store Python files in the running graph."""
    from ..api.main import app
    from ..agents.code_scanner import scan_repository

    graph = app.state.graph
    scan_repository(graph, path)
    click.echo(f"{len(graph.nodes)} nodes")
