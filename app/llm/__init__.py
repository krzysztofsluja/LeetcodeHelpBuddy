"""
LLM adapters and interfaces for LeetCode Help Buddy.

This module provides abstract base classes and concrete implementations
for chatting with various LLM providers, designed to be extensible for
future integration with LangChain/LangGraph while maintaining clean abstractions.
"""

from __future__ import annotations

from .base import BaseLLMAdapter, LLMResponse
from .models import ExplanationRequest, ExplanationResponse, GenerationRequest
from .openai_adapter import OpenAIAdapter
from .factory.factory import LLMAdapterFactory, create_adapter
from .service import LLMService, get_llm_service

__all__ = [
    "BaseLLMAdapter",
    "LLMResponse"
    "ExplanationRequest",
    "ExplanationResponse", 
    "GenerationRequest",
    "OpenAIAdapter",
    "LLMAdapterFactory",
    "create_adapter",
    "LLMService",
    "get_llm_service",
]
