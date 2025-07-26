"""Minimal GPT connector stub used in diagnostics tests."""

class GPTConnector:
    """Stub connector returning a canned response."""

    def query(self, prompt: str, temperature: float = 0.7, **kwargs) -> str:
        # Always return a fixed token; tests monkeypatch this method
        return "pong"