# core/services/engine.py

import os
import json
import time
from typing import Any, List, Dict, Tuple

from openai import OpenAI
from langsmith.wrappers import wrap_openai
from langsmith import traceable, Client

from core.services.reranking_service import RerankingConfig, RerankingPromptTemplate, RerankingService
from core.services.expanded_query_router_service import ExpandedQueryRouterService
from core.services.key_selection_service import KeySelectionConfig, KeySelectionPromptTemplate, KeySelectionService
from core.services.final_generation_service import FinalGenerationConfig, FinalGenerationPromptTemplate, FinalGenerationService
from core.services.semantic_routing_service import SemanticRoutingConfig, SemanticRoutingService
from core.services.query_expansion_service import QueryExpansionService
from core.prompts import PROMPT_RERANK_ROU, PROMPT_SELECT_KEY, PROMPT_FINAL_ANSWER
from data.subsectors import SUBSECTOR_ROUTES
from api.models import Metadata, Response, Query
from config import ROUTES_PATH, ROUTING_TABLE_PATH
from utils.logger import logger
from utils.file_utils import (
    normalize_dict_descriptions,
    read_and_merge,
    clean_text,
    get_nested_data,
    remove_think_tags,
)

TOP_N_ROUTES = 5

ls_client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"))
client = wrap_openai(
    OpenAI(base_url=os.path.join(os.getenv("PROVIDER_BASE_URL"), 'v1'),
            api_key=os.getenv("PROVIDER_API_KEY"),
            timeout=60.0)
    )

routing_config = SemanticRoutingConfig(
    routes_path=ROUTES_PATH,
    routing_table_path=ROUTING_TABLE_PATH,
    dense_encoder_name = os.getenv("DENSE_ENCODER_MODEL"),
    dense_encoder_device = os.getenv("DENSE_ENCODER_DEVICE")
)

routing_service = SemanticRoutingService(
        config = routing_config
)
routing_service.add_routers()

@traceable(client=ls_client, project_name="llamaindex_test", run_type = "retriever")
def rerank_routes(query_text: str, top_routes: Dict[str, str]) -> List[str]:
    """
    Reranks routes based on the user query.
    Args:
        query_text: User query text
        top_routes: List of dictionaries with routes, where each contains 'route' and 'description'
    Returns:
        Dictionary with keys:
            - selected_route: List[str] - list of selected routes
            - reasoning_step_by_step: List[str] - reasoning steps
            - reason: str - selection reason
    """
    try:
        config = RerankingConfig(
            model_name=os.getenv('RERANK_MODEL'),
            max_tokens=2048
        )

        prompt_template = RerankingPromptTemplate(
            system=PROMPT_RERANK_ROU["system"],
            user=PROMPT_RERANK_ROU["user"]
        )

        routes_reranker = RerankingService(
            client=client,
            config=config,
            prompt_template=prompt_template
        )

        logger.info(f"Reranking routes...\n")
        start_time = time.time()
        reranked_routes = routes_reranker.rerank_routes(query=query_text, routes=top_routes)
        elapsed_time = time.time() - start_time

        # Подсчет и вывод метрик
        logger.info(f"RERANKING handling time: {elapsed_time:.2f} seconds\n")
       
        return reranked_routes

    except ConnectionError as e:
        logger.info(f"Сonnection error on reranking: {str(e)}")
        raise ConnectionError(e)
    
    except Exception as e:
        logger.info(f"Error on reranking: {str(e)}")
        raise Exception(e)

@traceable(client=ls_client, project_name="llamaindex_test", run_type="retriever")
def select_relevant_keys(query: str, key_descriptions: Dict[str, str]) -> List[str]:
    """
    Uses LLM to select the most relevant keys based on the user query.

    Args:
        query (str): User query text.
        key_descriptions (Dict[str, str]): Dictionary where keys are key names,
            and values are their descriptions.

    Returns:
        List[str]: List of selected keys relevant to the user query.
    """
    config = KeySelectionConfig(
        model_name=os.getenv('KEY_SELECTION_MODEL'),
        max_tokens=4096
    )
    
    prompt_template = KeySelectionPromptTemplate(
        system=PROMPT_SELECT_KEY["system"],
        user=PROMPT_SELECT_KEY["user"]
    )
    
    key_selector = KeySelectionService(client, config, prompt_template)

    logger.info(f"Selecting relevant keys...\n")
    start_time = time.time()
    selected_keys = key_selector.select_relevant_keys(query, key_descriptions)
    elapsed_time = time.time() - start_time

    logger.info(f"KEYSELECTION handling time: {elapsed_time:.2f} seconds\n")

    return selected_keys

@traceable(client=ls_client, project_name="llamaindex_test", run_type = "retriever")
def generate_final_answer(user_query: str, context : str):
    """
    Generates an answer to the user's question.

    Args:
        user_query (str): user's question in the query
        context (str): Context for answer generation

    Returns:
        str: generated answer
    """

    try:
        config = FinalGenerationConfig(
            model_name=os.getenv('GENERATION_MODEL'),
            max_tokens=4096
        )

        prompt_template = FinalGenerationPromptTemplate(
            system=PROMPT_FINAL_ANSWER["system"],
            user=PROMPT_FINAL_ANSWER["user"]
        )

        final_answer_generator = FinalGenerationService(
            client=client,
            config=config,
            prompt_template=prompt_template
        )

        start_time = time.time()
        response = final_answer_generator.generate_final_answer(user_query, context)
        elapsed_time = time.time() - start_time

        # Обработка ответа
        answer = response.content if hasattr(
            response, 'content') else str(response)
        
        logger.info(f"FINAL GENERATION handling time: {elapsed_time:.2f} seconds\n")

        return answer

    except ConnectionError as e:
        logger.info(f"Error while generating answer: {str(e)}")
        raise ConnectionError(e)
    
    except Exception as e:
        logger.info(f"Error while generating answer: {str(e)}")
        raise Exception(e)

def process_drinks_subsector(question: str, selected_subsector: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Processes requests for the "drinks" subsector using query expansion.
    
    Args:
        question (str): User question
        selected_subsector (str): Selected subsector
        
    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: Tuple of relevant_routes and reranked_routes
    """
    # Вызов метода расширения запроса
    query_expansion_service = QueryExpansionService()
    expanded_queries = query_expansion_service.expand_query(question)
    logger.info("Query expanded using QueryExpansionService.")
    
    # Используем уже сконфигурированный routing_service (глобальная переменная)
    expanded_query_router_service = ExpandedQueryRouterService(routing_service)
    
    # Получаем объединённый словарь маршрутов по расширенным запросам
    merged_routes = expanded_query_router_service.route_expanded_queries(selected_subsector, expanded_queries)
    
    # Выбираем топ-1 маршрут из объединённых результатов
    if merged_routes:
        top_route = next(iter(merged_routes))
        relevant_routes = {top_route: merged_routes[top_route]}
        logger.info(f"Selected top route: {top_route}")
    else:
        logger.warning("No routes found via expanded query routing, falling back to dummy routes.")
        relevant_routes = {q: 1 for q in expanded_queries}
        
    # Для drinks пропускаем повторное ранжирование
    reranked_routes = relevant_routes
    
    return relevant_routes, reranked_routes


async def handle_query(query: Query) -> Response:
    logger.info(
        "REQUEST USER QUERY: %s, SUBSECTOR_ID: %s", query.question, query.subsector_id)
    
    # Проверяем существование отрасли
    if query.subsector_id not in SUBSECTOR_ROUTES:
        raise ValueError(f"INVALID SUBSECTOR_ID: {query.subsector_id}")

    selected_subsector = SUBSECTOR_ROUTES[query.subsector_id]
    logger.info(f"Subsector selected: {selected_subsector}")

    if selected_subsector == "drinks":
        # Обработка для подсектора "drinks" вынесена в отдельную функцию
        relevant_routes, reranked_routes = process_drinks_subsector(query.question, selected_subsector)
            
    else:
        # Исходный блок для семантического поиска релевантных файлов
        start_time = time.time()
        relevant_routes = routing_service.top_routes(
            subsector=selected_subsector,
            text=query.question,
            top_n=TOP_N_ROUTES
        )
        elapsed_time = time.time() - start_time
        logger.info(f"SEMANTIC SEARCH handling time: {elapsed_time} seconds\n")
        
        # Повторное ранжирование найденных маршрутов
        reranked_routes = rerank_routes(query.question, relevant_routes)

    # Путь к выбранной папке
    subsector_dir = os.path.join(ROUTES_PATH, selected_subsector)

    # Проверяем существование папки
    if not os.path.exists(subsector_dir):
        logger.error("Subsector dir not found: %s", subsector_dir)
        raise ValueError(f"Subesctor dir for {selected_subsector} not found")
    
    # возврат полного пути к выбранным файлам/маршруту
    if reranked_routes:
        reranked_routes_paths = [os.path.join(subsector_dir, r + '.json') for r in reranked_routes]
    else:
        logger.info(f"Reranking failed; Falling back to semantic top_routes:\n {relevant_routes}")
        reranked_routes_paths = [os.path.join(subsector_dir, r + '.json') for r in relevant_routes.keys()][:TOP_N_ROUTES]

    # Шаги 1-4: Подготовка данных
    merged_files : Dict[str, Any] = read_and_merge(reranked_routes_paths)

    key_descriptions = normalize_dict_descriptions(merged_files)

    relevant_keys = select_relevant_keys(query.question, key_descriptions)

    if not relevant_keys:
        answer = 'К сожалению не удалось сформировать ответ. Попробуйте переформулировать и уточнить вопрос.'
        logger.info('No relevant_keys found, cannot generate final answer!')
    else:
        relevant_data = {
            key: get_nested_data(merged_files[key], ['product_list'])
            for key in relevant_keys
            if key in merged_files
        }

        formatted_content = json.dumps(
            relevant_data, indent=2, ensure_ascii=False)
        cleaned_content = clean_text(formatted_content)

        # Шаг 3 находим релевантную информацию (ключи) и генерируем ответ в заключительном модуле "process_json_and_answer"
        answer = generate_final_answer(
            user_query=query.question,
            context=cleaned_content
        )
        answer = remove_think_tags(answer)
        logger.info("Answer formed successfully.")
        
    metadata = Metadata(
        selected_keys=relevant_keys,
        selected_files=reranked_routes_paths,
        app_version=os.getenv('APP_VERSION'),
        key_selection_model=os.getenv('KEY_SELECTION_MODEL'),
        rerank_model=os.getenv('RERANK_MODEL'),
        generation_model=os.getenv('GENERATION_MODEL')
    )

    return Response(answer=answer, meta=metadata)