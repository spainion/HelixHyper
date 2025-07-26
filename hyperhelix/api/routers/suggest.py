from __future__ import annotations

from fastapi import APIRouter, Depends, Body, HTTPException

from ..dependencies import get_graph
from ...core import HyperHelix
from ...agents.llm import (
    OpenAIChatModel,
    OpenRouterChatModel,
    HuggingFaceChatModel,
    TransformersChatModel,
)
from ...utils import get_api_key
from ...agents.context import graph_summary

router = APIRouter()


@router.post('/suggest')
def suggest(
    prompt: str = Body(..., embed=True),
    provider: str = Body('openai'),
    model: str | None = Body(None),
    graph: HyperHelix = Depends(get_graph),
) -> dict[str, str]:
    if provider == 'openai':
        llm = OpenAIChatModel(
            model=model or 'gpt-3.5-turbo',
            api_key=get_api_key('OPENAI_API_KEY', 'test'),
        )
    elif provider == 'openrouter':
        llm = OpenRouterChatModel(
            model=model or 'openai/gpt-4o',
            api_key=get_api_key('OPENROUTER_API_KEY'),
        )
    elif provider in {'hf', 'huggingface'}:
        llm = HuggingFaceChatModel(
            model=model or 'HuggingFaceH4/zephyr-7b-beta',
            api_key=get_api_key('HUGGINGFACE_API_TOKEN'),
        )
    elif provider in {'local', 'transformers'}:
        llm = TransformersChatModel(model=model or 'sshleifer/tiny-gpt2')
    else:
        raise HTTPException(status_code=400, detail='Unknown provider')
    messages = [
        {'role': 'system', 'content': graph_summary(graph)},
        {'role': 'user', 'content': prompt},
    ]
    response = llm.generate_response(messages)
    return {'response': response}

