"""
Изолированный тестовый файл для проверки Tool Calling логики HoReCa.

Этот файл тестирует полный цикл работы HoReCaHandler без интеграции
с engine.py и без вызова generate_final_answer.
"""

import json
import time
from typing import Dict, Any

# Импортируем наш хендлер
from ...horeca.service import HoReCaHandler
from ...base.types import FilterParameters


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
            # Возвращаем пустой tool call для неизвестных запросов
            return {
                "tool_calls": [{
                    "function": {
                        "name": "filter_horeca_products",
                        "arguments": json.dumps({})
                    }
                }]
            }


def load_test_data() -> Dict[str, Any]:
    """
    Загружает тестовые данные из файла ready_sauces.json или создает мок-данные.
    
    Returns:
        Тестовые данные для фильтрации
    """
    try:
        # Пытаемся загрузить реальные данные
        with open('/Users/mask/Documents/Проеты_2025/snabik_sales/szsb_sales/app/routes/horeca/ready_sauces.json', 'r', encoding='utf-8') as f:
            sauce_data = json.load(f)
        return sauce_data['ready_sauces']
    except FileNotFoundError:
        # Используем мок-данные
        return {
            "product_list": [
                '{"name": "Соус на основе растительных масел «Горчичный» Millgri®", "kbgu": "КДж/ккал – 865/207\\nБелки, г – 1,3\\nЖиры, г – 11,7\\nУглеводы, г – 23,1", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев при температуре от 1 °С до 27 °С"}',
                '{"name": "Соус томатный «Барбекю» Millgri®", "kbgu": "КДж/ккал – 801/189\\nБелки, г – 0,9\\nЖиры, г – 0,1\\nУглеводы, г – 44,3", "packaging": "Упаковка «bag-in-box» помещенная в гофрокороб, масса нетто 10 кг", "shelf_life": "12 месяцев при температуре от 1 °С до 27 °С"}',
                '{"name": "Соус майонезный «Сливочно-чесночный» Millgri®", "kbgu": "КДж/ккал – 1586/385\\nБелки, г – 0,5\\nЖиры, г – 40,2\\nУглеводы, г – 5,0", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев при температуре от 1 °С до 27 °С"}'
            ]
        }


def test_scenario(handler: HoReCaHandler, test_data: Dict[str, Any], query: str, description: str) -> None:
    """
    Тестирует один сценарий обработки запроса.
    
    Args:
        handler: Экземпляр HoReCaHandler
        test_data: Тестовые данные
        query: Пользовательский запрос
        description: Описание теста
    """
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"📝 Запрос: {query}")
    print('='*60)
    
    start_time = time.time()
    
    try:
        # Выполняем полный цикл обработки
        result = handler.process(query, test_data, "ready_sauces")
        
        execution_time = time.time() - start_time
        
        print(f"✅ Обработка завершена за {execution_time:.3f}с")
        print(f"📊 Результат: {'Успех' if result.success else 'Ошибка'}")
        
        if result.success:
            original_count = len(test_data.get("product_list", []))
            filtered_count = len(result.filtered_data.get("product_list", []))
            print(f"📈 Отфильтровано: {filtered_count} из {original_count} продуктов")
            print(f"🔧 Применены фильтры: {result.applied_filters}")
            
            # Показываем первые несколько результатов
            filtered_products = result.filtered_data.get("product_list", [])
            for i, product_json in enumerate(filtered_products[:3], 1):
                try:
                    product = json.loads(product_json)
                    product_name = product.get('name', 'Неизвестное название')[:60]
                    print(f"  {i}. {product_name}{'...' if len(product.get('name', '')) > 60 else ''}")
                except json.JSONDecodeError:
                    print(f"  {i}. [Ошибка парсинга JSON]")
            
            if len(filtered_products) > 3:
                print(f"  ... и еще {len(filtered_products) - 3} продуктов")
        else:
            print(f"❌ Ошибка: {result.error_message}")
    
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"💥 Исключение за {execution_time:.3f}с: {str(e)}")
    
    print(f"{'='*60}")


def main():
    """Основная функция тестирования."""
    print("🚀 НАЧАЛО ТЕСТИРОВАНИЯ HoReCaHandler")
    print("="*80)
    
    # Инициализируем мок LLM сервис
    mock_llm = MockLLMService()
    
    # Создаем хендлер с мок-сервисом
    handler = HoReCaHandler("01", mock_llm)
    
    # Загружаем тестовые данные
    test_data = load_test_data()
    original_count = len(test_data.get("product_list", []))
    print(f"📦 Загружено {original_count} тестовых продуктов")
    
    # Тестовые сценарии
    test_scenarios = [
        ("Найти соус Барбекю", "Поиск по названию продукта"),
        ("Покажи горчичный соус", "Поиск другого типа соуса"),
        ("Какие соусы продаются в пластиковых бутылках?", "Фильтрация по упаковке"),
        ("Найди низкокалорийные соусы", "Фильтрация по калорийности"),
        ("Покажи высокожирные продукты", "Фильтрация по содержанию жиров"),
        ("Что есть от бренда Millgri?", "Фильтрация по бренду"),
        ("Покажи все экзотические фрукты", "Обработка неизвестного запроса")
    ]
    
    # Выполняем тесты
    for i, (query, description) in enumerate(test_scenarios, 1):
        test_scenario(handler, test_data, query, f"ТЕСТ {i}: {description}")
    
    # Тестируем генерацию схем отдельно
    print(f"\n{'='*60}")
    print("🧪 ДОПОЛНИТЕЛЬНЫЙ ТЕСТ: Генерация tool схем")
    print('='*60)
    
    try:
        schemas = handler.generate_schema(test_data, "ready_sauces")
        print(f"✅ Сгенерировано схем: {len(schemas)}")
        
        if schemas:
            schema = schemas[0]
            function_props = schema.function.get("parameters", {}).get("properties", {})
            print(f"📋 Доступных свойств в схеме: {len(function_props)}")
            print(f"🔑 Ключи: {list(function_props.keys())}")
    except Exception as e:
        print(f"❌ Ошибка генерации схемы: {str(e)}")
    
    print(f"\n{'='*80}")
    print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print(f"📊 Всего выполнено тестов: {len(test_scenarios) + 1}")
    print("="*80)


if __name__ == "__main__":
    main()