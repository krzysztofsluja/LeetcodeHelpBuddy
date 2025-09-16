from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from app.domain.shared.leetcode.models import LeetCodeProblemDetails


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class TestCase(BaseModel):
    test_case_content: str
    expected_result: str
    is_edge_case: bool = False

class EdgeTestCase(TestCase):
    is_edge_case: Literal[True] = True

class ProblemTestCases(BaseModel):
    test_cases: List[TestCase]

@dataclass(frozen=True)
class TestCaseGenerationRequest(BaseModel):
    user_message: str = Field(..., description="User message containing question slug, name, or description")
    difficulty: Difficulty = Field(..., description="Difficulty level for test case generation")
    num_test_cases: int = Field(default=1, description="Number of test cases to generate")
    problem_details: LeetCodeProblemDetails = Field(..., description="Problem details")

    def __post_init__(self):
        if self.num_test_cases < 1:
            raise ValueError("Number of test cases must be at least 1")
        if self.num_test_cases > 10:
            self.num_test_cases = 10
        if self.difficulty not in Difficulty:
            raise ValueError("Invalid difficulty level")
        if self.problem_details is None:
            raise ValueError("Problem details are required")
        if not self.user_message or self.user_message.strip() == "":
            raise ValueError("User message is required")

class TestCaseGenerationResponse(BaseModel):
    question_slug: str = Field(..., description="Identified or normalized question slug")
    test_cases: ProblemTestCases = Field(..., description="Generated test cases")

difficulty_description = {
    Difficulty.EASY: """
- Focus on basic functionality testing
- Use simple, straightforward inputs
- Keep test cases relatively small in size
- Test core algorithm behavior""",
    Difficulty.MEDIUM: """
- Include moderate complexity scenarios
- Test boundary conditions (but not edge cases)
- Use medium-sized inputs
- Cover multiple solution paths""",
    Difficulty.HARD: """
- Generate complex, challenging scenarios
- Use larger input sizes where appropriate
- Test algorithmic efficiency requirements
- Include intricate cases that test deep understanding"""
}

