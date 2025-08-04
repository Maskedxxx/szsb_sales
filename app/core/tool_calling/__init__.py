"""
Tool Calling модуль для обработки запросов с использованием LLM инструментов.

Этот модуль предоставляет расширяемую архитектуру для интеграции Tool Calling 
в различные отрасли (подсекторы) системы.

Основные компоненты:
- ToolService: главный координатор и точка входа
- BaseToolHandler: базовый класс для хендлеров отраслей
- Registry: реестр хендлеров по subsector_id

Поддерживаемые отрасли:
- HoReCa (subsector_id: "01") - гостинично-ресторанный комплекс
- Молочная отрасль (subsector_id: "04") - молочные продукты и ингредиенты

Использование:
    from app.core.tool_calling import ToolService
    
    tool_service = ToolService()
    
    # Для HoReCa
    result = tool_service.process_query(
        subsector_id="01",
        query="Найти соус Барбекю",
        data=horeca_data
    )
    
    # Для молочной отрасли
    result = tool_service.process_query(
        subsector_id="04", 
        query="Покажи концентраты молочного белка с высоким содержанием белка",
        data=milk_data
    )
"""

from .service import ToolService

__all__ = ["ToolService"]