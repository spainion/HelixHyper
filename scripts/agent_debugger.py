#!/usr/bin/env python3
"""
Agent Debugger - run linters, type checks, tests and emit structured logs.

Usage:
  python scripts/agent_debugger.py --branch agent/debug-2025-08-24 --outdir logs

Behavior:
- Runs commands in the repo root.
- Captures stdout/stderr to logs/<timestamp>.json and a human-readable log.
- Exits non-zero if tests or critical checks fail.
"""
import argparse
import json
import os
import subprocess
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "logs"

CHECK_COMMANDS = [
    ("ruff", ["ruff", "."], False),         # change to ruff/flake8 as available
    ("mypy", ["mypy", "."], False),
    ("bandit", ["bandit", "-r", "."], False),
    ("pytest", ["pytest", "-q", "--maxfail=1"], True),
    # Add more commands as needed
]

def run_cmd(cmd, cwd=ROOT, env=None, timeout=None):
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, text=True)
        return {"cmd": cmd, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    except Exception as e:
        return {"cmd": cmd, "returncode": 128, "stdout": "", "stderr": f"Exception while running command: {e}"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--branch", default=None, help="Branch name being used")
    p.add_argument("--outdir", default=str(DEFAULT_OUTDIR), help="Output directory for logs")
    p.add_argument("--skip", nargs="*", default=[], help="Skip checks by name (ruff,mypy,bandit,pytest)")
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    run_id = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    logfile = outdir / f"agent_run_{run_id}.json"
    human_log = outdir / f"agent_run_{run_id}.log"

    results = {
        "run_id": run_id,
        "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "branch": args.branch,
        "cwd": str(ROOT),
        "checks": []
    }

    overall_failed = False

    for name, cmd, required in CHECK_COMMANDS:
        if name in args.skip:
            results["checks"].append({"name": name, "skipped": True})
            continue
        # Only run commands that exist on PATH
        try:
            entry = run_cmd(cmd)
        except FileNotFoundError:
            entry = {"cmd": cmd, "returncode": 127, "stdout": "", "stderr": "executable not found"}
        entry_summary = {
            "name": name,
            "cmd": cmd,
            "returncode": entry["returncode"],
            "stdout_snippet": (entry["stdout"][:4000] if entry["stdout"] else ""),
            "stderr_snippet": (entry["stderr"][:4000] if entry["stderr"] else ""),
        }
        results["checks"].append(entry_summary)
        overall_failed = overall_failed or (required and entry["returncode"] != 0)

    # Save JSON log
    with open(logfile, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Save a short human log
    with open(human_log, "w", encoding="utf-8") as f:
        f.write(f"Agent run {run_id}\n")
        f.write(f"Timestamp: {results['timestamp_utc']}\n")
        f.write(f"Branch: {results['branch']}\n\n")
        for c in results["checks"]:
            f.write(f"- {c['name']}: returncode={{c.get('returncode','skipped')}}\n")
            if c.get("stderr_snippet"):
                f.write(f"  stderr: {{c['stderr_snippet'][:1000].replace(chr(10),' ')}}\n")
        f.write("\nJSON log: " + str(logfile) + "\n")

    # Append a brief entry into AGENT_RUNS.md (best-effort)
    try:
        from subprocess import run as _run
        run_summary = f"- {{results['timestamp_utc']}} | branch={{args.branch}} | run_id={{run_id}} | failed={{overall_failed}}\n"
        runs_md = ROOT / "AGENT_RUNS.md"
        with open(runs_md, "a", encoding="utf-8") as f:
            f.write(run_summary)
    except Exception:
        pass

    if overall_failed:
        print(f"Agent debug detected failures. See: {human_log}", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"Agent debug OK. See: {human_log}")
        sys.exit(0)

if __name__ == "__main__":
    main()