"""
Универсальный промежуточный маппинг enum → реальные данные для всех файлов HoReCa.

Расширяет ready_sauces_enum_mapping.py для поддержки всех 9 файлов HoReCa.
Использует regex для числовых значений и текстовые паттерны для остальных.
"""

import re
from typing import List, Dict, Callable

# Импортируем готовые функции из ready_sauces_enum_mapping
from ready_sauces_enum_mapping import (
    KBGU_CHECKERS, check_calorie_range, check_fat_content
)

# ===================== ДОПОЛНИТЕЛЬНЫЕ РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ =====================

# Извлечение белков из текста КБЖУ
PROTEIN_REGEX = re.compile(r"Белки,\s*г\s*[-–—]?\s*([\d,\.]+)", re.IGNORECASE)

# Извлечение углеводов из текста КБЖУ
CARBS_REGEX = re.compile(r"Углеводы,\s*г\s*[-–—]?\s*([\d,\.]+)", re.IGNORECASE)

# Извлечение веса из упаковки
WEIGHT_REGEX = re.compile(r"(\d+(?:,\d+)?)\s*кг", re.IGNORECASE)

# Извлечение объема из упаковки
VOLUME_REGEX = re.compile(r"(\d+(?:,\d+)?)\s*л", re.IGNORECASE)

# Извлечение срока хранения в месяцах
SHELF_MONTHS_REGEX = re.compile(r"(\d+)\s*месяц", re.IGNORECASE)

# ===================== УНИВЕРСАЛЬНЫЕ ТЕКСТОВЫЕ МАППИНГИ =====================

# Общие маппинги для всех файлов HoReCa
UNIVERSAL_ENUM_MAPPING: Dict[str, List[str]] = {
    
    # ========== ОБЩИЕ БРЕНДЫ ==========
    "Millgri": ["Millgri®", "Millgri", "MILLGRI"],
    "КЛАССИКА": ["«КЛАССИКА»", "КЛАССИКА", "Классика"],
    "DEL_AR": ["DEL'AR®", "DEL'AR", "DELAR"],
    "AIBI": ["AIBI®", "AIBI"],
    "DENFAI": ["DENFAI®", "DENFAI"],
    "Densoy": ["Densoy", "DENSOY"],
    
    # ========== ОБЩИЕ ТИПЫ УПАКОВКИ ==========
    "бутылка_пластиковая": ["Бутылка пластиковая", "бутылка пластиковая", "Бутылка"],
    "ведро_пластиковое": ["Ведро пластиковое", "ведро пластиковое", "Ведро"],
    "bag_in_box": ["bag-in-box", "bag in box", "«bag-in-box»"],
    "блистер": ["Блистер", "блистер"],
    "крафт_мешок": ["Крафт-мешок", "крафт-мешок", "крафт мешок"],
    "металлизированные_пакеты": ["Металлизированные пакеты", "металлизированные пакеты"],
    "канистра_пластиковая": ["Канистра пластиковая", "канистра пластиковая"],
    "оболочка": ["Оболочка", "оболочка"],
    "гофрокороб": ["гофрокороб", "Гофрокороб"],
    
    # ========== ОБЩИЕ ДИАПАЗОНЫ ВЕСА ==========
    "до_1кг": ["до 1 кг", "0,8 кг", "0,9 кг"],
    "1_5кг": ["1 кг", "2 кг", "3 кг", "4 кг", "5 кг"],
    "5_15кг": ["5 кг", "10 кг", "12 кг", "15 кг"],
    "15_25кг": ["15 кг", "20 кг", "25 кг"],
    
    # ========== ОБЩИЕ ОБЪЕМЫ ==========
    "25мл": ["25 мл"],
    "0_8л": ["0,8 л"],
    "0_9л": ["0,9 л"],
    "1л": ["1 л"],
    
    # ========== ОБЩИЕ УСЛОВИЯ ХРАНЕНИЯ ==========
    "12_месяцев": ["12 месяцев", "12 месяца"],
    "6_месяцев": ["6 месяцев", "6 месяца"],
    "9_месяцев": ["9 месяцев", "9 месяца"],
    "3_месяца": ["3 месяца", "3 месяца"],
    "4_месяца": ["4 месяца", "4 месяца"],
    "18_месяцев": ["18 месяцев", "18 месяца"],
    "24_месяца": ["24 месяца", "24 месяца"],
    
    # ========== ТЕМПЕРАТУРНЫЕ РЕЖИМЫ ==========
    "0_20_градусов": ["0 °С до 20 °С", "от 0 °С до 20 °С"],
    "1_27_градусов": ["1 °С до 27 °С", "от 1 °С до 27 °С"],
    "2_6_градусов": ["2 °С до 6 °С", "от 2 °С до 6 °С"],
    "5_30_градусов": ["5 °С до 30 °С", "от 5 °С до 30 °С"],
    "0_25_градусов": ["0 °С до 25 °С", "от 0 °С до 25 °С"],
    
    # ========== СПЕЦИФИЧНЫЕ МАППИНГИ ПО ФАЙЛАМ ==========
    
    # BREADINGS_AND_CUTLETS
    "панировка": ["Панировка", "панировка"],
    "кляр": ["Кляр", "кляр"],
    "котлетная_смесь": ["котлетная смесь", "Котлетная смесь"],
    "для_курицы": ["Для курицы", "для курицы"],
    "оригинальная": ["Оригинальная", "оригинальная"],
    "острая": ["Острая", "острая"],
    "темпурная": ["Темпурная", "темпурная"],
    "льезон": ["Льезон", "льезон"],
    
    # CHEESES_AND_MILK
    "моцарелла": ["MOZZARELLA", "Mozzarella", "моцарелла"],
    "творожный": ["творожный", "Творожный"],
    "полутвердый": ["полутвердый", "Полутвердый"],
    "для_пиццы": ["для пиццы", "Для пиццы"],
    "классическая": ["Классическая", "классическая"],
    "люкс": ["Люкс", "люкс"],
    "лайт": ["Лайт", "лайт"],
    "МОЦАРЕЛЛА_ДЛЯ_ПИЦЦЫ": ["МОЦАРЕЛЛА ДЛЯ ПИЦЦЫ"],
    "ЛОМТЕВЫЕ_СЫРЫ": ["ЛОМТЕВЫЕ СЫРЫ"],
    "МЯГКИЕ_СЫРЫ": ["МЯГКИЕ СЫРЫ"],
    
    # DRINK_CONCENTRATES
    "квасное_сусло": ["квасного сусла", "Квасного сусла"],
    "лимонад": ["лимонад", "Лимонад"],
    "ягодный_концентрат": ["ягодный", "Ягодный"],
    "мохито": ["Мохито", "мохито"],
    "клубника": ["Клубника", "клубника"],
    "клюква": ["Клюква", "клюква"],
    "облепиха": ["Облепиха", "облепиха"],
    "сухой": ["сухой", "Сухой"],
    "жидкий": ["жидкий", "Жидкий"],
    
    # FILLINGS
    "кремовые": ["КРЕМОВЫЕ", "кремовые"],
    "жировые": ["ЖИРОВЫЕ", "жировые"],
    "фруктовые_ягодные": ["ФРУКТОВЫЕ И ЯГОДНЫЕ", "фруктовые и ягодные"],
    "гастрономические": ["ГАСТРОНОМИЧЕСКИЕ", "гастрономические"],
    "ваниль": ["ванили", "Ванили", "ваниль"],
    "шоколад": ["шоколад", "Шоколад"],
    "вишня": ["вишня", "Вишня"],
    "банан": ["банан", "Банан"],
    "творог": ["творог", "Творог"],
    "йогурт": ["йогурт", "Йогурт"],
    "карамель": ["карамель", "Карамель"],
    "орех": ["орех", "Орех"],
    "трюфель": ["трюфель", "Трюфель"],
    "пралине": ["пралине", "Пралине"],
    "апельсин": ["апельсин", "Апельсин"],
    "ананас": ["ананас", "Ананас"],
    "малина": ["малина", "Малина"],
    "черника": ["черника", "Черника"],
    "яблоко": ["яблоко", "Яблоко"],
    "горчица": ["горчица", "Горчица"],
    "грибы": ["грибы", "Грибы"],
    "зелень_чеснок": ["зелень", "чеснок", "Зелень", "Чеснок"],
    "паприка": ["паприка", "Паприка"],
    "томат_базилик": ["томат", "базилик", "Томат", "Базилик"],
    "огурец": ["огурец", "Огурец"],
    
    # LUNCH_MIXES
    "бульон": ["бульон", "Бульон"],
    "суп": ["Суп", "суп"],
    "куриный": ["Куриный", "куриный"],
    "овощной": ["овощной", "Овощной"],
    "грибной": ["Грибной", "грибной"],
    "сырный": ["сырный", "Сырный"],
    "с_беконом": ["с беконом", "Беконом"],
    "Natural": ["Natural", "NATURAL"],
    "Классик": ["Классик", "КЛАССИК"],
    "Premium": ["Premium", "PREMIUM"],
    
    # PRESERVATIVES
    "глюкоза_ферментированная": ["Глюкоза ферментированная", "глюкоза ферментированная"],
    "1_01": ["1.01", "1,01"],
    "1_50": ["1.50", "1,50"],
    
    # READY_SAUCES (наследуем из ready_sauces_enum_mapping)
    "горчичный": ["Горчичный", "горчичный"],
    "барбекю": ["Барбекю", "барбекю"],
    "майонезный": ["майонезный", "Майонезный"],
    "кетчуп": ["Кетчуп", "кетчуп"],
    "карри": ["Карри", "карри"],
    "терияки": ["Терияки", "терияки"],
    "растительные_масла": ["растительных масел", "Растительных масел"],
    "томатный": ["томатный", "Томатный"],
    "соевый": ["соевый", "Соевый"],
    "сливочный": ["сливочный", "Сливочный", "сливочно"],
    "премиум": ["Премиум", "премиум"],
    "первая_категория": ["первой категории", "Первой категории"],
    "с_дозатором": ["с дозатором", "дозатором"],
    "в_гофрокоробе": ["в гофрокороб", "гофрокороб"],
    
    # SAUCE_MIXES
    "бешамель": ["Бешамель", "бешамель"],
    "деми_глас": ["деми глас", "Деми глас"],
    "быстрого_приготовления": ["быстрого приготовления", "Быстрого приготовления"],
    "кулинарный": ["кулинарный", "Кулинарный"],
    
    # TOPPINGS
    "топпинг": ["Топпинг", "топпинг"],
    "сливочная_помадка": ["сливочная помадка", "Сливочная помадка"],
}

# ===================== ФУНКЦИИ ДЛЯ ДОПОЛНИТЕЛЬНЫХ ЧИСЛОВЫХ ПРОВЕРОК =====================

def check_protein_content(kbgu_text: str, enum_value: str) -> bool:
    """
    Проверяет содержание белков с помощью regex.
    
    Args:
        kbgu_text: Текст с КБЖУ данными
        enum_value: Enum значение содержания белков
        
    Returns:
        True если содержание белков соответствует диапазону, False иначе
    """
    match = PROTEIN_REGEX.search(kbgu_text)
    if not match:
        return False
    
    try:
        protein_content = float(match.group(1).replace(',', '.'))
        
        if enum_value == "низкобелковые_до_5":
            return protein_content < 5
        elif enum_value == "среднебелковые_5_10":
            return 5 <= protein_content <= 10
        elif enum_value == "среднебелковые_5_15":
            return 5 <= protein_content <= 15
        elif enum_value == "среднебелковые_10_15":
            return 10 <= protein_content <= 15
        elif enum_value == "высокобелковые_свыше_10":
            return protein_content > 10
        elif enum_value == "высокобелковые_свыше_15":
            return protein_content > 15
        
    except (ValueError, IndexError):
        pass
    
    return False


def check_carbs_content(kbgu_text: str, enum_value: str) -> bool:
    """
    Проверяет содержание углеводов с помощью regex.
    
    Args:
        kbgu_text: Текст с КБЖУ данными
        enum_value: Enum значение содержания углеводов
        
    Returns:
        True если содержание углеводов соответствует диапазону, False иначе
    """
    match = CARBS_REGEX.search(kbgu_text)
    if not match:
        return False
    
    try:
        carbs_content = float(match.group(1).replace(',', '.'))
        
        if enum_value == "низкоуглеводные_до_50":
            return carbs_content < 50
        elif enum_value == "среднеуглеводные_50_70":
            return 50 <= carbs_content <= 70
        elif enum_value == "высокоуглеводные_свыше_70":
            return carbs_content > 70
        elif enum_value == "высокоуглеводные_50_90":
            return 50 <= carbs_content <= 90
        elif enum_value == "высокоуглеводные_50_75":
            return 50 <= carbs_content <= 75
        
    except (ValueError, IndexError):
        pass
    
    return False


def check_weight_range(packaging_text: str, enum_value: str) -> bool:
    """
    Проверяет диапазон веса упаковки с помощью regex.
    
    Args:
        packaging_text: Текст с информацией об упаковке
        enum_value: Enum значение диапазона веса
        
    Returns:
        True если вес соответствует диапазону, False иначе
    """
    match = WEIGHT_REGEX.search(packaging_text)
    if not match:
        return False
    
    try:
        weight = float(match.group(1).replace(',', '.'))
        
        if enum_value == "до_1кг":
            return weight < 1
        elif enum_value == "1_5кг":
            return 1 <= weight <= 5
        elif enum_value == "5_15кг":
            return 5 < weight <= 15
        elif enum_value == "15_25кг":
            return 15 < weight <= 25
        
    except (ValueError, IndexError):
        pass
    
    return False


def check_shelf_duration(shelf_life_text: str, enum_value: str) -> bool:
    """
    Проверяет срок хранения с помощью regex.
    
    Args:
        shelf_life_text: Текст с информацией о сроке хранения
        enum_value: Enum значение срока хранения
        
    Returns:
        True если срок соответствует, False иначе
    """
    match = SHELF_MONTHS_REGEX.search(shelf_life_text)
    if not match:
        return False
    
    try:
        months = int(match.group(1))
        
        if enum_value == "3_месяца":
            return months == 3
        elif enum_value == "6_месяцев":
            return months == 6
        elif enum_value == "9_месяцев":
            return months == 9
        elif enum_value == "12_месяцев":
            return months == 12
        elif enum_value == "18_месяцев":
            return months == 18
        elif enum_value == "24_месяца":
            return months == 24
        
    except (ValueError, IndexError):
        pass
    
    return False


# ===================== РАСШИРЕННЫЕ СПЕЦИАЛЬНЫЕ ПРОВЕРКИ =====================

# Объединяем все проверки в один словарь
UNIVERSAL_KBGU_CHECKERS: Dict[str, Callable[[str, str], bool]] = {
    # Калорийность (наследуем от ready_sauces)
    **KBGU_CHECKERS,
    
    # Дополнительные диапазоны калорийности
    "низкокалорийные_до_200": check_calorie_range,
    "до_250": check_calorie_range,
    "250_300": check_calorie_range,
    "свыше_300": check_calorie_range,
    "до_150": check_calorie_range,
    "150_250": check_calorie_range,
    "250_400": check_calorie_range,
    "низкие_до_100": check_calorie_range,
    "высокие_250_300": check_calorie_range,
    
    # Белки
    "низкобелковые_до_5": check_protein_content,
    "среднебелковые_5_10": check_protein_content,
    "среднебелковые_5_15": check_protein_content,
    "среднебелковые_10_15": check_protein_content,
    "высокобелковые_свыше_10": check_protein_content,
    "высокобелковые_свыше_15": check_protein_content,
    
    # Жиры (расширенные диапазоны)
    "низкожирные_до_5": check_fat_content,
    "низкожирные_до_20": check_fat_content,
    "среднежирные_15_25": check_fat_content,
    "среднежирные_20_25": check_fat_content,
    "высокожирные_свыше_25": check_fat_content,
    
    # Углеводы
    "низкоуглеводные_до_50": check_carbs_content,
    "среднеуглеводные_50_70": check_carbs_content,
    "высокоуглеводные_свыше_70": check_carbs_content,
    "высокоуглеводные_50_90": check_carbs_content,
    "высокоуглеводные_50_75": check_carbs_content,
}

# Специальные проверки для упаковки
PACKAGING_CHECKERS: Dict[str, Callable[[str, str], bool]] = {
    "до_1кг": check_weight_range,
    "1_5кг": check_weight_range,
    "5_15кг": check_weight_range,
    "15_25кг": check_weight_range,
}

# Специальные проверки для срока хранения
SHELF_LIFE_CHECKERS: Dict[str, Callable[[str, str], bool]] = {
    "3_месяца": check_shelf_duration,
    "6_месяцев": check_shelf_duration,
    "9_месяцев": check_shelf_duration,
    "12_месяцев": check_shelf_duration,
    "18_месяцев": check_shelf_duration,
    "24_месяца": check_shelf_duration,
}

# ===================== ОСНОВНЫЕ ФУНКЦИИ =====================

def get_universal_patterns(enum_value: str) -> List[str]:
    """
    Возвращает паттерны поиска для enum значения из универсального маппинга.
    
    Args:
        enum_value: Значение enum из horeca_enum_mapping.py
        
    Returns:
        Список паттернов для поиска в реальных данных
    """
    patterns = UNIVERSAL_ENUM_MAPPING.get(enum_value, [])
    
    # Если паттерны не найдены, возвращаем исходное значение как fallback
    if not patterns:
        return [enum_value]
    
    return patterns


def has_universal_enum_match(text: str, enum_value: str, field_key: str = None) -> bool:
    """
    Универсальная проверка совпадения enum значения с текстом.
    
    Args:
        text: Текст для поиска
        enum_value: Значение enum
        field_key: Ключ поля для специальной обработки
        
    Returns:
        True если найдено совпадение, False иначе
    """
    if not text or not enum_value:
        return False
    
    # Специальная обработка для ключа kbgu
    if field_key == "kbgu" and enum_value in UNIVERSAL_KBGU_CHECKERS:
        checker_func = UNIVERSAL_KBGU_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    # Специальная обработка для ключа packaging
    if field_key == "packaging" and enum_value in PACKAGING_CHECKERS:
        checker_func = PACKAGING_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    # Специальная обработка для ключа shelf_life
    if field_key == "shelf_life" and enum_value in SHELF_LIFE_CHECKERS:
        checker_func = SHELF_LIFE_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    # Обычный текстовый поиск
    patterns = get_universal_patterns(enum_value)
    text_lower = text.lower()
    
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return True
    
    return False


# ===================== ТЕСТИРОВАНИЕ =====================

if __name__ == "__main__":
    print("=== ТЕСТ УНИВЕРСАЛЬНЫХ ТЕКСТОВЫХ ПАТТЕРНОВ ===")
    print(f"'моцарелла' паттерны: {get_universal_patterns('моцарелла')}")
    print(f"'кремовые' паттерны: {get_universal_patterns('кремовые')}")
    print(f"'бульон' паттерны: {get_universal_patterns('бульон')}")
    print(f"'DEL_AR' паттерны: {get_universal_patterns('DEL_AR')}")
    
    print("\n=== ТЕСТ ТЕКСТОВЫХ СОВПАДЕНИЙ ===")
    print(f"'MOZZARELLA для пиццы' содержит 'моцарелла': {has_universal_enum_match('MOZZARELLA для пиццы', 'моцарелла')}")
    print(f"'КРЕМОВЫЕ начинки' содержит 'кремовые': {has_universal_enum_match('КРЕМОВЫЕ начинки', 'кремовые')}")
    print(f"'Бульон куриный' содержит 'бульон': {has_universal_enum_match('Бульон куриный', 'бульон')}")
    print(f"'DEL'AR Premium' содержит 'DEL_AR': {has_universal_enum_match('DEL\'AR Premium', 'DEL_AR')}")
    
    print("\n=== ТЕСТ ЧИСЛОВЫХ ПРОВЕРОК ===")
    test_kbgu_protein = "КДж/ккал – 1384/326\\nБелки, г – 9,9\\nЖиры, г – 1,1\\nУглеводы, г – 68,8"
    test_kbgu_carbs = "КДж/ккал – 1425/371\\nБелки, г – 4,0\\nЖиры, г – 0,0\\nУглеводы, г – 88,0"
    test_packaging = "Ведро пластиковое с крышкой массой нетто 2,5 кг"
    test_shelf = "12 месяцев при температуре от 5 °С до 30 °С"
    
    print(f"Белки 9.9г -> 'среднебелковые_5_15': {has_universal_enum_match(test_kbgu_protein, 'среднебелковые_5_15', 'kbgu')}")
    print(f"Углеводы 88г -> 'высокоуглеводные_50_90': {has_universal_enum_match(test_kbgu_carbs, 'высокоуглеводные_50_90', 'kbgu')}")
    print(f"Упаковка 2.5кг -> '1_5кг': {has_universal_enum_match(test_packaging, '1_5кг', 'packaging')}")
    print(f"Срок 12 месяцев -> '12_месяцев': {has_universal_enum_match(test_shelf, '12_месяцев', 'shelf_life')}")
    
    print("\n✅ Универсальное тестирование завершено успешно")