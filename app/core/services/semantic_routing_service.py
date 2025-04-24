from dataclasses import dataclass
import json
import numpy as np
import math
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
    alpha : float = 0.7
    aggregation : str = "mean"

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
        
    def aggregate_scores(self, scores, alpha=0.5):
        """
        Агрегирует множественные оценки одного маршрута.
        
        Args:
            scores (List[float]): Список оценок для одного маршрута
            alpha (float): Коэффициент баланса между максимумом (1.0) и средним (0.0)
            
        Returns:
            float: Агрегированная оценка
        """
        if not scores:
            return 0.0
        
        max_score = max(scores)
        avg_score = sum(scores) / len(scores)
        
        # Учитываем и количество совпадений с логарифмическим масштабированием
        count_boost = 1 + (math.log(len(scores) + 1, 2) / 10)
        
        # Смешивание max и avg с учетом коэффициента alpha
        mixed_score = alpha * max_score + (1 - alpha) * avg_score
        
        # Применяем небольшой буст за множественные совпадения
        final_score = mixed_score * count_boost
        
        return round(final_score, 4)


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
      Создает и возвращает объект Router.

      Args:
          route_objs [List[Route]]: Список объектов Route

      Returns:
          Router: Объекты Router.
      """
      
      return HybridRouter(
          encoder=self.dense_encoder,
          sparse_encoder=self.sparse_encoder,  # Используем существующий энкодер
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

    def top_routes(self, subsector: str, text: str, top_n: int = 5, use_aggregation: bool = True, alpha: float = 0.8) -> List[Dict[str, Any]]:
      """
      Находит наиболее релевантные маршруты для заданного текста.
      
      Args:
          subsector (str): Название подсектора для выбора роутера
          text (str): Запрос для поиска релевантных маршрутов
          top_n (int): Количество маршрутов для возврата
          use_aggregation (bool): Использовать ли агрегацию множественных совпадений
          alpha (float): Коэффициент баланса для функции агрегации
          
      Returns:
          List[Dict[str, Any]]: Список релевантных маршрутов с оценками
      """
      dl, route_scores = self.routers[subsector], {}
      original_alpha = dl.alpha
      try:
          # Получаем эмбеддинги и запрашиваем индекс
          dense_vec, sparse_vec = np.array(dl.encoder([text])), dl.sparse_encoder([text])
          vector, sparse_vector = dl._convex_scaling(dense=dense_vec, sparse=sparse_vec)
          scores, routes = dl.index.query(vector=vector[0], top_k=top_n*5, sparse_vector=sparse_vector[0])
          
          # Собираем все оценки для каждого маршрута
          for i, route in enumerate(routes):
              if route is None: continue
              score = float(scores[i].item())
              
              # Вместо дедупликации собираем все оценки для каждого маршрута
              if route not in route_scores:
                  route_scores[route] = []
              route_scores[route].append(score)
          
          # Агрегируем оценки для каждого маршрута
          aggregated_routes = {}
          for route, scores_list in route_scores.items():
              if use_aggregation:
                  # Используем новую функцию агрегации
                  agg_score = self.aggregate_scores(scores_list, alpha)
              else:
                  # Традиционный подход: просто максимальная оценка
                  agg_score = max(scores_list)
                  
              aggregated_routes[route] = {
                  "name": route,
                  "scores": {
                      "hybrid": agg_score,
                      "max_score": max(scores_list),
                      "avg_score": sum(scores_list) / len(scores_list),
                      "match_count": len(scores_list)
                  }
              }
          
          # Сортировка и отбор топ-N
          top_routes_list = sorted(aggregated_routes.values(), 
                                  key=lambda x: x["scores"]["hybrid"], 
                                  reverse=True)[:top_n]
            
          # Формируем JSON для логирования с сохранением кодировки
          results_json = {"query": text, "subsector": subsector, "alpha": original_alpha, "routes": top_routes_list}
          logger.info(f"Топ-{top_n} маршрутов:\n{json.dumps(results_json, indent=2, ensure_ascii=False)}")
            
          # Формируем результат для API (с полными описаниями)
          return  [{"route": r["name"], 
                    "score": r["scores"]["hybrid"], 
                    "description": self.routing_table[subsector][r["name"]]["description"],
                    "match_count": r["scores"]["match_count"]} 
                    for r in top_routes_list]
      finally:
          pass
