"""
Простой тест для HoReCa Tool Calling.

Тестирует полный цикл работы с реальными данными HoReCa.
"""

import json
import time
from typing import Dict, Any

from ..service import ToolService
from ..adapters import MockAdapter
from ..horeca.service import HoReCaHandler


def load_test_data() -> Dict[str, Any]:
    """
    Загружает тестовые данные из ready_sauces.json.
    
    Returns:
        Словарь с данными продуктов
    """
    try:
        with open('app/routes/horeca/ready_sauces.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Файл ready_sauces.json не найден, используем тестовые данные")
        return {
            "ready_sauces": {
                "description": "Тестовые данные готовых соусов",
                "product_list": [
                    '{"name": "Соус на основе растительных масел «Горчичный» Millgri®", "kbgu": "КДж/ккал – 865/207\\nБелки, г – 1,3\\nЖиры, г – 11,7", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев при температуре от 1 °С до 27 °С"}',
                    '{"name": "Соус томатный «Барбекю» Millgri®", "kbgu": "КДж/ккал – 801/189\\nБелки, г – 0,9\\nЖиры, г – 0,1", "packaging": "Упаковка «bag-in-box» помещенная в гофрокороб", "shelf_life": "12 месяцев при температуре от 1 °С до 27 °С"}',
                    '{"name": "Соус майонезный «Сливочно-чесночный» Millgri®", "kbgu": "КДж/ккал – 1586/385\\nБелки, г – 0,5\\nЖиры, г – 40,2", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев при температуре от 1 °С до 27 °С"}',
                    '{"name": "Кетчуп «Томатный» первой категории Millgri®", "kbgu": "КДж/ккал – 465/109\\nБелки, г – 1,2\\nЖиры, г – 0,0", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев при температуре от 0 °С до 25 °С"}'
                ]
            }
        }


def test_horeca_tool_calling():
    """
    Тестирует полный цикл Tool Calling для HoReCa.
    
    Выполняет реальный вызов tool calling и возвращает отфильтрованные данные.
    """
    print("🚀 Запуск простого теста HoReCa Tool Calling")
    print("=" * 80)
    
    # Загружаем тестовые данные
    test_data = load_test_data()
    product_data = test_data["ready_sauces"]
    
    print(f"📊 Загружено {len(product_data['product_list'])} продуктов для тестирования")
    
    # Создаем мок-адаптер с предопределенными ответами
    mock_responses = {
        "барбекю": {"name": "барбекю"},
        "горчичный": {"name": "горчичный"},
        "бутылка": {"packaging": "бутылка_пластиковая"},
        "калори": {"kbgu": "низкие_до_150"},
        "жир": {"kbgu": "высокожирные_свыше_30"},
        "millgri": {"name": "Millgri"}
    }
    
    mock_adapter = MockAdapter(mock_responses)
    
    # Создаем универсальный ToolService
    tool_service = ToolService(mock_adapter)
    
    # Регистрируем HoReCa обработчик
    horeca_handler = HoReCaHandler()
    tool_service.register_subsector("01", horeca_handler)
    
    print(f"✅ Инициализирован ToolService с поддержкой отраслей: {tool_service.get_supported_subsectors()}")
    
    # Тестовые сценарии
    test_scenarios = [
        {
            "name": "Поиск соуса Барбекю",
            "query": "Найди соус Барбекю",
            "expected": "name: барбекю"
        },
        {
            "name": "Поиск горчичного соуса",
            "query": "Покажи горчичные соусы",
            "expected": "name: горчичный"
        },
        {
            "name": "Поиск по упаковке",
            "query": "Какие соусы в пластиковых бутылках?",
            "expected": "packaging: бутылка_пластиковая"
        },
        {
            "name": "Поиск по бренду",
            "query": "Соусы Millgri",
            "expected": "name: Millgri"
        }
    ]
    
    # Выполняем тестирование
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 ТЕСТ {i}: {scenario['name']}")
        print(f"📝 Запрос: {scenario['query']}")
        print(f"🎯 Ожидаемый фильтр: {scenario['expected']}")
        print("-" * 60)
        
        start_time = time.time()
        
        # Выполняем tool calling
        result = tool_service.process_query(
            query=scenario['query'],
            subsector_id="01",
            file_name="ready_sauces.json",
            data=product_data
        )
        
        execution_time = time.time() - start_time
        
        # Выводим результаты
        print(f"✅ Успех: {result.success}")
        print(f"🛠️ Выбранный tool: {result.selected_tool}")
        print(f"📋 Параметры: {result.tool_parameters}")
        print(f"⏱️ Время выполнения: {execution_time:.3f}с")
        
        if result.success and result.filtered_data:
            print(f"📦 Найдено продуктов: {len(result.filtered_data)}")
            
            # Показываем найденные продукты
            for j, product_json in enumerate(result.filtered_data, 1):
                try:
                    product = json.loads(product_json)
                    print(f"  {j}. {product['name']}")
                except json.JSONDecodeError:
                    print(f"  {j}. [Ошибка парсинга JSON]")
        else:
            print("❌ Фильтрация не удалась или не найдено продуктов")
            if result.error_message:
                print(f"💥 Ошибка: {result.error_message}")
    
    print(f"\n{'='*80}")
    print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print(f"{'='*80}")
    
    # Возвращаем информацию о последнем результате для проверки
    return {
        "service_info": tool_service.get_subsector_info("01"),
        "supported_subsectors": tool_service.get_supported_subsectors(),
        "last_result": result
    }


if __name__ == "__main__":
    # Запуск теста
    test_result = test_horeca_tool_calling()
    
    print("\n📊 ИТОГОВАЯ ИНФОРМАЦИЯ:")
    print(f"Поддерживаемые отрасли: {test_result['supported_subsectors']}")
    print(f"Информация о HoReCa: {test_result['service_info']}")
    print(f"Последний результат: успех={test_result['last_result'].success}")