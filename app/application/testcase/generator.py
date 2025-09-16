
from app.domain.ports.llm.llm_port import StructuredOutputLLMPort
from app.domain.ports.llm.models import LLMRequest
from app.domain.shared.exception.testcase.testcase_exception import TestCaseNotGeneratedException
from app.domain.shared.leetcode.models import LeetCodeProblemDetails
from app.domain.testcase.models.models import Difficulty, ProblemTestCases, TestCaseGenerationRequest, TestCaseGenerationResponse, difficulty_description


class TestCaseGenerator:
    def __init__(self, llm_port: StructuredOutputLLMPort, temperature: float = 0.7):
        self.llm_port = llm_port
        self.temperature = temperature

    async def generate_test_cases(self, request: TestCaseGenerationRequest) -> TestCaseGenerationResponse:

        try:
            llm_request = LLMRequest(
              user_prompt=self.__prepare_user_prompt(request),
                system_prompt=self.__prepare_system_prompt(request.difficulty),
                temperature=self.temperature
            )

            response = await self.llm_port.generate_structured_output(llm_request, ProblemTestCases)

            return TestCaseGenerationResponse(
                question_slug=request.problem_details.question_slug,
                test_cases=response.content
            )
        except Exception as e:
            raise TestCaseNotGeneratedException()

    def __prepare_system_prompt(self, test_case_difficulty: Difficulty) -> str:
        base_prompt = """You are an expert at generating LeetCode test cases. Your task is to:

1. Identify the problem from user input 
2. Generate diverse, non-edge test cases for the specified difficulty level
3. Ensure test cases cover different scenarios but are NOT edge cases
4. Before generating test cases YOU HAVE TO analyze the problem statement and the example testcases.
5. Before generating test cases YOU HAVE TO get to know with the problem description and the constraints.

You ARE ALLOWED TO generate test cases ONLY for problems present in the LeetCode database.
You ARE NOT ALLOWED TO generate test cases for problems that are not present in the LeetCode database.

Guidelines:
- Generate NORMAL test cases only, not edge cases
- Cover different input patterns and scenarios
- Ensure expected results are correct
- Use proper input/output format for the problem type
- Make test cases progressively challenging based on difficulty
- The testcases which are included in LeetCode problem description or examples are not allowed to be generated.
- Make sure to generate testcases which give the helping hand to the user while testing his approach to solve the problem.
YOU ARE NOT ALLOWED TO GENERATE EDGE CASES."""
        
        return base_prompt + "\n" + difficulty_description[test_case_difficulty]

    def __prepare_user_prompt(self, request: TestCaseGenerationRequest) -> str:
        return f"""Generate {request.num_test_cases} test cases for the problem provided in <PROBLEM_STATEMENT> section.:
YOU ARE NOT ALLOWED TO GENERATE EDGE CASES. YOU ARE NOT ALLOWED TO GENERATE TEST CASES WHICH ARE ALREADY PRESENT IN THE PROBLEM STATEMENT - <example_testcases> section.
<PROBLEM_STATEMENT>
{request.problem_details.question_content}
</PROBLEM_STATEMENT>
<EXAMPLE_TESTCASES>
{request.problem_details.example_testcases}
</EXAMPLE_TESTCASES>
"""