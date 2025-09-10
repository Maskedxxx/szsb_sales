"""
Универсальные паттерны фильтрации для мясной отрасли.
Плоский маппинг enum значений → паттерны поиска.
"""

import re
from typing import Dict, List, Any

# ===================== УНИВЕРСАЛЬНЫЙ МАППИНГ ENUM → ПАТТЕРНЫ =====================

UNIVERSAL_ENUM_MAPPING: Dict[str, List[str]] = {
    
    # ========== SEMIFINISHED.JSON -> FLAVOR_REGULATORS ==========
    # (Единственный субключ, который анализировался реальными данными)
    
    # name поле - типы продуктов:
    "глутамат_натрия": ["глутамат", "натрия", "Глутамат натрия"],
    "регулятор_вкуса": ["регулятор", "вкуса", "Регулятор вкуса"],
    "корректор_вкуса": ["корректор", "вкуса", "Корректор вкуса"],
    
    # name поле - бренды:
    "DEL'AR": ["DEL'AR®", "DEL'AR", "DELAR"],
    "номерная_серия": [r"\d+\.\d+\.\d+"],  # regex для "10.07.701", "10.07.702"
    
    # application_area поле - функции коррекции:
    "нивелирование_привкусов": ["нивелирование", "привкус"],
    "закрытие_вкуса_шкурки": ["закрывает", "шкурки", "шкурка"],
    "маскировка_БЭЖ": ["БЭЖ"],
    "сохранение_после_заморозки": ["сохраняет", "заморозки"],
    
    # flavor_profile поле - вкусовые компоненты:
    "лимон": ["лимон", "Лимон"],
    "сельдерей": ["сельдерей"],
    "тмин": ["тмин"],
    "розмарин": ["розмарин"],
    "петрушка": ["петрушка"],
    "гвоздика": ["гвоздика"],
    "горчица": ["горчица", "Горчица"],
    
    # is_halal поле - halal статусы:
    "халяль": ["true"],
    "не_указано": ["не указано", None],
    
    # ========== SEMIFINISHED.JSON -> SPICE_MIXES ==========
    
    # name поле - категории продуктов:
    "пельмени": ["пельмени", "Пельмени", "пельменей"],
    "котлеты": ["котлеты", "Котлеты", "котлет"],
    "фрикадельки": ["фрикадельки", "Фрикадельки"],
    "полуфабрикаты": ["полуфабрикатов", "полуфабрикаты"],
    "приправа": ["приправа", "Приправа"],
    
    # name поле - региональные стили:
    "восточная": ["восточная", "Восточная", "восточный", "Восточный"],
    "кавказская": ["кавказская", "Кавказская"],
    "деревенская": ["деревенская", "Деревенская"],
    "домашние": ["домашние", "Домашних"],
    
    # name поле - уровни качества:
    "naturel": ["Naturel", "NATUREL"],
    "премиум": ["премиум", "Премиум"],
    "extra": ["Extra", "EXTRA"],
    "люкс": ["люкс", "Люкс"],
    
    # name поле - вкусовые профили:
    "чесночно_пряная": ["чесноком", "Чесночно-пряная", "чесночно"],
    "сливочные": ["сливочные", "Сливочные"],
    "аппетитные": ["аппетитных", "Аппетитных"],
    "биф": ["биф", "Биф"],
    
    # application поле - ценовые сегменты:
    "премиум_сегмент": ["премиум", "Премиум", "Премиум-сегмент"],
    "средний_сегмент": ["средний", "средний сегменты"],
    "эконом_сегмент": ["эконом", "эконом сегменты", "эконом-сегменты"],
    "все_сегменты": ["всех ценовых", "все сегменты"],
    
    # application поле - типы продуктов:
    "рубленые_полуфабрикаты": ["рубленых полуфабрикатов", "производства рубленых полуфабрикатов"],
    
    # is_e_free поле - статус E-добавок:
    "с_E_добавками": ["false"],
}

# ===================== СПЕЦИАЛЬНЫЕ ПРОВЕРКИ =====================

def check_halal_status(field_value: Any, enum_value: str) -> bool:
    """Проверка halal статуса для is_halal поля."""
    if enum_value == "халяль":
        return field_value is True
    elif enum_value == "не_указано":
        return field_value is None or field_value == "не указано"
    return False

def check_e_free_status(field_value: Any, enum_value: str) -> bool:
    """Проверка статуса E-добавок для is_e_free поля."""
    if enum_value == "с_E_добавками":
        return field_value is False
    return False

def check_dosage_range(dosage_data: Any, enum_value: str) -> bool:
    """Проверка диапазонов дозировки для dosage поля."""
    if not dosage_data or not isinstance(dosage_data, dict):
        return False
    
    min_val = dosage_data.get("min_g_per_kg", 0)
    max_val = dosage_data.get("max_g_per_kg", 0)
    
    if enum_value == "низкие_4_6г":
        return 4 <= min_val <= 6 or 4 <= max_val <= 6
    elif enum_value == "средние_5_8г":
        return 5 <= min_val <= 8 or 5 <= max_val <= 8
    elif enum_value == "высокие_7_12г":
        return 7 <= min_val <= 12 or 7 <= max_val <= 12
    
    return False

# Специальные проверки
SPECIAL_CHECKERS = {
    "халяль": check_halal_status,
    "не_указано": check_halal_status,
    "с_E_добавками": check_e_free_status,
    "низкие_4_6г": check_dosage_range,
    "средние_5_8г": check_dosage_range,
    "высокие_7_12г": check_dosage_range,
}

# ===================== ОСНОВНЫЕ ФУНКЦИИ =====================

def get_universal_patterns(enum_value: str) -> List[str]:
    """
    Возвращает паттерны поиска для enum значения.
    
    Args:
        enum_value: Значение enum
        
    Returns:
        Список паттернов для поиска в реальных данных
    """
    patterns = UNIVERSAL_ENUM_MAPPING.get(enum_value, [])
    
    # Если паттерны не найдены, возвращаем исходное значение как fallback
    if not patterns:
        return [enum_value]
    
    return patterns

def has_universal_enum_match(text: str, enum_value: str, field_key: str = None, field_value: Any = None) -> bool:
    """
    Универсальная проверка совпадения enum значения с текстом или значением поля.
    
    Args:
        text: Текст для поиска
        enum_value: Значение enum
        field_key: Ключ поля для специальной обработки (не используется пока)
        field_value: Значение поля для специальных проверок
        
    Returns:
        True если найдено совпадение, False иначе
    """
    if not text and field_value is None:
        return False
    
    # Специальные проверки для is_halal
    if enum_value in SPECIAL_CHECKERS:
        checker_func = SPECIAL_CHECKERS[enum_value]
        return checker_func(field_value, enum_value)
    
    # Обычный текстовый поиск
    if not text:
        return False
        
    patterns = get_universal_patterns(enum_value)
    text_lower = text.lower()
    
    for pattern in patterns:
        # Проверяем regex паттерны
        if pattern.startswith(r"\d") or "\\" in pattern:
            try:
                if re.search(pattern, text):
                    return True
            except re.error:
                pass
        # Обычный поиск подстроки
        elif pattern.lower() in text_lower:
            return True
    
    return False

# ===================== ЭКСПОРТ =====================

# Обязательный экспорт для универсального загрузчика
universal_patterns = UNIVERSAL_ENUM_MAPPING