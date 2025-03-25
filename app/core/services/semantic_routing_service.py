# app/core/services/semantic_routing_service.py

from dataclasses import dataclass
import json

from typing import Any, Dict, List, Optional
from semantic_router import RouteLayer, Route
from semantic_router.encoders import HuggingFaceEncoder
from utils.file_utils import get_valid_routing_table
from utils.logger import logger
from utils.stop_words import clean_text, clean_utterances

@dataclass
class SemanticRoutingConfig:
    """
    Configuration for Semantic Routing
    
    Args:
        dense_encoder_name (str): Huggingface `dense_encoder` name.
        dense_encoder_device (str): Device for Huggingface `dense_encoder`.
        dense_score_threshold (float): A threshold value used for filtering or processing the embeddings of the `dense_encoder`.
    """
    routes_path: str
    routing_table_path: str
    dense_encoder_name: Optional[str] = "jinaai/jina-embeddings-v3"
    dense_encoder_device: Optional[str] = "cuda"
    dense_score_threshold: Optional[float] = 0.7

class SemanticRoutingService:

    def __init__(
            self,
            config: SemanticRoutingConfig,
            dense_encoder: Optional[HuggingFaceEncoder] = None,
    ):
        self.dense_encoder = dense_encoder if dense_encoder else HuggingFaceEncoder(
            name = config.dense_encoder_name,
            score_threshold = config.dense_score_threshold,
            device = config.dense_encoder_device,
            model_kwargs={"trust_remote_code": True}
        )
        self.config: SemanticRoutingConfig = config
        self.routers: Dict[str, RouteLayer] = {}
        self.routing_table = get_valid_routing_table(dir_path=config.routes_path,
                            routing_table_path=config.routing_table_path)

    def _create_routes(self, routes: Dict[str, List[str]]) -> List[Route]:
        """
        Creates and returns a list of Route objects.

        Args:
            routes (Dict[List[str]]): routes to be converted to `Route` objects

        Returns:
            List[Route]: list of `Route` objects.
        """
        route_objs = []
        for route_key, value in routes.items():
            # Изменение: очищаем примеры перед созданием маршрута, используя функцию из utils
            cleaned_utterances = clean_utterances(value["utterances"])
            route_objs.append(
                Route(
                    name=route_key,
                    utterances=cleaned_utterances
                )
            )

        return route_objs

    def _create_router(self, route_objs: List[Route]) -> RouteLayer:
        """
        Creates and returns a `Router` object.

        Args:
            route_objs [List[Route]]: List of `Route` objects

        Returns:
            Router: `Router` objects.
        """
        dense_encoder = HuggingFaceEncoder(
            name = self.config.dense_encoder_name,
            score_threshold = self.config.dense_score_threshold,
            device = self.config.dense_encoder_device,
            model_kwargs={"trust_remote_code": True}
            )
        
        return RouteLayer(
            encoder=dense_encoder,
            routes=route_objs,
            top_k=len(route_objs)*2
        )
    
    def add_routers(self):
        """
        Adds `Router` objects for each subsector of the routing_table.

        Args:
            routing_table Dict[str, Dict[str, List[str]]]: routing_table to convert
        """
        for subsector, routes in self.routing_table.items():
            route_objs = self._create_routes(routes=routes)
            router = self._create_router(route_objs=route_objs)
            self.routers[subsector]=router
            logger.info(f"Router for {subsector} created.")


    def _sort_routes(self, routes: Dict[str, Any]):
        # Сортируем маршруты по убыванию оценок
        sorted_routes = sorted(routes.items(),
                           key=lambda item: item[1], reverse=True)
        
        logger.info(json.dumps(sorted_routes, indent=4, sort_keys=True))

        return dict(sorted_routes)


    def _aggregate(self, routes: List[Dict[str, Any]]):
        aggregated_routes = {}    
        for r in routes:
            route_name = r['route']
            score = r['score']
            
            # MAX-Aggregation
            if route_name in aggregated_routes:
                aggregated_routes[route_name] = max(aggregated_routes[route_name], score)
            else:
                aggregated_routes[route_name] = score

        return aggregated_routes

    def top_routes(self, subsector: str, text: str, top_n: int = 5) -> List[Dict[str, Any]]:
        # Изменение: очищаем входящий запрос перед обработкой, используя функцию из utils
        cleaned_text = clean_text(text)
        
        dl: RouteLayer = self.routers[subsector]
        
        # Используем метод _encode для получения вектора из очищенного текста
        xq = dl._encode(text=cleaned_text)
        
        # Используем метод _retrieve для получения результатов запроса
        routes_with_scores = dl._retrieve(xq=xq, top_k=dl.top_k)
        
        aggregated_routes = self._aggregate(routes_with_scores)
        sorted_routes = self._sort_routes(aggregated_routes)

        routes_with_description: Dict[str, str] = {}
        for route in list(sorted_routes.keys())[:top_n]:
            description = self.routing_table[subsector][route]["description"]
            routes_with_description[route] = description

        return routes_with_description