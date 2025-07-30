"""
Общие типы и структуры данных для Tool Calling системы.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class ToolCallResult:
    """Результат выполнения Tool Calling."""
    
    success: bool
    filtered_data: Dict[str, Any]
    applied_filters: Dict[str, Any]
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class FilterParameters:
    """Параметры фильтрации, извлеченные из LLM ответа."""
    
    tool_name: str
    parameters: Dict[str, Any]
    confidence: Optional[float] = None


@dataclass
class ToolSchema:
    """Схема инструмента для OpenAI."""
    
    type: str
    function: Dict[str, Any]