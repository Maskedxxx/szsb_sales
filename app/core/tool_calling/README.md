# Архитектура и руководство по модулю Tool Calling

## 1. Назначение модуля

Модуль **Tool Calling** представляет собой систему расширенной фильтрации данных на основе семантического анализа пользовательского запроса. Его основная задача — не просто найти релевантный документ (как это делают предыдущие шаги пайплайна), а "понять" конкретные критерии внутри запроса (например, "ищу соус без глютена", "покажи топпинги с калорийностью до 300 ккал") и применить их для фильтрации списка продуктов.

Это позволяет значительно повысить точность ответа, предоставляя пользователю не весь список товаров из категории, а только те, что соответствуют его неявным или явным требованиям.

Система спроектирована как расширяемая, позволяя легко добавлять поддержку новых отраслей со своей уникальной логикой фильтрации.

## 2. Архитектура

Модуль имеет четкую иерархическую структуру, разработанную для изоляции логики каждой отрасли и обеспечения легкой расширяемости.

```
app/core/tool_calling/
├── README.md                      # Этот файл
├── __init__.py                    # Экспорт ToolService для доступа извне
├── service.py                     # ♠️ ToolService - Главный оркестратор и точка входа
├── registry.py                    # ♣️ HandlerRegistry - Реестр доступных обработчиков отраслей
├── base/                          # Абстрактные классы и общие типы
│   ├── handler.py                 # ♥️ BaseToolHandler - "Контракт", который должен выполнять каждый обработчик
│   └── types.py                   # Общие структуры данных (например, FilterArgument)
└── horeca/                        # ♦️ Модуль для отрасли HoReCa (пример реализации)
    ├── __init__.py
    ├── service.py                 # HoReCaHandler - Конкретная реализация логики для HoReCa
    ├── data_filter.py             # Логика фильтрации данных для HoReCa
    └── mappings/                  # Описание данных и правил для HoReCa
        ├── keys.py                # Структура ключей в JSON-файлах HoReCa
        ├── enums.py               # Enum-значения для генерации схем (например, список аллергенов)
        └── universal.py           # Паттерны для извлечения значений (regex для чисел, синонимы и т.д.)
```

### Ключевые компоненты:

-   **`ToolService` (`service.py`)**:
    -   **Единая точка входа** для всего пайплайна (`handle_tool_calling`).
    -   Проверяет, поддерживается ли Tool Calling для данной отрасли (`is_supported`).
    -   Получает из реестра нужный обработчик (`handler`).
    -   Вызывает LLM с динамически сгенерированными "инструментами" (схемами).
    -   Обрабатывает ответ LLM, извлекая аргументы для фильтрации.
    -   Вызывает метод `filter_data` у обработчика.
    -   Реализует **Graceful Fallback**: если что-то идет не так (LLM не выбрал инструмент, произошла ошибка), система просто возвращает исходные, нефильтрованные данные, не прерывая основной процесс.

-   **`HandlerRegistry` (`registry.py`)**:
    -   Простой класс, который хранит соответствие между `subsector_id` и классом-обработчиком (например, `"01": HoReCaHandler`).
    -   Загружает и регистрирует все обработчики при инициализации `ToolService`.

-   **`BaseToolHandler` (`base/handler.py`)**:
    -   Абстрактный базовый класс, определяющий "интерфейс" для всех отраслевых обработчиков.
    -   Требует от наследников реализации двух ключевых методов:
        1.  `generate_tool_schemas(self, data: Dict) -> List[Dict]`: Метод, который анализирует данные из JSON-файла и создает на их основе OpenAI Tool-схемы. Именно здесь определяется, по каким полям можно фильтровать и какие значения они могут принимать.
        2.  `filter_data(self, data: Dict, tool_args: List[FilterArgument]) -> Dict`: Метод, который принимает исходные данные и извлеченные из LLM аргументы, а затем применяет логику фильтрации.

-   **Отраслевой модуль (например, `horeca/`)**:
    -   **`service.py` (например, `HoReCaHandler`)**: Конкретная реализация `BaseToolHandler`. Здесь "оживает" вся логика для конкретной отрасли.
    -   **`data_filter.py`**: Содержит чистые функции для фильтрации. Например, `filter_by_text`, `filter_by_numeric_range`. Это позволяет держать логику фильтрации отделенной от основной логики обработчика.
    -   **`mappings/`**: "База знаний" об устройстве данных в отрасли.
        -   `keys.py`: Описывает, какие ключи в JSON-файле содержат информацию о продуктах, их характеристики и т.д.
        -   `enums.py`: Определяет возможные категориальные значения для полей (например, `Allergen(Enum)`), которые используются для генерации `enum` в схемах.
        -   `universal.py`: Содержит регулярные выражения и списки слов для извлечения и нормализации данных из запроса пользователя (например, как найти калорийность, вес, или понять, что "без сахара" означает `sugar_free`).

## 3. Пошаговый процесс работы (Workflow)

Рассмотрим полный workflow Tool Calling на конкретном примере HoReCa.

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
# engine.py:255
tool_service = ToolService(llm_service=client)
if tool_service.is_supported(query.subsector_id):  # "01"
```

**Что происходит:**
- `ToolService` проверяет `HandlerRegistry.is_supported("01")`
- В реестре найден `HoReCaHandler` для subsector_id="01"
- ✅ **Результат:** Tool Calling поддерживается для HoReCa

#### **Шаг 2: Получение обработчика отрасли**
```python
# service.py:78
handler = self.registry.get_handler(subsector_id)  # получаем HoReCaHandler
```

**Что происходит:**
- Создается экземпляр `HoReCaHandler("01", llm_service=client)`
- Инициализируется logger для данной отрасли

#### **Шаг 3: Генерация динамических tool схем**
```python
# service.py:91 -> horeca/service.py:69
schemas = handler.generate_schema(data, selected_key)  # "ready_sauces"
```

**Детальный процесс генерации схем:**

**3.1. Определение файла:**
```python
file_name = f"{selected_key}.json"  # "ready_sauces.json"
```

**3.2. Загрузка маппингов:**
```python
# Из horeca/mappings/keys.py
file_keys = HORECA_KEYS_MAPPING["ready_sauces.json"]
# Получаем:
{
    "product_keys": {
        "name": {"description": "Название готового соуса", ...},
        "kbgu": {"description": "Калорийность и пищевая ценность", ...},
        "packaging": {"description": "Упаковка готовых соусов", ...},
        "shelf_life": {"description": "Условия хранения", ...}
    }
}

# Из horeca/mappings/enums.py
file_enums = HORECA_ENUM_MAPPING["ready_sauces.json"]
# Получаем:
{
    "name": {
        "sauce_types": ["горчичный", "барбекю", "сырный", "майонезный"],
        "brands": ["Millgri", "КЛАССИКА"]
    },
    "kbgu": {
        "calorie_ranges": ["низкие_до_150", "средние_150_250", "высокие_250_400"],
        "fat_content": ["обезжиренные", "низкожирные_до_15", ...]
    },
    "packaging": {
        "package_types": ["бутылка_пластиковая", "bag_in_box", "блистер"]
    }
}
```

**3.3. Формирование OpenAI tool схемы:**
```python
# horeca/service.py:127-132
properties[key_name] = {
    "type": "string",
    "description": f"{key_info['description']}. {key_info['filter_impact']}",
    "enum": all_enum_values  # Все значения из categories
}
```

**Итоговая tool схема:**
```json
{
    "type": "function",
    "function": {
        "name": "filter_horeca_products",
        "description": "Фильтрует продукты HoReCa из файла ready_sauces.json по заданным критериям.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Название готового соуса. Позволяет искать по типу соуса и бренду",
                    "enum": ["горчичный", "барбекю", "сырный", "майонезный", "кетчуп", "Millgri", "КЛАССИКА"]
                },
                "kbgu": {
                    "type": "string", 
                    "description": "Калорийность и пищевая ценность соуса",
                    "enum": ["низкие_до_150", "средние_150_250", "высокие_250_400", "обезжиренные"]
                },
                "packaging": {
                    "type": "string",
                    "description": "Упаковка готовых соусов",
                    "enum": ["бутылка_пластиковая", "bag_in_box", "блистер"]
                }
            },
            "required": [],
            "additionalProperties": false
        },
        "strict": true
    }
}
```

#### **Шаг 4: Вызов LLM для анализа запроса**
```python
# horeca/service.py:184
response = self.llm_service.chat.completions.create(
    model="devstral:24b-small-2505-q8_0",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Покажи мне низкокалорийные соусы Millgri в пластиковых бутылках"}
    ],
    tools=llm_tools,  # Наша сгенерированная схема
    tool_choice="auto"
)
```

**Системный промпт:**
```
Ты - эксперт по анализу запросов пользователей для системы HoReCa.
Твоя задача - проанализировать запрос и выбрать подходящий инструмент для фильтрации продуктов.
```

**Анализ LLM:**
- 🔍 "низкокалорийные" → `kbgu: "низкие_до_150"`
- 🔍 "Millgri" → `name: "Millgri"`  
- 🔍 "пластиковых бутылках" → `packaging: "бутылка_пластиковая"`

#### **Шаг 5: Парсинг ответа LLM**
```python
# horeca/service.py:195-204
tool_call = tool_calls[0]
tool_name = tool_call.function.name  # "filter_horeca_products"
tool_params = json.loads(tool_call.function.arguments)
# Результат:
{
    "kbgu": "низкие_до_150",
    "name": "Millgri", 
    "packaging": "бутылка_пластиковая"
}
```

#### **Шаг 6: Применение фильтрации данных**
```python
# horeca/service.py:240-250
filtered_products = product_list
for filter_key, enum_value in parameters.parameters.items():
    filtered_products = filter_horeca_products_smart(
        filtered_products, 
        filter_key,     # "kbgu", "name", "packaging"
        enum_value      # "низкие_до_150", "Millgri", "бутылка_пластиковая"
    )
```

**Детали фильтрации для каждого критерия:**

**6.1. Фильтрация по калорийности (`kbgu: "низкие_до_150"`):**
```python
# data_filter.py:66 -> universal.py:543
if field_key == "kbgu" and enum_value in UNIVERSAL_KBGU_CHECKERS:
    checker_func = UNIVERSAL_KBGU_CHECKERS["низкие_до_150"]  # check_calorie_range
    return checker_func(text, enum_value)

# universal.py:213-214
calories = int(match.group(1))  # Извлекаем из "КДж/ккал – 865/207"
return calories < 150  # Проверяем диапазон
```

**6.2. Фильтрация по бренду (`name: "Millgri"`):**
```python
# universal.py:558-563
patterns = get_universal_patterns("Millgri")  # ["Millgri®", "Millgri", "MILLGRI"]
for pattern in patterns:
    if pattern.lower() in text_lower:  # Ищем в названии продукта
        return True
```

**6.3. Фильтрация по упаковке (`packaging: "бутылка_пластиковая"`):**
```python
patterns = get_universal_patterns("бутылка_пластиковая")  
# ["Бутылка пластиковая", "бутылка пластиковая", "Бутылка"]
# Поиск в тексте упаковки
```

#### **Шаг 7: Формирование результата**
```python
# horeca/service.py:252-257
filtered_data = data.copy()
filtered_data["product_list"] = filtered_products

# Логирование результатов
logger.info(f"Итого отфильтровано продуктов: {len(filtered_products)} из {len(product_list)}")
```

**Пример результата фильтрации:**
```python
# Было: 50 соусов
# Стало: 3 соуса
[
    '{"name": "Соус на основе растительных масел «Горчичный» Millgri®", "kbgu": "КДж/ккал – 865/109", "packaging": "Бутылка пластиковая объемом 0,8 л"}',
    '{"name": "Кетчуп «Томатный» Millgri®", "kbgu": "КДж/ккал – 512/122", "packaging": "Бутылка пластиковая объемом 0,9 л"}',
    '{"name": "Соус «Сырный» Millgri®", "kbgu": "КДж/ккал – 623/148", "packaging": "Бутылка пластиковая объемом 0,8 л"}'
]
```

#### **Шаг 8: Возврат в основной пайплайн**
```python
# service.py:96-98
result = handler.process(query, data, selected_key)
logger.info(f"Обработка завершена. Успех: {result.success}")
return result
```

**Структура ToolCallResult:**
```python
ToolCallResult(
    success=True,
    filtered_data=filtered_data,  # Отфильтрованные данные
    applied_filters={
        "kbgu": "низкие_до_150",
        "name": "Millgri", 
        "packaging": "бутылка_пластиковая"
    },
    metadata={
        "subsector_id": "01",
        "tool_name": "filter_horeca_products", 
        "selected_key": "ready_sauces"
    }
)
```

---

### 🎯 **Ключевые особенности workflow:**

1. **Динамическая генерация схем** - схемы создаются на основе реальной структуры данных
2. **Двойной маппинг** - описания полей (keys.py) + возможные значения (enums.py)
3. **Умная фильтрация** - regex для чисел, текстовый поиск для остального
4. **Graceful fallback** - при любой ошибке возвращаются исходные данные
5. **Полная трассировка** - каждый шаг логируется для отладки

## 4. Руководство: Как добавить поддержку новой отрасли

Предположим, нам нужно добавить поддержку для отрасли "Напитки" (`drinks`) с `subsector_id="05"`.

**Шаг 1: Создание структуры папок**

Создайте новую папку `drinks` внутри `app/core/tool_calling/`:

```
app/core/tool_calling/
└── drinks/
    ├── __init__.py
    ├── service.py
    ├── data_filter.py
    └── mappings/
        ├── __init__.py
        ├── keys.py
        ├── enums.py
        └── universal.py
```
*Совет: можно скопировать структуру из `horeca` и адаптировать ее.*

**Шаг 2: Настройка `mappings`**

-   **`mappings/keys.py`**: Изучите JSON-файлы с данными о напитках и опишите их структуру. Например:
    ```python
    # app/core/tool_calling/drinks/mappings/keys.py
    PRODUCT_LIST_KEY = "recipes" # Ключ, где лежит список напитков
    PRODUCT_NAME_KEY = "name"
    PRODUCT_DESCRIPTION_KEY = "description"
    # и т.д.
    ```
-   **`mappings/enums.py`**: Определите перечисления для категориальных данных. Например, типы напитков.
    ```python
    # app/core/tool_calling/drinks/mappings/enums.py
    from enum import Enum

    class DrinkType(Enum):
        SODA = "газировка"
        JUICE = "сок"
        NECTAR = "нектар"
    ```
-   **`mappings/universal.py`**: Задайте паттерны для извлечения числовых значений.
    ```python
    # app/core/tool_calling/drinks/mappings/universal.py
    SUGAR_CONTENT_PATTERN = r"сахар(?:а|ом)?\s*([<>]?\s*\d+)"
    # и т.д.
    ```

**Шаг 3: Реализация `data_filter.py`**

Скорее всего, базовые функции фильтрации из `horeca/data_filter.py` (фильтрация по тексту и числам) можно будет переиспользовать. Скопируйте их в `drinks/data_filter.py`. Если для напитков нужна уникальная логика (например, фильтрация по % содержания сока), добавьте ее сюда.

**Шаг 4: Реализация обработчика `DrinksHandler`**

-   **`service.py`**: Создайте класс `DrinksHandler`, унаследовав его от `BaseToolHandler`.

    ```python
    # app/core/tool_calling/drinks/service.py
    from typing import List, Dict
    from app.core.tool_calling.base.handler import BaseToolHandler
    from app.core.tool_calling.base.types import FilterArgument
    # Импортируем все необходимое из своего модуля drinks
    from .data_filter import filter_products
    from .mappings import keys, enums, universal

    class DrinksHandler(BaseToolHandler):
        def generate_tool_schemas(self, data: Dict) -> List[Dict]:
            # Логика генерации схем на основе mappings/keys.py и mappings/enums.py
            # ...
            # Пример:
            schema = {
                "type": "function",
                "function": {
                    "name": "filter_drinks",
                    "description": "Фильтрует напитки по заданным критериям",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "drink_type": {
                                "type": "string",
                                "description": "Тип напитка",
                                "enum": [e.value for e in enums.DrinkType]
                            },
                            "sugar_content": {
                                "type": "object",
                                "properties": {"min": {"type": "number"}, "max": {"type": "number"}}
                            }
                        },
                        "required": []
                    }
                }
            }
            return [schema]

        def filter_data(self, data: Dict, tool_args: List[FilterArgument]) -> Dict:
            # Вызываем свою же функцию фильтрации
            return filter_products(data, tool_args, keys.PRODUCT_LIST_KEY)

    ```

**Шаг 5: Регистрация нового обработчика**

-   Откройте `app/core/tool_calling/service.py`.
-   Импортируйте ваш новый `DrinksHandler`.
-   Добавьте его в метод `_register_handlers`.

    ```python
    # app/core/tool_calling/service.py

    # ... импорты
    from .horeca.service import HoReCaHandler
    from .drinks.service import DrinksHandler # <-- 1. Импортируем новый хендлер

    class ToolService:
        def _register_handlers(self):
            self.registry.register("01", HoReCaHandler)
            self.registry.register("05", DrinksHandler) # <-- 2. Регистрируем его с subsector_id
    # ... остальной код
    ```

**Готово!** Теперь, когда в `handle_query` придет запрос с `subsector_id="05"`, `ToolService` автоматически подхватит `DrinksHandler` и применит всю описанную вами логику фильтрации.
