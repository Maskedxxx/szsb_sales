"""
Основной сервис Tool Calling - координатор всей логики.

Предоставляет единую точку входа для обработки запросов
с использованием Tool Calling для различных отраслей.
"""

from typing import Dict, Any, Optional
import logging

from .registry import HandlerRegistry
from .base.types import ToolCallResult

class ToolService:
    """
    Главный сервис Tool Calling.
    
    Координирует работу хендлеров различных отраслей,
    предоставляя единый интерфейс для интеграции в engine.py.
    """
    
    def __init__(self, llm_service: Optional[Any] = None):
        """
        Инициализация сервиса с автоматической регистрацией хендлеров.
        
        Args:
            llm_service: Сервис для вызова LLM (например, OpenAI client)
        """
        self.registry = HandlerRegistry()
        self.logger = logging.getLogger("tool_calling.service")
        self.llm_service = llm_service
        
        # Автоматическая регистрация доступных хендлеров
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """
        Регистрирует все доступные хендлеры отраслей.
        
        При добавлении новых отраслей, импорты и регистрация
        добавляются здесь.
        """
        try:
            # Импорт и регистрация HoReCa хендлера
            from .horeca.service import HoReCaHandler
            self.registry.register_handler("01", HoReCaHandler("01", llm_service=self.llm_service))
            self.logger.info("HoReCa хендлер зарегистрирован")
            
            # Импорт и регистрация Milk хендлера
            from .milk.service import MilkHandler
            self.registry.register_handler("04", MilkHandler("04", llm_service=self.llm_service))
            self.logger.info("Milk хендлер зарегистрирован")
            
            # Здесь будут добавляться новые отрасли:
            # from .fat_oil.service import FatOilHandler
            # self.registry.register_handler("02", FatOilHandler("02", llm_service=self.llm_service))
            # from .confectionery.service import ConfectioneryHandler
            # self.registry.register_handler("03", ConfectioneryHandler("03", llm_service=self.llm_service))
            
        except ImportError as e:
            self.logger.warning(f"Не удалось загрузить некоторые хендлеры: {e}")
    
    def process_query(
        self, 
        subsector_id: str, 
        query: str, 
        data: Dict[str, Any], 
        selected_key: str
    ) -> ToolCallResult:
        """
        Обрабатывает запрос с использованием Tool Calling.
        
        Args:
            subsector_id: Идентификатор подсектора (например, "01" для HoReCa)
            query: Пользовательский запрос
            data: Данные отрасли для обработки
            selected_key: Выбранный ключ данных для фокусировки
            
        Returns:
            Результат обработки с отфильтрованными данными или исходными данными
        """
        self.logger.info(f"Обработка запроса для отрасли {subsector_id}")
        
        # Получаем хендлер для отрасли
        handler = self.registry.get_handler(subsector_id)
        
        if not handler:
            self.logger.info(f"Tool Calling не поддерживается для отрасли {subsector_id}")
            # Возвращаем исходные данные без изменений
            return ToolCallResult(
                success=False,
                filtered_data=data,
                applied_filters={},
                error_message=f"Tool Calling не поддерживается для отрасли {subsector_id}",
                metadata={
                    "subsector_id": subsector_id,
                    "fallback": True
                }
            )
        
        # Выполняем обработку через соответствующий хендлер
        try:
            result = handler.process(query, data, selected_key)
            self.logger.info(f"Обработка завершена. Успех: {result.success}")
            return result
            
        except Exception as e:
            self.logger.error(f"Критическая ошибка в Tool Calling: {str(e)}")
            # Graceful fallback - возвращаем исходные данные
            return ToolCallResult(
                success=False,
                filtered_data=data,
                applied_filters={},
                error_message=f"Критическая ошибка: {str(e)}",
                metadata={
                    "subsector_id": subsector_id,
                    "fallback": True,
                    "critical_error": True
                }
            )
    
    def is_supported(self, subsector_id: str) -> bool:
        """
        Проверяет, поддерживается ли Tool Calling для отрасли.
        
        Args:
            subsector_id: Идентификатор подсектора
            
        Returns:
            True, если отрасль поддерживается
        """
        return self.registry.is_supported(subsector_id)
    
    def get_supported_subsectors(self) -> list[str]:
        """
        Возвращает список отраслей с поддержкой Tool Calling.
        
        Returns:
            Список идентификаторов поддерживаемых подсекторов
        """
        return self.registry.get_supported_subsectors()