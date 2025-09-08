"""
Gradio UI for LeetCode Help Buddy

This module creates the Gradio Blocks interface with:
- Large text input for problem statements
- Generate Tests button for test case generation
- Explain button for problem explanation with streaming
- Results panel and clarifier messages
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, Generator, Optional, Tuple
from app.features.models import Feature
from app.features.router.feature_router import dispatch

import gradio as gr

from app.features.testcase.v1.models.models import TestCaseGenerationRequest
from app.ui.formatters.testcase.testcase_formatter import TestCaseFormatter

def create_gradio_interface() -> gr.Blocks:
    """Create the main Gradio interface using Blocks layout."""
    
    # Feature display names mapping
    FEATURE_DISPLAY_NAMES = {
        Feature.TEST_CASE_GENERATION: "GENERATE TEST CASES"
    }
    
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

    DEFAULT_OPERATION = Feature.TEST_CASE_GENERATION
    
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
                        choices=list(FEATURE_DISPLAY_NAMES.values()),
                        value=FEATURE_DISPLAY_NAMES[DEFAULT_OPERATION],
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
                
                # Difficulty selector (only visible for test case generation)
                from app.features.testcase.v1.models.models import Difficulty, difficulty_description
                
                # Create difficulty choices with descriptions
                difficulty_choices = []
                difficulty_info = {}
                for difficulty in Difficulty:
                    choice_label = f"{difficulty.value.upper()}"
                    difficulty_choices.append(choice_label)
                    difficulty_info[choice_label] = difficulty_description[difficulty].strip()
                
                difficulty_radio = gr.Radio(
                    label="Test Case Difficulty Level",
                    choices=difficulty_choices,
                    value=Difficulty.EASY.value.upper(),  # Default to EASY (single value, not list)
                    visible=(DEFAULT_OPERATION == Feature.TEST_CASE_GENERATION),
                    info="Select the difficulty level for test case generation"
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
        def handle_generate_tests(problem_input: str, statement: str, difficulty: str) -> Tuple[Any, str, str]:
            """Handle test generation request."""
            request = TestCaseGenerationRequest(
                user_message=problem_input,
                difficulty=difficulty
            )
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            response = loop.run_until_complete(dispatch(Feature.TEST_CASE_GENERATION, request))
            return (
                problem_input,
                TestCaseFormatter.format_testcase(response),
                "",
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
        
        def handle_send(problem_input: str, operation: str, difficulty: str) -> Tuple[str, Any, str]:
            """Send the problem statement to the server."""
            # Convert display name back to Feature
            feature_map = {v: k for k, v in FEATURE_DISPLAY_NAMES.items()}
            selected_feature = feature_map.get(operation)
            
            match selected_feature:
                case Feature.TEST_CASE_GENERATION:
                    print(f"Sending request to generate test cases: {problem_input, operation, difficulty}")
                    return handle_generate_tests(problem_input, operation, difficulty)
                case _:
                    return (problem_input, "There's nothing to show here :(", "")
        
        
        def toggle_difficulty_visibility(operation: str) -> gr.Radio:
            """Toggle visibility of difficulty radio buttons based on selected operation."""
            return gr.Radio(visible=(operation == FEATURE_DISPLAY_NAMES[Feature.TEST_CASE_GENERATION]))
        
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
            inputs=[problem_input, options_dropdown, difficulty_radio],
            outputs=[
                problem_input,
                test_results,
                clarifier_msg,
            ],
        )
        
        # Toggle difficulty radio visibility when operation changes
        options_dropdown.change(
            fn=toggle_difficulty_visibility,
            inputs=[options_dropdown],
            outputs=[difficulty_radio],
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
