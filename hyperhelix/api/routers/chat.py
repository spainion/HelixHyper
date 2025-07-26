from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from ...agents.llm import (
    OpenAIChatModel,
    OpenRouterChatModel,
    HuggingFaceChatModel,
    TransformersChatModel,
)
from ...utils import get_api_key

router = APIRouter()


@router.post('/chat')
def chat(prompt: str = Body(..., embed=True), provider: str = Body('openai'), model: str | None = Body(None)) -> dict[str, str]:
    """Return a raw LLM response without graph context."""
    if provider == 'openai':
        llm = OpenAIChatModel(model=model or 'gpt-3.5-turbo', api_key=get_api_key('OPENAI_API_KEY', 'test'))
    elif provider == 'openrouter':
        llm = OpenRouterChatModel(model=model or 'openai/gpt-4o', api_key=get_api_key('OPENROUTER_API_KEY'))
    elif provider in {'hf', 'huggingface'}:
        llm = HuggingFaceChatModel(model=model or 'HuggingFaceH4/zephyr-7b-beta', api_key=get_api_key('HUGGINGFACE_API_TOKEN'))
    elif provider in {'local', 'transformers'}:
        llm = TransformersChatModel(model=model or 'sshleifer/tiny-gpt2')
    else:
        raise HTTPException(status_code=400, detail='Unknown provider')
    response = llm.generate_response([{'role': 'user', 'content': prompt}])
    return {'response': response}
