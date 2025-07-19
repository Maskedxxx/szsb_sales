"""
Сервис для обработки Tool Calling логики в HoReCa системе.

Этот модуль реализует HoReCaHandler класс для:
1. Динамической генерации tool схем на основе структуры данных
2. Вызова LLM для выбора подходящего tool и его параметров
3. Фильтрации продуктов по выбранным критериям
"""

import json
import logging
from typing import Dict, List, Any

# Импорты для работы с существующими компонентами
from ..base import BaseToolHandler, FilterParameters, ToolSchema
from .mappings import HORECA_KEYS_MAPPING, HORECA_ENUM_MAPPING
from .data_filter import filter_horeca_products_smart

# Настройка логирования
logger = logging.getLogger(__name__)


class HoReCaHandler(BaseToolHandler):
    """
    Хендлер для обработки Tool Calling логики в HoReCa системе.
    
    Наследуется от BaseToolHandler и реализует специфичную логику
    для отрасли HoReCa (subsector_id: "01").
    """
    
    def __init__(self, subsector_id: str, llm_service=None):
        """
        Инициализация HoReCa хендлера.
        
        Args:
            subsector_id: Идентификатор подсектора ("01" для HoReCa)
            llm_service: Сервис для вызова LLM (будет передан из engine.py)
        """
        super().__init__(subsector_id)
        self.llm_service = llm_service
        logger.info(f"Инициализирован HoReCaHandler для подсектора {subsector_id}")
    
    def _get_file_specific_keys(self, file_name: str) -> Dict[str, Any]:
        """
        Возвращает специфичные ключи для конкретного файла HoReCa.
        
        Args:
            file_name: Имя файла (например, "ready_sauces.json")
            
        Returns:
            Словарь с ключами и их описаниями для файла
        """
        return HORECA_KEYS_MAPPING.get(file_name, {})
    
    def _get_enum_values_for_file_key(self, file_name: str, key_name: str) -> Dict[str, List[str]]:
        """
        Возвращает enum значения для конкретного ключа в конкретном файле.
        
        Args:
            file_name: Имя файла (например, "ready_sauces.json")
            key_name: Имя ключа (например, "name", "packaging")
            
        Returns:
            Словарь с enum категориями и значениями для данного ключа
        """
        file_data = HORECA_ENUM_MAPPING.get(file_name, {})
        return file_data.get(key_name, {})
    
    def generate_schema(self, data: Dict[str, Any], selected_key: str) -> List[ToolSchema]:
        """
        Генерирует динамические схемы инструментов для OpenAI на основе данных HoReCa.
        
        Args:
            data: Данные отрасли для анализа
            selected_key: Выбранный ключ для фокусировки схем
            
        Returns:
            Список схем инструментов для передачи в LLM
        """
        logger.info(f"Генерация tool схемы для HoReCa, выбранный ключ: {selected_key}")
        
        # Определяем имя файла из selected_key (например, "ready_sauces" -> "ready_sauces.json")
        file_name = f"{selected_key}.json"
        
        # Получаем маппинг ключей и enum'ов для файла
        file_keys = self._get_file_specific_keys(file_name)
        file_enums = HORECA_ENUM_MAPPING.get(file_name, {})
        
        if not file_keys or not file_enums:
            logger.error(f"Не найдены маппинги для файла: {file_name}")
            return []
        
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
        return [ToolSchema(type="function", function=tool_schema["function"])]
    
    def extract_parameters(self, query: str, schemas: List[ToolSchema]) -> FilterParameters:
        """
        Вызывает LLM для извлечения параметров фильтрации из запроса.
        
        Args:
            query: Пользовательский запрос
            schemas: Доступные схемы инструментов
            
        Returns:
            Извлеченные параметры фильтрации
        """
        logger.info(f"Извлечение параметров из запроса: {query[:100]}...")
        
        if not self.llm_service:
            logger.warning("LLM сервис не инициализирован, возвращаем пустые параметры")
            return FilterParameters(
                tool_name="filter_horeca_products",
                parameters={}
            )
        
        if not schemas:
            logger.error("Схемы инструментов не переданы")
            raise ValueError("Схемы инструментов не переданы")
        
        try:
            # Создаем промпт для LLM
            system_prompt = """
            Ты - эксперт по анализу запросов пользователей для системы HoReCa.
            Твоя задача - проанализировать запрос и выбрать подходящий инструмент для фильтрации продуктов.
            
            Используй предоставленный инструмент для точной фильтрации продуктов по критериям из запроса.
            Если в запросе несколько критериев, выбери самый важный для начальной фильтрации.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]

            # Преобразуем схемы в формат для LLM
            llm_tools = []
            for schema in schemas:
                llm_tools.append(
                    {"type": schema.type, "function": schema.function}
                )
            
            # Вызываем LLM с tool calling
            response = self.llm_service.chat.completions.create(
                model="devstral:24b-small-2505-q8_0 ",  # Или другая подходящая модель
                messages=messages,
                tools=llm_tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Парсим ответ LLM
            if tool_calls:
                tool_call = tool_calls[0]
                tool_name = tool_call.function.name
                tool_params = json.loads(tool_call.function.arguments)
                
                logger.info(f"LLM выбрал tool: {tool_name} с параметрами: {tool_params}")
                return FilterParameters(
                    tool_name=tool_name,
                    parameters=tool_params
                )
            else:
                logger.warning("LLM не вернул tool call")
                return FilterParameters(
                    tool_name="filter_horeca_products",
                    parameters={}
                )
                
        except Exception as e:
            logger.error(f"Ошибка при вызове LLM: {str(e)}")
            raise e
    
    def filter_data(self, data: Dict[str, Any], parameters: FilterParameters) -> Dict[str, Any]:
        """
        Применяет фильтрацию к данным на основе параметров.
        
        Args:
            data: Исходные данные для фильтрации
            parameters: Параметры фильтрации от LLM
            
        Returns:
            Отфильтрованные данные
        """
        logger.info(f"Фильтрация данных HoReCa по параметрам: {parameters.parameters}")
        
        # Извлекаем список продуктов
        product_list = data.get("product_list", [])
        if not product_list:
            logger.warning("Список продуктов пуст")
            return data
        
        if not parameters.parameters:
            logger.warning("Параметры фильтрации не переданы, возвращаем исходные данные")
            return data
        
        # Применяем фильтрацию по каждому параметру
        filtered_products = product_list
        
        for filter_key, enum_value in parameters.parameters.items():
            if enum_value:  # Проверяем, что значение не пустое
                logger.info(f"Применяем фильтр: {filter_key} = {enum_value}")
                filtered_products = filter_horeca_products_smart(
                    filtered_products, 
                    filter_key, 
                    enum_value
                )
                logger.info(f"После фильтрации по {filter_key}: {len(filtered_products)} продуктов")
        
        # Создаем новую структуру данных с отфильтрованными продуктами
        filtered_data = data.copy()
        filtered_data["product_list"] = filtered_products
        
        logger.info(f"Итого отфильтровано продуктов: {len(filtered_products)} из {len(product_list)}")
        return filtered_data


# Функция для совместимости со старым API
def create_horeca_tool_service(llm_service=None) -> HoReCaHandler:
    """
    Создает экземпляр HoReCaHandler для обратной совместимости.
    
    Args:
        llm_service: Сервис для вызова LLM
        
    Returns:
        Настроенный экземпляр HoReCaHandler
    """
    return HoReCaHandler("01", llm_service)


# Пример использования
if __name__ == "__main__":
    print("=== ТЕСТИРОВАНИЕ HoReCaHandler ===")
    
    # Инициализируем хендлер без LLM (для тестирования схемы)
    handler = HoReCaHandler("01")
    
    # Тестовые данные
    test_data = {
        "product_list": [
            '{"name": "Соус Горчичный", "kbgu": "КДж/ккал – 865/207", "packaging": "Бутылка пластиковая"}',
            '{"name": "Соус Барбекю", "kbgu": "КДж/ккал – 801/189", "packaging": "bag-in-box"}'
        ]
    }
    
    # Тестируем генерацию схемы
    print("\n1. Тестирование генерации tool схемы:")
    schemas = handler.generate_schema(test_data, "ready_sauces")
    if schemas:
        schema_dict = {"type": schemas[0].type, "function": schemas[0].function}
        print(json.dumps(schema_dict, indent=2, ensure_ascii=False))
    
    # Тестируем фильтрацию напрямую
    print("\n2. Тестирование фильтрации:")
    test_params = FilterParameters(
        tool_name="filter_horeca_products",
        parameters={"name": "барбекю"}
    )
    filtered_data = handler.filter_data(test_data, test_params)
    print(f"Отфильтровано продуктов: {len(filtered_data['product_list'])}")
    for product_json in filtered_data["product_list"]:
        product = json.loads(product_json)
        print(f"  - {product['name']}")
    
    print("\n✅ Тестирование завершено успешно")