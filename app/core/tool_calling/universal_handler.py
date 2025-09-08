"""
Универсальный обработчик Tool Calling для всех отраслей.

Этот класс заменяет отдельные хендлеры (HoReCaHandler, MilkHandler) 
единой реализацией, различающейся только mappings конфигурациями.
"""

import json
import importlib
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .base.handler import BaseToolHandler
from .base.types import ToolCallResult, FilterParameters, ToolSchema


@dataclass
class IndustryMappings:
    """Контейнер для mappings отрасли."""
    keys_mapping: Dict[str, Any]
    enum_mapping: Dict[str, Any]
    universal_patterns_func: callable
    key_to_file_mapping: Optional[Dict[str, str]] = None


class IndustryMappingsLoader:
    """
    Загружает mappings для любой отрасли по единому паттерну.
    Все отрасли имеют одинаковую структуру mappings.
    """
    
    INDUSTRY_MAPPING = {
        "01": "horeca",    # HoReCa
        "04": "milk",      # Молочная
        "00": "selo",      # Сельнозпродукция
        "03": "fat_and_oil",  # Масложировая отрасль
        "09": "drinks",    # Напитки
    }
    
    @staticmethod
    def load(subsector_id: str) -> IndustryMappings:
        """
        Динамически загружает mappings для отрасли.
        
        Args:
            subsector_id: ID отрасли ("01", "04", etc.)
            
        Returns:
            IndustryMappings с загруженными данными
            
        Raises:
            ValueError: Если отрасль не поддерживается
            ImportError: Если mappings модули не найдены
        """
        industry_name = IndustryMappingsLoader.INDUSTRY_MAPPING.get(subsector_id)
        if not industry_name:
            raise ValueError(f"Отрасль {subsector_id} не поддерживается")
            
        try:
            # Динамическая загрузка mappings модулей
            keys_module = importlib.import_module(f"app.core.tool_calling.{industry_name}.mappings.keys")
            enums_module = importlib.import_module(f"app.core.tool_calling.{industry_name}.mappings.enums") 
            universal_module = importlib.import_module(f"app.core.tool_calling.{industry_name}.mappings.universal")
            
            # Определяем правильные имена переменных mappings
            keys_mapping_name = f"{industry_name.upper()}_KEYS_MAPPING"
            enum_mapping_name = f"{industry_name.upper()}_ENUM_MAPPING"
            
            keys_mapping = getattr(keys_module, keys_mapping_name, {})
            enum_mapping = getattr(enums_module, enum_mapping_name, {})
            
            # Для Milk может быть KEY_TO_FILE_MAPPING
            key_to_file_mapping = None
            if hasattr(keys_module, "KEY_TO_FILE_MAPPING"):
                key_to_file_mapping = keys_module.KEY_TO_FILE_MAPPING
            
            return IndustryMappings(
                keys_mapping=keys_mapping,
                enum_mapping=enum_mapping,
                universal_patterns_func=universal_module.get_universal_patterns,
                key_to_file_mapping=key_to_file_mapping
            )
            
        except ImportError as e:
            raise ImportError(f"Ошибка загрузки mappings для {industry_name}: {str(e)}")


class UniversalIndustryHandler(BaseToolHandler):
    """
    Единственный обработчик для ВСЕХ отраслей.
    Различия только в mappings конфигурациях.
    """
    
    def __init__(self, subsector_id: str, llm_service):
        """
        Инициализация универсального хендлера.
        
        Args:
            subsector_id: ID отрасли
            llm_service: Сервис для работы с LLM
        """
        super().__init__(subsector_id)
        self.llm_service = llm_service
        self.mappings = IndustryMappingsLoader.load(subsector_id)
        
        self.logger.info(f"Инициализирован универсальный хендлер для отрасли {subsector_id}")
    
    def generate_schema(self, data: Dict[str, Any], selected_key: str) -> List[ToolSchema]:
        """
        Генерирует схемы ВСЕГДА в Milk-подходе:
        - strict: true
        - required: [все поля]  
        - type: ["string", "null"]
        - enum с None
        """
        try:
            # 1. Определяем файл (как в Milk)
            file_name = self._resolve_file_name(selected_key)
            
            # 2. Загружаем описания ключей
            file_keys = self._get_file_keys(file_name)
            if not file_keys:
                self.logger.warning(f"Не найдены ключи для файла {file_name}")
                return []
            
            # 3. Загружаем enum значения (с поддержкой субключей)
            file_enums = self._get_file_enums(file_name, selected_key)
            
            # 4. Создаем strict схему
            schema = self._create_strict_schema(file_name, file_keys, file_enums)
            
            self.logger.debug(f"Создана strict схема для {file_name} с {len(schema['function']['parameters']['properties'])} полями")
            return [schema]
            
        except Exception as e:
            self.logger.error(f"Ошибка генерации схемы: {str(e)}")
            return []
    
    def extract_parameters(self, query: str, schemas: List[ToolSchema]) -> FilterParameters:
        """
        Извлекает параметры через LLM с строгим промптом (как в Milk).
        """
        if not schemas:
            return FilterParameters(tool_name="", parameters={})
            
        try:
            # Строгий системный промпт с правилами безопасного вызова
            system_prompt = self._get_strict_system_prompt()
            
            # Подготавливаем инструменты для LLM
            llm_tools = [self._convert_schema_to_llm_tool(schema) for schema in schemas]
            
            # Вызываем LLM
            response = self.llm_service.chat.completions.create(
                model="devstral:24b-small-2505-q8_0",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                tools=llm_tools,
                tool_choice="auto"
            )
            
            # Парсим ответ
            if hasattr(response, 'choices') and response.choices:
                message = response.choices[0].message
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    tool_call = message.tool_calls[0]
                    tool_name = tool_call.function.name
                    tool_params = json.loads(tool_call.function.arguments)

                    # Список допустимых enum-значений по каждому полю из схемы
                    allowed_by_field: Dict[str, set] = {}
                    try:
                        if schemas:
                            props = schemas[0]["function"]["parameters"].get("properties", {})
                            for field, meta in props.items():
                                enums = meta.get("enum", [])
                                allowed_by_field[field] = {e for e in enums if e is not None}
                    except Exception:
                        allowed_by_field = {}

                    # Нормализуем параметры: убираем пустые/None и значения вне enum
                    normalized: Dict[str, Any] = {}
                    for k, v in (tool_params or {}).items():
                        if v is None:
                            continue
                        sval = str(v).strip()
                        if not sval:
                            continue
                        allowed = allowed_by_field.get(k)
                        if allowed is not None and sval not in allowed:
                            # Значение вне допустимого enum — пропускаем
                            continue
                        normalized[k] = sval

                    if normalized:
                        return FilterParameters(tool_name=tool_name, parameters=normalized)

            self.logger.warning("LLM не вернул tool call")
            return FilterParameters(tool_name="", parameters={})
            
        except Exception as e:
            self.logger.error(f"Ошибка извлечения параметров: {str(e)}")
            return FilterParameters(tool_name="", parameters={})
    
    def filter_data(self, data: Dict[str, Any], parameters: FilterParameters) -> Dict[str, Any]:
        """
        Применяет фильтрацию ВСЕГДА с поиском в субключах (как в Milk).
        """
        if not parameters.parameters:
            self.logger.info("Нет параметров для фильтрации")
            return data
            
        try:
            # 1. Извлекаем список продуктов (универсальный поиск)
            product_list = self._extract_product_list(data)
            if not product_list:
                self.logger.warning("Не найден список продуктов")
                return data
            
            original_count = len(product_list)
            self.logger.info(f"Начальное количество продуктов: {original_count}")
            
            # 2. Применяем фильтры последовательно
            filtered_products = product_list
            applied_filters = {}
            
            for filter_key, enum_value in parameters.parameters.items():
                if enum_value and str(enum_value).strip():
                    prev_products = filtered_products
                    self.logger.info(f"Применяем фильтр: {filter_key} = {enum_value}")

                    candidate = self._apply_smart_filter(
                        prev_products,
                        filter_key,
                        enum_value
                    )

                    if candidate:
                        filtered_products = candidate
                        applied_filters[filter_key] = enum_value
                        self.logger.info(f"После фильтрации по {filter_key}: {len(filtered_products)} продуктов")
                    else:
                        self.logger.warning(
                            f"Фильтр {filter_key}={enum_value} отброшен: обнуляет выдачу"
                        )
                        # Оставляем предыдущее множество без изменений (RELAX_ON_ZERO)
                        filtered_products = prev_products
            
            # 3. Создаем отфильтрованные данные
            filtered_data = self._create_filtered_data(data, filtered_products)
            
            final_count = len(filtered_products)
            self.logger.info(f"Итого отфильтровано продуктов: {final_count} из {original_count}")
            
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Ошибка фильтрации данных: {str(e)}")
            return data
    
    def process(self, query: str, data: Dict[str, Any], selected_key: str) -> ToolCallResult:
        """
        Переопределяет базовый процесс с четким fallback контролем.
        """
        try:
            self.logger.info(f"Начало Tool Calling для отрасли {self.subsector_id}")
            
            # 1. Генерация схем инструментов
            schemas = self.generate_schema(data, selected_key)
            if not schemas:
                return self._create_fallback_result(data, "no_schemas_generated")
            
            # 2. Извлечение параметров через LLM
            parameters = self.extract_parameters(query, schemas)
            if not parameters.parameters:
                return self._create_fallback_result(data, "no_parameters_extracted")
            
            # 3. Применение фильтрации
            filtered_data = self.filter_data(data, parameters)
            
            # 4. КЛЮЧЕВАЯ ПРОВЕРКА: есть ли отфильтрованные продукты?
            if self._has_filtered_products(filtered_data, data):
                self.logger.info("✅ Tool Calling успешен - найдены отфильтрованные продукты")
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
            else:
                self.logger.warning("⚠️ Tool Calling не нашел продуктов - fallback")
                return self._create_fallback_result(data, "no_products_found")
                
        except Exception as e:
            self.logger.error(f"❌ Tool Calling ошибка: {str(e)} - fallback")
            return self._create_fallback_result(data, str(e))
    
    # === Вспомогательные методы ===
    
    def _resolve_file_name(self, selected_key: str) -> str:
        """Определяет имя файла по selected_key."""
        # Для Milk может быть специальный маппинг
        if self.mappings.key_to_file_mapping and selected_key in self.mappings.key_to_file_mapping:
            return self.mappings.key_to_file_mapping[selected_key]
        # Для остальных - прямое соответствие
        return f"{selected_key}.json"
    
    def _get_file_keys(self, file_name: str) -> Dict[str, Any]:
        """Получает описания ключей файла."""
        return self.mappings.keys_mapping.get(file_name, {}).get("product_keys", {})
    
    def _get_file_enums(self, file_name: str, selected_key: str) -> Dict[str, Any]:
        """Получает enum значения (с поддержкой субключей)."""
        file_enum_mapping = self.mappings.enum_mapping.get(file_name, {})
        
        # Если есть субключ (как в Milk)
        if selected_key in file_enum_mapping:
            return file_enum_mapping[selected_key]
        
        # Иначе используем общие enum'ы
        return file_enum_mapping
    
    def _create_strict_schema(self, file_name: str, file_keys: Dict, file_enums: Dict) -> ToolSchema:
        """Создает strict схему (как в Milk)."""
        properties = {}
        required_fields = []
        
        for key_name, key_info in file_keys.items():
            # Собираем все enum значения для этого ключа
            enum_values = []
            key_enums = file_enums.get(key_name, {})

            for enum_category in key_enums.values():
                if isinstance(enum_category, list):
                    enum_values.extend(enum_category)
            
            # Добавляем None для strict mode
            enum_values.append(None)
            
            properties[key_name] = {
                "type": ["string", "null"],
                "description": f"{key_info['description']}. {key_info.get('filter_impact', '')}".strip(),
                "enum": enum_values
            }
            
            required_fields.append(key_name)
        
        industry_name = IndustryMappingsLoader.INDUSTRY_MAPPING[self.subsector_id]
        
        return {
            "type": "function",
            "function": {
                "name": f"filter_{industry_name}_products",
                "description": f"Фильтрует продукты отрасли {industry_name} из файла {file_name} по заданным критериям.",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_fields,
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    
    def _get_strict_system_prompt(self) -> str:
        """Возвращает строгий системный промпт c явными правилами для безопасного вызова инструмента."""
        industry_name = IndustryMappingsLoader.INDUSTRY_MAPPING[self.subsector_id]
        
        return f"""Ты — эксперт по анализу запросов пользователей для системы {industry_name}.
Твоя задача — при необходимости отфильтровать продукты с помощью предоставленного инструмента.

Правила вызова инструмента:
- Необязательный вызов: вызывай инструмент только если есть ХОТЯ БЫ ОДИН параметр, которому однозначно соответствует одно из допустимых значений (enum) из схемы.
- Ровно один вызов: если вызываешь — только один раз.
- Выбор значений: для каждого параметра выбирай строго одно допустимое значение из enum или null, если параметр не применим.
- Никаких догадок: если подходящих значений нет, не подбирай «на глаз», укажи null для таких параметров. Если все параметры null — НЕ вызывай инструмент вообще.

Учитывай смысл запроса и выбирай только те параметры, которые реально помогают фильтровать результаты по запросу пользователя."""
    
    def _convert_schema_to_llm_tool(self, schema: ToolSchema) -> Dict:
        """Конвертирует схему в формат для LLM."""
        return schema
    
    def _extract_product_list(self, data: Dict[str, Any]) -> List:
        """Универсальное извлечение product_list (поддержка субключей)."""
        # Сначала ищем в корне
        if "product_list" in data:
            product_list = data["product_list"]
            if isinstance(product_list, str):
                try:
                    return json.loads(product_list)
                except:
                    return []
            elif isinstance(product_list, list):
                return product_list
        
        # Ищем в субключах
        for key, value in data.items():
            if isinstance(value, dict) and "product_list" in value:
                sub_product_list = value["product_list"]
                if isinstance(sub_product_list, str):
                    try:
                        return json.loads(sub_product_list)
                    except:
                        continue
                elif isinstance(sub_product_list, list):
                    return sub_product_list
        
        return []
    
    def _apply_smart_filter(self, products: List, filter_key: str, enum_value: str) -> List:
        """Применяет умную фильтрацию используя universal patterns."""
        filtered = []
        patterns = self.mappings.universal_patterns_func(enum_value)
        
        for product in products:
            product_text = str(product).lower()
            
            # Проверяем каждый паттерн
            for pattern in patterns:
                if pattern.lower() in product_text:
                    filtered.append(product)
                    break
        
        return filtered
    
    def _create_filtered_data(self, original_data: Dict, filtered_products: List) -> Dict:
        """Создает отфильтрованную структуру данных."""
        filtered_data = original_data.copy()
        
        # Обновляем product_list в корне или субключах
        if "product_list" in filtered_data:
            filtered_data["product_list"] = filtered_products
        else:
            # Ищем в субключах
            for key, value in filtered_data.items():
                if isinstance(value, dict) and "product_list" in value:
                    filtered_data[key]["product_list"] = filtered_products
                    break
        
        return filtered_data
    
    def _has_filtered_products(self, filtered_data: Dict, original_data: Dict) -> bool:
        """Проверяет, есть ли отфильтрованные продукты."""
        filtered_products = self._extract_product_list(filtered_data)
        return len(filtered_products) > 0
    
    def _create_fallback_result(self, original_data: Dict, reason: str) -> ToolCallResult:
        """Создает результат fallback с исходными данными."""
        return ToolCallResult(
            success=False,
            filtered_data=original_data,  # ВСЕ исходные данные из selected_key
            applied_filters={},
            error_message=f"Tool Calling fallback: {reason}",
            metadata={
                "subsector_id": self.subsector_id,
                "fallback": True,
                "fallback_reason": reason
            }
        )
