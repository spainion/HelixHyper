import os

from hyperhelix.agents.llm import OpenAIChatModel, OpenRouterChatModel


def test_openai_chat_model_live():
    model = OpenAIChatModel(api_key=os.getenv('OPENAI_API_KEY'))
    resp = model.generate_response([{'role': 'user', 'content': 'Hello!'}])
    assert isinstance(resp, str) and resp


def test_openrouter_chat_model_live():
    model = OpenRouterChatModel(api_key=os.getenv('OPENROUTER_API_KEY'))
    resp = model.generate_response([{'role': 'user', 'content': 'Ping?'}])
    assert isinstance(resp, str) and resp
