from app.domain.ports.llm.llm_port import TextLLMPort
from app.domain.ports.llm.models import LLMRequest
from app.domain.explain.models.models import ExplainProblemStatementRequest, ExplainProblemStatementResponse


class ProblemStatementExplainer:
    def __init__(self, llm_port: TextLLMPort):
        self.llm_port = llm_port

    async def explain_problem_statement(self, request: ExplainProblemStatementRequest) -> ExplainProblemStatementResponse:
        llm_request = LLMRequest(
            user_prompt=self.__prepare_user_prompt(request),
            system_prompt=self.__prepare_system_prompt(request)
        )
        response = await self.llm_port.generate_text_output(llm_request)
        return ExplainProblemStatementResponse(
            question_slug=request.problem_statement.question_slug,
            explaination=response
        )
    
    def __prepare_system_prompt(self, request: ExplainProblemStatementRequest) -> str:
        return f"""
        You are an expert teacher with several years of experience who explains the LeetCode problem statement and makes it easy to understand.
        You HAVE TO understand that very often the statement is complex and can lead to incorrect solution and approach.
        Your task is to explain the problem statement in a way that is easy to understand and helps the user to understand what he has to do.
        Explain the problem like you are explaining to a beginner or 5 - year old child.
        <GUIDELINES>
            - YOU ARE NOT ALLOWED to provide any code or solution to the problem.
            - YOU ARE NOT ALLOWED TO go beyond the borders of the problem
            - YOU HAVE TO focus on the problem statement provided in <PROBLEM_STATEMENT> section.
            - YOU HAVE TO take into account the edge cases and the constraints provided within the problem statement.
        </GUIDELINES>
        <OUTPUT_FORMAT>
            - Provide simple explaination in plain text
            - YOU ARE NOT ALLOWED to provide any code or solution to the problem.
        </OUTPUT_FORMAT>
        <PROBLEM_STATEMENT>
        {request.problem_statement.question_content}
        </PROBLEM_STATEMENT>
        """

    def __prepare_user_prompt(self, request: ExplainProblemStatementRequest) -> str:
        return f"""
        Explain the problem statement like you are explaining to a beginner or 5 - year old child.
        """
        