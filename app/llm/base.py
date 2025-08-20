"""
Abstract base classes for LLM adapters.

This module defines the interface that all LLM adapters must implement,
providing a consistent API across different providers (OpenAI, Anthropic, etc.)
and future frameworks (LangChain, LangGraph).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from enum import Enum
from dataclasses import dataclass
import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseModel)


class SupportedLLMProvider(Enum):
    OPENAI = "openai"

@dataclass
class LLMResponse(Generic[T]):
    """Response wrapper for LLM calls."""
    content: T
    model_name: Optional[str] = None
    provider: Optional[SupportedLLMProvider] = None

@dataclass
class LLMRequest:
    user_prompt: str
    system_prompt: Optional[str]
    temperature: float = 0.1
    timeout_seconds: float = 30.0
    
class SimpleLLMAdapter(ABC):

    def __init__(self, provider: SupportedLLMProvider):
        self.provider = provider
        self.logger = logging.getLogger(f"{__name__}.{provider.value}")

    @abstractmethod
    async def generate_simple_text_output(
        self,
        request: LLMRequest
    ) -> str:
        """
        Generate a simple text response (convenience method).
        
        Args:
            request: LLMRequest
            
        Returns:
            Generated text content as string
        """
        pass
    
    def _log_request(self, prompt: str, **kwargs: Any) -> None:
        self.logger.debug(
            f"LLM request - provider: {self.provider.value}, "
            f"prompt_length: {len(prompt)}, kwargs: {list(kwargs.keys())}"
        )
    
    def _log_response(self, response: LLMResponse[T]) -> None:
        self.logger.info(
            f"LLM response - provider: {self.provider.value}, "
            f"model: {response.model}, latency: {response.latency_ms}ms, "
            f"usage: {response.usage}"
        )


class StructuredLLMAdapter(SimpleLLMAdapter, Generic[T]):
    """
    Abstract base class for all LLM adapters.
    
    This interface ensures consistency across different providers and 
    future framework integrations while maintaining flexibility for
    provider-specific features.
    
    Design principles:
    - Provider-agnostic: Works with OpenAI, Anthropic, local models, etc.
    - Framework-ready: Compatible with future LangChain/LangGraph integration
    - Type-safe: Uses Pydantic for structured outputs and type validation
    - Observable: Built-in logging, metrics, and error handling
    - Async-first: All operations are async for better performance
    """

    @abstractmethod
    async def generate_structured_output(
        self,
        request: LLMRequest
    ) -> LLMResponse[T]:
        """
        Generate a structured response using the specified Pydantic model.
        
        Args:
            request: LLMRequest
            
        Returns:
            LLMResponse containing the structured content and metadata
            
        Raises:
            LLMError: Base class for all LLM-related errors
            LLMRateLimitError: When rate limits exceeded
            LLMValidationError: When response doesn't match expected schema
            LLMTimeoutError: When request times out
        """
        pass