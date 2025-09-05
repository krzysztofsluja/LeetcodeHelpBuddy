"""
LLM adapters and interfaces for LeetCode Help Buddy.

This module provides abstract base classes and concrete implementations
for chatting with various LLM providers, designed to be extensible for
future integration with LangChain/LangGraph while maintaining clean abstractions.
"""

from __future__ import annotations

from .base import LLMResponse
from .openai_adapter import OpenAIAdapter
from .factory import ProviderFactory, create_adapter

__all__ = [
    "LLMResponse",
    "OpenAIAdapter",
    "ProviderFactory",
    "create_adapter"
]
