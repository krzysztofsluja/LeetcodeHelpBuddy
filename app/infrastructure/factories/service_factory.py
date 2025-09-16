
import os

from openai import AsyncOpenAI
from app.application.testcase.generator import TestCaseGenerator
from app.application.testcase.service import TestCaseService
from app.infrastructure.adapters.api.leetcode import AlfaLCGetProblemDetailsAdapter, SimpleQuestionSlugExtractorAdapter
from app.infrastructure.adapters.llm.openai import OpenAIAdapter


class ServiceFactory:

    @staticmethod
    def create_test_case_service() -> TestCaseService:
        return TestCaseService(
            slug_extractor=SimpleQuestionSlugExtractorAdapter(),
            problem_fetcher=AlfaLCGetProblemDetailsAdapter(),
            test_case_generator=TestCaseGenerator(
                llm_port=OpenAIAdapter(
                    client=AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")),
                    model_name="gpt-4o-mini",
                    temperature=0.7
                )
            )
        )