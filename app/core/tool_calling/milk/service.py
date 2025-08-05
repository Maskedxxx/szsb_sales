"""
Сервис для обработки Tool Calling логики в молочной отрасли.

Этот модуль реализует MilkHandler класс для:
1. Динамической генерации tool схем на основе структуры данных молочной отрасли
2. Вызова LLM для выбора подходящего tool и его параметров
3. Фильтрации продуктов по выбранным критериям
"""

import json
import logging
from typing import Dict, List, Any

# Импорты для работы с существующими компонентами
from ..base.handler import BaseToolHandler
from ..base.types import FilterParameters, ToolSchema
from .mappings import MILK_KEYS_MAPPING, MILK_ENUM_MAPPING
from .data_filter import filter_milk_products_smart

# Настройка логирования
logger = logging.getLogger(__name__)


class MilkHandler(BaseToolHandler):
    """
    Хендлер для обработки Tool Calling логики в молочной отрасли.
    
    Наследуется от BaseToolHandler и реализует специфичную логику
    для молочной отрасли (subsector_id: "04").
    """
    
    def __init__(self, subsector_id: str, llm_service=None):
        """
        Инициализация Milk хендлера.
        
        Args:
            subsector_id: Идентификатор подсектора ("04" для молочной отрасли)
            llm_service: Сервис для вызова LLM (будет передан из engine.py)
        """
        super().__init__(subsector_id)
        self.llm_service = llm_service
        logger.info(f"Инициализирован MilkHandler для подсектора {subsector_id}")
    
    def _get_file_specific_keys(self, file_name: str) -> Dict[str, Any]:
        """
        Возвращает специфичные ключи для конкретного файла молочной отрасли.
        
        Args:
            file_name: Имя файла (например, "milk_protein.json")
            
        Returns:
            Словарь с ключами и их описаниями для файла
        """
        return MILK_KEYS_MAPPING.get(file_name, {})
    
    def _get_enum_values_for_file_key(self, file_name: str, key_name: str) -> Dict[str, List[str]]:
        """
        Возвращает enum значения для конкретного ключа в конкретном файле.
        
        Args:
            file_name: Имя файла (например, "milk_protein.json")
            key_name: Имя ключа (например, "name", "properties")
            
        Returns:
            Словарь с enum категориями и значениями для данного ключа
        """
        file_data = MILK_ENUM_MAPPING.get(file_name, {})
        return file_data.get(key_name, {})
    
    def _find_file_for_key(self, selected_key: str) -> str:
        """
        Находит JSON файл, содержащий указанный ключ на основе маппинга всех ключей.
        
        Args:
            selected_key: Ключ для поиска
            
        Returns:
            Имя JSON файла
        """
        # Полный маппинг всех ключей к файлам из молочной отрасли
        KEY_TO_FILE_MAPPING = {
            # delar_flavor_collection.json
            "aromatic_emulsions": "delar_flavor_collection.json",
            "flavor_bases": "delar_flavor_collection.json", 
            "gastronomic_flavors": "delar_flavor_collection.json",
            "juice_containing_flavors": "delar_flavor_collection.json",
            "spread_flavorings": "delar_flavor_collection.json",
            "sweet_flavors": "delar_flavor_collection.json",
            
            # fruit_fillings.json
            "nonthermostable_homogeneous_fillings": "fruit_fillings.json",
            "thermostable_homogeneous_fillings": "fruit_fillings.json",
            
            # starter_cultures.json
            "probiotic_cultures": "starter_cultures.json",
            "protective_cultures": "starter_cultures.json", 
            "starter_cultures": "starter_cultures.json",
            
            # Остальные файлы (ключ = имя файла)
            "cocoa_powder": "cocoa_powder.json",
            "confectionery_glaze_klassika": "confectionery_glaze.json",
            "denfruit_vegetable_fillings": "vegetable_fillings.json",
            "dyes": "dyes.json",
            "milk_protein_concentrate": "milk_protein.json",
            "multifunctional_systems": "multifunctional_systems.json",
            "phosphates": "phosphates.json",
            "preservatives_antioxidants_emulsifying_salts": "preservatives_antioxidants.json"
        }
        
        # Ищем прямое соответствие
        if selected_key in KEY_TO_FILE_MAPPING:
            file_name = KEY_TO_FILE_MAPPING[selected_key]
            logger.info(f"Найден файл для ключа {selected_key}: {file_name}")
            return file_name
        
        # Если не найден, возвращаем fallback
        fallback_file = "fruit_fillings.json"
        logger.warning(f"Ключ {selected_key} не найден в маппинге, используем fallback: {fallback_file}")
        return fallback_file

    def _get_llm_model(self) -> str:
        """
        Возвращает модель LLM для Tool Calling.
        
        Returns:
            Имя модели LLM
        """
        # TODO: Получать из переменных окружения или конфигурации
        import os
        return os.getenv('TOOL_CALLING_MODEL', 'devstral:24b-small-2505-q8_0')
    
    def generate_schema(self, data: Dict[str, Any], selected_key: str) -> List[ToolSchema]:
        """
        Генерирует динамические схемы инструментов для OpenAI на основе данных молочной отрасли.
        
        Args:
            data: Данные отрасли для анализа
            selected_key: Выбранный ключ для фокусировки схем
            
        Returns:
            Список схем инструментов для передачи в LLM
        """
        logger.info(f"Генерация tool схемы для молочной отрасли, выбранный ключ: {selected_key}")
        
        # Определяем имя файла из selected_key
        # В молочной отрасли selected_key может быть подключом внутри файла
        file_name = self._find_file_for_key(selected_key)
        
        # Получаем маппинг ключей и enum'ов для файла
        file_keys = self._get_file_specific_keys(file_name)
        
        # ВАЖНО: Получаем enum только для выбранного selected_key (подключа)
        file_enum_mapping = MILK_ENUM_MAPPING.get(file_name, {})
        
        # Для файлов с подключами (как fruit_fillings.json) берем enum'ы конкретного подключа
        if selected_key in file_enum_mapping:
            # Файл с подключами - используем enum'ы конкретного подключа
            file_enums = file_enum_mapping[selected_key]
            logger.info(f"Используем enum'ы для подключа {selected_key}")
        else:
            # Стандартный файл - используем общие enum'ы
            file_enums = file_enum_mapping
            logger.info(f"Используем общие enum'ы для файла {file_name}")
        
        if not file_keys or not file_enums:
            logger.error(f"Не найдены маппинги для файла: {file_name}")
            return []
        
        # Базовая структура tool schema
        tool_schema = {
            "type": "function",
            "function": {
                "name": "filter_milk_products",
                "description": f"Фильтрует продукты молочной отрасли из файла {file_name} по заданным критериям.",
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
        required_fields = tool_schema["function"]["parameters"]["required"]
        
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
            
            # Создаем свойство для этого ключа (согласно OpenAI strict mode)
            # Поля необязательны, поэтому добавляем null в type
            properties[key_name] = {
                "type": ["string", "null"],
                "description": f"{key_info['description']}. {key_info['filter_impact']}",
                "enum": all_enum_values + [None]  # Добавляем None для необязательных полей
            }
            
            # Добавляем все поля в required (обязательное требование strict mode)
            required_fields.append(key_name)
        
        logger.info(f"Сгенерирована схема с {len(properties)} свойствами, все поля в required")
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
                tool_name="filter_milk_products",
                parameters={}
            )
        
        if not schemas:
            logger.error("Схемы инструментов не переданы")
            raise ValueError("Схемы инструментов не переданы")
        
        try:
            # Создаем промпт для LLM
            system_prompt = """
            Ты - эксперт по анализу запросов пользователей для системы молочной промышленности.
            Твоя задача - проанализировать запрос и выбрать подходящий инструмент для фильтрации продуктов.
            
            ВАЖНО: Ты ДОЛЖЕН вызвать инструмент ТОЛЬКО ОДИН РАЗ. Никогда не делай несколько вызовов инструмента.
            Используй предоставленный инструмент для точной фильтрации продуктов по критериям из запроса.
            Если в запросе несколько критериев, выбери самый важный для начальной фильтрации.
            
            Обязательно выбери только ОДНО значение для каждого параметра или null если параметр не нужен.
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
                model=self._get_llm_model(),  # Получаем модель из конфигурации
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
                    tool_name="filter_milk_products",
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
        logger.info(f"Фильтрация данных молочной отрасли по параметрам: {parameters.parameters}")
        
        # Извлекаем список продуктов из различных возможных структур данных
        product_list = []
        
        # Ищем product_list в корне данных
        if "product_list" in data:
            if isinstance(data["product_list"], list):
                product_list = data["product_list"]
            elif isinstance(data["product_list"], str):
                # Если product_list это JSON строка, парсим ее
                try:
                    import json
                    product_list = json.loads(data["product_list"])
                except json.JSONDecodeError:
                    logger.warning("Не удалось распарсить product_list как JSON")
                    product_list = [data["product_list"]]
        else:
            # Ищем в подключах данных
            for key, value in data.items():
                if isinstance(value, dict) and "product_list" in value:
                    product_list = value["product_list"]
                    break
        
        if not product_list:
            logger.warning("Список продуктов не найден или пуст")
            return data
        
        if not parameters.parameters:
            logger.warning("Параметры фильтрации не переданы, возвращаем исходные данные")
            return data
        
        # Применяем фильтрацию по каждому параметру
        filtered_products = product_list
        
        try:
            for filter_key, enum_value in parameters.parameters.items():
                if enum_value and enum_value.strip():  # Проверяем, что значение не пустое
                    logger.info(f"Применяем фильтр: {filter_key} = {enum_value}")
                    
                    # Применяем умную фильтрацию
                    filtered_products = filter_milk_products_smart(
                        filtered_products, 
                        filter_key, 
                        enum_value
                    )
                    logger.info(f"После фильтрации по {filter_key}: {len(filtered_products)} продуктов")
                    
                    # Если после фильтрации не осталось продуктов, прерываем
                    if not filtered_products:
                        logger.warning(f"После фильтрации по {filter_key} не осталось продуктов")
                        break
                        
        except Exception as e:
            logger.error(f"Ошибка при фильтрации: {str(e)}")
            # При ошибке возвращаем исходные данные
            return data
        
        # Создаем новую структуру данных с отфильтрованными продуктами
        filtered_data = data.copy()
        
        # Обновляем product_list в правильном месте структуры данных
        if "product_list" in data:
            filtered_data["product_list"] = filtered_products
        else:
            # Обновляем в подключах
            for key, value in filtered_data.items():
                if isinstance(value, dict) and "product_list" in value:
                    filtered_data[key]["product_list"] = filtered_products
                    break
        
        logger.info(f"Итого отфильтровано продуктов: {len(filtered_products)} из {len(product_list)}")
        return filtered_data


# Функция для совместимости со старым API
def create_milk_tool_service(llm_service=None) -> MilkHandler:
    """
    Создает экземпляр MilkHandler для обратной совместимости.
    
    Args:
        llm_service: Сервис для вызова LLM
        
    Returns:
        Настроенный экземпляр MilkHandler
    """
    return MilkHandler("04", llm_service)