"""Trivial Python interpreter plugin used by the CLI and agents."""

from __future__ import annotations

import contextlib
import io
import sys


class PythonInterpreter:
    """Execute arbitrary Python code and capture stdout."""

    def execute(self, code: str) -> str:
        """Run ``code`` in an isolated namespace and return printed output."""
        buf = io.StringIO()
        # Prepare a minimal global namespace; do not leak builtins
        namespace: dict = {}
        with contextlib.redirect_stdout(buf):
            try:
                exec(code, namespace)
            except Exception as exc:
                return str(exc)
        return buf.getvalue()