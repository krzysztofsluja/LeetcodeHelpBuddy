#Abstract, base class for LLM Providers
from typing import Generic, Type, TypeVar
from pydantic import BaseModel
from .models import LLMRequest, LLMResponse
from typing import Protocol

T = TypeVar('T', bound=BaseModel)

class TextLLMPort(Protocol):
    async def generate_text_output(self, request: LLMRequest) -> str: ...

class StructuredOutputLLMPort(Protocol, Generic[T]):
    async def generate_structured_output(self, request: LLMRequest, response_format: Type[T]) -> LLMResponse[T]: ...