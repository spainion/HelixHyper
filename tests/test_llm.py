import types

from hyperhelix.agents.llm import OpenAIChatModel


def test_openai_chat_model(monkeypatch):
    class DummyClient:
        class ChatCompletions:
            def create(self, model, messages):
                return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content='ok'))])
        def __init__(self, api_key=None):
            self.chat = types.SimpleNamespace(completions=self.ChatCompletions())
    monkeypatch.setattr('openai.OpenAI', lambda api_key=None: DummyClient(api_key))
    model = OpenAIChatModel(api_key='k')
    resp = model.generate_response([{'role': 'user', 'content': 'hi'}])
    assert resp == 'ok'
