from app.features.testcase.v1.models.models import TestCaseGenerationResponse


class TestCaseFormatter:

    @staticmethod
    def format_testcase(response: TestCaseGenerationResponse) -> str:
        lines = []
        for testcase in response.test_cases:
            lines.append(f"Input: {testcase.test_case}")
            lines.append(f"Expected Output: {testcase.expected_result}")
            lines.append(f"Is Edge Case: {testcase.is_edge_case}")
            lines.append("")
        return "\n".join(lines)