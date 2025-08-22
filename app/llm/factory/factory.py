"""
Factory for creating LLM adapter instances.

This module provides a centralized way to create LLM adapters
with proper configuration and future-proofing for multiple providers.
"""

from __future__ import annotations

from typing import Any, Protocol, Type, TypeVar

from pydantic import BaseModel

from ..base import SimpleLLMAdapter, SupportedLLMProvider

T = TypeVar("T", bound=BaseModel)

class ProviderFactory(Protocol):
    def create_adapter(
        self,
        *,
        model_name: str,
        response_format: Type[T] | None = None,
        **kw: Any
    ) -> SimpleLLMAdapter[T]: ...

_registry: dict[SupportedLLMProvider, ProviderFactory] = {}

def register_factory(p: SupportedLLMProvider, f: ProviderFactory) -> None:
    _registry[p] = f

def create_adapter(
    provider: SupportedLLMProvider,
    model_name: str,
    response_format: Type[T] | None = None,
    **kw: Any
) -> SimpleLLMAdapter[T]:
    try:
        return _registry[provider].create_adapter(
            model_name=model_name, response_format=response_format, **kw
        )
    except KeyError:
        raise ValueError(f"No factory registered for {provider}") from None