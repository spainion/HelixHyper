from __future__ import annotations

import abc
import logging
import json
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
        """Create an OpenAI chat model wrapper.

        The API key is read from the ``api_key`` argument or the
        ``OPENAI_API_KEY`` environment variable. A missing key results in a
        ``RuntimeError`` so tests can monkeypatch ``generate_response`` without
        actually hitting the API.
        """
        import os
        import openai

        key = api_key or os.getenv("OPENAI_API_KEY", "test")
        self.client = openai.OpenAI(api_key=key)
        self.model = model

    def generate_response(self, messages: Sequence[dict]) -> str:
        try:
            resp = self.client.chat.completions.create(model=self.model, messages=list(messages))
            return resp.choices[0].message.content
        except Exception:  # pragma: no cover - network failures
            logger.exception("LLM request failed")
            raise


class OpenRouterChatModel(BaseChatModel):
    """Chat model that calls the OpenRouter API."""

    def __init__(self, model: str = "openai/gpt-4o", api_key: str | None = None) -> None:
        import httpx  # locally imported to ease mocking in tests

        self.httpx = httpx
        self.model = model
        self.api_key = api_key

    def generate_response(self, messages: Sequence[dict]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "messages": list(messages)}
        try:
            resp = self.httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception:  # pragma: no cover - network failures
            logger.exception("OpenRouter request failed")
            raise

    def stream_response(self, messages: Sequence[dict]) -> str:
        """Return a streaming reply joined into a final string."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "messages": list(messages), "stream": True}
        try:
            text = ""
            with self.httpx.stream(
                "POST",
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=None,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            piece = json.loads(data)["choices"][0]["delta"].get("content")
                        except Exception:
                            piece = None
                        if piece:
                            text += piece
            return text
        except Exception:  # pragma: no cover - network failures
            logger.exception("OpenRouter streaming request failed")
            raise


class HuggingFaceChatModel(BaseChatModel):
    """Use the Hugging Face Inference API for chat completions."""

    def __init__(self, model: str = "HuggingFaceH4/zephyr-7b-beta", api_key: str | None = None) -> None:
        import httpx  # imported locally for easier mocking

        self.httpx = httpx
        self.model = model
        self.api_key = api_key

    def generate_response(self, messages: Sequence[dict]) -> str:
        prompt = "\n".join(m["content"] for m in messages)
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        url = f"https://api-inference.huggingface.co/models/{self.model}"
        try:
            resp = self.httpx.post(url, json={"inputs": prompt}, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list) and data and "generated_text" in data[0]:
                return data[0]["generated_text"]
            if isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            raise RuntimeError("Unexpected response")
        except Exception:  # pragma: no cover - network failures
            logger.exception("HuggingFace request failed")
            raise

def list_openrouter_models(api_key: str | None = None) -> list[str]:
    """Return a list of available model IDs from OpenRouter."""
    import httpx

    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    try:
        resp = httpx.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        return [m["id"] for m in data.get("data", [])]
    except Exception:  # pragma: no cover - network failures
        logger.exception("Failed to list models")
        raise

