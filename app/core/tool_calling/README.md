# Архитектура и руководство по модулю Tool Calling

## 1. Назначение модуля

Модуль **Tool Calling** представляет собой систему расширенной фильтрации данных на основе семантического анализа пользовательского запроса. Его основная задача — не просто найти релевантный документ (как это делают предыдущие шаги пайплайна), а "понять" конкретные критерии внутри запроса (например, "ищу соус без глютена", "покажи топпинги с калорийностью до 300 ккал") и применить их для фильтрации списка продуктов.

Это позволяет значительно повысить точность ответа, предоставляя пользователю не весь список товаров из категории, а только те, что соответствуют его неявным или явным требованиям.

С августа 2025 года система использует **универсальную архитектуру** с единым обработчиком `UniversalIndustryHandler`, который динамически загружает маппинги для любой отрасли, что значительно упрощает добавление новых отраслей.

## 2. Новая универсальная архитектура

Модуль полностью переработан для использования **Factory Pattern** с единым универсальным обработчиком:

```
app/core/tool_calling/
├── README.md                      # Этот файл  
├── __init__.py                    # Экспорт ToolService
├── service.py                     # ♠️ ToolService - Главный оркестратор
├── registry.py                    # ♣️ HandlerRegistry - Реестр отраслей
├── universal_handler.py           # ♥️ UniversalIndustryHandler - Единый обработчик
├── base/                          # Базовые классы и типы
│   ├── handler.py                 # BaseToolHandler (для совместимости)
│   └── types.py                   # Общие структуры данных
├── .backup/                       # Backup старых хендлеров
│   └── README.md                  # Инструкции по восстановлению
├── horeca/                        # ♦️ HoReCa mappings в новом формате
│   ├── __init__.py
│   └── mappings/
│       ├── keys.py                # Структура полей продуктов
│       ├── enums.py               # Enum значения (с субключами)
│       └── universal.py           # Паттерны для фильтрации
└── milk/                          # ♦️ Молочная отрасль mappings  
    ├── __init__.py
    └── mappings/
        ├── keys.py                # Структура полей продуктов
        ├── enums.py               # Enum значения (с субключами) 
        └── universal.py           # Паттерны для фильтрации
```

### Ключевые компоненты новой архитектуры:

-   **`ToolService` (`service.py`)**:
    -   **Единая точка входа** для всего пайплайна (`handle_tool_calling`).
    -   Проверяет, поддерживается ли Tool Calling для данной отрасли (`is_supported`).
    -   Создает единый `UniversalIndustryHandler` для всех отраслей.
    -   Координирует весь процесс от генерации схем до фильтрации данных.
    -   Реализует **Graceful Fallback**: при любой ошибке возвращает исходные данные.

-   **`HandlerRegistry` (`registry.py`)**:
    -   Реестр поддерживаемых отраслей с их `subsector_id`.
    -   Хранит соответствие `subsector_id → industry_name` (например, `"01": "horeca"`).
    -   Автоматически определяет доступные отрасли по наличию папок с mappings.

-   **`UniversalIndustryHandler` (`universal_handler.py`)**:
    -   **Единый обработчик** для всех отраслей, заменивший индивидуальные хендлеры.
    -   Использует **Factory Pattern** и **IndustryMappingsLoader** для динамической загрузки.
    -   Ключевые возможности:
        - Динамическая генерация OpenAI tool схем на основе структуры данных
        - Поддержка **субключей** для сложных JSON структур
        - **Strict mode** для точного соответствия схем
        - Умная фильтрация с regex и текстовыми паттернами
        - Автоматическое определение типов полей (string, number, array)

-   **`IndustryMappingsLoader`**:
    -   Динамически загружает mappings для любой отрасли через `importlib`.
    -   Автоматически импортирует `keys.py`, `enums.py`, `universal.py`.
    -   Обеспечивает изоляцию между отраслями.

-   **Mappings отрасли (например, `horeca/mappings/`)**:
    -   **`keys.py`**: Описывает структуру полей продуктов, `KEY_TO_FILE_MAPPING` для субключей.
    -   **`enums.py`**: Enum значения в новом формате с поддержкой субключей и категорий.
    -   **`universal.py`**: Паттерны поиска, regex функции, специальные чекеры для числовых значений.

## 3. Универсальный процесс работы (Workflow)

С новой архитектурой workflow значительно упрощен благодаря единому `UniversalIndustryHandler`.

### 📝 **Пример запроса пользователя:**
```
"Покажи мне низкокалорийные соусы Millgri в пластиковых бутылках"
```

**Контекст:**
- `subsector_id = "01"` (HoReCa)
- `selected_key = "ready_sauces"` (выбранный на предыдущих этапах пайплайна)
- Данные из файла `ready_sauces.json` уже загружены

---

### 🔄 **Детальный пошаговый процесс:**

#### **Шаг 1: Инициализация и проверка поддержки**
```python
# engine.py (в рамках обработки запроса)
tool_service = ToolService(llm_service=client)
if tool_service.is_supported(query.subsector_id):  # "01"
```

**Что происходит:**
- `ToolService` проверяет `HandlerRegistry.is_supported("01")`
- Реестр определяет отрасль как `"horeca"` для subsector_id="01"
- ✅ **Результат:** Tool Calling поддерживается для HoReCa

#### **Шаг 2: Создание универсального обработчика**
```python
# service.py
handler = UniversalIndustryHandler(
    subsector_id="01",
    industry_name="horeca", 
    llm_service=client
)
```

**Что происходит:**
- Создается единый `UniversalIndustryHandler` для обработки любой отрасли
- `IndustryMappingsLoader` динамически загружает HoReCa mappings

#### **Шаг 3: Динамическая загрузка маппингов**
```python
# universal_handler.py
self.mappings_loader = IndustryMappingsLoader()
mappings = self.mappings_loader.load_mappings(industry_name)  # "horeca"
```

**Что происходит:**
- Динамически импортируются модули `horeca.mappings.keys`, `horeca.mappings.enums`, `horeca.mappings.universal`
- Загружаются: `HORECA_KEYS_MAPPING`, `HORECA_ENUM_MAPPING`, функции фильтрации

#### **Шаг 4: Генерация динамических tool схем**
```python  
# universal_handler.py:generate_tool_schemas()
schemas = handler.generate_tool_schemas(data, selected_key)  # "ready_sauces"
```

**Детальный процесс генерации схем:**

**4.1. Определение файла и субключа:**
```python
# Проверка, является ли selected_key субключом
file_name = mappings.KEY_TO_FILE_MAPPING.get(selected_key)
if file_name:
    # selected_key является субключом (например, aromatic_emulsions)
    actual_file_name = file_name
    is_subkey = True
else:
    # selected_key - это прямой файл (например, ready_sauces)
    actual_file_name = f"{selected_key}.json"
    is_subkey = False
```

**4.2. Загрузка структуры полей:**
```python
# Из horeca/mappings/keys.py
file_keys = mappings.keys_mapping[actual_file_name]
# Получаем:
{
    "product_keys": {
        "name": {"description": "Название готового соуса", ...},
        "kbgu": {"description": "Калорийность и пищевая ценность", ...},
        "packaging": {"description": "Упаковка готовых соусов", ...}
    }
}
```

**4.3. Загрузка enum значений:**
```python
# Из horeca/mappings/enums.py
file_enums = mappings.enum_mapping[actual_file_name]
# Получаем структуру с субключами:
{
    "name": {
        "sauce_types": ["горчичный", "барбекю", "сырный", "майонезный"],  
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

**4.4. Формирование OpenAI tool схемы с strict mode:**
```python
# universal_handler.py
properties[key_name] = {
    "type": "string",
    "description": f"{key_info['description']}. {key_info['filter_impact']}",
    "enum": list(set(all_enum_values))  # Уникальные значения из всех категорий
}
required_fields = []  # Strict mode требует пустой список required
```

**Итоговая tool схема (с strict mode):**
```json
{
    "type": "function",
    "function": {
        "name": "filter_horeca_products", 
        "description": "Универсальный фильтр для продуктов отрасли horeca из файла ready_sauces.json",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Название готового соуса. Позволяет искать по типу соуса и бренду",
                    "enum": ["горчичный", "барбекю", "сырный", "майонезный", "кетчуп", "Millgri", "КЛАССИКА", "соус"]
                },
                "kbgu": {
                    "type": "string", 
                    "description": "Калорийность и пищевая ценность соуса. Позволяет фильтровать по диапазонам калорийности",
                    "enum": ["низкие_до_150", "средние_150_250", "высокие_250_400", "обезжиренные", "низкожирные_до_15"]
                },
                "packaging": {
                    "type": "string",
                    "description": "Упаковка готовых соусов. Позволяет искать по типу упаковки",
                    "enum": ["бутылка_пластиковая", "bag_in_box", "блистер", "дой_пак"]
                }
            },
            "required": [],
            "additionalProperties": false
        },
        "strict": true
    }
}
```

#### **Шаг 5: Вызов LLM для анализа запроса**
```python
# universal_handler.py:call_llm_with_tools()
response = self.llm_service.chat.completions.create(
    model=LLM_MODEL,  # Из настроек
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ],
    tools=llm_tools,  # Наша сгенерированная схема
    tool_choice="auto"
)
```

**Универсальный системный промпт:**
```
Ты - эксперт по анализу запросов пользователей для системы фильтрации товаров отрасли {industry_name}.
Проанализируй пользовательский запрос и выбери подходящие параметры фильтрации из доступных инструментов.

Твоя задача - точно извлечь критерии поиска и сопоставить их с enum значениями в схеме.
```

**Анализ LLM (с новыми enum значениями):**
- 🔍 "низкокалорийные" → `kbgu: "низкие_до_150"`
- 🔍 "Millgri" → `name: "Millgri"`  
- 🔍 "пластиковых бутылках" → `packaging: "бутылка_пластиковая"`

#### **Шаг 6: Парсинг ответа LLM**
```python
# universal_handler.py:parse_llm_response()
tool_call = response.choices[0].message.tool_calls[0] 
tool_name = tool_call.function.name  # "filter_horeca_products"
tool_params = json.loads(tool_call.function.arguments)

# Результат (структурированные параметры):
{
    "kbgu": "низкие_до_150",
    "name": "Millgri", 
    "packaging": "бутылка_пластиковая"
}
```

#### **Шаг 7: Универсальная фильтрация данных**
```python
# universal_handler.py:filter_data_by_criteria()
filtered_products = list(product_list)  # Копируем список
for filter_key, enum_value in tool_params.items():
    filtered_products = self.apply_single_filter(
        filtered_products, 
        filter_key,     # "kbgu", "name", "packaging"
        enum_value,     # "низкие_до_150", "Millgri", "бутылка_пластиковая"
        self.mappings   # Загруженные mappings отрасли
    )
```

**Детали универсальной фильтрации для каждого критерия:**

**7.1. Фильтрация по калорийности (`kbgu: "низкие_до_150"`):**
```python
# universal_handler.py:apply_single_filter()
# Используем универсальные функции из mappings.universal
if hasattr(mappings.universal, 'has_universal_enum_match'):
    match_found = mappings.universal.has_universal_enum_match(
        product_field_text,  # "КДж/ккал – 865/207" 
        enum_value,          # "низкие_до_150"
        field_key           # "kbgu"
    )
    
# Внутри horeca/mappings/universal.py:
# UNIVERSAL_KBGU_CHECKERS["низкие_до_150"](text) → check_calorie_range(text, 0, 150)
# calories = 207 → return 207 <= 150 → False (продукт не проходит фильтр)
```

**7.2. Фильтрация по бренду (`name: "Millgri"`):**
```python
# universal_handler.py использует текстовые паттерны
patterns = mappings.universal.get_universal_patterns("Millgri")
# Возвращает: ["Millgri®", "Millgri", "MILLGRI", "millgri"]

# Проверка в названии продукта:
product_name = "Соус на основе растительных масел «Горчичный» Millgri®"
for pattern in patterns:
    if pattern.lower() in product_name.lower():  
        return True  # Найден "Millgri" → продукт проходит фильтр
```

**7.3. Фильтрация по упаковке (`packaging: "бутылка_пластиковая"`):**
```python  
patterns = mappings.universal.get_universal_patterns("бутылка_пластиковая")
# Возвращает: ["Бутылка пластиковая", "бутылка пластиковая", "Бутылка", "пластиковая"]

# Проверка в описании упаковки:
packaging_text = "Бутылка пластиковая объемом 0,8 л"
for pattern in patterns:
    if pattern.lower() in packaging_text.lower():
        return True  # Найдена "бутылка пластиковая" → продукт проходит фильтр
```

#### **Шаг 8: Формирование результата**
```python
# universal_handler.py:process()
# Создаем копию данных с отфильтрованными продуктами
filtered_data = data.copy()
filtered_data[product_list_key] = filtered_products

# Логирование результатов через универсальный logger
self.logger.info(f"Отфильтровано продуктов: {len(filtered_products)} из {len(original_products)}")
self.logger.info(f"Применены фильтры: {tool_params}")
```

**Пример результата фильтрации:**
```python
# Было: 50 соусов в ready_sauces.json
# Применены фильтры: {"kbgu": "низкие_до_150", "name": "Millgri", "packaging": "бутылка_пластиковая"}  
# Стало: 2 соуса (1 продукт отфильтрован по калорийности)

[
    '{"name": "Соус на основе растительных масел «Горчичный» Millgri®", "kbgu": "КДж/ккал – 865/109", "packaging": "Бутылка пластиковая объемом 0,8 л"}',
    '{"name": "Соус «Сырный» Millgri®", "kbgu": "КДж/ккал – 623/148", "packaging": "Бутылка пластиковая объемом 0,8 л"}'
]
```

#### **Шаг 9: Возврат в основной пайплайн**
```python
# service.py:handle_tool_calling()
result = handler.process(user_query, data, selected_key)
if result.success:
    logger.info(f"✅ Tool Calling успешен для {subsector_id}")
    return result.filtered_data
else:
    logger.warning(f"⚠️ Tool Calling неуспешен, возвращаем исходные данные")
    return data  # Graceful fallback
```

**Структура ToolCallResult (новая):**
```python
ToolCallResult(
    success=True,
    filtered_data=filtered_data,  # Отфильтрованные данные
    applied_filters=tool_params,  # Параметры от LLM: {"kbgu": "низкие_до_150", ...}
    metadata={
        "subsector_id": "01",
        "industry_name": "horeca",
        "tool_name": f"filter_{industry_name}_products", 
        "selected_key": "ready_sauces",
        "handler_type": "UniversalIndustryHandler",
        "original_count": 50,
        "filtered_count": 2
    }
)
```

---

### 🎯 **Ключевые особенности новой универсальной архитектуры:**

1. **Единый обработчик** - `UniversalIndustryHandler` заменяет все индивидуальные хендлеры
2. **Динамическая загрузка** - `IndustryMappingsLoader` подгружает mappings через `importlib` 
3. **Поддержка субключей** - `KEY_TO_FILE_MAPPING` для сложных JSON структур
4. **Strict mode** - точное соответствие OpenAI схем требованиям 
5. **Graceful fallback** - при любой ошибке возвращаются исходные данные
6. **Расширяемость** - добавление новой отрасли требует только создания папки mappings
7. **Изоляция отраслей** - каждая отрасль полностью независима

## 4. Руководство: Как добавить поддержку новой отрасли

Благодаря универсальной архитектуре, добавление новой отрасли стало намного проще. Рассмотрим на примере отрасли "Напитки" (`drinks`) с `subsector_id="05"`.

### Шаг 1: Создание структуры mappings

Создайте новую папку `drinks` внутри `app/core/tool_calling/`:

```
app/core/tool_calling/
└── drinks/                        # Новая отрасль
    ├── __init__.py                 # Пустой файл (для импорта)
    └── mappings/                   # Mappings для отрасли
        ├── keys.py                 # Структура полей продуктов
        ├── enums.py                # Enum значения с субключами
        └── universal.py            # Паттерны для фильтрации
```

**Важно:** Больше не нужны `service.py`, `data_filter.py` - они заменены универсальным обработчиком!

### Шаг 2: Реализация `mappings/keys.py`

Изучите JSON-файлы с данными о напитках и опишите их структуру в новом формате:

```python
# app/core/tool_calling/drinks/mappings/keys.py
"""
Маппинг ключей продуктов для каждого JSON файла drinks отрасли.
"""

# Маппинг ключей продуктов для каждого файла
DRINKS_KEYS_MAPPING = {
    "juices.json": {
        "file_description": "Соки и нектары для HoReCa",
        "product_keys": {
            "name": {
                "description": "Название напитка",
                "filter_impact": "Позволяет искать по типу напитка и бренду",
                "data_type": "string"
            },
            "sugar_content": {
                "description": "Содержание сахара",
                "filter_impact": "Позволяет фильтровать по уровню сахара",
                "data_type": "string"
            }
        }
    }
}

# Маппинг selected_key к файлам для субключей (если есть сложные структуры)
KEY_TO_FILE_MAPPING = {
    "fruit_juices": "juices.json",
    "vegetable_juices": "juices.json"
}

# Экспорт для универсального загрузчика
keys_mapping = DRINKS_KEYS_MAPPING
```

### Шаг 3: Реализация `mappings/enums.py`

Создайте enum значения в новом формате с поддержкой субключей:

```python
# app/core/tool_calling/drinks/mappings/enums.py
"""
Enum значения для создания динамических tool схем для drinks отрасли.
Новый формат с субключами и категориями.
"""

# Enum значения для каждого файла
DRINKS_ENUM_MAPPING = {
    "juices.json": {
        "name": {
            "drink_types": ["сок", "нектар", "морс", "компот"],
            "fruit_types": ["яблочный", "апельсиновый", "виноградный", "вишневый"],
            "brands": ["Rich", "Sandora", "Наш Сок"]
        },
        "sugar_content": {
            "sugar_levels": ["без_сахара", "низкое_содержание", "среднее_содержание", "высокое_содержание"]
        }
    }
}

# Экспорт для универсального загрузчика
enum_mapping = DRINKS_ENUM_MAPPING
```

### Шаг 4: Реализация `mappings/universal.py`

Создайте паттерны для фильтрации, следуя образцу из HoReCa/Milk:

```python
# app/core/tool_calling/drinks/mappings/universal.py
"""
Универсальные паттерны для фильтрации напитков.
"""
import re
from typing import List, Dict, Callable

# Специфичные маппинги для напитков
DRINKS_SPECIFIC_MAPPING: Dict[str, List[str]] = {
    "сок": ["СОК", "сок", "Сок"],
    "нектар": ["НЕКТАР", "нектар", "Нектар"],
    "без_сахара": ["без сахара", "БЕЗ САХАРА", "sugar free"],
    "яблочный": ["ЯБЛОЧНЫЙ", "яблочный", "яблоко"],
    "Rich": ["Rich", "RICH", "Рич"]
}

# Regex для содержания сахара
SUGAR_CONTENT_REGEX = re.compile(r"сахар.*?(\d+(?:,\d+)?)", re.IGNORECASE)

def get_universal_patterns(enum_value: str) -> List[str]:
    """Возвращает паттерны поиска для enum значения."""
    return DRINKS_SPECIFIC_MAPPING.get(enum_value, [enum_value])

def has_universal_enum_match(text: str, enum_value: str, field_key: str = None) -> bool:
    """Универсальная проверка совпадения enum значения с текстом."""
    patterns = get_universal_patterns(enum_value)
    text_lower = text.lower()
    
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return True
    return False
```

### Шаг 5: Регистрация новой отрасли

**Единственное изменение в коде** - обновите реестр отраслей:

```python
# app/core/tool_calling/registry.py
class HandlerRegistry:
    def __init__(self):
        self.supported_industries = {
            "01": "horeca",
            "02": "milk", 
            "05": "drinks"  # <-- Добавляем новую отрасль
        }
```

**Готово!** 🎉 

Универсальная архитектура автоматически:
- Обнаружит папку `drinks/mappings/`
- Загрузит все mappings через `IndustryMappingsLoader`
- Создаст `UniversalIndustryHandler` для отрасли `drinks`
- Сгенерирует динамические tool схемы
- Применит фильтрацию через универсальную логику

**Время реализации:** 30-60 минут вместо 2-4 часов!
