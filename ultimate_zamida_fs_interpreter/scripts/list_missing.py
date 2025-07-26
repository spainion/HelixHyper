"""Search files for a pattern and optionally count occurrences.

This script walks a directory tree looking for files matching a
specified extension (or all files when ``--ext=*``) and containing a
given text pattern.  It prints relative paths of matching files and
optionally the total count of occurrences.
"""

from __future__ import annotations

import argparse
import os


def run(argv: list[str]) -> None:
    """Execute the missing‑marker finder with command‑line style arguments."""
    parser = argparse.ArgumentParser(description="List files containing a pattern")
    parser.add_argument("--root", default=".", help="Directory to search")
    parser.add_argument("--pattern", default="TODO", help="Text pattern to find")
    parser.add_argument("--ext", default=".py", help="File extension filter or '*' for any")
    parser.add_argument("--count", action="store_true", help="Print total count of matches")
    args = parser.parse_args(argv)

    root = args.root
    pattern = args.pattern
    ext = args.ext
    count_flag = args.count

    matches: list[str] = []
    total = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if ext != "*" and not fname.endswith(ext):
                continue
            path = os.path.join(dirpath, fname)
            try:
                text = open(path, "r", encoding="utf-8").read()
            except Exception:
                continue
            if pattern in text:
                # print relative path from root
                rel = os.path.relpath(path, root)
                matches.append(rel)
                if count_flag:
                    total += text.count(pattern)
    for m in matches:
        print(m)
    if count_flag:
        print(total)