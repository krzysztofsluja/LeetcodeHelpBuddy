from abc import ABC, abstractmethod
from app.domain.shared.leetcode.models import LeetCodeProblem, LeetCodeProblemDetails

class GetProblemDetailsPort(ABC):
    @abstractmethod
    def get_by_question_slug(self, question_slug: LeetCodeProblem) -> LeetCodeProblemDetails: 
        """
        Fetches problem details by its title slug.

        Args:
            question_slug: The title slug of the problem.

        Returns:
            A LeetCodeProblemDetails object containing the details.

        Raises:
            LeetCodeProblemNotFoundError: If the problem cannot be found.
            LeetCodeApiError: For other API-related errors.
        """
        raise NotImplementedError
