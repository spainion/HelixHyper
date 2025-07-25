from __future__ import annotations

import os
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


@cli.command()
@click.argument("repo")
def issues(repo: str) -> None:
    """List open issues for a GitHub repository."""
    import httpx

    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"https://api.github.com/repos/{repo}/issues"
    resp = httpx.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    for issue in resp.json():
        click.echo(f"#{issue['number']}: {issue['title']}")


@cli.command()
@click.argument("prompt")
@click.option(
    "--provider",
    type=click.Choice(["openai", "openrouter", "huggingface", "local"], case_sensitive=False),
    default="openrouter",
    show_default=True,
)
def codex(prompt: str, provider: str) -> None:
    """Return a quick LLM response using the configured provider."""
    from ..agents import llm

    provider = provider.lower()
    if provider == "openai":
        model = llm.OpenAIChatModel(api_key=os.getenv("OPENAI_API_KEY"))
    elif provider == "openrouter":
        model = llm.OpenRouterChatModel(api_key=os.getenv("OPENROUTER_API_KEY"))
    elif provider == "huggingface":
        model = llm.HuggingFaceChatModel(api_key=os.getenv("HUGGINGFACE_API_TOKEN"))
    else:
        model = llm.TransformersChatModel()

    response = model.generate_response([{"role": "user", "content": prompt}])
    click.echo(response)
