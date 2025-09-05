from typing import Any, Type, TypeVar
from pydantic import BaseModel
from app.llm.base import SimpleLLMAdapter, SupportedLLMProvider
from app.llm.openai_adapter import OpenAIAdapter
from app.llm.factory.factory import register_factory

T = TypeVar("T", bound=BaseModel)

class OpenAIAdapterFactory:
    def create_adapter(
        self,
        *,
        model_name: str = "gpt-4o-mini",
        response_format: Type[T] | None = None,
        **kw: Any
    ) -> SimpleLLMAdapter[T]:
        return OpenAIAdapter(model_name=model_name, response_format=response_format)
    
register_factory(SupportedLLMProvider.OPENAI, OpenAIAdapterFactory())