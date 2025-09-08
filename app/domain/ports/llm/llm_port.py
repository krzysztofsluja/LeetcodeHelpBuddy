#Abstract, base class for LLM Providers
from typing import Generic, TypeVar
from pydantic import BaseModel
from .models import LLMRequest, LLMResponse
from typing import Protocol

T = TypeVar('T', bound=BaseModel)

class LLMPort(Protocol, Generic[T]):
    async def generate_text_output(self, request: LLMRequest) -> str: ...
    async def generate_structured_output(self, request: LLMRequest) -> LLMResponse[T]: ...