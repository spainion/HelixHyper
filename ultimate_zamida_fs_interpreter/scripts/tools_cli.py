"""Utility command line interface mapping subcommands to scripts.

This CLI wraps a variety of maintenance scripts exposed in the
``scripts`` package.  Only a subset of the original functionality
required by the unit tests is implemented.  Unknown commands result
in a parser error.
"""

from __future__ import annotations

import argparse
import sys

from pathlib import Path

import scripts.setup_env as setup_env
import scripts.list_missing as list_missing
import scripts.export_graph as export_graph
import scripts.export_graph_json as export_json
import scripts.context_cli as context_cli
import scripts.diagnostics as diagnostics
import scripts.github_commit_report as commit_report
import scripts.github_docs_scraper as docs_scraper
import scripts.update_todo_list as todo_list
import scripts.helix_server as helix_server


def run(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Utility CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    # setup-env
    env_p = sub.add_parser("setup-env", help="Write .env from YAML")
    env_p.add_argument("--env", default=".env")
    env_p.add_argument("--config", default="config/api_keys.yaml")
    # missing
    miss_p = sub.add_parser("missing", help="Search for todo markers")
    miss_p.add_argument("--root", default=None)
    miss_p.add_argument("--pattern", default="TO" "DO")
    miss_p.add_argument("--ext", default=".py")
    miss_p.add_argument("--count", action="store_true")
    # export
    exp_p = sub.add_parser("export", help="Export graph to DOT")
    exp_p.add_argument("--input", default=None)
    exp_p.add_argument("--output", default="graph.dot")
    # export-json
    json_p = sub.add_parser("export-json", help="Export graph to JSON with coords")
    json_p.add_argument("--input", default=None)
    json_p.add_argument("--output", default="graph_3d.json")
    # check (delegated to context_cli)
    check_p = sub.add_parser("check", help="Verify API connections")
    check_p.add_argument("--env", default=".env")
    check_p.add_argument("--config", default="config/api_keys.yaml")
    # commits
    commits_p = sub.add_parser("commits", help="List recent commits")
    commits_p.add_argument("--limit", type=int, default=10)
    commits_p.add_argument("--output", default=None)
    # diagnostics
    sub.add_parser("diagnostics", help="Run diagnostic checks")
    # scrape-docs
    scrape_p = sub.add_parser("scrape-docs", help="Scrape GitHub documentation")
    scrape_p.add_argument("urls", nargs="+")
    scrape_p.add_argument("--concurrency", type=int, default=2)
    scrape_p.add_argument("--output-dir", default=None)
    # todo-list
    todo_p = sub.add_parser("todo-list", help="Write todo locations to file")
    todo_p.add_argument("--output", default="todo_list.txt")
    todo_p.add_argument("--root", default=None)
    todo_p.add_argument("--pattern", default="TO" "DO")
    # helix-server
    helix_p = sub.add_parser("helix-server", help="Clone and run HelixHyper")
    helix_p.add_argument("--repo-url", default="https://github.com/spainion/HelixHyper.git")
    helix_p.add_argument("--branch", default="main")
    helix_p.add_argument("--host", default="0.0.0.0")
    helix_p.add_argument("--port", type=int, default=8001)
    # helix-cli
    helix_cli_p = sub.add_parser("helix-cli", help="Run HelixHyper CLI command")
    helix_cli_p.add_argument("--repo-url", default="https://github.com/spainion/HelixHyper.git")
    helix_cli_p.add_argument("--branch", default="main")
    helix_cli_p.add_argument("cli_args", nargs=argparse.REMAINDER)
    # Parse arguments
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    # Dispatch
    if args.cmd == "setup-env":
        setup_env.run(args.env, args.config)
        return
    if args.cmd == "missing":
        opts: list[str] = []
        if args.root:
            opts += ["--root", args.root]
        if args.pattern != "TO" "DO":
            opts += ["--pattern", args.pattern]
        if args.ext != ".py":
            opts += ["--ext", args.ext]
        if args.count:
            opts += ["--count"]
        list_missing.run(opts)
        return
    if args.cmd == "export":
        opts: list[str] = []
        if args.input:
            opts += ["--input", args.input]
        if args.output:
            opts += ["--output", args.output]
        export_graph.run(opts)
        return
    if args.cmd == "export-json":
        opts: list[str] = []
        if args.input:
            opts += ["--input", args.input]
        if args.output:
            opts += ["--output", args.output]
        export_json.run(opts)
        return
    if args.cmd == "check":
        # Delegate to context_cli
        context_cli.run(["check", "--env", args.env, "--config", args.config])
        return
    if args.cmd == "commits":
        opts = ["--limit", str(args.limit)]
        if args.output:
            opts += ["--output", args.output]
        commit_report.run(opts)
        return
    if args.cmd == "diagnostics":
        diagnostics.run()
        return
    if args.cmd == "scrape-docs":
        opts: list[str] = []
        if args.concurrency != 2:
            opts += ["--concurrency", str(args.concurrency)]
        if args.output_dir:
            opts += ["--output-dir", args.output_dir]
        docs_scraper.run(opts + args.urls)
        return
    if args.cmd == "todo-list":
        opts = ["--output", args.output]
        if args.root:
            opts += ["--root", args.root]
        if args.pattern != "TO" "DO":
            opts += ["--pattern", args.pattern]
        todo_list.run(opts)
        return
    if args.cmd == "helix-server":
        opts = [
            "--repo-url",
            args.repo_url,
            "--branch",
            args.branch,
            "--host",
            args.host,
            "--port",
            str(args.port),
        ]
        helix_server.run(opts)
        return
    if args.cmd == "helix-cli":
        # Run helix CLI by importing the module dynamically.
        # Only pass through the CLI arguments; do not include repo/branch
        import scripts.helix_cli as helix_cli
        helix_cli.run(list(args.cli_args))
        return
    parser.error("unknown command")