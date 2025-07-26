"""Agent that simply echoes its input."""

from .base_agent import BaseAgent


class EchoAgent(BaseAgent):
    """Return the prompt unchanged."""

    def act(self, prompt: str) -> str:  # type: ignore[override]
        return prompt