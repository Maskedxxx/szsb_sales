# Как работает приложение: Обзор конвейера (Pipeline)

Этот документ описывает полный цикл обработки запроса пользователя в приложении, от получения HTTP-запроса до генерации финального ответа.

## Шаг 1: Входная точка и валидация запроса

-   **Файл:** `app/api/endpoints.py`
-   **Эндпоинт:** `POST /api/v1/process_query`
-   **Функция:** `process_query(query: Query)`

1.  Пользователь отправляет запрос, содержащий `question` (текст вопроса) и `subsector_id` (ID отраслевого справочника).
2.  Эндпоинт вызывает основную функцию-обработчик `handle_query` из `app/core/engine.py`.
3.  В `handle_query` происходит начальная валидация: система проверяет, существует ли `subsector_id` в словаре `SUBSECTOR_ROUTES` (определенном в `app/data/__init__.py`). Если нет, выбрасывается исключение `ValueError`.

## Шаг 2: Семантическая маршрутизация (Выбор релевантных файлов)

-   **Файл:** `app/core/engine.py`
-   **Сервис:** `SemanticRoutingService` (из `app/core/services/semantic_routing_service.py`)
-   **Функция:** `routing_service.top_routes(...)`

1.  На основе текста вопроса (`query.question`) и `subsector_id` сервис ищет наиболее подходящие "маршруты". Маршрут — это, по сути, JSON-файл с данными в директории `app/routes/<subsector_name>/`.
2.  `SemanticRoutingService` использует гибридный поиск:
    *   **Dense Encoder:** `HuggingFaceEncoder` (модель `TatonkaHF/bge-m3_en_ru`) для семантического поиска (понимания смысла).
    *   **Sparse Encoder:** `TfidfEncoder` для поиска по ключевым словам.
3.  Функция `top_routes` возвращает список из `TOP_N_ROUTES` (по умолчанию 5) наиболее релевантных имен файлов (маршрутов) с их оценками.

## Шаг 3: Переранжирование маршрутов (Уточнение выбора файла)

-   **Файл:** `app/core/engine.py`
-   **Функция:** `rerank_routes(query_text: str, top_routes: Dict[str, str], subsector_id: str)`
-   **Сервис:** `EntityRankingService` (из `app/core/services/entity_ranking_service.py`)

1.  Список из 5 маршрутов, полученный на предыдущем шаге, передается в функцию `rerank_routes` для более точной оценки.
2.  `EntityRankingService` использует более мощную языковую модель (определенную в `.env` как `RERANK_MODEL`) для переоценки релевантности каждого маршрута.
3.  В модель передается системный промпт `PROMPT_ENTITY_RANKING` (из `app/data/prompts.py`), который инструктирует ее, как оценивать сущности.
4.  Для повышения точности используются "контекстные подсказки" (`context_hints`), которые загружаются функцией `get_router_hint` из `app/data/context_hints.py`. Эти подсказки дают модели дополнительную информацию о том, какой маршрут для какого типа запросов предназначен.
5.  В результате выбирается **один** самый релевантный маршрут.

## Шаг 4: Загрузка и подготовка данных

-   **Файл:** `app/core/engine.py`
-   **Утилиты:** `read_and_merge`, `normalize_dict_descriptions` (из `app/utils/file_utils.py`)

1.  Система формирует полный путь к выбранному JSON-файлу (например, `app/routes/bakery/sweetener_collection.json`).
2.  Функция `read_and_merge` считывает этот файл и загружает его содержимое в словарь Python.
3.  Функция `normalize_dict_descriptions` извлекает описания для каждого ключа верхнего уровня в JSON-файле, чтобы подготовить их для следующего шага.

## Шаг 5: Выбор релевантных ключей (Поиск данных внутри файла)

-   **Файл:** `app/core/engine.py`
-   **Функция:** `select_relevant_keys(query: str, key_descriptions: Dict[str, str], ...)`
-   **Сервис:** `EntityRankingService`

1.  Теперь, когда файл выбран, нужно найти в нем самые релевантные разделы (ключи).
2.  Процесс очень похож на Шаг 3: `EntityRankingService` снова используется, но на этот раз для оценки ключей из JSON-файла, а не самих файлов.
3.  Используется модель, определенная как `KEY_SELECTION_MODEL`.
4.  Контекстные подсказки также применяются, но уже более специфичные, для конкретных ключей, и загружаются функцией `get_key_hint` из `app/data/context_hints.py`.
5.  Функция возвращает список наиболее релевантных имен ключей.

## Шаг 6: Tool Calling (Расширенная фильтрация для поддерживаемых отраслей)

-   **Файл:** `app/core/engine.py`
-   **Модуль:** `app/core/tool_calling` 
-   **Сервис:** `ToolService`

1.  **Проверка поддержки отрасли:** Система проверяет, поддерживается ли Tool Calling для текущего `subsector_id` через `tool_service.is_supported()`.

2.  **Для поддерживаемых отраслей (HoReCa, Молочная отрасль):**
    *   Создается единый `UniversalIndustryHandler` для обработки любой отрасли
    *   **Динамическая загрузка:** `IndustryMappingsLoader` автоматически загружает mappings отрасли
    *   **Генерация схем:** На основе структуры данных создаются динамические OpenAI tool схемы с strict mode
    *   **Поддержка субключей:** `KEY_TO_FILE_MAPPING` для сложных JSON структур
    *   **LLM анализ:** LLM анализирует пользовательский запрос и выбирает подходящие параметры фильтрации
    *   **Умная фильтрация:** Продукты фильтруются по критериям с использованием regex и текстовых паттернов
    *   **Результат:** Возвращаются отфильтрованные данные для дальнейшей обработки

3.  **Для неподдерживаемых отраслей:** 
    *   Система использует стандартную логику без фильтрации
    *   Данные передаются без изменений (graceful fallback)

4.  **Универсальная архитектура Tool Calling (с августа 2025):**
    ```
    app/core/tool_calling/
    ├── service.py                  # ToolService - единая точка входа
    ├── registry.py                 # HandlerRegistry - реестр отраслей
    ├── universal_handler.py        # UniversalIndustryHandler - единый обработчик
    ├── base/                       # Базовые классы и типы
    ├── horeca/mappings/           # HoReCa mappings (keys, enums, universal)
    ├── milk/mappings/             # Milk mappings (keys, enums, universal)
    └── .backup/                   # Backup старых хендлеров
    ```

## Шаг 7: Подготовка контекста для генерации ответа

-   **Файл:** `app/core/engine.py`
-   **Утилиты:** `get_nested_data`, `clean_json_text`

1.  Из обработанных данных (отфильтрованных через Tool Calling или исходных) извлекаются `product_list` для каждого релевантного ключа.
2.  Данные форматируются в виде строки JSON.
3.  `clean_json_text` удаляет лишние символы, чтобы подготовить "чистый" контекст для финальной модели.

## Шаг 8: Генерация финального ответа

-   **Файл:** `app/core/engine.py`
-   **Функция:** `generate_final_answer(user_query: str, context: str, ...)`
-   **Сервис:** `FinalGenerationService` (из `app/core/services/final_generation_service.py`)

1.  Это заключительный этап. Исходный вопрос пользователя и подготовленный на Шаге 6 контекст передаются в `generate_final_answer`.
2.  `FinalGenerationService` использует самую мощную модель (определенную как `GENERATION_MODEL`) для создания развернутого ответа.
3.  Используется промпт `PROMPT_FINAL_ANSWER` (из `app/data/prompts.py`), который инструктирует модель, как структурировать ответ в формате Markdown.
4.  Применяются финальные, самые точные контекстные подсказки от `get_final_answer_hint`.
5.  К сгенерированному ответу добавляется стандартное предупреждение: "⚠️ **ВАЖНО**: Нейропомощник может ошибаться...".

## Шаг 9: Формирование и отправка ответа

-   **Файл:** `app/core/engine.py`
-   **Модель ответа:** `Response` (из `app/api/api_models/models.py`)

1.  Финальный текстовый ответ упаковывается в Pydantic-модель `Response`.
2.  В ответ также добавляются метаданные (`Metadata`): какие файлы и ключи были выбраны, какие модели использовались, версия приложения.
3.  Объект `Response` сериализуется в JSON и возвращается пользователю как результат HTTP-запроса.

---

## Схемы пайплайна

### Базовый пайплайн (для неподдерживаемых отраслей):
```
Query → Semantic Routing → Reranking → Key Selection → Context Preparation → Final Generation → Response
```

### Расширенный пайплайн (для отраслей с Tool Calling):
```
Query → Semantic Routing → Reranking → Key Selection → **Tool Calling** → Context Preparation → Final Generation → Response
```

### Поддерживаемые отрасли с Tool Calling:
- **HoReCa** (subsector_id: "01") - полная поддержка с динамическими схемами и умной фильтрацией
- **Молочная отрасль** (subsector_id: "02") - полная поддержка с субключами и regex фильтрацией

### Планируемые к добавлению:
- **Кондитерская промышленность** (subsector_id: "03") - время реализации 30-60 минут
- **Хлебопекарная промышленность** (subsector_id: "04") - время реализации 30-60 минут

---

## Универсальная архитектура Tool Calling (с августа 2025)

### Factory Pattern с единым обработчиком:
```
app/core/tool_calling/
├── __init__.py                    # Экспорт ToolService
├── service.py                     # ToolService - главный координатор
├── registry.py                    # HandlerRegistry - реестр отраслей
├── universal_handler.py           # UniversalIndustryHandler - единый обработчик
├── base/                          # Базовые классы и типы
│   ├── handler.py                 # BaseToolHandler (для совместимости)
│   └── types.py                   # Общие типы данных
├── .backup/                       # Backup старых хендлеров
│   ├── README.md                  # Инструкции по восстановлению
│   └── *.py.old                   # Старые файлы
├── horeca/                        # HoReCa mappings ✅
│   ├── __init__.py                # Пустой модуль
│   └── mappings/                  # Маппинги данных
│       ├── keys.py                # Структура полей + KEY_TO_FILE_MAPPING
│       ├── enums.py               # Enum значения с субключами
│       └── universal.py           # Regex и текстовые паттерны
└── milk/                          # Milk mappings ✅
    ├── __init__.py                # Пустой модуль
    └── mappings/                  # Маппинги данных
        ├── keys.py                # Структура полей + KEY_TO_FILE_MAPPING
        ├── enums.py               # Enum значения с субключами
        └── universal.py           # Regex и текстовые паттерны
```

### Принципы новой архитектуры:

1. **Единый обработчик:** `UniversalIndustryHandler` заменяет все индивидуальные хендлеры
2. **Динамическая загрузка:** `IndustryMappingsLoader` автоматически импортирует mappings через `importlib`
3. **Поддержка субключей:** `KEY_TO_FILE_MAPPING` для сложных JSON структур
4. **Strict mode:** OpenAI tool схемы с точным соответствием требованиям
5. **Graceful fallback:** При ошибках система продолжает работу с исходными данными
6. **Изоляция отраслей:** Каждая отрасль содержит только свои mappings

### Добавление новой отрасли:

Благодаря универсальной архитектуре добавление новой отрасли максимально упрощено:

1. **Создать папку mappings:** `app/core/tool_calling/INDUSTRY_NAME/mappings/`
2. **Реализовать 3 файла:** `keys.py`, `enums.py`, `universal.py` (следуя формату HoReCa/Milk)
3. **Зарегистрировать:** Добавить одну строку в `HandlerRegistry.supported_industries`

**Время реализации:** 30-60 минут вместо 2-4 часов!
