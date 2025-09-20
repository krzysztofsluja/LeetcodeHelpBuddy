from app.domain.shared.leetcode.models import LeetCodeProblemDetails
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum

class ExplainationMode(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass(frozen=True)
class ExplainProblemStatementRequest(BaseModel):
    problem_statement: LeetCodeProblemDetails
    mode: ExplainationMode = ExplainationMode.BEGINNER

    def __post_init__(self):
        if self.mode not in ExplainationMode:
            raise ValueError("Invalid explaination mode")
        if self.problem_statement is None:
            raise ValueError("Problem statement is required")

@dataclass(frozen=True)
class ExplainProblemStatementResponse(BaseModel):
    question_slug: str
    explaination: str

    def __post_init__(self):
        if self.question_slug is None:
            raise ValueError("Question slug is required")
        if self.explaination is None:
            raise ValueError("Explaination is required")
