"""
LLM adapters and interfaces for LeetCode Help Buddy.

This module provides abstract base classes and concrete implementations
for chatting with various LLM providers, designed to be extensible for
future integration with LangChain/LangGraph while maintaining clean abstractions.
"""

from __future__ import annotations

from .base import BaseLLMAdapter, LLMResponse
from .config import LLMConfig, get_llm_config
from .models import ExplanationRequest, ExplanationResponse, GenerationRequest
from .openai_adapter import OpenAIAdapter
from .factory import LLMAdapterFactory, create_default_adapter, create_openai_adapter
from .service import LLMService, get_llm_service

__all__ = [
    "BaseLLMAdapter",
    "LLMResponse"
    "LLMConfig",
    "get_llm_config",
    "ExplanationRequest",
    "ExplanationResponse", 
    "GenerationRequest",
    "OpenAIAdapter",
    "LLMAdapterFactory",
    "create_default_adapter",
    "create_openai_adapter",
    "LLMService",
    "get_llm_service",
]
