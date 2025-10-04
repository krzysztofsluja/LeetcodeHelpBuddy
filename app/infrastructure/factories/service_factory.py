
import os

from openai import AsyncOpenAI
from app.application.testcase.generator import TestCaseGenerator
from app.application.testcase.service import TestCaseService
from app.application.explain.service import ExplanationService
from app.infrastructure.adapters.api.leetcode import AlfaLCGetProblemDetailsAdapter, SimpleQuestionSlugExtractorAdapter
from app.infrastructure.adapters.llm.openai import OpenAIAdapter, OpenAITemperatureConfigurableAdapter
from app.application.explain.generator import ProblemStatementExplainer
from app.application.solution.service import SolutionService
from app.application.solution.generator import SolutionGenerator


class ServiceFactory:

    @staticmethod
    def create_test_case_service() -> TestCaseService:
        return TestCaseService(
            slug_extractor=SimpleQuestionSlugExtractorAdapter(),
            problem_fetcher=AlfaLCGetProblemDetailsAdapter(),
            test_case_generator=TestCaseGenerator(
                llm_port=OpenAITemperatureConfigurableAdapter(
                    client=AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")),
                    model_name="gpt-4o-mini",
                    temperature=0.7
                )
            )
        )

    @staticmethod
    def create_explanation_service() -> ExplanationService:
        return ExplanationService(
            question_slug_extractor=SimpleQuestionSlugExtractorAdapter(),
            problem_details_port=AlfaLCGetProblemDetailsAdapter(),
            problem_statement_explainer=ProblemStatementExplainer(
                llm_port=OpenAIAdapter(
                    client=AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")),
                    model_name="o3-mini"
                )
            )
        )

    @staticmethod
    def create_solution_service() -> SolutionService:
        return SolutionService(
            slug_extractor=SimpleQuestionSlugExtractorAdapter(),
            problem_details_port=AlfaLCGetProblemDetailsAdapter(),
            solution_generator=SolutionGenerator(
                llm_port=OpenAIAdapter(
                    client=AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")),
                    model_name="o3-mini"
                )
            )
        )