# Универсальный Workflow Tool Calling

## Обзор

Этот документ описывает пошаговый процесс работы **универсальной архитектуры Tool Calling** с единым `UniversalIndustryHandler`. Архитектура была переработана в августе 2025 года для упрощения добавления новых отраслей и обеспечения консистентности обработки данных.

## Основные принципы новой архитектуры

### 1. Factory Pattern
- **Единый обработчик** `UniversalIndustryHandler` заменяет все индивидуальные хендлеры
- **Динамическая загрузка** mappings через `IndustryMappingsLoader`
- **Изоляция отраслей** - каждая отрасль содержит только свои mappings

### 2. Поддерживаемые отрасли
- **HoReCa** (`subsector_id: "01"`, `industry_name: "horeca"`)
- **Молочная отрасль** (`subsector_id: "02"`, `industry_name: "milk"`)
- **Готово для расширения** - добавление новой отрасли займет 30-60 минут

### 3. Структура mappings
```
industry_name/
└── mappings/
    ├── keys.py      # Структура полей продуктов + KEY_TO_FILE_MAPPING
    ├── enums.py     # Enum значения с субключами для OpenAI schemas
    └── universal.py # Паттерны фильтрации и regex функции
```

---

## Пошаговый Workflow

### Этап 1: Инициализация
```python
# В engine.py при обработке запроса
tool_service = ToolService(llm_service=client)
```

**Что происходит:**
- Создается `HandlerRegistry` с маппингом `subsector_id → industry_name`
- Реестр определяет поддерживаемые отрасли: `{"01": "horeca", "02": "milk"}`

### Этап 2: Проверка поддержки отрасли
```python
if tool_service.is_supported(subsector_id):  # Например: "01"
```

**Что происходит:**
- `HandlerRegistry.is_supported("01")` → `True` (HoReCa поддерживается)
- Определяется `industry_name = "horeca"`

### Этап 3: Создание универсального обработчика
```python
# В ToolService.handle_tool_calling()
handler = UniversalIndustryHandler(
    subsector_id="01",
    industry_name="horeca", 
    llm_service=self.llm_service
)
```

**Что происходит:**
- Создается единый обработчик для любой отрасли
- `IndustryMappingsLoader` начинает процесс динамической загрузки

### Этап 4: Динамическая загрузка mappings
```python
# В UniversalIndustryHandler.__init__()
self.mappings = IndustryMappingsLoader().load_mappings("horeca")
```

**Детали загрузки:**
```python
# IndustryMappingsLoader автоматически импортирует:
- horeca.mappings.keys     → mappings.keys_mapping, KEY_TO_FILE_MAPPING
- horeca.mappings.enums    → mappings.enum_mapping  
- horeca.mappings.universal → mappings.universal (функции фильтрации)
```

### Этап 5: Обработка запроса
```python
result = handler.process(user_query, data, selected_key)
```

**Входные данные:**
- `user_query`: "Покажи низкокалорийные соусы Millgri в пластиковых бутылках"
- `data`: Загруженные данные из JSON файла
- `selected_key`: "ready_sauces" (определен на предыдущих этапах пайплайна)

### Этап 6: Определение файла и субключей
```python
# UniversalIndustryHandler.process()
file_name = self.mappings.KEY_TO_FILE_MAPPING.get(selected_key)
if file_name:
    # selected_key является субключом (например, "aromatic_emulsions")
    actual_file = file_name      # "delar_flavor_collection.json"
    is_subkey = True
else:
    # selected_key соответствует файлу (например, "ready_sauces")
    actual_file = f"{selected_key}.json"  # "ready_sauces.json"
    is_subkey = False
```

### Этап 7: Генерация динамических tool схем
```python
schemas = self.generate_tool_schemas(data, selected_key)
```

**Процесс генерации схем:**

**7.1. Загрузка структуры полей:**
```python
file_info = self.mappings.keys_mapping[actual_file]
# Получаем из horeca/mappings/keys.py:
{
    "file_description": "Готовые соусы для HoReCa",
    "product_keys": {
        "name": {"description": "Название соуса", "filter_impact": "..."},
        "kbgu": {"description": "Калорийность", "filter_impact": "..."},
        "packaging": {"description": "Упаковка", "filter_impact": "..."}
    }
}
```

**7.2. Загрузка enum значений:**
```python
file_enums = self.mappings.enum_mapping[actual_file]
# Получаем из horeca/mappings/enums.py (новый формат с субключами):
{
    "name": {
        "sauce_types": ["горчичный", "барбекю", "сырный"],
        "brands": ["Millgri", "КЛАССИКА"]
    },
    "kbgu": {
        "calorie_ranges": ["низкие_до_150", "средние_150_250", "высокие_250_400"]
    },
    "packaging": {
        "package_types": ["бутылка_пластиковая", "bag_in_box", "блистер"]
    }
}
```

**7.3. Создание OpenAI tool схемы (strict mode):**
```python
# Объединяем все enum значения из категорий
for field_name, field_info in product_keys.items():
    all_enums = []
    for category, values in file_enums[field_name].items():
        all_enums.extend(values)
    
    properties[field_name] = {
        "type": "string",
        "description": f"{field_info['description']}. {field_info['filter_impact']}",
        "enum": list(set(all_enums))  # Уникальные значения
    }

schema = {
    "type": "function", 
    "function": {
        "name": f"filter_{self.industry_name}_products",
        "description": f"Универсальный фильтр для отрасли {self.industry_name}",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": [],  # Strict mode требует пустой список
            "additionalProperties": false
        },
        "strict": true
    }
}
```

### Этап 8: Вызов LLM для анализа запроса
```python
response = self.call_llm_with_tools(user_query, schemas)
```

**Системный промпт:**
```
Ты - эксперт по анализу запросов для системы фильтрации товаров отрасли {industry_name}.
Проанализируй пользовательский запрос и выбери подходящие параметры фильтрации.
```

**Анализ LLM:**
```json
// Запрос: "низкокалорийные соусы Millgri в пластиковых бутылках"
{
    "kbgu": "низкие_до_150",      // "низкокалорийные"
    "name": "Millgri",            // "Millgri" 
    "packaging": "бутылка_пластиковая"  // "пластиковых бутылках"
}
```

### Этап 9: Универсальная фильтрация данных
```python
filtered_data = self.filter_data_by_criteria(data, tool_params, selected_key)
```

**Процесс фильтрации:**
```python
# Получаем список продуктов
product_list = self.extract_product_list(data, selected_key)

# Применяем каждый фильтр
filtered_products = list(product_list)
for field_key, enum_value in tool_params.items():
    filtered_products = self.apply_single_filter(
        filtered_products, field_key, enum_value
    )
```

**Детали фильтрации по критериям:**

**9.1. Фильтрация по калорийности:**
```python
# Используем универсальные функции из horeca/mappings/universal.py
has_match = self.mappings.universal.has_universal_enum_match(
    product_field_text,  # "КДж/ккал – 865/109"
    enum_value,          # "низкие_до_150"  
    field_key           # "kbgu"
)

# Внутри horeca/mappings/universal.py вызывается:
# check_calorie_range(text, 0, 150) → calories = 109 → 109 <= 150 → True
```

**9.2. Фильтрация по тексту (бренд, упаковка):**
```python
patterns = self.mappings.universal.get_universal_patterns("Millgri")
# Возвращает: ["Millgri®", "Millgri", "MILLGRI"]

for pattern in patterns:
    if pattern.lower() in product_text.lower():
        return True  # Совпадение найдено
```

### Этап 10: Формирование результата
```python
# Создаем структуру результата
result = ToolCallResult(
    success=True,
    filtered_data=filtered_data,
    applied_filters=tool_params,
    metadata={
        "subsector_id": self.subsector_id,
        "industry_name": self.industry_name, 
        "tool_name": f"filter_{self.industry_name}_products",
        "selected_key": selected_key,
        "handler_type": "UniversalIndustryHandler",
        "original_count": len(original_products),
        "filtered_count": len(filtered_products)
    }
)
```

### Этап 11: Возврат в основной пайплайн
```python
# В ToolService.handle_tool_calling()
if result.success:
    logger.info(f"✅ Tool Calling успешен для {subsector_id}")
    return result.filtered_data  # Отфильтрованные данные
else:
    logger.warning("⚠️ Tool Calling неуспешен, возвращаем исходные данные")
    return data  # Graceful fallback
```

---

## Добавление новой отрасли: Пошаговая инструкция

### Время реализации: 30-60 минут ⚡

### Шаг 1: Создание структуры mappings
```bash
mkdir app/core/tool_calling/новая_отрасль/
mkdir app/core/tool_calling/новая_отрасль/mappings/
touch app/core/tool_calling/новая_отрасль/__init__.py
```

### Шаг 2: Реализация mappings/keys.py
```python
# Структура полей продуктов + субключи
ОТРАСЛЬ_KEYS_MAPPING = {
    "products.json": {
        "file_description": "Описание продуктов отрасли",
        "product_keys": {
            "name": {
                "description": "Название продукта",
                "filter_impact": "Позволяет искать по названию и бренду",
                "data_type": "string"
            }
        }
    }
}

# Маппинг для сложных структур (если нужно)
KEY_TO_FILE_MAPPING = {
    "subkey1": "products.json",
    "subkey2": "products.json"
}

# Обязательный экспорт
keys_mapping = ОТРАСЛЬ_KEYS_MAPPING
```

### Шаг 3: Реализация mappings/enums.py
```python
# Enum значения с субключами
ОТРАСЛЬ_ENUM_MAPPING = {
    "products.json": {
        "name": {
            "categories": ["категория1", "категория2"],
            "brands": ["бренд1", "бренд2"]
        }
    }
}

# Обязательный экспорт
enum_mapping = ОТРАСЛЬ_ENUM_MAPPING
```

### Шаг 4: Реализация mappings/universal.py
```python
# Паттерны для фильтрации
ОТРАСЛЬ_SPECIFIC_MAPPING = {
    "категория1": ["КАТЕГОРИЯ1", "категория1"],
    "бренд1": ["БРЕНД1", "бренд1", "Brand1"]
}

def get_universal_patterns(enum_value: str):
    return ОТРАСЛЬ_SPECIFIC_MAPPING.get(enum_value, [enum_value])

def has_universal_enum_match(text: str, enum_value: str, field_key: str = None):
    patterns = get_universal_patterns(enum_value)
    text_lower = text.lower()
    return any(pattern.lower() in text_lower for pattern in patterns)
```

### Шаг 5: Регистрация в реестре
```python
# app/core/tool_calling/registry.py
class HandlerRegistry:
    def __init__(self):
        self.supported_industries = {
            "01": "horeca",
            "02": "milk",
            "XX": "новая_отрасль"  # Добавить новую отрасль
        }
```

### Готово! 🎉

Универсальная архитектура автоматически:
- ✅ Обнаружит новую папку mappings
- ✅ Загрузит все mappings через `IndustryMappingsLoader` 
- ✅ Создаст `UniversalIndustryHandler` для новой отрасли
- ✅ Сгенерирует динамические tool схемы
- ✅ Применит фильтрацию через универсальную логику

**Никаких дополнительных классов, сервисов или фильтров не требуется!**

---

## Graceful Fallback

Система обеспечивает надежность через **Graceful Fallback**:

### Уровень 1: ToolService
- Если отрасль не поддерживается → возврат исходных данных
- Если произошла ошибка в процессе → возврат исходных данных

### Уровень 2: UniversalIndustryHandler  
- Если mappings не загружены → возврат исходных данных
- Если LLM не выбрал инструмент → возврат исходных данных
- Если произошла ошибка фильтрации → возврат исходных данных

### Уровень 3: IndustryMappingsLoader
- Если модуль не найден → логирование ошибки + fallback
- Если атрибут отсутствует → логирование предупреждения + fallback

**Результат:** Tool Calling никогда не ломает основной пайплайн!

---

## Преимущества универсальной архитектуры

### 🚀 **Скорость разработки**
- Добавление новой отрасли: **30-60 минут** (было 2-4 часа)
- Только mappings, никаких дополнительных классов

### 🏗️ **Архитектурная чистота**
- Единый обработчик для всех отраслей
- Полная изоляция mappings между отраслями
- Factory Pattern для масштабируемости

### 🔧 **Простота поддержки**  
- Изменения в одной отрасли не влияют на другие
- Единая логика фильтрации и генерации схем
- Централизованное логирование и обработка ошибок

### 📊 **Консистентность данных**
- Единый формат mappings для всех отраслей
- Стандартизованные tool схемы с strict mode
- Унифицированная структура результатов

---

## Архитектурные решения

### Factory Pattern
- `UniversalIndustryHandler` создает обработчик для любой отрасли
- `IndustryMappingsLoader` динамически загружает нужные mappings
- Полное разделение бизнес-логики и конфигурации

### Dependency Injection
- LLM сервис инжектится в обработчик
- Mappings загружаются динамически по требованию
- Полная тестируемость всех компонентов

### Strategy Pattern
- Разные отрасли = разные стратегии фильтрации
- Единый интерфейс для всех стратегий
- Легкое переключение между отраслями

Этот документ отражает текущую архитектуру Tool Calling и будет обновляться по мере развития системы.