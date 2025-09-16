"""
LeetCode Help Buddy - Main FastAPI application with Gradio UI

This module sets up the FastAPI application and mounts the Gradio interface
for test case generation and problem explanation.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config.logging_config import configure_logging
from app.infrastructure.ui.app_ui import create_gradio_interface


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    configure_logging()
    print("Starting LeetCode Help Buddy...")
    load_dotenv()
    
    # Verify OpenAI API key is configured
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set. LLM features will not work.")
    
    yield
    
    # Shutdown
    print("Shutting down LeetCode Help Buddy...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="LeetCode Help Buddy",
        description="Generate test cases and explain problems without full solutions",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # CORS middleware for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create and mount Gradio interface
    gradio_app = create_gradio_interface()
    app = gr.mount_gradio_app(app, gradio_app, path="/app")
    
    @app.get("/")
    async def root():
        """Root endpoint redirect to the app."""
        return {"message": "LeetCode Help Buddy", "app_url": "/app"}
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
