from pydantic import BaseModel, Field


class SolutionAnalysisRequest(BaseModel):
    title: str = Field(..., description="The title of the LeetCode problem.")
    code: str = Field(..., description="The user's solution code.")


class SolutionAnalysisResponse(BaseModel):
    feedback: str = Field(..., description="Feedback on the user's solution.")
