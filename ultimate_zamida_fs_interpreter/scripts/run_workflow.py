"""Execute a YAML‑defined workflow of agent actions.

This script reads one or more workflow configuration files and
executes a sequence of agent invocations.  Each configuration file
should be YAML with a top‑level ``steps`` list; each step is a
mapping containing at least an ``agent`` name and a list of ``args``.

Agents are resolved by name from the available modules in the
``agents`` package.  The special name ``code_suggestion`` maps to
``CodeAgent`` which executes Python code and returns its standard
output.  Additional agents can be added here as needed.

Upon completion of all steps the context graph is saved to the
location specified by the ``GRAPH_PATH`` environment variable via
``ContextDB.save_graph``.  If no graph path is configured the graph is
still updated in memory but not persisted.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Any

import yaml  # type: ignore

from agents.code_agent import CodeAgent
from memory.context_db import ContextDB


def _load_workflow(path: str) -> List[dict[str, Any]]:
    """Load a YAML workflow file and return its list of steps."""
    data = yaml.safe_load(Path(path).read_text())
    if not isinstance(data, dict) or "steps" not in data:
        raise ValueError(f"Invalid workflow file: {path}")
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        raise ValueError(f"Invalid steps in workflow file: {path}")
    return steps  # type: ignore[return-value]


def run(argv: List[str] | None = None) -> None:
    """Execute one or more workflow files specified on the command line.

    Parameters
    ----------
    argv: list[str] | None
        A list of command‑line arguments.  If ``None``, the function
        expects ``sys.argv[1:]``.  Each argument should be a path to a
        YAML workflow file.

    This function loads each workflow file, iterates over the defined
    steps and invokes the corresponding agent.  Currently only the
    ``code_suggestion`` agent is supported, which will execute Python
    code and ignore its return value.  After all steps are executed
    the context graph is saved if a graph path is configured.
    """
    import sys

    args = list(argv) if argv is not None else sys.argv[1:]
    if not args:
        raise ValueError("No workflow files specified")
    # Use existing graph if present, otherwise create a new one
    db = ContextDB()
    for wf_path in args:
        steps = _load_workflow(wf_path)
        for step in steps:
            agent_name = step.get("agent")
            agent_args = step.get("args", [])
            if agent_name == "code_suggestion":
                # Execute Python code using CodeAgent
                agent = CodeAgent()
                # Flatten args to single string for code execution if list provided
                code = agent_args[0] if agent_args else ""
                try:
                    agent.act(code)
                except Exception:
                    # Ignore exceptions to allow workflows to continue
                    pass
            else:
                # Unknown agent names are ignored for simplicity
                continue
    # Persist the graph if a path is configured
    if db.graph_path:
        db.save_graph()


if __name__ == "__main__":  # pragma: no cover - manual use
    run()
