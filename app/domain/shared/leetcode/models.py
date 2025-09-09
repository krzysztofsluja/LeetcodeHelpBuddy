from dataclasses import dataclass
import re


@dataclass(frozen=True)
class LeetCodeProblemSlug:
    question_slug: str

    def __post_init__(self) -> None:
        if not self.question_slug or self.question_slug.strip() == "":
            raise ValueError("Question slug cannot be empty")
        if not re.fullmatch(r"[a-z-]+", self.question_slug) or re.fullmatch(r"-+", self.question_slug):
            raise ValueError("Question slug must contain only lowercase letters and underscores")

    @classmethod
    def of(cls, question_slug: str) -> "LeetCodeProblemSlug":
        return LeetCodeProblemSlug(question_slug=question_slug)

@dataclass(frozen=True)
class LeetCodeProblem:
    question_slug: LeetCodeProblemSlug

@dataclass(frozen=True)
class LeetCodeProblemDetails:
    question_slug: str
    question_title: str
    question_content: str
    example_testcases: str
    difficulty: str