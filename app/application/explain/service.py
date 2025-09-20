from app.domain.ports.api.leetcode import GetProblemDetailsPort, QuestionSlugExtractorPort
from app.domain.shared.leetcode.models import LeetCodeProblem
from app.application.explain.generator import ProblemStatementExplainer
from app.domain.explain.models.models import ExplainProblemStatementRequest, ExplainationMode


class ExplanationError(Exception):
    pass


class ExplanationService:
    def __init__(
        self,
        question_slug_extractor: QuestionSlugExtractorPort,
        problem_details_port: GetProblemDetailsPort,
        problem_statement_explainer: ProblemStatementExplainer,
    ) -> None:
        self._question_slug_extractor = question_slug_extractor
        self._problem_details_port = problem_details_port
        self._problem_statement_explainer = problem_statement_explainer

    async def explain(self, user_input: str) -> str:
        try:
            question_slug = self._question_slug_extractor.extract_question_slug(user_input)
            problem = LeetCodeProblem.of(question_slug)
            problem_details = self._problem_details_port.get_problem_details(problem)
            explain_problem_statement_request = ExplainProblemStatementRequest(
                problem_statement=problem_details,
                mode=ExplainationMode.BEGINNER
            )
            return await self._problem_statement_explainer.explain_problem_statement(explain_problem_statement_request)
        except Exception as e:
            raise ExplanationError(f"Failed to generate explanation: {e}") from e
