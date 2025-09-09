from abc import ABC, abstractmethod
from app.domain.shared.leetcode.models import LeetCodeProblemSlug, LeetCodeProblemDetails
from cattrs import Converter

class GetProblemDetailsPort(ABC):
    @abstractmethod
    def get_problem_details(self, converter: Converter, payload: dict) -> LeetCodeProblemDetails: 
        """
        Fetches problem details by its title slug.

        Args:
            converter: The converter to use to convert the response to a LeetCodeProblemDetails object.
            payload: The payload to use to get the problem details.

        Returns:
            A LeetCodeProblemDetails object containing the details.

        Raises:
            LeetCodeProblemNotFoundError: If the problem cannot be found.
            LeetCodeApiError: For other API-related errors.
        """
        raise NotImplementedError

class QuestionSlugExtractorPort(ABC):
    @abstractmethod
    def extract_question_slug(self, user_input: str) -> LeetCodeProblemSlug:
        """
        Extracts the question slug from a given user input.

        Args:
            user_input: The user input to extract the question slug from.

        Returns:
            A LeetCodeProblemSlug object containing the question slug.
        """
        raise NotImplementedError
