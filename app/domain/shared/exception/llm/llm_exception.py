from abc import ABC
from typing import Any, Dict, Optional
from app.domain.shared.exception.base import BaseApplicationException


class LLMException(BaseApplicationException, ABC):
    """Raised when an error occurs in the LLM."""

    def __init__(self, provider: str, message: str = "AI service encountered an issue."):
        context = {"provider": provider}
        super().__init__(message, context)


class LLMProviderError(LLMException):
    """Raised when the LLM provider returns an error."""

    def __init__(self, provider: str, message: str = "LLM provider returned an error."):
        super().__init__(provider, message)


class StructuredOutputNotGeneratedException(LLMException):
    """Raised when structured output is not generated."""

    def __init__(
        self,
        provider: str,
        response_format_name: str,
        message: str = "Could not generate structured output from the LLM.",
    ):
        context = {"provider": provider, "response_format_name": response_format_name}
        super(LLMException, self).__init__(provider, message)
        self.context.update(context)


class EmptyResponseException(LLMException):
    """Raised when the response is empty."""

    def __init__(self, provider: str, message: str = "The LLM returned an empty response."):
        super().__init__(provider, message)