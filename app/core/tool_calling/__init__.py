"""
Tool Calling модуль для обработки запросов с использованием LLM инструментов.

Обновлен для новой универсальной архитектуры с UniversalIndustryHandler.
Все отрасли теперь используют единый обработчик с конфигурационными mappings.

Основные компоненты:
- ToolService: главный координатор и точка входа
- UniversalIndustryHandler: единый обработчик для всех отраслей
- IndustryMappingsLoader: динамическая загрузка mappings
- BaseToolHandler: базовый класс (наследуется UniversalIndustryHandler)

Поддерживаемые отрасли:
- HoReCa (subsector_id: "01") - гостинично-ресторанный комплекс
- Молочная отрасль (subsector_id: "04") - молочные продукты и ингредиенты
 - Напитки (subsector_id: "09") - напитки, рецептуры, ароматизаторы, красители

Использование:
    from app.core.tool_calling import ToolService
    
    tool_service = ToolService(llm_service=your_llm_client)
    
    # Для любой поддерживаемой отрасли
    result = tool_service.process_query(
        subsector_id="01",  # или "04" для молочной
        query="Найти низкокалорийные соусы Millgri в пластиковых бутылках",
        data=industry_data,
        selected_key="ready_sauces"
    )
    
    # Проверка поддержки отрасли
    if tool_service.is_supported("01"):
        # Обработка запроса...
        pass
"""

from .service import ToolService
from .universal_handler import UniversalIndustryHandler

__all__ = ["ToolService", "UniversalIndustryHandler"]
