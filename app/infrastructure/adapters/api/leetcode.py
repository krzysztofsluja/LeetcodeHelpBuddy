from typing import Dict, Final, override
from app.domain.ports.api.leetcode import GetProblemDetailsPort, QuestionSlugExtractorPort
from app.domain.shared.exception.api.api_exception import LeetCodeApiError, LeetCodeProblemNotFoundError
from app.domain.shared.leetcode.models import LeetCodeProblem, LeetCodeProblemDetails, LeetCodeProblemSlug
import requests
import re
from cattrs import Converter


class GetProblemDetailsAdapter(GetProblemDetailsPort):

    def __init__(self, get_problem_details_endpoint: str):
        self.get_problem_details_endpoint = get_problem_details_endpoint

    @override
    def get_problem_details(self, converter: Converter, payload: Dict[str, str]) -> LeetCodeProblemDetails:
        try:
            request = requests.get(self.get_problem_details_endpoint, params=payload)
            if request.status_code != 200:
                raise LeetCodeApiError()
            return converter.structure(request.json(), LeetCodeProblemDetails)
        except Exception as e:
            raise LeetCodeApiError()

class SimpleQuestionSlugExtractorAdapter(QuestionSlugExtractorPort):

    def extract_question_slug(self, user_input: str) -> LeetCodeProblemSlug:
        if not user_input or user_input.strip() == "":
            raise LeetCodeProblemNotFoundError()
        cleaned = user_input.strip().lower()
        cleaned = re.sub(r'^(leetcode\s*)?(\d+\.?\s*)?', '', cleaned)
        cleaned = re.sub(r'\s*(problem|question)\s*$', '', cleaned)
        slug = re.sub(r'[^\w\s-]', '', cleaned)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        try:
            return LeetCodeProblem.of(slug)
        except ValueError as e:
            raise LeetCodeProblemNotFoundError(f"Generated invalid slug '{slug}': {e}")