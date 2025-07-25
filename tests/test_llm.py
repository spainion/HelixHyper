import os

from hyperhelix.agents.llm import (
    OpenAIChatModel,
    OpenRouterChatModel,
    HuggingFaceChatModel,
    list_openrouter_models,
)


import pytest


@pytest.mark.skipif(
    not os.getenv('OPENAI_API_KEY'),
    reason='OPENAI_API_KEY not set; skipping live OpenAI test',
)
def test_openai_chat_model_live():
    model = OpenAIChatModel(api_key=os.getenv('OPENAI_API_KEY'))
    resp = model.generate_response([{'role': 'user', 'content': 'Hello!'}])
    assert isinstance(resp, str) and resp


@pytest.mark.skipif(
    not os.getenv('OPENROUTER_API_KEY'),
    reason='OPENROUTER_API_KEY not set; skipping live OpenRouter test',
)
def test_openrouter_chat_model_live():
    model = OpenRouterChatModel(api_key=os.getenv('OPENROUTER_API_KEY'))
    resp = model.generate_response([{'role': 'user', 'content': 'Ping?'}])
    assert isinstance(resp, str) and resp


@pytest.mark.skipif(
    not os.getenv('OPENROUTER_API_KEY'),
    reason='OPENROUTER_API_KEY not set; skipping live streaming test',
)
def test_openrouter_stream_live():
    model = OpenRouterChatModel(api_key=os.getenv('OPENROUTER_API_KEY'))
    resp = model.stream_response([{'role': 'user', 'content': 'Hello'}])
    assert isinstance(resp, str) and resp


@pytest.mark.skipif(
    not os.getenv('OPENROUTER_API_KEY'),
    reason='OPENROUTER_API_KEY not set; skipping model listing test',
)
def test_list_models_live():
    models = list_openrouter_models(api_key=os.getenv('OPENROUTER_API_KEY'))
    assert isinstance(models, list) and models


def test_openrouter_defaults_to_env(monkeypatch):
    monkeypatch.setenv('OPENROUTER_API_KEY', 'xyz')
    model = OpenRouterChatModel()
    assert model.api_key == 'xyz'


def test_huggingface_defaults_to_env(monkeypatch):
    monkeypatch.setenv('HUGGINGFACE_API_TOKEN', 'abc')
    model = HuggingFaceChatModel()
    assert model.api_key == 'abc'

