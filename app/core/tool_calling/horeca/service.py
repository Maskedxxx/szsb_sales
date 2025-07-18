"""
HoReCa обработчик для Tool Calling.

Реализует специфичную логику обработки запросов для отрасли HoReCa.
"""

import json
import logging
from typing import Dict, List, Any, Optional

from ..service import ToolCallResult
from .mappings import KEYS_MAPPING, ENUM_MAPPING, get_search_patterns
from .filters import filter_products

logger = logging.getLogger(__name__)


class HoReCaHandler:
    """
    Обработчик Tool Calling для отрасли HoReCa.
    
    Реализует полный цикл обработки запросов:
    1. Генерация динамических tool схем
    2. Вызов LLM для выбора инструментов
    3. Фильтрация данных по выбранным критериям
    """
    
    def __init__(self):
        """Инициализация обработчика HoReCa."""
        logger.info("Инициализирован HoReCaHandler")
    
    def get_capabilities(self) -> List[str]:
        """
        Возвращает список возможностей обработчика.
        
        Returns:
            Список возможностей
        """
        return [
            "dynamic_tool_schema_generation",
            "product_filtering",
            "regex_numeric_matching",
            "brand_filtering",
            "packaging_filtering",
            "nutritional_filtering"
        ]
    
    def generate_tool_schema(self, file_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерирует динамическую схему tool на основе структуры данных файла.
        
        Args:
            file_name: Имя файла HoReCa (например, "ready_sauces.json")
            data: Данные продуктов из файла
            
        Returns:
            Словарь с OpenAI tool schema
        """
        logger.info(f"Генерация tool схемы для файла: {file_name}")
        
        # Получаем маппинги для файла
        file_keys = KEYS_MAPPING.get(file_name, {})
        file_enums = ENUM_MAPPING.get(file_name, {})
        
        if not file_keys or not file_enums:
            logger.warning(f"Не найдены маппинги для файла: {file_name}, используем fallback")
            return self._generate_fallback_schema(file_name)
        
        # Базовая структура tool schema
        tool_schema = {
            "type": "function",
            "function": {
                "name": "filter_products",
                "description": f"Фильтрует продукты HoReCa из файла {file_name} по заданным критериям.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
        
        # Добавляем свойства для каждого ключа
        properties = tool_schema["function"]["parameters"]["properties"]
        product_keys = file_keys.get("product_keys", {})
        
        for key_name, key_info in product_keys.items():
            if key_name not in file_enums:
                continue
                
            # Получаем enum значения для этого ключа
            enum_categories = file_enums[key_name]
            
            # Собираем все возможные enum значения
            all_enum_values = []
            for category, values in enum_categories.items():
                all_enum_values.extend(values)
            
            # Создаем свойство для этого ключа
            properties[key_name] = {
                "type": "string",
                "description": f"{key_info['description']}. {key_info['filter_impact']}",
                "enum": all_enum_values
            }
        
        logger.info(f"Сгенерирована схема с {len(properties)} свойствами")
        return tool_schema
    
    def _generate_fallback_schema(self, file_name: str) -> Dict[str, Any]:
        """Генерирует fallback схему для неизвестных файлов."""
        return {
            "type": "function",
            "function": {
                "name": "filter_products",
                "description": f"Фильтрует продукты из файла {file_name}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Фильтр по названию продукта",
                            "enum": ["горчичный", "барбекю", "сырный", "майонезный"]
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    
    def process_query(
        self, 
        query: str, 
        file_name: str, 
        data: Dict[str, Any], 
        llm_adapter
    ) -> ToolCallResult:
        """
        Обрабатывает запрос пользователя через tool calling.
        
        Args:
            query: Запрос пользователя
            file_name: Имя файла HoReCa
            data: Данные продуктов
            llm_adapter: Адаптер для работы с LLM
            
        Returns:
            Результат обработки
        """
        logger.info(f"Обработка HoReCa запроса для файла: {file_name}")
        
        try:
            # Шаг 1: Генерируем tool схему
            tool_schema = self.generate_tool_schema(file_name, data)
            if not tool_schema:
                return ToolCallResult(
                    success=False,
                    error_message=f"Не удалось сгенерировать tool схему для {file_name}"
                )
            
            # Шаг 2: Вызываем LLM
            system_prompt = self._create_system_prompt()
            llm_response = llm_adapter.call_with_tools(system_prompt, query, [tool_schema])
            
            # Шаг 3: Обрабатываем ответ LLM
            if not llm_response or "tool_calls" not in llm_response:
                logger.info("LLM не выбрал инструменты, возвращаем все продукты")
                product_list = data.get("product_list", [])
                return ToolCallResult(
                    success=True,
                    selected_tool="filter_products",
                    tool_parameters={},
                    filtered_data=product_list
                )
            
            # Шаг 4: Извлекаем параметры tool
            tool_call = llm_response["tool_calls"][0]
            tool_name = tool_call["function"]["name"]
            tool_params = json.loads(tool_call["function"]["arguments"])
            
            # Шаг 5: Фильтруем продукты
            product_list = data.get("product_list", [])
            filtered_products = self._apply_filters(product_list, tool_params)
            
            return ToolCallResult(
                success=True,
                selected_tool=tool_name,
                tool_parameters=tool_params,
                filtered_data=filtered_products
            )
            
        except Exception as e:
            logger.error(f"Ошибка при обработке HoReCa запроса: {str(e)}")
            return ToolCallResult(
                success=False,
                error_message=str(e)
            )
    
    def _create_system_prompt(self) -> str:
        """Создает системный промпт для LLM."""
        return """
        Ты - эксперт по анализу запросов пользователей для системы HoReCa.
        Твоя задача - проанализировать запрос и выбрать подходящий инструмент для фильтрации продуктов.
        
        Используй предоставленный инструмент для точной фильтрации продуктов по критериям из запроса.
        Если в запросе несколько критериев, выбери самый важный для начальной фильтрации.
        
        Примеры:
        - "Найди соусы Барбекю" → name: "барбекю"
        - "Покажи продукты в пластиковых бутылках" → packaging: "бутылка_пластиковая"
        - "Нужны низкокалорийные продукты" → kbgu: "низкие_до_150"
        """
    
    def _apply_filters(self, product_list: List[str], tool_params: Dict[str, Any]) -> List[str]:
        """
        Применяет фильтры к списку продуктов.
        
        Args:
            product_list: Список JSON строк продуктов
            tool_params: Параметры фильтрации от LLM
            
        Returns:
            Отфильтрованный список продуктов
        """
        if not tool_params:
            return product_list
        
        filtered_products = product_list
        
        # Применяем фильтрацию по каждому параметру
        for filter_key, enum_value in tool_params.items():
            if enum_value:
                logger.info(f"Применяем фильтр: {filter_key} = {enum_value}")
                filtered_products = filter_products(
                    filtered_products, 
                    filter_key, 
                    enum_value
                )
                logger.info(f"После фильтрации по {filter_key}: {len(filtered_products)} продуктов")
        
        return filtered_products