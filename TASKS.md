# ЗАДАЧИ ПРОЕКТА SZSB_SALES

## ЗАВЕРШЕННАЯ ЗАДАЧА: Создание расширяемой логики Tool Calling

### ОПИСАНИЕ ЗАДАЧИ
Создана универсальная архитектура Tool Calling для улучшения точности обработки запросов через использование специализированных инструментов LLM. Система построена с расчетом на масштабирование на все отрасли.

### СИСТЕМНЫЙ АНАЛИЗ

#### ЦЕЛЬ
Внедрить расширяемый промежуточный этап Tool Calling в существующий пайплайн для улучшения точности обработки запросов через использование специализированных инструментов LLM.

#### КОНТЕКСТ
- **Базовый пайплайн:** Query → Semantic Routing → Reranking → Key Selection → Context Preparation → Final Generation → Response
- **Расширенный пайплайн:** Query → Semantic Routing → Reranking → Key Selection → **Tool Calling** → Context Preparation → Final Generation → Response

#### ТРЕБОВАНИЯ
1. **Функциональные требования:**
   - Модульная архитектура с возможностью добавления новых отраслей
   - Интеграция между `select_relevant_keys` и `generate_final_answer`
   - Совместимость с существующим пайплайном
   - Полная обратная совместимость для неподдерживаемых отраслей

2. **Нефункциональные требования:**
   - Единая точка входа через ToolService
   - Логирование всех операций
   - Обработка ошибок с graceful fallback
   - Расширяемая модульная архитектура
   - Качественная документация кода

## РЕАЛИЗОВАННАЯ АРХИТЕКТУРА

### Модульная структура Tool Calling:
```
app/core/tool_calling/
├── __init__.py                    # Точка входа: ToolService
├── service.py                     # ToolService - главный координатор
├── registry.py                    # HandlerRegistry - реестр хендлеров
├── base/                          # Базовые классы и интерфейсы
│   ├── __init__.py
│   ├── handler.py                 # BaseToolHandler - базовый класс
│   └── types.py                   # Общие типы: ToolCallResult, FilterParameters
├── horeca/                        # Модуль HoReCa ✅
│   ├── __init__.py
│   ├── service.py                 # HoReCaHandler(BaseToolHandler)
│   ├── data_filter.py             # Фильтрация продуктов HoReCa
│   └── mappings/                  # Маппинги данных
│       ├── __init__.py
│       ├── keys.py                # Маппинг ключей продуктов
│       ├── enums.py               # Enum значения для LLM
│       └── universal.py           # Универсальные паттерны и regex
└── tests/                         # Изолированные тесты
    ├── __init__.py
    └── horeca/
        ├── __init__.py
        └── test_handler.py         # Тесты HoReCa хендлера
```

### Архитектурные принципы:

#### 1. **Единая точка входа**
```python
from app.core.tool_calling import ToolService

tool_service = ToolService()
result = tool_service.process_query(
    subsector_id="01",  # HoReCa
    query="Найти соус Барбекю",
    data=product_data,
    selected_key="ready_sauces"
)
```

#### 2. **Автоматическая регистрация хендлеров**
- Хендлеры регистрируются автоматически при инициализации ToolService
- Реестр управляет доступными хендлерами по subsector_id

#### 3. **Graceful degradation**
- При отсутствии хендлера для отрасли возвращаются исходные данные
- При ошибке в Tool Calling система продолжает работу с fallback

## ПЛАН МАСШТАБИРОВАНИЯ НА ДРУГИЕ ОТРАСЛИ

### ЭТАП 1: Подготовка к добавлению новой отрасли

#### 1.1 Анализ данных отрасли
- [ ] Изучить структуру JSON файлов новой отрасли
- [ ] Проанализировать ключи продуктов и их типы данных
- [ ] Определить критерии фильтрации (аналоги КБЖУ, упаковки, сроков хранения)
- [ ] Выявить специфичные для отрасли паттерны поиска

#### 1.2 Планирование маппингов
- [ ] Создать список ключей продуктов с описаниями для tool схем
- [ ] Определить enum значения для каждого ключа
- [ ] Спланировать regex паттерны для числовых значений
- [ ] Подготовить текстовые паттерны для брендов и категорий

### ЭТАП 2: Создание хендлера новой отрасли

#### 2.1 Создание базовой структуры (пример для масложировой отрасли)
```bash
mkdir -p app/core/tool_calling/fat_oil/mappings
```

#### 2.2 Создание файлов маппингов
```python
# app/core/tool_calling/fat_oil/mappings/keys.py
FAT_OIL_KEYS_MAPPING = {
    "vegetable_oils.json": {
        "file_description": "Растительные масла и жиры",
        "product_keys": {
            "name": {
                "description": "Название масла или жира",
                "filter_impact": "Позволяет искать по типу масла (подсолнечное, оливковое, кокосовое)",
                "data_type": "string",
                "examples": ["Масло подсолнечное рафинированное", "Масло оливковое Extra Virgin"]
            },
            "composition": {
                "description": "Состав жирных кислот",
                "filter_impact": "Позволяет фильтровать по содержанию насыщенных/ненасыщенных жиров",
                "data_type": "string",
                "examples": ["Омега-3: 15%, Омега-6: 60%"]
            }
            # ... другие ключи
        }
    }
}
```

#### 2.3 Создание enum маппингов
```python
# app/core/tool_calling/fat_oil/mappings/enums.py
FAT_OIL_ENUM_MAPPING = {
    "vegetable_oils.json": {
        "name": {
            "oil_types": ["подсолнечное", "оливковое", "кокосовое", "льняное"],
            "processing": ["рафинированное", "нерафинированное", "extra_virgin"],
            "brands": ["СЛОБОДА", "ЗЛАТО", "IDEAL"]
        },
        "composition": {
            "fatty_acids": ["высокоомега3", "низкоомега6", "насыщенные_жиры"],
            "vitamin_content": ["витамин_E", "витамин_D", "без_добавок"]
        }
    }
}
```

#### 2.4 Создание универсальных паттернов
```python
# app/core/tool_calling/fat_oil/mappings/universal.py
FAT_OIL_UNIVERSAL_MAPPING = {
    "подсолнечное": ["подсолнечное", "Подсолнечное", "sunflower"],
    "оливковое": ["оливковое", "Оливковое", "olive"],
    "кокосовое": ["кокосовое", "Кокосовое", "coconut"],
    # Regex для жирных кислот
    "высокоомега3": ["Омега-3.*[1-9][0-9]%", "Omega-3.*[1-9][0-9]%"]
}
```

#### 2.5 Создание функции фильтрации
```python
# app/core/tool_calling/fat_oil/data_filter.py
def filter_fat_oil_products_smart(product_list: List[str], filter_key: str, enum_value: str) -> List[str]:
    # Аналогично horeca/data_filter.py, но адаптировано для масложировой отрасли
    pass
```

#### 2.6 Создание хендлера отрасли
```python
# app/core/tool_calling/fat_oil/service.py
class FatOilHandler(BaseToolHandler):
    def __init__(self, subsector_id: str, llm_service=None):
        super().__init__(subsector_id)
        self.llm_service = llm_service
        
    def generate_schema(self, data: Dict[str, Any], selected_key: str) -> List[ToolSchema]:
        # Реализация генерации схем для масложировой отрасли
        pass
        
    def extract_parameters(self, query: str, schemas: List[ToolSchema]) -> FilterParameters:
        # Аналогично HoReCa хендлеру
        pass
        
    def filter_data(self, data: Dict[str, Any], parameters: FilterParameters) -> Dict[str, Any]:
        # Использует filter_fat_oil_products_smart
        pass
```

### ЭТАП 3: Регистрация новой отрасли

#### 3.1 Обновление ToolService
```python
# app/core/tool_calling/service.py - метод _register_handlers()
def _register_handlers(self) -> None:
    try:
        # Существующий HoReCa хендлер
        from .horeca.service import HoReCaHandler
        self.registry.register_handler("01", HoReCaHandler("01", llm_service=None))
        
        # НОВЫЙ: Масложировая отрасль
        from .fat_oil.service import FatOilHandler
        self.registry.register_handler("02", FatOilHandler("02", llm_service=None))
        self.logger.info("Масложировая отрасль зарегистрирована")
        
    except ImportError as e:
        self.logger.warning(f"Не удалось загрузить некоторые хендлеры: {e}")
```

#### 3.2 Создание тестов
```python
# app/core/tool_calling/tests/fat_oil/test_handler.py
# Аналогично тестам HoReCa, но для масложировой отрасли
```

### ЭТАП 4: Тестирование и валидация

#### 4.1 Проверка интеграции
- [ ] Запустить тесты новой отрасли
- [ ] Проверить автоматическую регистрацию в ToolService
- [ ] Протестировать end-to-end флоу через engine.py

#### 4.2 Проверка обратной совместимости
- [ ] Убедиться, что HoReCa продолжает работать
- [ ] Проверить fallback для неподдерживаемых отраслей
- [ ] Протестировать graceful degradation при ошибках

## ШАБЛОН ДЛЯ БЫСТРОГО ДОБАВЛЕНИЯ ОТРАСЛИ

### Минимальный набор файлов для новой отрасли "INDUSTRY_NAME":

1. **Структура директорий:**
```bash
mkdir -p app/core/tool_calling/INDUSTRY_NAME/mappings
mkdir -p app/core/tool_calling/tests/INDUSTRY_NAME
```

2. **Обязательные файлы:**
```
INDUSTRY_NAME/
├── __init__.py                    # Экспорт хендлера
├── service.py                     # IndustryHandler(BaseToolHandler)
├── data_filter.py                 # filter_industry_products_smart()
└── mappings/
    ├── __init__.py               # Экспорт всех маппингов
    ├── keys.py                   # INDUSTRY_KEYS_MAPPING
    ├── enums.py                  # INDUSTRY_ENUM_MAPPING  
    └── universal.py              # Паттерны и regex функции
```

3. **Регистрация в ToolService:**
```python
# service.py: добавить в _register_handlers()
from .INDUSTRY_NAME.service import IndustryHandler
self.registry.register_handler("XX", IndustryHandler("XX", llm_service=None))
```

### Время реализации:
- **Быстрое добавление:** 2-4 часа (базовая функциональность)
- **Полная реализация:** 1-2 дня (включая тесты и оптимизацию)
- **Продвинутая настройка:** 3-5 дней (специфичные regex, сложная логика)

## ТЕКУЩИЙ СТАТУС

### ЗАВЕРШЕНО ✅
- [x] **Создана расширяемая модульная архитектура Tool Calling**
- [x] **Реализован полнофункциональный хендлер для HoReCa**
- [x] **Интеграция в engine.py с единой точкой входа**
- [x] **Система автоматической регистрации хендлеров**
- [x] **Graceful fallback и обработка ошибок**
- [x] **Полная документация и тесты**

### ГОТОВО К МАСШТАБИРОВАНИЮ 🚀
- **Архитектура:** Спроектирована для легкого добавления новых отраслей
- **Шаблоны:** Готовы детальные инструкции и шаблоны кода
- **Тестирование:** Методология тестирования отработана на HoReCa
- **Документация:** Подробные гайды по добавлению новых отраслей

### СЛЕДУЮЩИЕ ОТРАСЛИ ДЛЯ РЕАЛИЗАЦИИ
1. **Масложировая промышленность** (subsector_id: "02") - приоритет высокий
2. **Кондитерская промышленность** (subsector_id: "03") - приоритет средний  
3. **Хлебопекарная промышленность** (subsector_id: "04") - приоритет средний

---

**Дата создания:** 2025-07-18  
**Дата рефакторинга:** 2025-07-18  
**Статус:** Завершено и готово к масштабированию  
**Архитектор:** Claude (рефакторинг модульной архитектуры)