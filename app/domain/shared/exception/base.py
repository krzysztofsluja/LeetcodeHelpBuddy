from abc import ABC
from typing import Any, Dict, Optional


class BaseApplicationException(Exception, ABC):
    """Base exception for the application."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
