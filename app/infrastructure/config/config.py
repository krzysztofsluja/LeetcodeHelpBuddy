"""
Configuration module for LeetCode Help Buddy.

Loads configuration from environment variables with sensible defaults.
"""

from __future__ import annotations

import os
from typing import Optional


class Config:
    """Application configuration loaded from environment variables."""

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # LeetCode API Configuration
    LEETCODE_API_BASE_URL: str = os.getenv(
        "LEETCODE_API_BASE_URL", "http://localhost:3000"
    )
    LEETCODE_API_TIMEOUT: int = int(os.getenv("LEETCODE_API_TIMEOUT", "30"))

    # Application Configuration
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    APP_RELOAD: bool = os.getenv("APP_RELOAD", "false").lower() == "true"

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        """
        Validate required configuration values.

        Raises:
            ValueError: If required configuration is missing.
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required. Set it in your environment or .env file."
            )


# Singleton instance
config = Config()
