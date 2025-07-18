"""
Базовые классы и интерфейсы для Tool Calling системы.

Этот модуль содержит абстрактные классы и общие типы,
которые используются всеми хендлерами отраслей.
"""

from .handler import BaseToolHandler
from .types import ToolCallResult, FilterParameters

__all__ = ["BaseToolHandler", "ToolCallResult", "FilterParameters"]