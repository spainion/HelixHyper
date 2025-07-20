from __future__ import annotations

import click


@click.group()
def cli() -> None:
    """Command-line interface entry point."""


@cli.command()
def serve() -> None:
    click.echo("Serving API")
