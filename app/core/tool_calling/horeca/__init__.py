"""
HoReCa Tool Calling модуль.

Реализует Tool Calling логику для отрасли HoReCa (subsector_id: "01").
Включает генерацию динамических схем, фильтрацию продуктов и маппинги данных.

Компоненты:
- HoReCaHandler: основной хендлер для обработки запросов
- Mappings: маппинги ключей, enum'ов и универсальные паттерны
- DataFilter: функции фильтрации продуктов
"""

from .service import HoReCaHandler

__all__ = ["HoReCaHandler"]