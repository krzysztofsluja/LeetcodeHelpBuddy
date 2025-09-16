from abc import ABC
from typing import Any, Dict, Optional
from app.domain.shared.exception.base import BaseApplicationException


class TestCaseException(BaseApplicationException, ABC):
    """Base exception for test case operations."""

    def __init__(self, message: str = "An error occurred during test case processing."):
        super().__init__(message)


class TestCaseNotGeneratedException(TestCaseException):
    """Raised when test cases are not generated."""

    def __init__(self, message: str = "Could not generate test cases."):
        super().__init__(message)