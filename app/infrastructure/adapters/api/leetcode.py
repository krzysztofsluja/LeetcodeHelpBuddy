import os
from sqlite3 import paramstyle
from typing import Dict, Final, override
from app.domain.ports.api.leetcode import GetProblemDetailsPort, QuestionSlugExtractorPort
from app.domain.shared.exception.api.api_exception import LeetCodeApiError, LeetCodeProblemNotFoundError
from app.domain.shared.leetcode.models import LeetCodeProblem, LeetCodeProblemDetails, LeetCodeProblemSlug
import requests
import re
from cattrs import Converter
from dotenv import load_dotenv

class AlfaLCGetProblemDetailsAdapter(GetProblemDetailsPort):

    def __init__(self):
        # TODO: Implement this
        load_dotenv()
        if not os.getenv("ALFA_LEETCODE_API_URL"):
            raise LeetCodeApiError("ALFA_LEETCODE_API_URL is not set")
        api_url = os.getenv("ALFA_LEETCODE_API_URL")
        self.get_problem_details_endpoint = api_url + "/select"

    @override
    def get_problem_details(self, problem: LeetCodeProblem) -> LeetCodeProblemDetails:
        converter = self.__prepare_converter()
        try:
            payload = {'titleSlug': problem.question_slug.question_slug}
            request = requests.get(self.get_problem_details_endpoint, params=payload)
            if request.status_code != 200:
                raise LeetCodeApiError()
            return converter.structure(request.json(), LeetCodeProblemDetails)
        except Exception as e:
            raise LeetCodeApiError()

    def __prepare_converter(self) -> Converter:
        converter = Converter()
        converter.register_structure_hook(
            LeetCodeProblemDetails, 
            lambda dct, _: LeetCodeProblemDetails(
                question_slug=dct['titleSlug'],
                question_title=dct['questionTitle'],
                question_content=dct['question'],
                example_testcases=dct['exampleTestcases'],
                difficulty=dct['difficulty']
            )
        )
        return converter

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