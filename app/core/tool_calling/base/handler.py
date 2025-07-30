"""
Базовый абстрактный класс для хендлеров Tool Calling отраслей.

Все хендлеры отраслей должны наследоваться от BaseToolHandler
и реализовывать его абстрактные методы.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

from .types import ToolCallResult, FilterParameters, ToolSchema


class BaseToolHandler(ABC):
    """
    Базовый класс для обработчиков Tool Calling различных отраслей.
    
    Определяет общий интерфейс для всех хендлеров и предоставляет
    базовую функциональность логирования и обработки ошибок.
    """
    
    def __init__(self, subsector_id: str):
        """
        Инициализация базового хендлера.
        
        Args:
            subsector_id: Идентификатор подсектора (например, "01" для HoReCa)
        """
        self.subsector_id = subsector_id
        self.logger = logging.getLogger(f"tool_calling.{subsector_id}")
    
    @abstractmethod
    def generate_schema(self, data: Dict[str, Any], selected_key: str) -> List[ToolSchema]:
        """
        Генерирует схемы инструментов для OpenAI на основе данных.
        
        Args:
            data: Данные отрасли для анализа
            selected_key: Выбранный ключ для фокусировки схем
            
        Returns:
            Список схем инструментов для передачи в LLM
        """
        pass
    
    @abstractmethod
    def extract_parameters(self, query: str, schemas: List[ToolSchema]) -> FilterParameters:
        """
        Вызывает LLM для извлечения параметров фильтрации из запроса.
        
        Args:
            query: Пользовательский запрос
            schemas: Доступные схемы инструментов
            
        Returns:
            Извлеченные параметры фильтрации
        """
        pass
    
    @abstractmethod
    def filter_data(self, data: Dict[str, Any], parameters: FilterParameters) -> Dict[str, Any]:
        """
        Применяет фильтрацию к данным на основе параметров.
        
        Args:
            data: Исходные данные для фильтрации
            parameters: Параметры фильтрации от LLM
            
        Returns:
            Отфильтрованные данные
        """
        pass
    
    def process(self, query: str, data: Dict[str, Any], selected_key: str) -> ToolCallResult:
        """
        Выполняет полный цикл Tool Calling для запроса.
        
        Args:
            query: Пользовательский запрос
            data: Данные отрасли
            selected_key: Выбранный ключ данных
            
        Returns:
            Результат обработки с отфильтрованными данными
        """
        try:
            self.logger.info(f"Начало обработки Tool Calling для {self.subsector_id}")
            
            # 1. Генерация схем инструментов
            schemas = self.generate_schema(data, selected_key)
            self.logger.debug(f"Сгенерировано {len(schemas)} схем инструментов")
            
            # 2. Извлечение параметров через LLM
            parameters = self.extract_parameters(query, schemas)
            self.logger.debug(f"Извлечены параметры: {parameters.tool_name}")
            
            # 3. Применение фильтрации
            filtered_data = self.filter_data(data, parameters)
            self.logger.info("Фильтрация завершена успешно")
            
            return ToolCallResult(
                success=True,
                filtered_data=filtered_data,
                applied_filters=parameters.parameters,
                metadata={
                    "subsector_id": self.subsector_id,
                    "tool_name": parameters.tool_name,
                    "selected_key": selected_key
                }
            )
            
        except Exception as e:
            self.logger.error(f"Ошибка в Tool Calling: {str(e)}")
            return ToolCallResult(
                success=False,
                filtered_data=data,  # Возвращаем исходные данные при ошибке
                applied_filters={},
                error_message=str(e),
                metadata={
                    "subsector_id": self.subsector_id,
                    "fallback": True
                }
            )