"""
Универсальные паттерны для фильтрации продуктов отрасли selo.
Поддерживает различные варианты написания названий продуктов.
"""
from typing import List, Dict

# Специфичные маппинги для отрасли selo
SELO_SPECIFIC_MAPPING: Dict[str, List[str]] = {
    "БИОКОНСЕРВАНТ AIBI® 4X4": ["AIBI® 4X4", "AIBI 4X4", "4X4", "БИОКОНСЕРВАНТ AIBI® 4X4"],
    "БИОКОНСЕРВАНТ AIBI® 15.10F": ["AIBI® 15.10F", "AIBI 15.10F", "15.10F", "БИОКОНСЕРВАНТ AIBI® 15.10F"],
    "Биоконсервант Ультра": ["Ультра", "ультра", "УЛЬТРА", "Биоконсервант Ультра"],
    "АІВІ® СЕРИЯ LCLBB 24.02": ["LCLBB 24.02", "АІВІ", "AIBI", "LCLBB", "24.02", "АІВІ® СЕРИЯ LCLBB 24.02"]
}

def get_universal_patterns(enum_value: str) -> List[str]:
    """Возвращает паттерны поиска для enum значения."""
    return SELO_SPECIFIC_MAPPING.get(enum_value, [enum_value])

def has_universal_enum_match(text: str, enum_value: str, field_key: str = None) -> bool:
    """Универсальная проверка совпадения enum значения с текстом."""
    patterns = get_universal_patterns(enum_value)
    text_lower = text.lower()
    
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return True
    return False