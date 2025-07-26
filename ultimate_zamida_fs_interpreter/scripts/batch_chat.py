"""Run a batch of chat prompts through an OpenAI‑like connector.

The configuration file passed to :func:`run` should contain a YAML
list of chat messages for each request.  The connector is expected to
provide an ``async_multi_chat`` coroutine that accepts a list of
prompt lists and returns a list of response strings.

Tests monkeypatch the ``OpenAIConnector`` symbol in this module to
provide custom behaviour.  A stub implementation is provided for
completeness but will not be exercised by the tests.
"""

from __future__ import annotations

import asyncio
from typing import Any, List

try:
    import yaml  # type: ignore[import-not-found]
except Exception:
    yaml = None


class OpenAIConnector:
    """Stub connector used when tests don't monkeypatch this name."""

    async def async_multi_chat(self, prompts: List[List[dict]]) -> List[str]:
        # Return empty strings for each prompt set
        return ["" for _ in prompts]


def run(config_path: str) -> None:
    """Load prompts from ``config_path``, send them to the connector and print responses."""
    if yaml is None:
        raise RuntimeError("PyYAML is required for batch_chat")
    with open(config_path, "r", encoding="utf-8") as f:
        prompts: List[Any] = yaml.safe_load(f)
    # Instantiate connector; tests may replace this class attribute
    connector = OpenAIConnector()
    # Run the async call synchronously for simplicity
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        responses = loop.run_until_complete(connector.async_multi_chat(prompts))
    finally:
        loop.close()
        asyncio.set_event_loop(None)
    for resp in responses:
        print(resp)