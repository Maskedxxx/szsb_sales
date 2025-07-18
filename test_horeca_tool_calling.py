"""
Изолированный тестовый файл для проверки Tool Calling логики HoReCa.

Этот файл тестирует полный цикл работы HoReCaToolService без интеграции
с engine.py и без вызова generate_final_answer.
"""

import json
import time
from typing import Dict, Any

# Импортируем наш сервис
from horeca_tool_service import HoReCaToolService


class MockLLMService:
    """
    Мок-сервис для симуляции вызова LLM с tool calling.
    
    Имитирует реальные ответы LLM для разных типов запросов.
    """
    
    def call_with_tools(self, system_prompt: str, user_query: str, tools: list) -> Dict[str, Any]:
        """
        Симулирует вызов LLM с tool calling.
        
        Args:
            system_prompt: Системный промпт
            user_query: Запрос пользователя
            tools: Список доступных инструментов
            
        Returns:
            Мок-ответ LLM с tool_calls
        """
        print(f"🤖 MockLLM получил запрос: {user_query}")
        
        # Анализируем запрос и выбираем подходящий tool call
        query_lower = user_query.lower()
        
        if "барбекю" in query_lower or "barbecue" in query_lower:
            return {
                "tool_calls": [{
                    "function": {
                        "name": "filter_horeca_products",
                        "arguments": json.dumps({"name": "барбекю"})
                    }
                }]
            }
        elif "горчичный" in query_lower or "горчица" in query_lower:
            return {
                "tool_calls": [{
                    "function": {
                        "name": "filter_horeca_products",
                        "arguments": json.dumps({"name": "горчичный"})
                    }
                }]
            }
        elif "бутылка" in query_lower or "упаковка" in query_lower:
            return {
                "tool_calls": [{
                    "function": {
                        "name": "filter_horeca_products",
                        "arguments": json.dumps({"packaging": "бутылка_пластиковая"})
                    }
                }]
            }
        elif "калори" in query_lower or "ккал" in query_lower:
            if "низк" in query_lower:
                return {
                    "tool_calls": [{
                        "function": {
                            "name": "filter_horeca_products",
                            "arguments": json.dumps({"kbgu": "низкие_до_150"})
                        }
                    }]
                }
            else:
                return {
                    "tool_calls": [{
                        "function": {
                            "name": "filter_horeca_products",
                            "arguments": json.dumps({"kbgu": "высокие_250_400"})
                        }
                    }]
                }
        elif "жир" in query_lower:
            return {
                "tool_calls": [{
                    "function": {
                        "name": "filter_horeca_products",
                        "arguments": json.dumps({"kbgu": "высокожирные_свыше_30"})
                    }
                }]
            }
        elif "millgri" in query_lower:
            return {
                "tool_calls": [{
                    "function": {
                        "name": "filter_horeca_products",
                        "arguments": json.dumps({"name": "Millgri"})
                    }
                }]
            }
        else:
            # Возвращаем None для неизвестных запросов
            return None


def load_test_data() -> Dict[str, Any]:
    """
    Загружает тестовые данные из ready_sauces.json.
    
    Returns:
        Словарь с данными продуктов
    """
    try:
        with open('/Users/mask/Documents/Проеты_2025/snabik_sales/szsb_sales/app/routes/horeca/ready_sauces.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Файл ready_sauces.json не найден, используем тестовые данные")
        return {
            "ready_sauces": {
                "description": "Тестовые данные",
                "product_list": [
                    '{"name": "Соус Горчичный Millgri®", "kbgu": "КДж/ккал – 865/207\\nБелки, г – 1,3\\nЖиры, г – 11,7", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев"}',
                    '{"name": "Соус Барбекю Millgri®", "kbgu": "КДж/ккал – 801/189\\nБелки, г – 0,9\\nЖиры, г – 0,1", "packaging": "Упаковка bag-in-box", "shelf_life": "12 месяцев"}',
                    '{"name": "Соус Сливочный", "kbgu": "КДж/ккал – 1586/385\\nБелки, г – 0,5\\nЖиры, г – 40,2", "packaging": "Бутылка пластиковая", "shelf_life": "6 месяцев"}'
                ]
            }
        }


def test_tool_calling_scenarios():
    """
    Тестирует различные сценарии Tool Calling.
    """
    print("=" * 80)
    print("🧪 ТЕСТИРОВАНИЕ TOOL CALLING ЛОГИКИ HORECA")
    print("=" * 80)
    
    # Инициализируем сервис
    mock_llm = MockLLMService()
    service = HoReCaToolService(llm_service=mock_llm)
    
    # Загружаем данные
    test_data = load_test_data()
    product_data = test_data["ready_sauces"]
    
    print(f"📊 Загружено {len(product_data['product_list'])} продуктов для тестирования")
    
    # Тестовые сценарии
    test_scenarios = [
        {
            "name": "Поиск соуса Барбекю",
            "query": "Найди соус Барбекю",
            "expected_filter": "name: барбекю"
        },
        {
            "name": "Поиск горчичного соуса",
            "query": "Покажи горчичные соусы",
            "expected_filter": "name: горчичный"
        },
        {
            "name": "Поиск по упаковке",
            "query": "Какие соусы в пластиковых бутылках?",
            "expected_filter": "packaging: бутылка_пластиковая"
        },
        {
            "name": "Поиск низкокалорийных",
            "query": "Найди низкокалорийные соусы",
            "expected_filter": "kbgu: низкие_до_150"
        },
        {
            "name": "Поиск высокожирных",
            "query": "Покажи жирные соусы",
            "expected_filter": "kbgu: высокожирные_свыше_30"
        },
        {
            "name": "Поиск по бренду",
            "query": "Соусы Millgri",
            "expected_filter": "name: Millgri"
        },
        {
            "name": "Неизвестный запрос",
            "query": "Какая погода сегодня?",
            "expected_filter": "fallback: все продукты"
        }
    ]
    
    # Выполняем тесты
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"🔍 ТЕСТ {i}: {scenario['name']}")
        print(f"📝 Запрос: {scenario['query']}")
        print(f"🎯 Ожидаемый фильтр: {scenario['expected_filter']}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Выполняем tool calling
        result = service.process_horeca_query(
            query=scenario['query'],
            file_name="ready_sauces.json",
            product_data=product_data
        )
        
        execution_time = time.time() - start_time
        
        # Выводим результаты
        print(f"✅ Успех: {result.success}")
        print(f"🛠️ Выбранный tool: {result.selected_tool}")
        print(f"📋 Параметры: {result.tool_parameters}")
        print(f"⏱️ Время выполнения: {execution_time:.3f}с")
        
        if result.success and result.filtered_products:
            print(f"📦 Найдено продуктов: {len(result.filtered_products)}")
            
            # Показываем первые 3 продукта
            for j, product_json in enumerate(result.filtered_products[:3], 1):
                try:
                    product = json.loads(product_json)
                    print(f"  {j}. {product['name']}")
                except json.JSONDecodeError:
                    print(f"  {j}. [Ошибка парсинга JSON]")
            
            if len(result.filtered_products) > 3:
                print(f"  ... и еще {len(result.filtered_products) - 3} продуктов")
        else:
            print("❌ Фильтрация не удалась или не найдено продуктов")
            if result.error_message:
                print(f"💥 Ошибка: {result.error_message}")
    
    print(f"\n{'='*80}")
    print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print(f"{'='*80}")


def test_tool_schema_generation():
    """
    Тестирует генерацию tool схемы.
    """
    print("\n" + "=" * 80)
    print("🔧 ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ TOOL СХЕМЫ")
    print("=" * 80)
    
    service = HoReCaToolService()
    test_data = load_test_data()
    
    # Тестируем генерацию схемы
    schema = service.generate_tool_schema("breadings_and_cutlets.json", test_data["breadings_and_cutlets"])
    
    print("📄 Сгенерированная схема:")
    print(json.dumps(schema, indent=2, ensure_ascii=False))
    
    # Проверяем основные элементы схемы
    if schema:
        function_def = schema.get("function", {})
        parameters = function_def.get("parameters", {})
        properties = parameters.get("properties", {})
        
        print("\n📊 Статистика схемы:")
        print(f"  - Имя функции: {function_def.get('name', 'N/A')}")
        print(f"  - Количество параметров: {len(properties)}")
        print(f"  - Доступные параметры: {list(properties.keys())}")
        
        # Проверяем каждый параметр
        for param_name, param_def in properties.items():
            enum_values = param_def.get("enum", [])
            print(f"  - {param_name}: {len(enum_values)} возможных значений")
    else:
        print("❌ Не удалось сгенерировать схему")


if __name__ == "__main__":
    print("🚀 Запуск изолированного тестирования Tool Calling")
    
    # Тест 1: Генерация схемы
    # test_tool_schema_generation()
    
    # Тест 2: Полный цикл tool calling
    test_tool_calling_scenarios()
    
    print("\n✅ Все тесты завершены успешно!")