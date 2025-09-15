from typing import Dict, List, Type, TypeVar, Final
from pydantic import BaseModel
from app.domain.shared.exception.llm.llm_exception import (
    EmptyResponseException,
    LLMException,
    LLMProviderError,
    StructuredOutputNotGeneratedException,
)
from app.domain.ports.llm.models import LLMRequest, LLMResponse
from openai import APIError, AsyncOpenAI


T = TypeVar('T', bound=BaseModel)

class OpenAIAdapter:
    
    PROVIDER: Final[str] = "OPENAI"

    def __init__(self, client: AsyncOpenAI, model_name: str, temperature: float = 0.5):
        self.model_name = model_name
        self.temperature = temperature
        self.client = client

    async def generate_text_output(self, request: LLMRequest) -> str:
        messages = self.__prepare_messages(request)
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
            )
            if not response.choices or not response.choices[0].message.content:
                raise EmptyResponseException(provider=self.PROVIDER)
            return response.choices[0].message.content
        except APIError as e:
            raise LLMProviderError(provider=self.PROVIDER)

    async def generate_structured_output(
        self, request: LLMRequest, response_format: Type[T]
    ) -> LLMResponse[T]:
        messages = self.__prepare_messages(request)
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                response_model=response_format,
            )
            if not response:
                raise StructuredOutputNotGeneratedException(
                    provider=self.PROVIDER,
                    response_format_name=response_format.__name__,
                )
            return LLMResponse(
                content=response,
                model_name=self.model_name,
                provider=self.PROVIDER,
            )
        except Exception as e:
            raise StructuredOutputNotGeneratedException(
                provider=self.PROVIDER,
                response_format_name=response_format.__name__,
            )

    @staticmethod
    def __prepare_messages(request: LLMRequest) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt}
        ]
