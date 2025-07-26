import os
import logging

logger = logging.getLogger(__name__)


def get_api_key(name: str, default: str | None = None) -> str | None:
    """Return API key from the environment.

    Logs a warning when the key is missing and no default is provided.
    """
    value = os.getenv(name, default)
    if value is None:
        logger.warning("%s not set", name)
    return value
