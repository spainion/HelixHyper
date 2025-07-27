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
@click.option("--model", default=None, help="Model identifier to use")
@click.option("--stream", is_flag=True, help="Stream output if supported")
def codex(prompt: str, provider: str, model: str | None, stream: bool) -> None:
    """Return a quick LLM response using the configured provider."""
    from ..agents import llm
    from ..api import main
    from ..agents.context import graph_summary

    provider = provider.lower()
    if provider == "openai":
        from ..utils import get_api_key

        chat = llm.OpenAIChatModel(
            model=model or "gpt-3.5-turbo", api_key=get_api_key("OPENAI_API_KEY")
        )
        messages = [
            {"role": "system", "content": graph_summary(main.app.state.graph)},
            {"role": "user", "content": prompt},
        ]
        response = chat.generate_response(messages)
    elif provider == "openrouter":
        from ..utils import get_api_key

        chat = llm.OpenRouterChatModel(
            model=model or "openai/gpt-4o",
            api_key=get_api_key("OPENROUTER_API_KEY") or "test",
        )
        messages = [
            {"role": "system", "content": graph_summary(main.app.state.graph)},
            {"role": "user", "content": prompt},
        ]
        if stream:
            response = chat.stream_response(messages)
        else:
            response = chat.generate_response(messages)
    elif provider == "huggingface":
        from ..utils import get_api_key

        chat = llm.HuggingFaceChatModel(
            model=model or "HuggingFaceH4/zephyr-7b-beta",
            api_key=get_api_key("HUGGINGFACE_API_TOKEN"),
        )
        messages = [
            {"role": "system", "content": graph_summary(main.app.state.graph)},
            {"role": "user", "content": prompt},
        ]
        response = chat.generate_response(messages)
    else:
        chat = llm.TransformersChatModel(model=model or "sshleifer/tiny-gpt2")
        messages = [
            {"role": "system", "content": graph_summary(main.app.state.graph)},
            {"role": "user", "content": prompt},
        ]
        response = chat.generate_response(messages)

    click.echo(response)


@cli.command()
@click.option(
    "--provider",
    type=click.Choice(["openrouter", "huggingface"], case_sensitive=False),
    default="openrouter",
    show_default=True,
)
@click.option("--query", "-q", default="gpt2", show_default=True, help="Search term for HuggingFace")
@click.option("--limit", "-n", default=5, show_default=True, help="Number of HuggingFace models")
def models(provider: str, query: str, limit: int) -> None:
    """List available model identifiers."""
    from ..agents import llm

    provider = provider.lower()
    try:
        if provider == "openrouter":
            from ..utils import get_api_key

            api_key = get_api_key("OPENROUTER_API_KEY")
            if not api_key:
                click.echo("OPENROUTER_API_KEY not set")
                return
            model_list = llm.list_openrouter_models(api_key=api_key)
        else:
            model_list = llm.list_huggingface_models(search=query, limit=limit)
    except Exception as exc:  # pragma: no cover - network failures
        click.echo(f"Failed to list models: {exc}")
        return

    for mid in model_list:
        click.echo(mid)


@cli.command()
@click.argument("output", default="-")
def export(output: str) -> None:
    """Export the current graph as JSON."""
    from ..api.main import app
    from ..visualization.threejs_renderer import node_to_json
    import json
    from pathlib import Path

    graph = app.state.graph
    data = {
        "nodes": [node_to_json(n) for n in graph.nodes.values()],
        "edges": [
            {"a": a, "b": b, "weight": w}
            for a, node in graph.nodes.items()
            for b, w in node.edges.items()
            if a < b
        ],
    }
    text = json.dumps(data)
    if output == "-":
        click.echo(text)
    else:
        Path(output).write_text(text)
        click.echo(f"Exported to {output}")


@cli.command("import-context")
@click.argument("path", type=click.Path(exists=True))
def import_context(path: str) -> None:
    """Merge a context database at ``PATH`` into the running graph."""
    from pathlib import Path

    from ultimate_zamida_fs_interpreter.memory import persistence
    from .. import importer
    from ..api.main import app

    db_path = Path(path)
    if not db_path.is_file():
        raise click.BadParameter("path must reference a file")

    mem_graph = persistence.load(db_path)
    importer.merge_memory_graph(mem_graph, app.state.graph)
    edge_count = sum(len(t) for m in mem_graph.nodes.values() for t in m.edges.values())
    click.echo(
        f"Imported {len(mem_graph.nodes)} nodes and {edge_count} edges from {db_path}"
    )
