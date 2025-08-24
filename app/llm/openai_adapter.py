"""
OpenAI-specific LLM adapter implementation.

This module provides a concrete implementation of the BaseLLMAdapter
for OpenAI's API, including structured outputs, streaming, and retries.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional, Type, TypeVar
import os
from openai import AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

from app.llm.exception.llm_exception import LLMError

from .base import (
    StructuredLLMAdapter,
    SupportedLLMProvider,
    LLMResponse,
    LLMRequest
)

T = TypeVar('T', bound=BaseModel)


class OpenAIAdapter(StructuredLLMAdapter[T]):
    """
    OpenAI-specific implementation of the LLM adapter.
    
    Features:
    - Structured outputs using OpenAI's JSON Schema support
    - Streaming responses with optional final structured parsing
    - Exponential backoff retry logic
    - Token usage tracking and cost estimation
    - Comprehensive error handling and logging
    """
    
    def __init__(self, model_name: str, response_format: Optional[Type[T]] = None):
        if not model_name:
            raise ValueError("Model name is required")
        super().__init__(SupportedLLMProvider.OPENAI)
        load_dotenv()
        
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            timeout=30.0,
        )
        self.model = model_name
        self.response_format = response_format

    async def _call_llm_api(self, request: LLMRequest) -> Any:
        return self.client.responses.create(
            model=self.model,
            instructions=request.system_prompt,
            input=request.user_prompt,
            temperature=request.temperature)
    
    async def generate_simple_text_output(self, request: LLMRequest) -> str:
        response = await self._call_llm_api(request)
        return response.output_text

        
    async def generate_structured_output(
        self,
        request: LLMRequest,
        response_format: Optional[Type[T]] = None
    ) -> LLMResponse[T]:
        """Generate a structured response using OpenAI's structured outputs."""
        
        self._log_request(request.user_prompt, temperature=request.temperature)
        schema = self.response_format or response_format
        if schema is None:
            raise ValueError("Response format is required")
        
        try:
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.user_prompt})
            
            llm_response = await self._call_llm_api_with_structured_output(
                messages=messages,
                response_format=schema,
                temperature=request.temperature
            )
            self._log_response(llm_response)
            return llm_response
            
        except Exception as e:
            if isinstance(e, (LLMError)):
                raise
            raise LLMError(
                f"Unexpected error in OpenAI structured generation: {e}",
                provider=SupportedLLMProvider.OPENAI,
                original_error=e
            )
    
    async def validate_connection(self) -> bool:
        """Validate OpenAI connection by making a simple API call."""
        try:
            self.client.models.list()
        except openai.AuthenticationError:
            return False
        else:
            return True
    
    async def _call_llm_api_with_structured_output(
        self,
        messages: list[Dict[str, str]],
        response_format: Type[T],
        temperature: float,
    ) -> LLMResponse[T]:
        """Call the LLM API with structured output."""
        completion = await self.client.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=response_format,
            temperature=temperature
        )
        response = completion.choices[0].message
        if response.refusal:
            raise LLMError(
                f"OpenAI refused to generate a response: {response.refusal}",
                provider=SupportedLLMProvider.OPENAI
            )
        return LLMResponse(
            content=response.parsed,
            model_name=self.model,
            provider=SupportedLLMProvider.OPENAI
        )