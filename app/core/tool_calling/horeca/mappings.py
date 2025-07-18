"""
Маппинги для HoReCa отрасли.

Содержит все необходимые маппинги для работы с данными HoReCa:
- Ключи продуктов и их описания
- Enum значения для каждого ключа
- Универсальные паттерны для сопоставления
"""

import re
from typing import Dict, List, Callable

# ===================== КЛЮЧИ ПРОДУКТОВ =====================

# Импортированный из horeca_keys_mapping.py
KEYS_MAPPING = {
    "breadings_and_cutlets.json": {
        "file_description": "Панировки быстрого приготовления и котлетные смеси DENFAI®",
        "product_keys": {
            "name": {
                "description": "Название продукта - панировки или котлетной смеси",
                "filter_impact": "Позволяет искать конкретные продукты по названию или типу",
                "data_type": "string",
                "examples": ["Панировка быстрого приготовления «Для курицы Оригинальная» DENFAI®"]
            },
            "kbgu": {
                "description": "Калорийность, белки, жиры, углеводы на 100г продукта",
                "filter_impact": "Позволяет фильтровать по энергетической ценности",
                "data_type": "string",
                "examples": ["КДж/ккал – 1384/326\\nБелки, г – 9,9\\nЖиры, г – 1,1"]
            },
            "shelf_life": {
                "description": "Условия и сроки хранения продукта",
                "filter_impact": "Позволяет фильтровать по срокам годности",
                "data_type": "string",
                "examples": ["12 месяцев при температуре от 5 °С до 30 °С"]
            },
            "packaging": {
                "description": "Тип и вес упаковки продукта",
                "filter_impact": "Позволяет фильтровать по типам упаковки и весу",
                "data_type": "string",
                "examples": ["Металлизированные пакеты массой нетто 5 кг"]
            }
        }
    },
    "ready_sauces.json": {
        "file_description": "Готовые соусы Millgri® и «КЛАССИКА»",
        "product_keys": {
            "name": {
                "description": "Название готового соуса",
                "filter_impact": "Позволяет искать по типу соуса (горчичный, барбекю, сырный) и бренду",
                "data_type": "string",
                "examples": ["Соус на основе растительных масел «Горчичный» Millgri®"]
            },
            "kbgu": {
                "description": "Калорийность и пищевая ценность соуса",
                "filter_impact": "Позволяет фильтровать по калорийности и содержанию жиров",
                "data_type": "string",
                "examples": ["КДж/ккал – 865/207\\nБелки, г – 1,3\\nЖиры, г – 11,7"]
            },
            "shelf_life": {
                "description": "Условия хранения готовых соусов",
                "filter_impact": "Позволяет фильтровать по срокам годности и температуре хранения",
                "data_type": "string",
                "examples": ["6 месяцев при температуре от 1 °С до 27 °С"]
            },
            "packaging": {
                "description": "Упаковка готовых соусов",
                "filter_impact": "Позволяет фильтровать по типу упаковки и объему",
                "data_type": "string",
                "examples": ["Бутылка пластиковая объемом 0,8 л"]
            }
        }
    }
    # Добавить остальные файлы по аналогии...
}

# ===================== ENUM ЗНАЧЕНИЯ =====================

# Импортированный из horeca_enum_mapping.py
ENUM_MAPPING = {
    "ready_sauces.json": {
        "name": {
            "sauce_types": ["горчичный", "барбекю", "сырный", "майонезный", "кетчуп", "карри", "терияки"],
            "base_types": ["растительные_масла", "томатный", "соевый", "сливочный"],
            "brands": ["Millgri", "КЛАССИКА"],
            "categories": ["премиум", "первая_категория"]
        },
        "kbgu": {
            "calorie_ranges": ["низкие_до_150", "средние_150_250", "высокие_250_400"],
            "fat_content": ["обезжиренные", "низкожирные_до_15", "среднежирные_15_30", "высокожирные_свыше_30"]
        },
        "shelf_life": {
            "duration": ["6_месяцев", "9_месяцев", "12_месяцев"],
            "storage_temp": ["0_20_градусов", "1_27_градусов"],
            "after_opening": ["2_дня_холодильник", "30_дней_холодильник", "4_месяца_холодильник"]
        },
        "packaging": {
            "package_types": ["бутылка_пластиковая", "bag_in_box", "блистер"],
            "volume_ranges": ["25мл", "0_8л", "0_9л", "1кг", "10_12кг"],
            "special": ["с_дозатором", "в_гофрокоробе"]
        }
    }
    # Добавить остальные файлы по аналогии...
}

# ===================== УНИВЕРСАЛЬНЫЕ ПАТТЕРНЫ =====================

# Регулярные выражения для числовых значений
CALORIES_REGEX = re.compile(r"ккал\\s*[-–—]?\\s*\\d+/(\\d+)", re.IGNORECASE)
FAT_REGEX = re.compile(r"Жиры,\\s*г\\s*[-–—]?\\s*([\\d,\\.]+)", re.IGNORECASE)
PROTEIN_REGEX = re.compile(r"Белки,\\s*г\\s*[-–—]?\\s*([\\d,\\.]+)", re.IGNORECASE)
CARBS_REGEX = re.compile(r"Углеводы,\\s*г\\s*[-–—]?\\s*([\\d,\\.]+)", re.IGNORECASE)

# Универсальные текстовые маппинги
UNIVERSAL_MAPPING: Dict[str, List[str]] = {
    # Общие бренды
    "Millgri": ["Millgri®", "Millgri", "MILLGRI"],
    "КЛАССИКА": ["«КЛАССИКА»", "КЛАССИКА", "Классика"],
    
    # Типы упаковки
    "бутылка_пластиковая": ["Бутылка пластиковая", "бутылка пластиковая", "Бутылка"],
    "bag_in_box": ["bag-in-box", "bag in box", "«bag-in-box»"],
    "блистер": ["Блистер", "блистер"],
    
    # Соусы
    "горчичный": ["Горчичный", "горчичный"],
    "барбекю": ["Барбекю", "барбекю"],
    "сырный": ["Сырный", "сырный", "СЫРНЫЙ"],
    "майонезный": ["майонезный", "Майонезный"],
    "кетчуп": ["Кетчуп", "кетчуп"],
    "карри": ["Карри", "карри"],
    "терияки": ["Терияки", "терияки"],
    
    # Основы соусов
    "растительные_масла": ["растительных масел", "Растительных масел"],
    "томатный": ["томатный", "Томатный"],
    "соевый": ["соевый", "Соевый"],
    "сливочный": ["сливочный", "Сливочный", "сливочно"],
    
    # Сроки хранения
    "6_месяцев": ["6 месяцев", "6 месяца"],
    "9_месяцев": ["9 месяцев", "9 месяца"],
    "12_месяцев": ["12 месяцев", "12 месяца"],
    
    # Температурные режимы
    "0_20_градусов": ["0 °С до 20 °С", "от 0 °С до 20 °С"],
    "1_27_градусов": ["1 °С до 27 °С", "от 1 °С до 27 °С"],
    
    # Дополнительные элементы
    "с_дозатором": ["с дозатором", "дозатором"],
    "в_гофрокоробе": ["в гофрокороб", "гофрокороб"],
    "премиум": ["Премиум", "премиум"],
    "первая_категория": ["первой категории", "Первой категории"],
}

# ===================== ФУНКЦИИ ДЛЯ ЧИСЛОВЫХ ПРОВЕРОК =====================

def check_calorie_range(kbgu_text: str, enum_value: str) -> bool:
    """Проверяет попадание калорийности в указанный диапазон."""
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
    """Проверяет содержание жиров."""
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


# Маппинг enum'ов к функциям проверки
KBGU_CHECKERS: Dict[str, Callable[[str, str], bool]] = {
    "низкие_до_150": check_calorie_range,
    "средние_150_250": check_calorie_range,
    "высокие_250_400": check_calorie_range,
    "обезжиренные": check_fat_content,
    "низкожирные_до_15": check_fat_content,
    "среднежирные_15_30": check_fat_content,
    "высокожирные_свыше_30": check_fat_content,
}

# ===================== ОСНОВНЫЕ ФУНКЦИИ =====================

def get_search_patterns(enum_value: str) -> List[str]:
    """Возвращает паттерны поиска для enum значения."""
    patterns = UNIVERSAL_MAPPING.get(enum_value, [])
    return patterns if patterns else [enum_value]


def has_enum_match(text: str, enum_value: str, field_key: str = None) -> bool:
    """Проверяет, содержит ли текст совпадение с enum значением."""
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