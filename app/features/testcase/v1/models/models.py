from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from app.features.models import FeatureRequest, FeatureResponse


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class TestCase(BaseModel):
    question_slug: str
    test_case: str
    expected_result: str
    is_edge_case: bool = False

class EdgeTestCase(TestCase):
    is_edge_case: Literal[True] = True

class TestCaseGenerationRequest(BaseModel):
    user_message: str = Field(..., description="User message containing question slug, name, or description")
    difficulty: Difficulty = Field(..., description="Difficulty level for test case generation")
    num_test_cases: int = Field(default=3, description="Number of test cases to generate")

class TestCaseGenerationResponse(BaseModel):
    question_slug: str = Field(..., description="Identified or normalized question slug")
    test_cases: List[TestCase] = Field(..., description="Generated test cases")
    reasoning: str = Field(..., description="Explanation of test case generation approach")

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

