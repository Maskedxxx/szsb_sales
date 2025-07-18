"""
Промежуточный маппинг enum → реальные данные для ready_sauces.json

Преобразует "чистые" enum'ы в паттерны поиска для реальных данных продуктов.
Использует regex для числовых значений (калорийность, жиры).
"""

import re
from typing import List, Dict, Any, Callable

# ===================== РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ =====================

# Извлечение калорийности из текста КБЖУ (число после слэша: КДж/ккал – 865/207)
CALORIES_REGEX = re.compile(r"ккал\s*[-–—]?\s*\d+/(\d+)", re.IGNORECASE)

# Извлечение жиров из текста КБЖУ  
FAT_REGEX = re.compile(r"Жиры,\s*г\s*[-–—]?\s*([\d,\.]+)", re.IGNORECASE)

# ===================== ПРОСТЫЕ ТЕКСТОВЫЕ МАППИНГИ =====================

# Маппинг enum'ов к паттернам поиска в реальных данных ready_sauces.json
READY_SAUCES_ENUM_MAPPING: Dict[str, List[str]] = {
    
    # ========== Ключ "name" ==========
    # sauce_types
    "горчичный": ["Горчичный", "горчичный"],
    "барбекю": ["Барбекю", "барбекю"],
    "сырный": ["Сырный", "сырный", "СЫРНЫЙ"],
    "майонезный": ["майонезный", "Майонезный"],
    "кетчуп": ["Кетчуп", "кетчуп"],
    "карри": ["Карри", "карри"],
    "терияки": ["Терияки", "терияки"],
    
    # base_types
    "растительные_масла": ["растительных масел", "Растительных масел"],
    "томатный": ["томатный", "Томатный"],
    "соевый": ["соевый", "Соевый"],
    "сливочный": ["сливочный", "Сливочный", "сливочно"],
    
    # brands
    "Millgri": ["Millgri®", "Millgri"],
    "КЛАССИКА": ["«КЛАССИКА»", "КЛАССИКА"],
    
    # categories
    "премиум": ["Премиум", "премиум"],
    "первая_категория": ["первой категории", "Первой категории"],
    
    # ========== Ключ "packaging" ==========
    # package_types
    "бутылка_пластиковая": ["Бутылка пластиковая", "бутылка пластиковая"],
    "bag_in_box": ["bag-in-box", "bag in box"],
    "блистер": ["Блистер", "блистер"],
    
    # volume_ranges
    "25мл": ["25 мл"],
    "0_8л": ["0,8 л"],
    "0_9л": ["0,9 л"],
    "1кг": ["1 кг"],
    "10_12кг": ["10 кг", "12 кг", "10-12 кг", "10–12 кг"],
    
    # special
    "с_дозатором": ["с дозатором", "дозатором"],
    "в_гофрокоробе": ["в гофрокороб", "гофрокороб"],
    
    # ========== Ключ "shelf_life" ==========
    # duration
    "6_месяцев": ["6 месяцев", "6 месяца"],
    "9_месяцев": ["9 месяцев", "9 месяца"],
    "12_месяцев": ["12 месяцев", "12 месяца"],
    
    # storage_temp
    "0_20_градусов": ["0 °С до 20 °С", "от 0 °С до 20 °С"],
    "1_27_градусов": ["1 °С до 27 °С", "от 1 °С до 27 °С"],
    
    # after_opening
    "2_дня_холодильник": ["2 дня при температуре от 2 °С до 6 °С"],
    "30_дней_холодильник": ["30 дней при температуре от 2 °С до 6 °С"],
    "4_месяца_холодильник": ["4 месяца при температуре от 2 °С до 6 °С"],
    "6_месяцев": ["6 месяцев при температуре от 1 °С до 27 °С"],
}

# ===================== ФУНКЦИИ ДЛЯ ЧИСЛОВЫХ ПРОВЕРОК =====================

def check_calorie_range(kbgu_text: str, enum_value: str) -> bool:
    """
    Проверяет попадание калорийности в указанный диапазон с помощью regex.
    
    Args:
        kbgu_text: Текст с КБЖУ данными
        enum_value: Enum значение диапазона калорийности
        
    Returns:
        True если калорийность в диапазоне, False иначе
    """
    match = CALORIES_REGEX.search(kbgu_text)
    if not match:
        return False
    
    try:
        calories = int(match.group(1))
        
        if enum_value == "низкие_до_150":
            return calories < 150
        elif enum_value == "средние_150_250":
            return 150 <= calories <= 250
        elif enum_value == "высокие_250_400":
            return 250 < calories <= 400
        
    except (ValueError, IndexError):
        pass
    
    return False


def check_fat_content(kbgu_text: str, enum_value: str) -> bool:
    """
    Проверяет содержание жиров с помощью regex.
    
    Args:
        kbgu_text: Текст с КБЖУ данными
        enum_value: Enum значение содержания жиров
        
    Returns:
        True если содержание жиров соответствует диапазону, False иначе
    """
    match = FAT_REGEX.search(kbgu_text)
    if not match:
        return False
    
    try:
        fat_content = float(match.group(1).replace(',', '.'))
        
        if enum_value == "обезжиренные":
            return fat_content == 0.0
        elif enum_value == "низкожирные_до_15":
            return 0 < fat_content <= 15
        elif enum_value == "среднежирные_15_30":
            return 15 < fat_content <= 30
        elif enum_value == "высокожирные_свыше_30":
            return fat_content > 30
        
    except (ValueError, IndexError):
        pass
    
    return False


# ===================== СПЕЦИАЛЬНЫЕ ПРОВЕРКИ ДЛЯ KBGU =====================

# Маппинг enum'ов KBGU к функциям проверки
KBGU_CHECKERS: Dict[str, Callable[[str, str], bool]] = {
    # Калорийность
    "низкие_до_150": check_calorie_range,
    "средние_150_250": check_calorie_range,
    "высокие_250_400": check_calorie_range,
    
    # Содержание жиров
    "обезжиренные": check_fat_content,
    "низкожирные_до_15": check_fat_content,
    "среднежирные_15_30": check_fat_content,
    "высокожирные_свыше_30": check_fat_content,
}

# ===================== ОСНОВНЫЕ ФУНКЦИИ =====================

def get_search_patterns(enum_value: str) -> List[str]:
    """
    Возвращает паттерны поиска для enum значения.
    
    Args:
        enum_value: Значение enum из horeca_enum_mapping.py
        
    Returns:
        Список паттернов для поиска в реальных данных
    """
    patterns = READY_SAUCES_ENUM_MAPPING.get(enum_value, [])
    
    # Если паттерны не найдены, возвращаем исходное значение как fallback
    if not patterns:
        return [enum_value]
    
    return patterns


def has_enum_match(text: str, enum_value: str, field_key: str = None) -> bool:
    """
    Проверяет, содержит ли текст совпадение с enum значением.
    
    Args:
        text: Текст для поиска
        enum_value: Значение enum
        field_key: Ключ поля (для специальной обработки kbgu)
        
    Returns:
        True если найдено совпадение, False иначе
    """
    if not text or not enum_value:
        return False
    
    # Специальная обработка для ключа kbgu
    if field_key == "kbgu" and enum_value in KBGU_CHECKERS:
        checker_func = KBGU_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    # Обычный текстовый поиск
    patterns = get_search_patterns(enum_value)
    text_lower = text.lower()
    
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return True
    
    return False


# ===================== ТЕСТИРОВАНИЕ =====================

if __name__ == "__main__":
    print("=== ТЕСТ ТЕКСТОВЫХ ПАТТЕРНОВ ===")
    print(f"'барбекю' паттерны: {get_search_patterns('барбекю')}")
    print(f"'bag_in_box' паттерны: {get_search_patterns('bag_in_box')}")
    print(f"'6_месяцев' паттерны: {get_search_patterns('6_месяцев')}")
    
    print("\n=== ТЕСТ ТЕКСТОВЫХ СОВПАДЕНИЙ ===")
    print(f"'Соус Барбекю' содержит 'барбекю': {has_enum_match('Соус Барбекю', 'барбекю')}")
    print(f"'bag-in-box' содержит 'bag_in_box': {has_enum_match('bag-in-box', 'bag_in_box')}")
    print(f"'Millgri®' содержит 'Millgri': {has_enum_match('Millgri®', 'Millgri')}")
    
    print("\n=== ТЕСТ ЧИСЛОВЫХ ПРОВЕРОК ===")
    kbgu_low = "КДж/ккал – 465/109\\nБелки, г – 1,2\\nЖиры, г – 0,0"
    kbgu_high = "КДж/ккал – 1586/385\\nБелки, г – 0,5\\nЖиры, г – 40,2"
    
    print(f"KBGU {kbgu_low}")
    print(f"  'низкие_до_150': {has_enum_match(kbgu_low, 'низкие_до_150', 'kbgu')}")
    print(f"  'обезжиренные': {has_enum_match(kbgu_low, 'обезжиренные', 'kbgu')}")
    
    print(f"KBGU {kbgu_high}")
    print(f"  'высокие_250_400': {has_enum_match(kbgu_high, 'высокие_250_400', 'kbgu')}")
    print(f"  'высокожирные_свыше_30': {has_enum_match(kbgu_high, 'высокожирные_свыше_30', 'kbgu')}")
    
    print("\n=== ТЕСТ REGEX ИЗВЛЕЧЕНИЯ ===")
    test_kbgu = "КДж/ккал – 1297/315\\nБелки, г – 0,3\\nЖиры, г – 32,2\\nУглеводы, г – 5,9"
    
    cal_match = CALORIES_REGEX.search(test_kbgu)
    fat_match = FAT_REGEX.search(test_kbgu)
    
    print(f"Извлеченные калории: {cal_match.group(1) if cal_match else 'Не найдено'}")
    print(f"Извлеченные жиры: {fat_match.group(1) if fat_match else 'Не найдено'}")