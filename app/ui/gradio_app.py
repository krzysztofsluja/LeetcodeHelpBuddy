"""
Gradio UI for LeetCode Help Buddy

This module creates the Gradio Blocks interface with:
- Large text input for problem statements
- Generate Tests button for test case generation
- Explain button for problem explanation with streaming
- Results panel and clarifier messages
"""

from __future__ import annotations

import json
from typing import Any, Dict, Generator, Optional, Tuple
from enum import Enum

import gradio as gr

class Operation(Enum):
    GENERATE_TESTS = "GENERATE TESTS CASES"
    EXPLAIN_PROBLEM = "EXPLAIN PROBLEM"

def create_gradio_interface() -> gr.Blocks:
    """Create the main Gradio interface using Blocks layout."""
    
    # Custom CSS for better styling
    custom_css = """
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .button-row {
        display: flex;
        gap: 10px;
        margin: 10px 0;
    }
    .results-container {
        margin-top: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
    }
    .clarifier-message {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        padding: 10px;
        margin: 10px 0;
        color: #856404;
    }
    """

    DEFAULT_OPERATION = Operation.GENERATE_TESTS
    
    with gr.Blocks(
        title="LeetCode Help Buddy",
        css=custom_css,
        theme=gr.themes.Soft(),
    ) as interface:
        
        # Header
        gr.Markdown(
            """
            # 🚀 LeetCode Help Buddy
            
            **Generate high-quality test cases** from problem constraints and examples, or get **progressive hints** to understand problems better.
            
            **Integrity Mode**: We provide hints and test cases, not full solutions.
            """
        )
        
        with gr.Row(elem_classes=["main-container"]):
            with gr.Column():
                # Main input area
                problem_input = gr.Textbox(
                    label="Problem Statement",
                    placeholder="""Paste your LeetCode problem here. For test generation, make sure to include:

1. **Constraints** (e.g., "1 ≤ n ≤ 10^5", "-10^9 ≤ nums[i] ≤ 10^9")
2. **Examples** with input/output pairs

For explanations, just paste the problem statement and click 'Explain'.""",
                    lines=12,
                    max_lines=20,
                    interactive=True,
                )
                
                # Button row
                with gr.Row(elem_classes=["button-row"]):
                    """generate_btn = gr.Button(
                        "🎯 Generate Tests",
                        variant="primary",
                        size="lg",
                        scale=1,
                    )
                    explain_btn = gr.Button(
                        "💡 Explain Problem", 
                        variant="secondary",
                        size="lg",
                        scale=1,
                    )"""
                    options_dropdown = gr.Dropdown(
                        label="Select an operation",
                        choices=[Operation.GENERATE_TESTS.value, Operation.EXPLAIN_PROBLEM.value],
                        value=DEFAULT_OPERATION.value,
                        interactive=True,
                    )
                    with gr.Column():
                        clear_btn = gr.Button(
                            "🗑️ Clear",
                            size="lg",
                            scale=0,
                        )
                        send_btn = gr.Button(
                            "🔍 Send",
                            size="lg",
                            scale=0,
                        )
                
                # Clarifier message area (initially hidden)
                clarifier_msg = gr.Markdown(
                    visible=False,
                    elem_classes=["clarifier-message"],
                )
                
                # Results area
                with gr.Column(elem_classes=["results-container"]):
                    gr.Markdown("### Results")
                    
                    with gr.Row():
                        test_results = gr.Textbox(
                            label="LeetBuddy's Response",
                            lines=10,
                            max_lines=20,
                            interactive=False
                        )
        
        # Event handlers
        def handle_generate_tests(problem_input: str, statement: str) -> Tuple[Any, str, str]:
            """Handle test generation request."""
            if not statement.strip():
                return (
                    None,
                    "Please enter a problem statement first.",
                    """
                    ⚠️ **Missing Input**: Please paste a problem statement with **Constraints** and **Examples**.
                    
                    Example format:
                    ```
                    Constraints:
                    • 1 ≤ n ≤ 10^5
                    • -10^9 ≤ nums[i] ≤ 10^9
                    
                    Example 1:
                    Input: nums = [2,7,11,15], target = 9
                    Output: [0,1]
                    ```
                    """,
                )
            
            # For now, return a placeholder response
            # This will be replaced with actual parser and generator logic
            sample_tests = {
                "generated_cases": [
                    {
                        "input": {"nums": [1], "target": 1},
                        "tags": ["boundary", "min_length"]
                    },
                    {
                        "input": {"nums": [1, 2], "target": 3},
                        "tags": ["boundary", "small_case"]
                    },
                    {
                        "input": {"nums": [-1000000000, 1000000000], "target": 0},
                        "tags": ["boundary", "extreme_values"]
                    }
                ],
                "metadata": {
                    "total_cases": 3,
                    "generation_time_ms": 42
                }
            }
            
            summary = f"""
            ✅ **Generated {len(sample_tests['generated_cases'])} test cases**
            
            **Coverage:**
            - Boundary cases: 3
            - Edge cases: 2
            - Random cases: 1
            
            **Tags used:** `boundary`, `min_length`, `small_case`, `extreme_values`
            """
            
            return (
                problem_input,
                summary,
                "",  # Clear clarifier message on success
            )
        
        def handle_explain_problem(statement: str) -> str:
            """Handle problem explanation request."""
            if not statement.strip():
                return "Please enter a problem statement to explain."
            
            # Placeholder explanation - will be replaced with actual LLM integration
            return f"""
            ## 🔍 Problem Analysis
            
            **Restatement:** Based on your input, this appears to be a problem involving finding pairs or elements that satisfy certain conditions.
            
            **Input/Output Shapes:**
            - Input: Array of integers, target value
            - Output: Indices or values that satisfy the condition
            
            **Key Constraints:**
            - Array size and element ranges will affect algorithm choice
            - Consider time/space complexity trade-offs
            
            **Progressive Hints:**
            
            **💡 Hint 1 (Gentle):** Think about what complementary values you need to find the target.
            
            **💡 Hint 2 (Intermediate):** Can you trade space for time? What data structure helps with fast lookups?
            
            **💡 Hint 3 (Stronger):** Consider scanning the array once while maintaining a lookup structure for complements.
            
            **Common Edge Cases:**
            - Empty array or single element
            - Duplicate elements
            - No valid solution exists
            - Multiple valid solutions
            """
        
        def handle_clear() -> Tuple[str, Any, str]:
            """Clear all inputs and outputs."""
            return (
                "",  # problem_input
                None,  # test_results
                "",  # clarifier_msg
            )
        
        def handle_send(problem_input: str, operation: str) -> Tuple[str, Any, str]:
            """Send the problem statement to the server."""
            match operation:
                case Operation.GENERATE_TESTS.value:
                    return handle_generate_tests(problem_input, operation)
                case _:
                    return (problem_input, "There's nothing to show here :(", "")
        
        
        clear_btn.click(
            fn=handle_clear,
            outputs=[
                problem_input,
                test_results,
                clarifier_msg,
            ],
        )

        send_btn.click(
            fn=handle_send,
            inputs=[problem_input, options_dropdown],
            outputs=[
                problem_input,
                test_results,
                clarifier_msg,
            ],
        )
    
    return interface


def stream_explanation(statement: str) -> Generator[str, None, None]:
    """
    Stream explanation tokens (placeholder for actual LLM streaming).
    
    This will be replaced with actual OpenAI streaming integration.
    """
    explanation_parts = [
        "## 🔍 Problem Analysis\n\n",
        "**Restatement:** ",
        "Analyzing your problem statement...\n\n",
        "**Input/Output Shapes:**\n",
        "- Determining data types and structures...\n\n",
        "**Progressive Hints:**\n\n",
        "**💡 Hint 1:** Think about the core operation...\n\n",
        "**💡 Hint 2:** Consider algorithmic approaches...\n\n",
        "**💡 Hint 3:** Final nudge toward solution pattern...\n\n",
    ]
    
    for part in explanation_parts:
        yield part
