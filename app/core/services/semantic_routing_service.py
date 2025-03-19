# app/core/services/semantic_routing_service.py

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from semantic_router import RouteLayer, Route
from semantic_router.encoders import HuggingFaceEncoder, BaseEncoder
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
    """
    routes_path: str
    routing_table_path: str
    dense_encoder_name: Optional[str] = "jinaai/jina-embeddings-v3"
    dense_encoder_device: Optional[str] = "cuda"
    dense_score_threshold: Optional[float] = 0.7

class SemanticRoutingService:

    # Словарь стоп-слов для русского языка
    RUSSIAN_STOP_WORDS: Set[str] = {
        'а', 'без', 'более', 'бы', 'был', 'была', 'были', 'было', 'быть', 'в', 
        'вам', 'вас', 'весь', 'во', 'вот', 'все', 'всего', 'всех', 'вы', 'где', 
        'да', 'даже', 'для', 'до', 'его', 'ее', 'если', 'есть', 'ещё', 'же', 
        'за', 'здесь', 'и', 'из', 'или', 'им', 'их', 'к', 'как', 'ко', 'когда', 
        'кто', 'ли', 'либо', 'мне', 'может', 'мы', 'на', 'надо', 'наш', 'не', 
        'него', 'неё', 'нет', 'ни', 'них', 'но', 'ну', 'о', 'об', 'однако', 
        'он', 'она', 'они', 'оно', 'от', 'очень', 'по', 'под', 'при', 'с', 
        'со', 'так', 'также', 'такой', 'там', 'те', 'тем', 'то', 'того', 
        'тоже', 'той', 'только', 'том', 'ты', 'у', 'уже', 'хотя', 'чего', 
        'чей', 'чем', 'что', 'чтобы', 'чьё', 'чья', 'эта', 'эти', 'это', 
        'я', 'мне', 'мой', 'моя', 'моё', 'мои'
    }
    
    # Дополнительные слова, специфичные для предметной области напитков
    DOMAIN_STOP_WORDS: Set[str] = {
        'мне', 'надо', 'нужно', 'хочу', 'есть', 'ли', 'пожалуйста',
        'скажите', 'подскажите', 'помогите', 'посоветуйте'
    }

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

    def clean_text(self, text: str) -> str:
        """
        Очищает текст от стоп-слов и других элементов, не несущих семантической ценности.
        
        Args:
            text (str): Текст для очистки
            
        Returns:
            str: Очищенный текст
        """
        # Приводим к нижнему регистру
        text = text.lower()
        
        # Удаляем пунктуацию и лишние пробелы
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Удаляем стоп-слова
        words = text.split()
        cleaned_words = [word for word in words if word not in self.RUSSIAN_STOP_WORDS 
                         and word not in self.DOMAIN_STOP_WORDS 
                         and len(word) > 1]  # Игнорируем односимвольные слова
        
        # Собираем очищенный текст
        cleaned_text = ' '.join(cleaned_words)
        
        return cleaned_text

    def clean_utterances(self, utterances: List[str]) -> List[str]:
        """
        Очищает список примеров от стоп-слов.
        
        Args:
            utterances (List[str]): Список примеров
            
        Returns:
            List[str]: Список очищенных примеров
        """
        return [self.clean_text(utterance) for utterance in utterances]

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
            # Изменение: очищаем примеры перед созданием маршрута
            cleaned_utterances = self.clean_utterances(value["utterances"])
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
        # Изменение: очищаем входящий запрос перед обработкой
        cleaned_text = self.clean_text(text)
        
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