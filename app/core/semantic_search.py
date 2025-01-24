# core/semantic_search.py

import os
from typing import Literal, List, Dict, Any

from pydantic import BaseModel, Field
from openai import OpenAI
from langsmith.wrappers import wrap_openai
from langsmith import traceable, Client
from semantic_router.hybrid_layer import HybridRouteLayer

from data.subsectors import SUBSECTOR_ROUTES
from core.prompts import PROMPT_RERANK_ROU
from utils.logger import logger
from utils.file_utils import (
    get_json_filenames,
    create_routes,
    get_route_description,
    get_top_routes_utils,
    setup_encoder_and_layer
)

# Оборачиваем OpenAI клиента для LangSmith
ls_client = Client(api_key = os.getenv("LANGCHAIN_API_KEY"))
client = wrap_openai(
    OpenAI(
        base_url=os.path.join(os.getenv("PROVIDER_BASE_URL"), 'v1'),
        api_key=os.getenv("PROVIDER_API_KEY")
        )
    )

def get_top_routes(dl: HybridRouteLayer,
                    expanded_query: str,
                    top_k: int,
                    total_routes: int) -> List[Dict[str, str]]:
    """Получает топ маршрутов для заданного запроса.

    Функция выполняет семантический поиск с использованием слоя маршрутизации `dl` 
    и расширенного запроса `expanded_query`.

    Args:
        dl (HybridRouteLayer): Инициализированный слой маршрутизации.
        expanded_query (str): Текст запроса пользователя
        top_k (int): Максимальное количество маршрутов для возврата.
        total_routes (int): Общее количество маршрутов в системе.

    Returns:
        list: Список словарей, каждый из которых содержит информацию о маршруте:
              - 'route': имя маршрута (строка).
              - 'description': описание маршрута (строка).
              Список отсортирован по релевантности запросу.
    """
    try:
        # Получаем все маршруты с оценками схожести, отсортированные по релевантности
        all_routes = get_top_routes_utils(dl, expanded_query, top_k=total_routes)
        logger.info(f"Оценки всех маршрутов для запроса: {expanded_query}")
        for route in all_routes:
            logger.info(f"Маршрут: {route['route']}, Оценка: {route['score']}")
        
        # Ограничиваем количество маршрутов до 5
        top_routes = all_routes[:top_k]
        
        # Добавляем описания к маршрутам
        routes_with_descriptions = []
        for route in top_routes:
            route_name = route['route']
            # Получаем описание маршрута
            description = get_route_description(route_name, selected_folder) 
            routes_with_descriptions.append({
                'route': route_name,
                'description': description
            })
        
        return routes_with_descriptions
    except Exception as e:
        logger.info(f"Ошибка при получении топ маршрутов: {e}")
        return []

@traceable(client=ls_client, project_name="llamaindex_test", run_type = "retriever")
def rerank_routes(query_text: str, top_routes: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Переранжирует маршруты на основе вопроса пользователя.
    Args:
        query_text: Текст запроса пользователя
        top_routes: Список словарей с маршрутами, где каждый содержит 'route' и 'description'
    Returns:
        Словарь с ключами:
            - selected_route: List[str] - список выбранных маршрутов
            - reasoning_step_by_step: List[str] - шаги рассуждения
            - reason: str - причина выбора
    """

    
    # Извлекаем имена маршрутов
    route_names = [route['route'] for route in top_routes]
    
    # Создаем Pydantic модель с Literal типом для строгого выбора маршрута
    RouteType = Literal[tuple(route_names)]
    
    class RouteSelection(BaseModel):
        selected_route: List[RouteType] = Field(
            ...,
            max_items=1,
            description="Полное название / имя выбранного маршрута без его описания!"
        )
        reasoning_step_by_step: List[str] = Field(
            ...,
            min_items=1,
            max_items=3,
            description="Массив строк с пошаговым рассуждением. Каждый элемент должен быть полным предложением."
        )
        reason: str = Field(
            ...,
            description="Краткая причина выбора этого маршрута"
        )

    # Подготавливаем описания маршрутов для передачи в промпт
    routes_str = [f"{r['route']}: описание: {r['description']}..." for r in top_routes]
    
    # Формируем запрос с оригинальными промптами
    messages = [
        {"role": "system", "content": PROMPT_RERANK_ROU["system"]},
        {"role": "user", "content": PROMPT_RERANK_ROU["user"].format(
            query=query_text, 
            routes="\n".join(routes_str)
        )}
    ]

    logger.info("Описания выбранных топ маршрутов:")
    for route in routes_str:
        logger.info(route[:80] + "...")

    try:
        logger.info("Запускаем модель РЕРАНКА : %s", os.getenv('RERANK_MODEL'))
        completion = client.beta.chat.completions.parse(
            temperature=0,
            model=os.getenv('RERANK_MODEL'),
            messages=messages,
            response_format=RouteSelection,
        )

        route_response = completion.choices[0].message
        logger.info("Ответ получен...")
        logger.info(f"**Содержимое обьекта ответа `message`**: \n {route_response}")
        if route_response.parsed:
            result = route_response.parsed.model_dump()
            logger.info(f"**Распарсенные аргументы JSON из ответа модели**: \n {result}")
            
            # Выводим результаты
            logger.info("Выбранные маршруты:")
            for route in result['selected_route']:
                logger.info(f"***{route}***")
            
            return result
        elif route_response.refusal:
            raise ValueError(f"Модель отказалась делать выбор: {route_response.refusal}")
            
    except Exception as e:
        raise ValueError(f"Ошибка при ранжировании маршрутов: {str(e)}")


def run(base_directory: str, utterances_json_path: str, query_text: str, subsector_id: str) -> List[str]:
    """
    Выполняет поиск и маршрутизацию запроса.
    
    Args:
        base_directory (str): Базовая директория для поиска
        utterances_json_path (str): Путь к JSON файлу с utterances
        query_text (str): Текст запроса пользователя
        
    Returns:
        List[str]: Список путей к найденным JSON файлам
    """
    global selected_folder
    
    selected_folder = SUBSECTOR_ROUTES[subsector_id]
    logger.info(f"Выбрана папка отрасли: {selected_folder}")
    
    # Путь к выбранной папке
    selected_directory = os.path.join(base_directory, selected_folder)
    
    # Проверяем существование папки
    if not os.path.exists(selected_directory):
        logger.error("Папка отрасли не существует: %s", selected_directory)
        raise ValueError(f"Папка для отрасли {selected_folder} не найдена")
    
    # Получение JSON файлов из выбранной папки
    json_filenames = get_json_filenames(selected_directory)
    
    # Создание маршрутов из файлов выбранной папки
    routes, total_routes = create_routes(json_filenames, utterances_json_path)
    
    # Создаём гибридный слой маршрутизации из роутеров (маршрутов)
    dl = setup_encoder_and_layer(routes)
    
    # получаем топ маршруты близкие к вопросу
    top_routes = get_top_routes(dl, query_text, top_k=5, total_routes=total_routes)
    
    # повторное ранжирование найденных топ маршрутов
    reranked_route = rerank_routes(query_text, top_routes)
    
    # возврат полного пути к выбранным файлам/маршруту
    if reranked_route:
        # Так как selected_route теперь список, берем первый элемент
        selected_routes = reranked_route['selected_route']
        return [os.path.join(selected_folder, route + '.json') for route in selected_routes]
    else:
        logger.info(f"Реранжирование не удалось, возвращаем первый маршрут: {top_routes[0]['route']}")
        return [os.path.join(selected_folder, top_routes[0]['selected_route'] + '.json')]
