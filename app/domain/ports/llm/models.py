from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


@dataclass
class LLMRequest:
    user_prompt: str
    system_prompt: Optional[str]

@dataclass
class LLMResponse(Generic[T]):
    content: T
    model_name: Optional[str] = None
    provider: Optional[str] = None