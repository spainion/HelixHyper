import os
import pytest
from hyperhelix.api.routers import suggest


@pytest.fixture
def capture_openai(monkeypatch):
    """Patch ``OpenAIChatModel.generate_response`` unless live tests requested."""
    captured: dict | None = {} if os.getenv("USE_REAL_LLM", "").lower() not in {"1", "true", "yes"} else None
    if captured is not None:
        def fake_generate(self, messages):
            captured["messages"] = messages
            return "ok"
        monkeypatch.setattr(suggest.OpenAIChatModel, "generate_response", fake_generate)
        if not os.getenv("OPENAI_API_KEY"):
            monkeypatch.setenv("OPENAI_API_KEY", "test")
    yield captured
