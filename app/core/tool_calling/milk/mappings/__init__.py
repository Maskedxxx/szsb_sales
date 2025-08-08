"""
Маппинги для молочной отрасли.

Экспортирует все необходимые маппинги и функции для работы с данными молочной отрасли.
"""

from .keys import MILK_KEYS_MAPPING
from .enums import MILK_ENUM_MAPPING
from .universal import has_milk_enum_match, get_milk_patterns

__all__ = [
    "MILK_KEYS_MAPPING",
    "MILK_ENUM_MAPPING", 
    "has_milk_enum_match",
    "get_milk_patterns"
]