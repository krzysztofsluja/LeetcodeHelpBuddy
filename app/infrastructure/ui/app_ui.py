import asyncio
import json
import logging
import traceback
from typing import Optional

import gradio as gr

from app.domain.testcase.models.models import Difficulty, difficulty_description
from app.infrastructure.factories.service_factory import ServiceFactory
from app.domain.shared.exception.base import BaseApplicationException

logger = logging.getLogger(__name__)


def create_gradio_interface() -> gr.Blocks:
    
    # Initialize the service
    test_case_service = ServiceFactory.create_test_case_service()
    
    async def handle_generate_test_cases(
        problem_text: str, 
        difficulty_str: str
    ) -> str:
        """Handle test case generation with comprehensive error handling."""
        try:
            if not problem_text or problem_text.strip() == "":
                return "❌ **Error**: Please enter a problem statement."
            
            try:
                difficulty = Difficulty(difficulty_str)
            except ValueError:
                return f"❌ **Error**: Invalid difficulty level: {difficulty_str}"

            response = await test_case_service.generate_test_cases(
                user_input=problem_text,
                difficulty=difficulty,
                num_test_cases=1
            )
            
            result = f"## ✅ Test Cases Generated for: {response.question_slug}\n\n"
            
            for i, test_case in enumerate(response.test_cases.test_cases, 1):
                edge_indicator = "🔥 **Edge Case**" if test_case.is_edge_case else "📝 **Test Case**"
                result += f"### {edge_indicator} #{i}\n"
                result += f"**Input:** `{test_case.test_case_content}`\n"
                result += f"**Expected Output:** `{test_case.expected_result}`\n\n"
            
            return result
            
        except BaseApplicationException as e:
            logger.error(
                "An application error occurred: %s",
                e,
                exc_info=True,
                extra={"context": e.context},
            )
            return f"❌ **Error**: {str(e)}"
        except Exception as e:
            logger.critical(
                "An unexpected error occurred: %s", e, exc_info=True
            )
            error_details = traceback.format_exc()
            return f"❌ **Unexpected Error**: {str(e)}\n\n```\n{error_details}\n```"
    
    def handle_clear() -> tuple[str, str]:
        """Clear all inputs and outputs."""
        return "", ""

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

    with gr.Blocks(
        title="LeetCode Help Buddy",
        css=custom_css,
        theme=gr.themes.Soft(),
    ) as interface:
        gr.Markdown( 
            """
            # 🚀 LeetCode Help Buddy
            
            **Generate high-quality test cases** from problem constraints and examples, or get **progressive hints** to understand problems better.
            
            **Integrity Mode**: We provide hints and test cases, not full solutions.
            """
        )

        with gr.Row(elem_classes=["main-container"]):
            with gr.Column():
                problem_input = gr.Textbox(
                    label="Problem Statement",
                    placeholder="Paste your LeetCode problem here.",
                    lines=12,
                    max_lines=20,
                    interactive=True,
                )

                with gr.Row(elem_classes=["button-row"]):
                    """generate_btn = gr.Button(
                        "🎯 Generate Tests",
                        variant="primary",
                        size="lg",
                        scale=1,
                    )"""
                    options_dropdown = gr.Dropdown(
                        label="Select an operation",
                        choices=["GENERATE TEST CASES"],
                        value="GENERATE TEST CASES",
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
            
                difficulty_choices = []
                difficulty_info = {}
                for difficulty in Difficulty:
                    choice_label = f"{difficulty.value.upper()}"
                    difficulty_choices.append(choice_label)
                    difficulty_info[choice_label] = difficulty_description[difficulty].strip()
                
                difficulty_radio = gr.Radio(
                    label="Test Case Difficulty Level",
                    choices=difficulty_choices,
                    value=Difficulty.EASY.value.upper(),
                    info="Select the difficulty level for test case generation"
                )
            
                with gr.Column(elem_classes=["results-container"]):
                    gr.Markdown("### Results")
                    
                    with gr.Row():
                        test_results = gr.Textbox(
                            label="LeetBuddy's Response",
                            lines=10,
                            max_lines=20,
                            interactive=False
                        )
        
        # Wire up event handlers
        send_btn.click(
            fn=handle_generate_test_cases,
            inputs=[problem_input, difficulty_radio],
            outputs=[test_results],
            show_progress=True
        )
        
        clear_btn.click(
            fn=handle_clear,
            inputs=[],
            outputs=[problem_input, test_results],
            show_progress=False
        )
    
    return interface