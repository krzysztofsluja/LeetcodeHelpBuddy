from app.domain.solution.models.models import (
    SolutionAnalysisRequest,
    SolutionAnalysisResponse,
)
from app.application.solution.generator import SolutionGenerator
from app.domain.ports.api.leetcode import GetProblemDetailsPort, QuestionSlugExtractorPort
from app.domain.shared.leetcode.models import LeetCodeProblem


class SolutionService:

    def __init__(
            self,
            slug_extractor: QuestionSlugExtractorPort,
            problem_details_port: GetProblemDetailsPort,
            solution_generator: SolutionGenerator
    ):
        self.slug_extractor = slug_extractor
        self.problem_details_port = problem_details_port
        self.solution_generator = solution_generator

    async def process(self, request: SolutionAnalysisRequest) -> SolutionAnalysisResponse:
        question_slug = self.slug_extractor.extract_question_slug(request.title)
        problem = LeetCodeProblem.of(question_slug)
        problem_details = self.problem_details_port.get_problem_details(problem)

        feedback = await self.solution_generator.generate_feedback(request, problem_details)
        return SolutionAnalysisResponse(feedback=feedback)
