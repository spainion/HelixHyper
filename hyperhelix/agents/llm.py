from __future__ import annotations

import abc
import logging
from typing import Sequence

logger = logging.getLogger(__name__)


class BaseChatModel(abc.ABC):
    """Abstract interface for chat-based LLM providers."""

    @abc.abstractmethod
    def generate_response(self, messages: Sequence[dict]) -> str:
        """Return a model-generated reply for the given messages."""


class OpenAIChatModel(BaseChatModel):
    """Simple OpenAI chat completion wrapper."""

    def __init__(self, model: str = "gpt-3.5-turbo", api_key: str | None = None) -> None:
        import openai

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def generate_response(self, messages: Sequence[dict]) -> str:
        try:
            resp = self.client.chat.completions.create(model=self.model, messages=list(messages))
            return resp.choices[0].message.content
        except Exception:  # pragma: no cover - network failures
            logger.exception("LLM request failed")
            raise
