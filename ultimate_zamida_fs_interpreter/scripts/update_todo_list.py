"""Generate a TODO list file from pattern matches (stub used by tools_cli)."""

from __future__ import annotations

from typing import List

from scripts.list_missing import run as list_missing_run


def run(argv: List[str]) -> None:
    # Forward arguments to list_missing and capture output to file if requested
    output = None
    opts: list[str] = []
    it = iter(argv)
    for arg in it:
        if arg == "--output":
            try:
                output = next(it)
            except StopIteration:
                output = None
        else:
            opts.append(arg)
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    buf = StringIO()
    sys.stdout = buf
    try:
        # Always append --count to count matches.  The tests monkeypatch
        # list_missing.run and expect the additional flag.
        list_missing_run(opts + ["--count"])
    finally:
        sys.stdout = old_stdout
    lines = buf.getvalue()
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(lines)
    else:
        print(lines, end="")