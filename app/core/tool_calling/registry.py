"""
Реестр хендлеров Tool Calling для различных отраслей.

Управляет регистрацией и получением хендлеров по subsector_id.
"""

from typing import Dict, Optional
import logging

from .base import BaseToolHandler


class HandlerRegistry:
    """
    Реестр хендлеров Tool Calling.
    
    Хранит и управляет хендлерами для различных отраслей,
    позволяя легко добавлять новые и получать существующие.
    """
    
    def __init__(self):
        """Инициализация пустого реестра."""
        self._handlers: Dict[str, BaseToolHandler] = {}
        self.logger = logging.getLogger("tool_calling.registry")
    
    def register_handler(self, subsector_id: str, handler: BaseToolHandler) -> None:
        """
        Регистрирует хендлер для отрасли.
        
        Args:
            subsector_id: Идентификатор подсектора
            handler: Экземпляр хендлера для данной отрасли
        """
        self._handlers[subsector_id] = handler
        self.logger.info(f"Зарегистрирован хендлер для отрасли {subsector_id}")
    
    def get_handler(self, subsector_id: str) -> Optional[BaseToolHandler]:
        """
        Получает хендлер для отрасли.
        
        Args:
            subsector_id: Идентификатор подсектора
            
        Returns:
            Хендлер для отрасли или None, если не найден
        """
        handler = self._handlers.get(subsector_id)
        if not handler:
            self.logger.debug(f"Хендлер для отрасли {subsector_id} не найден")
        return handler
    
    def is_supported(self, subsector_id: str) -> bool:
        """
        Проверяет, поддерживается ли отрасль.
        
        Args:
            subsector_id: Идентификатор подсектора
            
        Returns:
            True, если отрасль поддерживается
        """
        return subsector_id in self._handlers
    
    def get_supported_subsectors(self) -> list[str]:
        """
        Возвращает список поддерживаемых отраслей.
        
        Returns:
            Список идентификаторов поддерживаемых подсекторов
        """
        return list(self._handlers.keys())