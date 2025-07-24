from __future__ import annotations

import os
from fastapi import APIRouter, Depends, Body, HTTPException

from ..dependencies import get_graph
from ...core import HyperHelix
from ...agents.llm import OpenAIChatModel, OpenRouterChatModel
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
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise HTTPException(status_code=503, detail='OPENAI_API_KEY not set')
        llm = OpenAIChatModel(model=model or 'gpt-3.5-turbo', api_key=api_key)
    elif provider == 'openrouter':
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise HTTPException(status_code=503, detail='OPENROUTER_API_KEY not set')
        llm = OpenRouterChatModel(model=model or 'openai/gpt-4o', api_key=api_key)
    else:
        raise HTTPException(status_code=400, detail='Unknown provider')
    messages = [
        {'role': 'system', 'content': graph_summary(graph)},
        {'role': 'user', 'content': prompt},
    ]
    response = llm.generate_response(messages)
    return {'response': response}

