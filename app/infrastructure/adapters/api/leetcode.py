from __future__ import annotations

import functools
import re
from typing import override

import requests
from cattrs import Converter

from app.domain.ports.api.leetcode import (
    GetProblemDetailsPort,
    QuestionSlugExtractorPort,
)
from app.domain.shared.exception.api.api_exception import (
    LeetCodeApiError,
    LeetCodeApiRequestError,
    LeetCodeApiUnexpectedError,
    LeetCodeProblemNotFoundError,
)
from app.domain.shared.leetcode.models import (
    LeetCodeProblem,
    LeetCodeProblemDetails,
    LeetCodeProblemSlug,
)
from app.infrastructure.config.config import config


class AlfaLCGetProblemDetailsAdapter(GetProblemDetailsPort):

    def __init__(self):
        if not config.LEETCODE_API_BASE_URL:
            raise LeetCodeApiError("LEETCODE_API_BASE_URL is not set in configuration")
        
        self.base_url = config.LEETCODE_API_BASE_URL.rstrip("/")
        self.get_problem_details_endpoint = f"{self.base_url}/select"
        self.timeout = config.LEETCODE_API_TIMEOUT

    @override
    @functools.lru_cache(maxsize=40)
    def get_problem_details(self, problem: LeetCodeProblem) -> LeetCodeProblemDetails:
        converter = self.__prepare_converter()
        try:
            payload = {"titleSlug": problem.question_slug.question_slug}
            response = requests.get(
                self.get_problem_details_endpoint,
                params=payload,
                timeout=self.timeout,
            )
            
            if response.status_code != 200:
                raise LeetCodeApiRequestError(
                    endpoint=self.get_problem_details_endpoint,
                    question_slug=problem.question_slug.question_slug,
                    status_code=response.status_code,
                    response_text=response.text,
                )
            
            return converter.structure(response.json(), LeetCodeProblemDetails)
        
        except LeetCodeApiRequestError:
            raise
        except Exception as e:
            raise LeetCodeApiUnexpectedError(
                endpoint=self.get_problem_details_endpoint,
                question_slug=problem.question_slug.question_slug,
                original_exception=e,
            )

    def __prepare_converter(self) -> Converter:
        converter = Converter()
        converter.register_structure_hook(
            LeetCodeProblemDetails,
            lambda dct, _: LeetCodeProblemDetails(
                question_slug=dct["titleSlug"],
                question_title=dct["questionTitle"],
                question_content=dct["question"],
                example_testcases=dct["exampleTestcases"],
                difficulty=dct["difficulty"],
            ),
        )
        return converter

class SimpleQuestionSlugExtractorAdapter(QuestionSlugExtractorPort):

    def extract_question_slug(self, user_input: str) -> LeetCodeProblemSlug:
        """
        Extract and normalize a LeetCode question slug from user input.

        Args:
            user_input: Raw user input (e.g., "two-sum", "1. Two Sum", "leetcode 1 two sum").

        Returns:
            LeetCodeProblemSlug instance.

        Raises:
            LeetCodeProblemNotFoundError: If input is empty or invalid.
        """
        if not user_input or user_input.strip() == "":
            raise LeetCodeProblemNotFoundError()
        cleaned = user_input.strip().lower()
        cleaned = re.sub(r"^(leetcode\s*)?(\d+\.?\s*)?", "", cleaned)
        cleaned = re.sub(r"\s*(problem|question)\s*$", "", cleaned)
        slug = re.sub(r"[^\w\s-]", "", cleaned)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = re.sub(r"-+", "-", slug).strip("-")
        
        try:
            return LeetCodeProblem.of(slug)
        except ValueError as e:
            raise LeetCodeProblemNotFoundError(question_slug=slug)