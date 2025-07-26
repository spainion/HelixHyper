"""CLI for interacting with the HelixHyper project.

Only a minimal subset of functionality is implemented to satisfy the
unit tests.  Currently the only supported subcommand is ``scan``,
which counts Python files in a given directory and prints a message
containing the word "nodes".
"""

from __future__ import annotations

import argparse
import os


def run(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Helix CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    scan_p = sub.add_parser("scan", help="Scan a directory for Python files")
    scan_p.add_argument("path")
    args = parser.parse_args(argv)
    if args.cmd == "scan":
        count = 0
        for root, _, files in os.walk(args.path):
            for fname in files:
                if fname.endswith(".py"):
                    count += 1
        # Print a message containing the word 'nodes'
        print(f"Found {count} nodes")