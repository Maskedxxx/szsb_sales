"""
HoReCa Tool Calling модуль.

Обновлено для новой универсальной архитектуры - теперь использует UniversalIndustryHandler.
Содержит только mappings для данных HoReCa отрасли.

Компоненты:
- mappings/keys.py: структура полей продуктов HoReCa
- mappings/enums.py: возможные значения для фильтрации (в формате Milk с субключами)
- mappings/universal.py: паттерны для умной фильтрации
"""

# Не экспортируем старые хендлеры - они заменены на UniversalIndustryHandler
__all__ = []