# core/engine.py

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Literal, Union, Optional

import tiktoken
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
from langsmith.wrappers import wrap_openai
from langsmith import traceable, Client

from core.prompts import PROMPT_SELECT_KEY, PROMPT_FINAL_ANSWER
from core.semantic_search import run as semantic_search
from data.subsectors import SUBSECTOR_ROUTES
from api.models import Metadata, Response, Query
from config import ROUTES_PATH, UTTERANCES_PATH
from utils.logger import logger
from utils.file_utils import (
    extract_key_descriptions,
    read_and_merge_json,
    clean_text,
    get_nested_data,
    clean_string
)

ls_client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"))
client = wrap_openai(
    OpenAI(base_url=os.path.join(os.getenv("OLLAMA_BASE_URL"), 'v1'),
            api_key=os.getenv("OLLAMA_API_KEY"))
    )

# Установите кодировщик для используемой модели
enc = tiktoken.encoding_for_model("gpt-4")


def count_tokens(s: str) -> int:
    """
    Подсчитывает количество токенов в строке.

    Args:
        s: Входная строка

    Returns:
        Количество токенов
    """
    return len(enc.encode(s))


@traceable(client=ls_client, project_name="llamaindex_test", run_type="retriever")
def select_relevant_keys(query: str, key_descriptions: Dict[str, str]) -> List[str]:
    """
    Использует LLM для выбора наиболее релевантных ключей на основе запроса пользователя.

    Args:
        query (str): Текст запроса пользователя.
        key_descriptions (Dict[str, str]): Словарь, где ключи — имена ключей,
            а значения — их описания.

    Returns:
        List[str]: Список выбранных ключей, релевантных запросу пользователя.
    """

    logger.info("Переданные ключи с описанием:\n" + "\n".join(
        f"\t{k}: {v[:50] + '...' if len(v) > 50 else v}"
        for k, v in key_descriptions.items()
    ))

    all_keys = list(key_descriptions.keys())  # Берем все ключи

    # Динамически формируем Pydantic модель на основе доступных ключей
    KeyType = Literal[tuple(all_keys)]

    class KeySelection(BaseModel):
        keys: List[KeyType] = Field(
            ...,
            max_items=1,
            description="Полное название / имя выбранного маршрута/ключа без его описания!"
        )
        reasoning_step_by_step: List[str] = Field(
            ...,
            min_items=1,
            max_items=3,
            description="Массив строк с пошаговым рассуждением. Каждый элемент должен быть полным предложением"
        )

    # Подготовка ключей с описаниями для промпта
    keys_with_descriptions = "\n".join(
        [f"{key}: {desc}" for key, desc in key_descriptions.items()])

    # Формируем сообщения для модели
    messages = [
        {"role": "system", "content": PROMPT_SELECT_KEY["system"]},
        {"role": "user", "content": PROMPT_SELECT_KEY["user"].format(
            query=query,
            keys=keys_with_descriptions
        )}
    ]

    try:
        # Запрос к модели с указанием схемы ответа
        logger.info("ЗАПУСКАЕМ МОДЕЛЬ ВЫБОРА КЛЮЧЕЙ : %s", os.getenv('KEY_SELECTION_MODEL'))
        completion = client.beta.chat.completions.parse(
            temperature=0,
            model=os.getenv('KEY_SELECTION_MODEL'),
            messages=messages,
            response_format=KeySelection,  # Передаем схему Pydantic
        )

        route_response = completion.choices[0].message
        logger.info("Ответ получен...")
        logger.info(
            f"**Содержимое обьекта ответа `message`**: \n {route_response}")

        # Если парсинг успешен
        if route_response.parsed:
            result = route_response.parsed.model_dump()
            logger.info(
                f"**Распарсенные аргументы JSON из ответа модели**: \n {result}")

            # Вывод результатов
            logger.info(f"Выбранные ключи: {result['keys']}")

            return result["keys"]
        elif route_response.refusal:
            raise ValueError(
                f"Модель отказалась делать выбор: {route_response.refusal}")

    except Exception as e:
        logger.info(f"Ошибка при выборе ключей с помощью LLM: {e}")
        return []


def process_json_and_answer(json_path: Union[Path, str], selected_files: List[str], user_query: str, nested_keys: Optional[List[str]] = ['product_list']):
    """
    Обрабатывает JSON файлы и генерирует ответ на вопрос пользователя.

    Args:
        json_path (Path): Путь к директории с JSON файлами для обработки
        selected_files (List[str]): Список имен файлов, которые нужно обработать
        user_query (str): Вопрос пользователя для генерации ответа
        nested_keys: Optional[List[str]]: Имя вложенного ключа или ключей в JSON, содержащего данные для ответа.
                                    По умолчанию 'product_list'

    Returns:
        str: Сгенерированный ответ с префиксом имен использованных файлов

    Raises:
        FileNotFoundError: Если указанный путь или файлы не существуют
        JSONDecodeError: При ошибке парсинга JSON файлов
        Exception: При других ошибках обработки запроса
    """

    # Преобразуем json_path в Path, если это строка
    if isinstance(json_path, str):
        json_path = Path(json_path)

    try:
        # Шаги 1-4: Подготовка данных
        json_contents = read_and_merge_json(json_path, selected_files)
        key_descriptions = extract_key_descriptions(json_contents)

        selected_keys = select_relevant_keys(user_query, key_descriptions)
        relevant_data = {
            key: get_nested_data(json_contents[key], nested_keys)
            for key in selected_keys
            if key in json_contents
        }

        # Шаг 5: Генерация ответа
        llm = ChatOllama(
            temperature=0.1,
            min_tokens=500,
            top_p=0.95,
            top_k=50,
            model=os.getenv('GENERATION_MODEL'),
            base_url=os.getenv('OLLAMA_BASE_URL'),
            format='json'
        )

        formatted_content = json.dumps(
            relevant_data, indent=2, ensure_ascii=False)
        cleaned_content = clean_text(formatted_content)

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", PROMPT_FINAL_ANSWER["system"]),
            ("user", PROMPT_FINAL_ANSWER["user"]),
        ])

        logger.info("ЗАПУСК МОДЕЛИ ДЛЯ ФИНАЛЬНОГО ОТВЕТА : %s", os.getenv('GENERATION_MODEL'))
        chain = prompt_template | llm

        # Замер времени и генерация ответа
        start_time = time.time()
        response = chain.invoke({
            "question": user_query,
            "content": cleaned_content,
        })
        elapsed_time = time.time() - start_time

        # Обработка ответа
        content = response.content if hasattr(
            response, 'content') else str(response)

        # Формирование финального ответа с префиксом
        # file_list = ", ".join(selected_files)
        # prefix = f"\n\nЕсли ответ не полный перейдите в соответствующие документы --> {file_list}\n\n"
        # final_response = f"{content} {prefix}"

        # Подсчет и вывод метрик
        response_tokens = float(count_tokens(content))
        tokens_per_second = response_tokens / elapsed_time if elapsed_time > 0 else 0.0

        logger.info(f"Время генерации ответа: {elapsed_time:.2f} секунд")
        logger.info(f"Всего сгенерировано токенов: {response_tokens}")
        logger.info(
            f"Скорость генерации токенов: {tokens_per_second:.2f} токенов/секунду")

        return clean_string(content), selected_keys

    except ConnectionError as e:
        logger.info(f"Ошибка при обработке запроса: {str(e)}")
        raise ConnectionError(e)
    
    except Exception as e:
        logger.info(f"Ошибка при обработке запроса: {str(e)}")
        raise Exception(e)


async def handle_query(query: Query) -> tuple[str, dict[str,any]]:
    logger.info(
        "Получен вопрос: %s, subsector_id: %s" ,query.question, query.subsector_id)
    
    # Проверяем существование отрасли
    if query.subsector_id not in SUBSECTOR_ROUTES:
        raise ValueError(f"Неверный ID отрасли: {query.subsector_id}")

    # Шаг 1 находим релевантный файл с помощью модуля "semantic_search"
    selected_files = semantic_search(
        ROUTES_PATH, UTTERANCES_PATH, query.question, query.subsector_id)
    logger.info(f"Пути к выбранным файлам: {selected_files}")

    # Шаг 2 Получаем полный путь к выбранной папке в которой оказался релевантный файл
    selected_folder = os.path.dirname(selected_files[0])
    folder_path_for_answer: Path = Path(ROUTES_PATH) / selected_folder

    # Шаг 3 находим релевантную информацию (ключи) и генерируем ответ в заключительном модуле "process_json_and_answer"
    answer, selected_keys = process_json_and_answer(
        folder_path_for_answer,
        [os.path.basename(f) for f in selected_files],
        query.question)
    
    metadata = Metadata(
        selected_keys=selected_keys,
        selected_files=selected_files,
        app_version=os.getenv('APP_VERSION'),
        key_selection_model=os.getenv('KEY_SELECTION_MODEL'),
        rerank_model=os.getenv('RERANK_MODEL'),
        generation_model=os.getenv('GENERATION_MODEL')
    )

    logger.info("Успешно сформирован ответ.")
    return Response(answer=answer, meta=metadata)
