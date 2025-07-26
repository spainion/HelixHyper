"""Clone and run the HelixHyper FastAPI server."""

from __future__ import annotations

import argparse
import importlib

from scripts.helix_utils import clone_repo


def run(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Run HelixHyper server")
    parser.add_argument("--repo-url", default="https://github.com/spainion/HelixHyper.git")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args(argv)
    # Clone the repo (cached) and ignore the path; tests monkeypatch clone_repo
    clone_repo(args.repo_url, branch=args.branch)
    # Import the FastAPI app from the expected module path
    module = importlib.import_module("hyperhelix.api.main")
    app = getattr(module, "app")
    # Run via uvicorn; tests monkeypatch uvicorn.run
    import uvicorn  # imported here to allow monkeypatching
    uvicorn.run(app, host=args.host, port=args.port)