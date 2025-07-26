"""Base class for simple agents."""


class BaseAgent:
    """Defines a common interface for agents."""

    def act(self, prompt: str) -> str:
        raise NotImplementedError