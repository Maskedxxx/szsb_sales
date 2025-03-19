# app/core/services/expanded_query_router_service.py

"""
Сервис для маршрутизации расширенных запросов.
"""

from typing import Dict, List, Optional
from utils.logger import logger

from core.services.semantic_routing_service import SemanticRoutingService


class ExpandedQueryRouterService:
    """
    Сервис для маршрутизации расширенных запросов.
    Принимает список расширенных запросов, определяет их оценки к маршрутам
    и выбирает маршрут с наивысшей оценкой.
    """
    
    def __init__(
        self,
        semantic_routing_service: SemanticRoutingService
    ):
        """
        Инициализация сервиса маршрутизации расширенных запросов.
        
        Args:
            semantic_routing_service: Сервис семантической маршрутизации
        """
        self.semantic_routing_service = semantic_routing_service
        logger.info("ExpandedQueryRouterService инициализирован")
    
    def route_expanded_queries(self, subsector: str, expanded_queries: List[str], top_n: int = 5) -> Dict[str, str]:
        """
        Маршрутизирует расширенные запросы и выбирает лучший маршрут.
        
        Args:
            subsector: Подсектор для маршрутизации
            expanded_queries: Список расширенных запросов
            top_n: Количество возвращаемых маршрутов
            
        Returns:
            Dict[str, str]: Словарь выбранных маршрутов с их описаниями
        """
        logger.info(f"Маршрутизация {len(expanded_queries)} расширенных запросов")
        
        # Словарь для подсчета частоты маршрутов на первой позиции
        top_routes_count = {}
        
        # Для каждого расширенного запроса получаем топ маршруты
        for i, query in enumerate(expanded_queries):
            logger.info(f"Обработка запроса {i+1}: {query}")
            
            # Получаем топ маршруты для текущего запроса
            routes = self.semantic_routing_service.top_routes(
                subsector=subsector,
                text=query,
                top_n=top_n
            )
            
            if routes:
                # Получаем первый маршрут (он имеет наивысшую оценку)
                top_route = next(iter(routes))
                
                # Увеличиваем счетчик для этого маршрута
                if top_route not in top_routes_count:
                    top_routes_count[top_route] = {
                        'count': 0,
                        'description': routes[top_route]
                    }
                
                top_routes_count[top_route]['count'] += 1
                logger.info(f"Топ маршрут: {top_route}, всего упоминаний: {top_routes_count[top_route]['count']}")
            else:
                logger.warning(f"Не найдено маршрутов для запроса: {query}")
        
        # Сортируем маршруты по количеству появлений на первой позиции
        sorted_routes = dict(sorted(
            top_routes_count.items(),
            key=lambda item: item[1]['count'],
            reverse=True
        ))
        
        # Формируем результат
        result = {}
        for route, info in sorted_routes.items():
            result[route] = info['description']
            logger.info(f"Маршрут: {route}, Количество первых мест: {info['count']}")
        
        return result