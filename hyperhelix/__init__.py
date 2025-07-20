import logging
import logging.config
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config' / 'logging.yaml'

if CONFIG_PATH.exists():
    with CONFIG_PATH.open('r') as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)
else:
    logging.basicConfig(level=logging.INFO)  # pragma: no cover

__all__ = ['core', 'node', 'edge', 'metadata']
