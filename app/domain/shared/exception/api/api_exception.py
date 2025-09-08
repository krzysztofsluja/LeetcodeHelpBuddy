class LeetCodeApiError(Exception):
    """Base exception for LeetCode API interactions."""
    pass


class LeetCodeProblemNotFoundError(LeetCodeApiError):
    """Raised when a specific problem slug is not found."""
    def __init__(self, question_slug: str):
        self.question_slug = question_slug
        super().__init__(f"Problem with slug '{question_slug}' not found.")