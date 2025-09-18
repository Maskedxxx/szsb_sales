"""
Основной сервис Tool Calling - координатор всей логики.

Предоставляет единую точку входа для обработки запросов
с использованием Tool Calling для различных отраслей.

Обновлено для новой универсальной архитектуры с UniversalIndustryHandler.
"""

from typing import Dict, Any, Optional
import logging

from .registry import HandlerRegistry
from .base.types import ToolCallResult
from .universal_handler import UniversalIndustryHandler

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
        
        В новой архитектуре используется ТОЛЬКО UniversalIndustryHandler
        для всех поддерживаемых отраслей.
        """
        try:
            # Регистрируем универсальный хендлер для HoReCa
            handler_horeca = UniversalIndustryHandler("01", self.llm_service)
            self.registry.register_handler("01", handler_horeca)
            self.logger.info("Универсальный HoReCa хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Milk
            handler_milk = UniversalIndustryHandler("04", self.llm_service)
            self.registry.register_handler("04", handler_milk)
            self.logger.info("Универсальный Milk хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Selo
            handler_selo = UniversalIndustryHandler("00", self.llm_service)
            self.registry.register_handler("00", handler_selo)
            self.logger.info("Универсальный Selo хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Fat and Oil
            handler_fat_and_oil = UniversalIndustryHandler("03", self.llm_service)
            self.registry.register_handler("03", handler_fat_and_oil)
            self.logger.info("Универсальный Fat and Oil хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Drinks
            handler_drinks = UniversalIndustryHandler("09", self.llm_service)
            self.registry.register_handler("09", handler_drinks)
            self.logger.info("Универсальный Drinks хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Semi-finished
            handler_semi_finished = UniversalIndustryHandler("02", self.llm_service)
            self.registry.register_handler("02", handler_semi_finished)
            self.logger.info("Универсальный Semi-finished хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Meat
            handler_meat = UniversalIndustryHandler("08", self.llm_service)
            self.registry.register_handler("08", handler_meat)
            self.logger.info("Универсальный Meat хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Bakery
            handler_bakery = UniversalIndustryHandler("07", self.llm_service)
            self.registry.register_handler("07", handler_bakery)
            self.logger.info("Универсальный Bakery хендлер зарегистрирован")
            
            # Регистрируем универсальный хендлер для Ice Cream
            handler_ice_cream = UniversalIndustryHandler("05", self.llm_service)
            self.registry.register_handler("05", handler_ice_cream)
            self.logger.info("Универсальный Ice Cream хендлер зарегистрирован")
            
        except Exception as e:
            self.logger.error(f"Ошибка регистрации универсальных хендлеров: {e}")
            self.logger.warning("Будет использован fallback режим")
    
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
