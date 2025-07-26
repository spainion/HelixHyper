"""Command line interface for managing context database files.

Supported commands:

``init``
    Initialise a new context by creating graph, registry and log files.

``register``
    Register all agents discovered in the ``agents`` directory into
    the specified registry.

``status``
    Print a summary of the number of nodes, agents and log entries.

``check``
    Delegate to another module's ``run`` function; used by tools_cli.
"""

from __future__ import annotations

import argparse
from typing import List

from controller.agent_factory import discover_agents
from memory.context_db import ContextDB
from memory.agent_registry import AgentRegistry


def run(argv: List[str]) -> None:
    parser = argparse.ArgumentParser(description="Context DB CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    # init
    init_p = sub.add_parser("init", help="Initialise context files")
    init_p.add_argument("--graph", required=True)
    init_p.add_argument("--registry", required=True)
    init_p.add_argument("--log", required=True)
    init_p.add_argument("--lock", required=False)
    # register
    reg_p = sub.add_parser("register", help="Register available agents")
    reg_p.add_argument("--registry", required=True)
    # status
    status_p = sub.add_parser("status", help="Print summary")
    status_p.add_argument("--graph", required=True)
    status_p.add_argument("--registry", required=True)
    status_p.add_argument("--log", required=True)
    # check (delegated)
    check_p = sub.add_parser("check", help="Proxy to check script")
    check_p.add_argument("--env")
    check_p.add_argument("--config")
    args = parser.parse_args(argv)

    if args.cmd == "init":
        # Initialise context database and persist graph immediately
        db = ContextDB(graph_path=args.graph, log_path=args.log, registry_path=args.registry)
        db.save_graph()
        # Ensure registry and log files exist (ContextDB initialises them)
        return
    if args.cmd == "register":
        # register all agents in the agents directory
        reg = AgentRegistry(args.registry)
        agents = discover_agents("agents")
        for name in agents.keys():
            reg.register(name)
        return
    if args.cmd == "status":
        db = ContextDB(graph_path=args.graph, log_path=args.log, registry_path=args.registry)
        print(f"Nodes: {len(db.graph.nodes)}")
        if db.registry:
            agents = db.registry.list_agents()
            print(f"Agents: {len(agents)}")
        if db.change_log:
            entries = list(db.change_log.entries())
            if entries:
                print(f"Last log: {entries[-1]['entry']}")
        return
    if args.cmd == "check":
        # Look for a `check` attribute on this module; tests will monkeypatch it
        check_mod = globals().get("check")
        if check_mod is None:
            raise RuntimeError("check module not available")
        opts: list[str] = []
        if args.env:
            opts += ["--env", args.env]
        if args.config:
            opts += ["--config", args.config]
        # Expect the check module to provide a run() function
        check_mod.run(opts)  # type: ignore[misc]