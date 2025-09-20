from typing import Dict, List, Type, TypeVar, Final, Any
from pydantic import BaseModel
from app.domain.shared.exception.llm.llm_exception import (
    EmptyResponseException,
    LLMException,
    LLMProviderError,
    StructuredOutputNotGeneratedException,
)
from app.domain.ports.llm.models import LLMRequest, LLMResponse
from openai import APIError, AsyncOpenAI
from abc import ABC, abstractmethod


T = TypeVar('T', bound=BaseModel)

class BaseOpenAIAdapter(ABC):

    PROVIDER: Final[str] = "OPENAI"

    def __init__(self, client: AsyncOpenAI, model_name: str):
        self.model_name = model_name
        self.client = client

    @abstractmethod
    def _get_generation_params(self) -> Dict[str, Any]:
        """Returns model-specific generation parameters."""
        pass

    async def generate_text_output(self, request: LLMRequest) -> str:
        messages = self.__prepare_messages(request)
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **self._get_generation_params(),
            )
            if not response.choices or not response.choices[0].message.content:
                raise EmptyResponseException(provider=self.PROVIDER)
            return response.choices[0].message.content
        except APIError as e:
            raise LLMProviderError(provider=self.PROVIDER) from e

    async def generate_structured_output(
        self, request: LLMRequest, response_format: Type[T]
    ) -> LLMResponse[T]:
        messages = self.__prepare_messages(request)
        try:
            response = await self.client.responses.parse(
                model=self.model_name,
                input=messages,
                text_format=response_format,
                **self._get_generation_params(),
            )
            if response.error or not response.output:
                raise StructuredOutputNotGeneratedException(
                    provider=self.PROVIDER,
                    response_format_name=response_format.__name__,
                )
            return LLMResponse(
                content=response.output_parsed,
                model_name=self.model_name,
                provider=self.PROVIDER,
            )
        except Exception as e:
            raise StructuredOutputNotGeneratedException(
                provider=self.PROVIDER,
                response_format_name=response_format.__name__,
            ) from e

    @staticmethod
    def __prepare_messages(request: LLMRequest) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt}
        ]

class OpenAIAdapter(BaseOpenAIAdapter):

    def _get_generation_params(self) -> Dict[str, Any]:
        return {}

class OpenAITemperatureConfigurableAdapter(BaseOpenAIAdapter):
    
    def __init__(self, client: AsyncOpenAI, model_name: str, temperature: float = 0.5):
        super().__init__(client, model_name)
        self.temperature = temperature

    def _get_generation_params(self) -> Dict[str, Any]:
        return {"temperature": self.temperature}