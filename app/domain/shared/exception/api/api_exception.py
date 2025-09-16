from abc import ABC
from typing import Any, Dict, Optional
from app.domain.shared.exception.base import BaseApplicationException


class LeetCodeApiError(BaseApplicationException, ABC):
    """Base exception for Le-etCode API interactions."""

    pass


class LeetCodeApiRequestError(LeetCodeApiError):
    """Raised when an API request fails."""

    def __init__(
        self,
        endpoint: str,
        question_slug: str,
        status_code: int,
        response_text: str,
        message: str = "Failed to fetch problem details from LeetCode API due to a request error.",
    ):
        context = {
            "endpoint": endpoint,
            "question_slug": question_slug,
            "status_code": status_code,
            "response_text": response_text,
        }
        super().__init__(message, context)


class LeetCodeApiUnexpectedError(LeetCodeApiError):
    """Raised for unexpected errors during API interaction."""

    def __init__(
        self,
        endpoint: str,
        question_slug: str,
        original_exception: Exception,
        message: str = "An unexpected error occurred while interacting with the LeetCode API.",
    ):
        context = {
            "endpoint": endpoint,
            "question_slug": question_slug,
            "original_exception": str(original_exception),
        }
        super().__init__(message, context)


class LeetCodeProblemNotFoundError(LeetCodeApiError):
    """Raised when a specific problem slug is not found."""

    def __init__(self, question_slug: str or None):
        message = f"Problem with slug '{question_slug}' not found."
        context = {"question_slug": question_slug}
        super().__init__(message, context)