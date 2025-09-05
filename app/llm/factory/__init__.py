"""
Factory package for LLM adapter creation.

This package auto-registers all available LLM provider factories
by importing their modules, ensuring the registration side effects execute.
"""

# Import factory modules to trigger registration
from . import openai_factory  # noqa: F401

# Re-export the main factory interface
from .factory import ProviderFactory, create_adapter, register_factory

__all__ = [
    "ProviderFactory",
    "create_adapter", 
    "register_factory"
]
