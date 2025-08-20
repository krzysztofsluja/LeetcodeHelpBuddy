from typing import Optional
from app.llm.base import SupportedLLMProvider

class LLMError(Exception):
    """Base exception for LLM-related errors."""
    
    def __init__(self, message: str, provider: Optional[SupportedLLMProvider] = None, 
                 original_error: Optional[Exception] = None):
        super().__init__(message)
        self.provider = provider
        self.original_error = original_error


class LLMRateLimitError(LLMError):
    """Raised when rate limits are exceeded."""
    pass


class LLMValidationError(LLMError):
    """Raised when structured output validation fails."""
    pass


class LLMTimeoutError(LLMError):
    """Raised when requests timeout."""
    pass
