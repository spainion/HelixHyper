from __future__ import annotations

import os
import logging
from fastapi import APIRouter, HTTPException
from typing import List

from ...agents.llm import list_openrouter_models, list_huggingface_models

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/models/openrouter', response_model=List[str])
def get_openrouter_models() -> list[str]:
    """Return available model identifiers from OpenRouter."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        logger.error('OPENROUTER_API_KEY not set')
        raise HTTPException(status_code=503, detail='OPENROUTER_API_KEY not set')
    return list_openrouter_models(api_key=api_key)


@router.get('/models/huggingface', response_model=List[str])
def get_huggingface_models(q: str = 'gpt2', limit: int = 5) -> list[str]:
    """Return popular Hugging Face models."""
    try:
        return list_huggingface_models(search=q, limit=limit)
    except Exception:
        raise HTTPException(status_code=503, detail='Failed to fetch models')

