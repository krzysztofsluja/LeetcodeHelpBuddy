from app.application.testcase.generator import TestCaseGenerator
from app.domain.ports.api.leetcode import GetProblemDetailsPort, QuestionSlugExtractorPort
from app.domain.shared.leetcode.models import LeetCodeProblem
from app.domain.testcase.models.models import Difficulty, TestCaseGenerationRequest, TestCaseGenerationResponse


class TestCaseService:
    def __init__(self, 
                 slug_extractor: QuestionSlugExtractorPort,
                 problem_fetcher: GetProblemDetailsPort,
                 test_case_generator: TestCaseGenerator):
        self.slug_extractor = slug_extractor
        self.problem_fetcher = problem_fetcher
        self.test_case_generator = test_case_generator
    
    async def generate_test_cases(
        self, 
        user_input: str,
        difficulty: Difficulty,
        num_test_cases: int = 1
    ) -> TestCaseGenerationResponse:

        problem_slug = self.slug_extractor.extract_question_slug(user_input)
        problem = LeetCodeProblem.of(problem_slug)

        problem_details = self.problem_fetcher.get_problem_details(problem)

        request = TestCaseGenerationRequest(
            user_message=user_input,
            problem_details=problem_details,
            difficulty=difficulty,
            num_test_cases=num_test_cases
        )
        
        return await self.test_case_generator.generate_test_cases(request)