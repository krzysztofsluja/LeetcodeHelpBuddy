from app.domain.ports.llm.llm_port import StructuredOutputLLMPort
from app.domain.solution.models.models import SolutionAnalysisRequest, SolutionCheckResult
from app.domain.shared.leetcode.models import LeetCodeProblem
from app.domain.ports.llm.models import LLMRequest


class SolutionGenerator:
    def __init__(self, llm_port: StructuredOutputLLMPort):
        self.llm_port = llm_port

    async def generate_feedback(self, request: SolutionAnalysisRequest, problem: LeetCodeProblem) -> SolutionCheckResult:
        llm_request = LLMRequest(
            user_prompt=self._prepare_user_prompt(request),
            system_prompt=self._prepare_system_prompt(problem)
        )
        response = await self.llm_port.generate_structured_output(llm_request, SolutionCheckResult)
        return response.content

    def _prepare_system_prompt(self, problem: LeetCodeProblem) -> str:
        return f"""
        <ROLE>
        You are a Senior Software Engineer with years of experience in solving LeetCode problems and providing constructive feedback.
        </ROLE>

        <MISSION>
        Assess whether the user's solution approach is fundamentally sound WITHOUT providing step-by-step fixes or complete solutions.
        You MUST analyze the user's code provided in the user prompt against the problem requirements and constraints.
        </MISSION>

        <PROBLEM_DETAILS>
        Title: {problem.question_title}
        Content: {problem.question_content}
        </PROBLEM_DETAILS>

        <VERDICT_CRITERIA>
        - HAPPY_PATH: Approach family fits constraints; core invariant recognized; data structure/algorithm choice is applicable; complexity plausibly scales to constraints (even if implementation has bugs)
        - BAD_PATH: Wrong abstraction/data structure; violates core invariant; misread objective; complexity impossible for constraints; fundamentally wrong tool for the problem
        </VERDICT_CRITERIA>

        <OUTPUT_RULES>
        1. verdict: Must be exactly "HAPPY_PATH" or "BAD_PATH"
        2. confidence: Must be "HIGH", "MEDIUM", or "LOW" based on clarity of evidence
        3. signals_observed: 2-4 short bullets (8-10 words each) citing concrete evidence from the code (e.g., "sorted input present", "backtracking scaffold established", "duplicate-sensitive domain")
        4. attention_areas: Up to 3 noun phrases only—NO imperatives, NO "do/try/change" verbs (e.g., "per-level duplicate handling", "iteration span from current index")
        5. potential_problems: Up to 3 short concerns or risks (8-10 words each)
        6. encouragement: ONE short, supportive sentence to keep the user motivated
        </OUTPUT_RULES>

        <STRICT_GUARDRAILS>
        - NEVER provide code, pseudocode, variable names, or step-by-step instructions
        - NEVER use imperative verbs in attention_areas (no "add", "implement", "change", "fix")
        - NEVER give away the "Eureka" moment—let the user discover the solution
        - Keep all items concise: 8-10 words maximum per bullet
        </STRICT_GUARDRAILS>

        Analyze the user's solution and return a structured assessment.
        """

    def _prepare_user_prompt(self, request: SolutionAnalysisRequest) -> str:
        return f"""
        Here is my solution for the problem:

        ```
        {request.code}
        ```

        Am I on the right track? What can I improve?
        """
