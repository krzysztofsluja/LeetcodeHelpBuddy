class LLMException(Exception):
    """Raised when an error occurs in the LLM."""
    pass

class StructuredOutputNotGeneratedException(LLMException):
    """Raised when structured output is not generated."""
    pass

class EmptyResponseException(LLMException):
    """Raised when the response is empty."""
    pass