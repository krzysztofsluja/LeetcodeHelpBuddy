from app.features.testcase.v1.generator.generator import TestCaseGenerator
from app.features.testcase.v1.models.models import TestCaseGenerationRequest, TestCaseGenerationResponse
from app.features.testcase.v1.generator.generator import SupportedLLMProvider


class TestCaseGenerationService:

    def __init__(self):
        self.generator = TestCaseGenerator(model_name="gpt-4o-mini-2024-07-18", provider=SupportedLLMProvider.OPENAI)

    async def handleRequest(self, request: TestCaseGenerationRequest) -> TestCaseGenerationResponse:
        print(f"Generating test cases for request: {request}")
        return await self.generator.generate_test_cases(request)