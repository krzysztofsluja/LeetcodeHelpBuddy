from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMRequest:
    user_prompt: str
    system_prompt: Optional[str]
    temperature: float = 0.1

@dataclass
class LLMResponse(Generic[T]):
    content: T
    model_name: Optional[str] = None