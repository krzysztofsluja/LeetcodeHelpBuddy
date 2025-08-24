"""
Test case generator service.

This module provides the TestCaseGenerator class for generating 
test cases for LeetCode problems using OpenAI's structured outputs.
"""

from __future__ import annotations

import logging
from typing import Optional

from app.llm.base import LLMRequest, SupportedLLMProvider
from app.llm.exception.llm_exception import LLMError
from app.llm.factory import create_adapter
from ..models.models import (
    Difficulty,
    TestCaseGenerationRequest,
    TestCaseGenerationResponse,
    difficulty_description,
)

logger = logging.getLogger(__name__)


class TestCaseGenerator:
    """
    Generates test cases for LeetCode problems using LLM.
    
    This class uses the OpenAI adapter to generate non-edge test cases
    based on user input and difficulty level.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        provider: SupportedLLMProvider = SupportedLLMProvider.OPENAI
    ):
        """
        Initialize the test case generator.
        
        Args:
            model_name: OpenAI model to use for generation
            provider: LLM provider (defaults to OpenAI)
        """
        self.model_name = model_name
        self.provider = provider
        self.logger = logging.getLogger(f"{__name__}.{provider.value}")
    
    async def generate_test_cases(
        self,
        request: TestCaseGenerationRequest
    ) -> TestCaseGenerationResponse:
        """
        Generate test cases based on user input and difficulty.
        
        Args:
            request: Test case generation request
            
        Returns:
            TestCaseGenerationResponse with generated test cases
            
        Raises:
            LLMError: When LLM generation fails
            ValueError: When input validation fails
        """
        self.logger.info(
            f"Generating test cases for "
            f"difficulty {request.difficulty}"
        )

        adapter = create_adapter(
            provider=self.provider,
            model_name=self.model_name,
            response_format=TestCaseGenerationResponse
        )

        system_prompt = self._build_system_prompt(request.difficulty)
        user_prompt = self._build_user_prompt(request)
        
        llm_request = LLMRequest(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=1
        )
        
        response = await adapter.generate_structured_output(llm_request)

        self.logger.info(
            f"Successfully generated {len(response.content.test_cases)} test cases "
            f"for question: {response.content.question_slug}"
        )
        
        return response.content
    
    def _build_system_prompt(self, difficulty: Difficulty) -> str:
        base_prompt = """You are an expert at generating LeetCode test cases. Your task is to:

1. Identify the problem from user input (question slug, name, or description)
2. Generate diverse, non-edge test cases for the specified difficulty level
3. Ensure test cases cover different scenarios but are NOT edge cases
4. Before generating test cases YOU HAVE TO identity the problem.
5. Before generating test cases YOU HAVE TO get to know with the problem description and the constraints.

You ARE ALLOWED TO generate test cases ONLY for problems present in the LeetCode database.
You ARE NOT ALLOWED TO generate test cases for problems that are not present in the LeetCode database.

Guidelines:
- Generate NORMAL test cases only, not edge cases
- Cover different input patterns and scenarios
- Ensure expected results are correct
- Use proper input/output format for the problem type
- Make test cases progressively challenging based on difficulty
- The testcases which are included in LeetCode problem description or examples are not allowed to be generated.
- Make sure to generate testcases which give the helping hand to the user while testing his approach to solve the problem.
YOU ARE NOT ALLOWED TO GENERATE EDGE CASES."""
        
        return base_prompt + "\n" + difficulty_description[difficulty]
    
    def _build_user_prompt(self, request: TestCaseGenerationRequest) -> str:
        return f"""Generate {request.num_test_cases} test cases for the following problem:

User input: "{request.user_message}"
Difficulty level: {request.difficulty}

Please identify the problem and generate appropriate test cases. Ensure each test case has:
- test_case: input data in proper format
- expected_result: correct output for the input

YOU ARE NOT ALLOWED TO GENERATE EDGE CASES."""
