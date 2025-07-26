"""Configuration loader for environment variables.

This module provides a simple `load_env` function that reads a local
`.env` file and a YAML configuration file from a `config` directory.  It
populates `os.environ` with any key/value pairs found in those files
without overwriting existing environment variables.  The `.env` file
should contain lines of the form `KEY=value`.  The YAML file
(`api_keys.yaml` by default) should map keys to values.  If either
file is missing, the loader silently continues.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    import yaml  # type: ignore[import-not-found]
except Exception:
    yaml = None  # fallback if PyYAML isn't installed


def load_env() -> None:
    """Load variables from a `.env` file and a YAML API key file.

    The function looks in the current working directory for a `.env`
    file and a `config/api_keys.yaml` file.  For each line in the
    `.env` file containing an equals sign, the key and value are
    separated and any surrounding whitespace trimmed.  Environment
    variables that are already set are left unchanged.

    If the YAML configuration file exists and the `yaml` package is
    available, it is parsed and any top‑level mappings are merged into
    `os.environ` as strings.  Missing files are ignored.
    """
    cwd = Path.cwd()
    # Load key=value pairs from .env
    env_file = cwd / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()
                # Only set if not already in the environment
                if key and key not in os.environ:
                    os.environ[key] = value
    # Load YAML API keys if PyYAML is available
    cfg_dir = cwd / "config"
    yaml_file = cfg_dir / "api_keys.yaml"
    if yaml_file.exists() and yaml is not None:
        try:
            data = yaml.safe_load(yaml_file.read_text()) or {}
        except Exception:
            data = {}
        if isinstance(data, dict):
            for key, value in data.items():
                key_str = str(key)
                if key_str and key_str not in os.environ:
                    os.environ[key_str] = str(value)