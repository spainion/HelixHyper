"""Generate a .env file from a YAML configuration of API keys."""

from __future__ import annotations

try:
    import yaml  # type: ignore[import-not-found]
except Exception:
    yaml = None

from typing import Optional


def run(env: str, cfg: str) -> None:
    """Write environment variables from a YAML config into an .env file.

    :param env: destination filename for the .env file
    :param cfg: YAML file mapping keys to values
    """
    if yaml is None:
        raise RuntimeError("PyYAML is required for setup_env")
    data = yaml.safe_load(open(cfg, "r", encoding="utf-8").read()) or {}
    with open(env, "w", encoding="utf-8") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")