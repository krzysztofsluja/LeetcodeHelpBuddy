from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Verdict(str, Enum):
    """Verdict on whether the user's solution approach is on the right track."""
    HAPPY_PATH = "HAPPY_PATH"
    BAD_PATH = "BAD_PATH"


class Confidence(str, Enum):
    """Confidence level in the verdict assessment."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class SolutionCheckResult(BaseModel):
    """Structured feedback on the user's solution approach."""
    
    verdict: Verdict = Field(
        ...,
        description="Binary assessment: HAPPY_PATH if approach can lead to solution, BAD_PATH if fundamentally wrong"
    )
    
    confidence: Confidence = Field(
        ...,
        description="Confidence level in the verdict (HIGH, MEDIUM, LOW)"
    )
    
    signals_observed: List[str] = Field(
        ...,
        max_length=4,
        description="Evidence-based observations about the approach (max 4 short bullets, 8-10 words each)"
    )
    
    attention_areas: List[str] = Field(
        ...,
        max_length=3,
        description="Areas requiring focus, as noun phrases only—no imperatives (max 3 items, 8-10 words each)"
    )
    
    potential_problems: List[str] = Field(
        ...,
        max_length=3,
        description="Concerns or risks in the current approach (max 3 items, 8-10 words each)"
    )
    
    encouragement: str = Field(
        ...,
        description="One short, supportive sentence to keep the user motivated"
    )


class SolutionAnalysisRequest(BaseModel):
    title: str = Field(..., description="The title of the LeetCode problem.")
    code: str = Field(..., description="The user's solution code.")


class SolutionAnalysisResponse(BaseModel):
    result: SolutionCheckResult = Field(..., description="Structured feedback on the user's solution.")
