"""
Маппинги данных для HoReCa Tool Calling.

Содержит все необходимые маппинги для преобразования между
LLM enum'ами и реальными данными продуктов HoReCa.
"""

from .keys import HORECA_KEYS_MAPPING
from .enums import HORECA_ENUM_MAPPING
from .universal import has_universal_enum_match, get_universal_patterns

__all__ = [
    "HORECA_KEYS_MAPPING",
    "HORECA_ENUM_MAPPING", 
    "has_universal_enum_match",
    "get_universal_patterns"
]