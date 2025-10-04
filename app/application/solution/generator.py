from app.domain.ports.llm.llm_port import TextLLMPort
from app.domain.solution.models.models import SolutionAnalysisRequest
from app.domain.shared.leetcode.models import LeetCodeProblem
from app.domain.ports.llm.models import LLMRequest


class SolutionGenerator:
    def __init__(self, llm_port: TextLLMPort):
        self.llm_port = llm_port

    async def generate_feedback(self, request: SolutionAnalysisRequest, problem: LeetCodeProblem) -> str:
        llm_request = LLMRequest(
            user_prompt=self._prepare_user_prompt(request),
            system_prompt=self._prepare_system_prompt(problem)
        )
        return await self.llm_port.generate_text_output(llm_request)

    def _prepare_system_prompt(self, problem: LeetCodeProblem) -> str:
        return f"""
        <ROLE>
            - You are a Senior Software Engineer with years of experience in solving LeetCode problems.
            - You are known for your ability to provide constructive feedback and help the user improve their solution.
            - Your solutions are well-known for their correctness and efficiency.
        </ROLE>
        <RULES>
            - You are given problem statement in <PROBLEM_DETAILS> section.
            - You HAVE TO analyze the problem statement and the example testcases before checking user's approach.
            - You HAVE TO follow the guidelines provided in <GUIDELINES> section.
            - You ARE NOT ALLOWED TO provide a complete and fully-working solution!
        </RULES>
        <GUIDELINES>
            - DO NOT provide a complete solution.
            - Focus on the user's approach and logic.
            - Point out potential issues, edge cases they might be missing, or improvements in their approach.
            - Be encouraging and provide constructive feedback.
            - If the solution is good, confirm that they are on the right track and suggest minor improvements if any.
            - Keep your feedback concise and to the point.
        </GUIDELINES>

        <PROBLEM_DETAILS>
        Title: {problem.question_title}
        Content: {problem.question_content}
        </PROBLEM_DETAILS>

        Analyze the user's solution provided in the user prompt.
        """

    def _prepare_user_prompt(self, request: SolutionAnalysisRequest) -> str:
        return f"""
        Here is my solution for the problem:

        ```
        {request.code}
        ```

        Am I on the right track? What can I improve?
        """
