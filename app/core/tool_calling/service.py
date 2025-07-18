"""
Универсальный сервис для Tool Calling.

Предоставляет единый интерфейс для работы с Tool Calling в различных отраслях.
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from .adapters import LLMAdapter

logger = logging.getLogger(__name__)


@dataclass
class ToolCallResult:
    """Результат выполнения tool calling."""
    success: bool
    subsector: Optional[str] = None
    selected_tool: Optional[str] = None
    tool_parameters: Optional[Dict[str, Any]] = None
    filtered_data: Optional[List[str]] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None


class ToolService:
    """
    Универсальный сервис для Tool Calling.
    
    Обеспечивает единый интерфейс для работы с tool calling в различных отраслях.
    Автоматически определяет подходящий обработчик на основе subsector_id.
    """
    
    def __init__(self, llm_adapter: LLMAdapter):
        """
        Инициализация сервиса.
        
        Args:
            llm_adapter: Адаптер для работы с LLM
        """
        self.llm_adapter = llm_adapter
        self._subsector_handlers = {}
        logger.info("Инициализирован универсальный ToolService")
    
    def register_subsector(self, subsector_id: str, handler):
        """
        Регистрирует обработчик для конкретной отрасли.
        
        Args:
            subsector_id: ID отрасли (например, "01" для HoReCa)
            handler: Обработчик отрасли
        """
        self._subsector_handlers[subsector_id] = handler
        logger.info(f"Зарегистрирован обработчик для отрасли: {subsector_id}")
    
    def is_supported(self, subsector_id: str) -> bool:
        """
        Проверяет, поддерживается ли tool calling для данной отрасли.
        
        Args:
            subsector_id: ID отрасли
            
        Returns:
            True если поддерживается, False иначе
        """
        return subsector_id in self._subsector_handlers
    
    def process_query(
        self, 
        query: str, 
        subsector_id: str,
        file_name: str, 
        data: Dict[str, Any]
    ) -> ToolCallResult:
        """
        Обрабатывает запрос пользователя через tool calling.
        
        Args:
            query: Запрос пользователя
            subsector_id: ID отрасли
            file_name: Имя файла данных
            data: Данные для обработки
            
        Returns:
            Результат обработки
        """
        start_time = time.time()
        
        logger.info(f"Обработка запроса для отрасли {subsector_id}: {query}")
        
        try:
            # Проверяем поддержку отрасли
            if not self.is_supported(subsector_id):
                return ToolCallResult(
                    success=False,
                    subsector=subsector_id,
                    error_message=f"Tool calling не поддерживается для отрасли {subsector_id}",
                    execution_time=time.time() - start_time
                )
            
            # Получаем обработчик отрасли
            handler = self._subsector_handlers[subsector_id]
            
            # Выполняем обработку
            result = handler.process_query(
                query=query,
                file_name=file_name,
                data=data,
                llm_adapter=self.llm_adapter
            )
            
            # Добавляем метаданные
            result.subsector = subsector_id
            result.execution_time = time.time() - start_time
            
            logger.info(f"Обработка завершена за {result.execution_time:.2f}с")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Ошибка при обработке запроса: {str(e)}")
            
            return ToolCallResult(
                success=False,
                subsector=subsector_id,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def get_supported_subsectors(self) -> List[str]:
        """
        Возвращает список поддерживаемых отраслей.
        
        Returns:
            Список ID отраслей
        """
        return list(self._subsector_handlers.keys())
    
    def get_subsector_info(self, subsector_id: str) -> Dict[str, Any]:
        """
        Возвращает информацию о конкретной отрасли.
        
        Args:
            subsector_id: ID отрасли
            
        Returns:
            Словарь с информацией об отрасли
        """
        if not self.is_supported(subsector_id):
            return {"supported": False, "error": "Отрасль не поддерживается"}
        
        handler = self._subsector_handlers[subsector_id]
        
        return {
            "supported": True,
            "subsector_id": subsector_id,
            "handler_type": type(handler).__name__,
            "capabilities": getattr(handler, 'get_capabilities', lambda: [])()
        }