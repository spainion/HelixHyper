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
