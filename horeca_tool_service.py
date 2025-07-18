"""
Сервис для обработки Tool Calling логики в HoReCa системе.

Этот модуль реализует единый класс HoReCaToolService для:
1. Динамической генерации tool схем на основе структуры данных
2. Вызова LLM для выбора подходящего tool и его параметров
3. Фильтрации продуктов по выбранным критериям
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Импорты для работы с существующими компонентами
from horeca_keys_mapping import HORECA_KEYS_MAPPING, get_file_specific_keys
from horeca_enum_mapping import HORECA_ENUM_MAPPING, get_enum_values_for_file_key
from universal_enum_mapping import has_universal_enum_match
from horeca_filter import filter_horeca_products_smart

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ToolCallResult:
    """Результат вызова tool calling."""
    success: bool
    selected_tool: Optional[str] = None
    tool_parameters: Optional[Dict[str, Any]] = None
    filtered_products: Optional[List[str]] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None


class HoReCaToolService:
    """
    Основной сервис для обработки Tool Calling логики в HoReCa системе.
    
    Выполняет полный цикл:
    1. Генерирует динамические tool схемы на основе структуры данных
    2. Вызывает LLM для выбора tool и параметров
    3. Фильтрует продукты по выбранным критериям
    """
    
    def __init__(self, llm_service=None):
        """
        Инициализация сервиса.
        
        Args:
            llm_service: Сервис для вызова LLM (будет передан из engine.py)
        """
        self.llm_service = llm_service
        logger.info("Инициализирован HoReCaToolService")
    
    def generate_tool_schema(self, file_name: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерирует динамическую схему tool на основе структуры данных файла.
        
        Args:
            file_name: Имя файла HoReCa (например, "ready_sauces.json")
            product_data: Данные продуктов из файла
            
        Returns:
            Словарь с OpenAI tool schema
        """
        logger.info(f"Генерация tool схемы для файла: {file_name}")
        
        # Получаем маппинг ключей и enum'ов для файла
        file_keys = get_file_specific_keys(file_name)
        file_enums = HORECA_ENUM_MAPPING.get(file_name, {})
        
        if not file_keys or not file_enums:
            logger.error(f"Не найдены маппинги для файла: {file_name}")
            return {}
        
        # Базовая структура tool schema
        tool_schema = {
            "type": "function",
            "function": {
                "name": "filter_horeca_products",
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
        
        # Получаем описания ключей продуктов
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
    
    def call_llm_with_tool(self, query: str, tool_schema: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Вызывает LLM для выбора подходящего tool и его параметров.
        
        Args:
            query: Пользовательский запрос
            tool_schema: Схема tool для LLM
            
        Returns:
            Tuple[bool, Optional[Dict]]: (успех, параметры_tool)
        """
        logger.info(f"Вызов LLM с tool schema для запроса: {query[:100]}...")
        
        if not self.llm_service:
            logger.error("LLM сервис не инициализирован")
            return False, None
        
        try:
            # Создаем промпт для LLM
            system_prompt = """
            Ты - эксперт по анализу запросов пользователей для системы HoReCa.
            Твоя задача - проанализировать запрос и выбрать подходящий инструмент для фильтрации продуктов.
            
            Используй предоставленный инструмент для точной фильтрации продуктов по критериям из запроса.
            Если в запросе несколько критериев, выбери самый важный для начальной фильтрации.
            """
            
            # Вызываем LLM с tool calling
            response = self.llm_service.call_with_tools(
                system_prompt=system_prompt,
                user_query=query,
                tools=[tool_schema]
            )
            
            # Парсим ответ LLM
            if response and "tool_calls" in response:
                tool_call = response["tool_calls"][0]
                tool_name = tool_call["function"]["name"]
                tool_params = json.loads(tool_call["function"]["arguments"])
                
                logger.info(f"LLM выбрал tool: {tool_name} с параметрами: {tool_params}")
                return True, tool_params
            else:
                logger.warning("LLM не вернул tool call")
                return False, None
                
        except Exception as e:
            logger.error(f"Ошибка при вызове LLM: {str(e)}")
            return False, None
    
    def filter_products(self, product_list: List[str], tool_parameters: Dict[str, Any]) -> List[str]:
        """
        Фильтрует продукты по параметрам, выбранным LLM.
        
        Args:
            product_list: Список JSON строк продуктов
            tool_parameters: Параметры фильтрации от LLM
            
        Returns:
            Отфильтрованный список продуктов
        """
        logger.info(f"Фильтрация {len(product_list)} продуктов по параметрам: {tool_parameters}")
        
        if not tool_parameters:
            logger.warning("Параметры фильтрации не переданы, возвращаем все продукты")
            return product_list
        
        # Применяем фильтрацию по каждому параметру
        filtered_products = product_list
        
        for filter_key, enum_value in tool_parameters.items():
            if enum_value:  # Проверяем, что значение не пустое
                logger.info(f"Применяем фильтр: {filter_key} = {enum_value}")
                filtered_products = filter_horeca_products_smart(
                    filtered_products, 
                    filter_key, 
                    enum_value
                )
                logger.info(f"После фильтрации по {filter_key}: {len(filtered_products)} продуктов")
        
        return filtered_products
    
    def process_horeca_query(
        self, 
        query: str, 
        file_name: str, 
        product_data: Dict[str, Any]
    ) -> ToolCallResult:
        """
        Основной метод для обработки запроса пользователя через Tool Calling.
        
        Выполняет полный цикл:
        1. Генерирует tool схему
        2. Вызывает LLM
        3. Фильтрует продукты
        
        Args:
            query: Пользовательский запрос
            file_name: Имя файла HoReCa
            product_data: Данные продуктов
            
        Returns:
            ToolCallResult с результатами обработки
        """
        import time
        start_time = time.time()
        
        logger.info(f"Начало обработки запроса для файла: {file_name}")
        logger.info(f"Запрос: {query}")
        
        try:
            # Шаг 1: Генерируем tool схему
            tool_schema = self.generate_tool_schema(file_name, product_data)
            if not tool_schema:
                return ToolCallResult(
                    success=False,
                    error_message=f"Не удалось сгенерировать tool схему для {file_name}"
                )
            
            # Шаг 2: Вызываем LLM
            success, tool_params = self.call_llm_with_tool(query, tool_schema)
            if not success or not tool_params:
                logger.warning("LLM не выбрал tool параметры, возвращаем все продукты")
                # Возвращаем все продукты без фильтрации
                product_list = product_data.get("product_list", [])
                return ToolCallResult(
                    success=True,
                    selected_tool="filter_horeca_products",
                    tool_parameters={},
                    filtered_products=product_list,
                    execution_time=time.time() - start_time
                )
            
            # Шаг 3: Фильтруем продукты
            product_list = product_data.get("product_list", [])
            filtered_products = self.filter_products(product_list, tool_params)
            
            execution_time = time.time() - start_time
            
            logger.info(f"Обработка завершена успешно за {execution_time:.2f}с")
            logger.info(f"Отфильтровано продуктов: {len(filtered_products)} из {len(product_list)}")
            
            return ToolCallResult(
                success=True,
                selected_tool="filter_horeca_products",
                tool_parameters=tool_params,
                filtered_products=filtered_products,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Ошибка при обработке запроса: {str(e)}")
            
            return ToolCallResult(
                success=False,
                error_message=str(e),
                execution_time=execution_time
            )


# Пример использования
if __name__ == "__main__":
    print("=== ТЕСТИРОВАНИЕ HoReCaToolService ===")
    
    # Инициализируем сервис без LLM (для тестирования схемы)
    service = HoReCaToolService()
    
    # Тестовые данные
    test_data = {
        "product_list": [
            '{"name": "Соус Горчичный", "kbgu": "КДж/ккал – 865/207", "packaging": "Бутылка пластиковая"}',
            '{"name": "Соус Барбекю", "kbgu": "КДж/ккал – 801/189", "packaging": "bag-in-box"}'
        ]
    }
    
    # Тестируем генерацию схемы
    print("\n1. Тестирование генерации tool схемы:")
    schema = service.generate_tool_schema("ready_sauces.json", test_data)
    print(json.dumps(schema, indent=2, ensure_ascii=False))
    
    # Тестируем фильтрацию
    print("\n2. Тестирование фильтрации:")
    test_params = {"name": "барбекю"}
    filtered = service.filter_products(test_data["product_list"], test_params)
    print(f"Отфильтровано продуктов: {len(filtered)}")
    for product in filtered:
        print(f"  - {json.loads(product)['name']}")
    
    print("\n✅ Тестирование завершено успешно")