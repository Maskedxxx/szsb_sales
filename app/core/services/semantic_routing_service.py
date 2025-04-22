from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from semantic_router import HybridRouter, Route
from semantic_router.encoders import TfidfEncoder, HuggingFaceEncoder
from utils.file_utils import get_valid_routing_table
from utils.logger import logger

@dataclass
class SemanticRoutingConfig:
    """
    Configuration for Semantic Routing
    
    Args:
        dense_encoder_name (str): Huggingface `dense_encoder` name.
        dense_encoder_device (str): Device for Huggingface `dense_encoder`.
        dense_score_threshold (float): A threshold value used for filtering or processing the embeddings of the `dense_encoder`.
        sparse_score_threshold (float): A threshold value used for filtering or processing the embeddings of the `sparse_encoder`.
        alpha (float): `dense_encoder` to `sparse_encoder` weight ratio.
        aggregation (str): aggregation method.
    """
    routes_path: str
    routing_table_path: str
    dense_encoder_name: Optional[str] = "TatonkaHF/bge-m3_en_ru"
    dense_encoder_device: Optional[str] = "cpu"
    dense_score_threshold: Optional[float] = 0.7
    sparse_score_threshold: Optional[float] = 0.75
    alpha : float = 0.59
    aggregation : str = "max"

class SemanticRoutingService:

    def __init__(
            self,
            config: SemanticRoutingConfig,
            dense_encoder: Optional[HuggingFaceEncoder] = None,
            sparse_encoder: Optional[TfidfEncoder] = None,
    ):
        self.dense_encoder = dense_encoder if dense_encoder else HuggingFaceEncoder(
            name = config.dense_encoder_name,
            score_threshold = config.dense_score_threshold,
            device = config.dense_encoder_device
        )
        self.sparse_encoder = sparse_encoder if sparse_encoder else TfidfEncoder()
        self.config: SemanticRoutingConfig = config
        self.routers: HybridRouter = {}
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
            route_objs.append(
                Route(
                    name=route_key,
                    utterances=value["utterances"]
                )
            )

        return route_objs

    def _create_router(self, route_objs: List[Route]) -> HybridRouter:
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
            device = self.config.dense_encoder_device
        )
        
        sparse_encoder = TfidfEncoder()

        return HybridRouter(
            encoder=self.dense_encoder,
            sparse_encoder=sparse_encoder,
            routes=route_objs,
            alpha=self.config.alpha,
            top_k=len(route_objs)*2,
            aggregation=self.config.aggregation
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
            router.add(route_objs)
            self.routers[subsector]=router
            logger.info(f"Router for {subsector} created.")
        logger.info(f"Всего роутеров создано: {len(self.routers)}")
        logger.info(f"Список категорий с роутерами: {list(self.routers.keys())}")


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
        dl: HybridRouter = self.routers[subsector]
        route_choices = dl(text=text, limit=top_n)

        result = []
        for route in route_choices:
            if route.name is None:
                continue
            result.append({
                "route": route.name,
                "score": route.similarity_score or 0.0,
                "description": self.routing_table[subsector][route.name]["description"]
            })

        return result
