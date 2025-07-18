"""
Функция фильтрации данных HoReCa с использованием промежуточного маппинга enum → реальные данные.

Использует готовые маппинги для точного поиска по паттернам и regex для числовых значений.
"""

import json
import pandas as pd
import logging
from typing import List

# Импортируем универсальный промежуточный маппинг
from universal_enum_mapping import has_universal_enum_match

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def filter_horeca_products_smart(
    product_list: List[str],
    filter_key: str,
    enum_value: str
) -> List[str]:
    """
    Фильтрует JSON строки продуктов используя промежуточный маппинг enum → реальные данные.
    
    Args:
        product_list: Список JSON строк из product_list файла HoReCa
        filter_key: Ключ для фильтрации ("name", "packaging", "kbgu", "shelf_life")
        enum_value: Значение enum из horeca_enum_mapping.py
        
    Returns:
        Список отфильтрованных JSON строк продуктов
    """
    logger.info(f"Умная фильтрация {len(product_list)} продуктов по ключу '{filter_key}' со значением '{enum_value}'")
    
    # Парсим все JSON строки в DataFrame для удобства
    products_data = []
    original_json_strings = []
    
    for product_json in product_list:
        try:
            product = json.loads(product_json)
            products_data.append(product)
            original_json_strings.append(product_json)
        except json.JSONDecodeError as e:
            logger.warning(f"Ошибка парсинга JSON: {e}")
            continue
    
    if not products_data:
        logger.warning("Нет валидных продуктов для фильтрации")
        return []
    
    # Создаем DataFrame
    df = pd.DataFrame(products_data)
    df['original_json'] = original_json_strings
    
    logger.info(f"Успешно обработано {len(df)} продуктов")
    
    # Проверяем наличие ключа
    if filter_key not in df.columns:
        logger.error(f"Ключ '{filter_key}' не найден в продуктах. Доступные ключи: {list(df.columns)}")
        return []
    
    # Умная фильтрация: используем универсальный промежуточный маппинг с паттернами и regex
    mask = df[filter_key].apply(lambda x: has_universal_enum_match(x, enum_value, filter_key))
    filtered_df = df[mask]
    
    logger.info(f"Найдено совпадений: {len(filtered_df)} из {len(df)}")
    
    # Возвращаем оригинальные JSON строки
    return filtered_df['original_json'].tolist()


# Полноценное тестирование с реальными данными
if __name__ == "__main__":
    print("=== ЗАГРУЗКА РЕАЛЬНЫХ ДАННЫХ ИЗ ready_sauces.json ===")
    
    # Загружаем все данные из файла ready_sauces.json
    try:
        with open('/Users/mask/Documents/Проеты_2025/snabik_sales/szsb_sales/app/routes/horeca/ready_sauces.json', 'r', encoding='utf-8') as f:
            sauce_data = json.load(f)
        
        # Извлекаем product_list
        product_list = sauce_data['ready_sauces']['product_list']
        print(f"Загружено {len(product_list)} продуктов из ready_sauces.json")
        
    except FileNotFoundError:
        print("Файл ready_sauces.json не найден, используем тестовые данные")
        product_list = [
            '{"name": "Соус на основе растительных масел «Горчичный» Millgri®", "kbgu": "КДж/ккал – 865/207\\nБелки, г – 1,3\\nЖиры, г – 11,7\\nУглеводы, г – 23,1", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев при температуре от 1 °С до 27 °С"}',
            '{"name": "Соус томатный «Барбекю» Millgri®", "kbgu": "КДж/ккал – 801/189\\nБелки, г – 0,9\\nЖиры, г – 0,1\\nУглеводы, г – 44,3", "packaging": "Упаковка «bag-in-box» помещенная в гофрокороб, масса нетто 10 кг", "shelf_life": "12 месяцев при температуре от 1 °С до 27 °С"}',
            '{"name": "Соус майонезный «Сливочно-чесночный» Millgri®", "kbgu": "КДж/ккал – 1586/385\\nБелки, г – 0,5\\nЖиры, г – 40,2\\nУглеводы, г – 5,0", "packaging": "Бутылка пластиковая объемом 0,8 л", "shelf_life": "6 месяцев при температуре от 1 °С до 27 °С"}'
        ]
    
    print("\n" + "="*70)
    print("ТЕСТИРУЕМ УМНУЮ ФИЛЬТРАЦИЮ КАК ИЗ TOOL CALLING")
    print("="*70)
    
    # ========== ТЕСТ 1: Фильтрация по названию (enum из tool) ==========
    print("\n🔍 ТЕСТ 1: LLM выбрала ключ='name' и enum='барбекю'")
    barbecue_results = filter_horeca_products_smart(product_list, "name", "барбекю")
    print(f"Найдено продуктов с 'барбекю': {len(barbecue_results)}")
    for i, product_json in enumerate(barbecue_results, 1):
        product = json.loads(product_json)
        print(f"  {i}. {product['name']}")
    
    # ========== ТЕСТ 2: Фильтрация по упаковке (enum из tool) ==========
    print("\n📦 ТЕСТ 2: LLM выбрала ключ='packaging' и enum='бутылка_пластиковая'")
    bottle_results = filter_horeca_products_smart(product_list, "packaging", "бутылка_пластиковая")
    print(f"Найдено продуктов в пластиковых бутылках: {len(bottle_results)}")
    for i, product_json in enumerate(bottle_results, 1):
        product = json.loads(product_json)
        print(f"  {i}. {product['name']} - {product['packaging'][:50]}...")
    
    # ========== ТЕСТ 3: Фильтрация по калорийности (regex) ==========
    print("\n🔥 ТЕСТ 3: LLM выбрала ключ='kbgu' и enum='низкие_до_150'")
    low_cal_results = filter_horeca_products_smart(product_list, "kbgu", "низкие_до_150")
    print(f"Найдено низкокалорийных продуктов (< 150 ккал): {len(low_cal_results)}")
    for i, product_json in enumerate(low_cal_results, 1):
        product = json.loads(product_json)
        kbgu_short = product['kbgu'].split('\\n')[0]  # Первая строка с калориями
        print(f"  {i}. {product['name']} - {kbgu_short}")
    
    # ========== ТЕСТ 4: Фильтрация по высокой калорийности (regex) ==========
    print("\n🔥 ТЕСТ 4: LLM выбрала ключ='kbgu' и enum='высокие_250_400'")
    high_cal_results = filter_horeca_products_smart(product_list, "kbgu", "высокие_250_400")
    print(f"Найдено высококалорийных продуктов (250-400 ккал): {len(high_cal_results)}")
    for i, product_json in enumerate(high_cal_results, 1):
        product = json.loads(product_json)
        kbgu_short = product['kbgu'].split('\\n')[0]  # Первая строка с калориями
        print(f"  {i}. {product['name']} - {kbgu_short}")
    
    # ========== ТЕСТ 5: Фильтрация по жирности (regex) ==========
    print("\n🧈 ТЕСТ 5: LLM выбрала ключ='kbgu' и enum='высокожирные_свыше_30'")
    high_fat_results = filter_horeca_products_smart(product_list, "kbgu", "высокожирные_свыше_30")
    print(f"Найдено высокожирных продуктов (> 30г жиров): {len(high_fat_results)}")
    for i, product_json in enumerate(high_fat_results, 1):
        product = json.loads(product_json)
        kbgu_lines = product['kbgu'].split('\\n')
        fat_line = next((line for line in kbgu_lines if 'Жиры' in line), 'N/A')
        print(f"  {i}. {product['name']} - {fat_line}")
    
    # ========== ТЕСТ 6: Фильтрация по сроку хранения ==========
    print("\n⏰ ТЕСТ 6: LLM выбрала ключ='shelf_life' и enum='12_месяцев'")
    shelf_12_results = filter_horeca_products_smart(product_list, "shelf_life", "12_месяцев")
    print(f"Найдено продуктов со сроком хранения 12 месяцев: {len(shelf_12_results)}")
    for i, product_json in enumerate(shelf_12_results, 1):
        product = json.loads(product_json)
        shelf_short = product['shelf_life'][:80] + "..." if len(product['shelf_life']) > 80 else product['shelf_life']
        print(f"  {i}. {product['name']} - {shelf_short}")
    
    # ========== ТЕСТ 7: Фильтрация по бренду ==========
    print("\n🏷️ ТЕСТ 7: LLM выбрала ключ='name' и enum='Millgri'")
    millgri_results = filter_horeca_products_smart(product_list, "name", "Millgri")
    print(f"Найдено продуктов бренда Millgri: {len(millgri_results)}")
    for i, product_json in enumerate(millgri_results[:5], 1):  # Показываем только первые 5
        product = json.loads(product_json)
        print(f"  {i}. {product['name']}")
    if len(millgri_results) > 5:
        print(f"  ... и еще {len(millgri_results) - 5} продуктов")
    
    print("\n" + "="*70)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print(f"Всего протестировано комбинаций: 7")
    print(f"Общее количество продуктов в базе: {len(product_list)}")
    print("="*70)