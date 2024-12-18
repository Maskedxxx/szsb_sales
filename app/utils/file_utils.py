# utils/file_utils.py

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Union, Tuple, Set
from semantic_router.route import Route
from semantic_router.encoders import TfidfEncoder, HuggingFaceEncoder
from semantic_router.hybrid_layer import HybridRouteLayer
from config import ROUTES_PATH
from utils.logger import logger


def get_json_filenames(directory: str) -> List[str]:
    """
    Возвращает список имен файлов с расширением ".json" в указанной директории.

    Args:
        directory (str): Путь к директории для поиска файлов.

    Returns:
        List[str]: Список имен файлов с расширением ".json".
    """
    path = Path(directory)
    json_files = [file.name for file in path.glob('*.json')]
    logger.info("Найдены JSON файлы в выбранной папке: %s ...", json_files[:5])
    logger.info("Количевство файлов JSON: %d штук", len(json_files))

    return json_files


def create_routes(file_names: List[str], json_path: str) -> Tuple[List[Route], int]:
    """
    Создает список объектов Route и возвращает их вместе с общим количеством.

    Args:
        file_names (List[str]): список имён файлов.
        json_path (str): путь к JSON файлу с utterances.

    Returns:
        Tuple[List[Route], int]: список маршрутов и их общее количество.
    """

    # Начало создания маршрутов/роутеров из файлов
    with open(json_path, 'r', encoding='utf-8') as file:  # Читаем данные из JSON файла
        utterances_data = json.load(file)

    routes = []  # Создаем список объектов Route
    for file_name in file_names:
        route_name = Path(file_name).stem  # Получаем имя файла без расширения
        # Проверяем существование роутера
        if route_name not in utterances_data or 'route' not in utterances_data[route_name]:
            logger.warning(
                "Предупреждение: для файла '%s' не найден соответствующий роутер", file_name)
            continue

        route_info = utterances_data[route_name]['route']
        # Извлекаем имя роутера или используем имя файла
        route_name = route_info.get('name', route_name)
        # Извлекаем utterances роутера
        utterances = route_info.get('utterances', [])
        routes.append(Route(name=route_name, utterances=utterances))

    total_routes = len(routes)
    # Проверяем, что для всех файлов найдены роутеры
    if total_routes == len(file_names):
        logger.info(
            f"Для всех файлов JSON найдены роутеры с utterances. Всего создано {total_routes} маршрутов.")
    else:
        logger.info(
            f"Создано {total_routes} маршрутов из {len(file_names)} файлов JSON.")

    return routes, total_routes


def setup_encoder_and_layer(routes: List[Route]) -> HybridRouteLayer:
    """
    Настраивает энкодеры и слой маршрутизации.

    Эта функция инициализирует два типа энкодеров:
      - `HuggingFaceEncoder`: плотный энкодер на основе модели Hugging Face.
      - `TfidfEncoder`: разреженный энкодер, использующий TF-IDF.

    Затем создается гибридный слой маршрутизации `HybridRouteLayer`, который комбинирует 
    результаты обоих энкодеров для повышения точности поиска.

    Args:
        routes (List[Route]): Список объектов маршрутов для слоя маршрутизации.

    Returns:
        HybridRouteLayer: Инициализированный слой маршрутизации, готовый 
                          для выполнения гибридного поиска.
    """

    logger.info("Начало создания HybridRouteLayer из роутеров")
    dense_encoder = HuggingFaceEncoder(score_threshold=0.7)
    sparse_encoder = TfidfEncoder(score_threshold=0.75)

    alpha = 0.59  # Вес плотного энкодера в гибридном слое 0.59 default
    top_k = 5
    aggregation = "max"

    dl = HybridRouteLayer(
        encoder=dense_encoder,
        sparse_encoder=sparse_encoder,
        routes=routes,
        alpha=alpha,
        top_k=top_k,
        aggregation=aggregation
    )
    logger.info(
        f"HybridRouteLayer готов. Параметры: alpha={alpha}, aggregation={aggregation}")
    return dl


def get_top_routes_utils(dl: HybridRouteLayer, text_query: str, top_k: int) -> List[Dict[str, Any]]:
    """
    Возвращает список топ-N маршрутов вместе с их оценками для заданного текста,
    группируя результаты по уникальным маршрутам.

    :param dl: Экземпляр HybridRouteLayer
    :param text_query: Текстовый запрос
    :param top_k: Количество возвращаемых маршрутов
    :return: Список словарей с именами маршрутов и их агрегированными оценками.
             Каждый словарь имеет структуру {"route": str, "score": float}.
    """
    # Здесь мы вызываем приватный метод _query
    query_results = dl._query(text_query, top_k * 2)
    route_scores = {}

    for result in query_results:
        route_name = result['route']
        score = result['score']
        # Агрегируем по максимуму
        if route_name in route_scores:
            route_scores[route_name] = max(route_scores[route_name], score)
        else:
            route_scores[route_name] = score

    # Сортируем маршруты по убыванию оценок
    sorted_routes = sorted(route_scores.items(),
                           key=lambda item: item[1], reverse=True)

    # Возвращаем только топ-N маршрутов
    return [{"route": name, "score": score} for name, score in sorted_routes]


def get_route_description(route_name: str, selected_folder: str) -> str:
    """
    Получает описание маршрута из JSON файла.

    Args:
        route_name: имя маршрута
        selected_folder: выбранная папка

    Returns:
        str: описание маршрута
    """
    file_path = Path(ROUTES_PATH) / selected_folder / f"{route_name}.json"
    data = json.loads(file_path.read_text(encoding='utf-8'))
    description = data.get('description')
    if description:
        return description

    raise ValueError(f"Отсутствует описание для маршрута {route_name}")


def read_and_merge_json(json_path: Path, selected_files: List[str]) -> Dict[str, Any]:
    """
    Читает JSON файлы из указанной папки и объединяет их содержимое в один словарь.

    Args:
        json_path (Path): Путь к директории с JSON файлами
        selected_files (List[str]): Список имен файлов для чтения

    Returns:
        Dict[str, Any]: Объединенный словарь с содержимым всех JSON файлов

    Raises:
        FileNotFoundError: Если указанный путь или файлы не существуют
        JSONDecodeError: При ошибке парсинга JSON файлов
    """
    json_contents = {}

    logger.info("ЧИтаем содержимое JSON файлов...")
    for file_name in selected_files:
        file_path = json_path / file_name
        try:
            content = json.loads(file_path.read_text(encoding='utf-8'))
            json_contents.update(content)
        except FileNotFoundError:
            logger.info(f"Файл не найден: {file_path}")
        except json.JSONDecodeError:
            logger.info(f"Ошибка при парсинге JSON файла: {file_name}")
        except Exception as e:
            logger.info(f"Ошибка при чтении файла {file_name}: {str(e)}")

    return json_contents


def extract_key_descriptions(json_content: Dict[str, Any], description_key: str = 'description', exclude_keys: Set[str] = {'description', 'keywords'}
                             ) -> Dict[str, str]:
    """
    Извлекает описания для каждого ключа из JSON-содержимого.

    Функция обрабатывает три случая:
    1. Значение — словарь с ключом описания
    2. Значение — список, где первый элемент содержит описание
    3. Значение — строка

    Args:
        json_content: JSON-данные в виде словаря
        description_key: Имя ключа с описанием, это подключ всех вернеуровневых ключей кроме ключей исключения `exclude_keys` (по умолчанию 'description')
        exclude_keys: Множество ключей для исключения, эти исключения являются ключами верхнего уровня (по умолчанию {'description', 'keywords'})

    Returns:
        Словарь, где ключи — из исходного JSON (кроме исключенных),
        а значения — соответствующие описания

    Example:
        >>> data = {
        ...     "item1": {"description": "desc1"},
        ...     "item2": ["Description: desc2"],
        ...     "item3": "simple string"
        ... }
        >>> extract_key_descriptions(data)
        {'item1': 'desc1', 'item2': 'desc2', 'item3': 'simple string'}
    """
    logger.info(
        "Извлекаем содержимое description (описания) всех выбранных ключей...")
    key_descriptions: Dict[str, str] = {}
    desc_marker = f"{description_key}:"

    for key, value in json_content.items():
        if key in exclude_keys:
            continue

        description = ""

        # Случай 1: Словарь с ключом описания
        if isinstance(value, dict):
            description = value.get(description_key, "")

        # Случай 2: Список с описанием в первом элементе
        elif isinstance(value, list) and value:
            first_item = value[0]
            if isinstance(first_item, str):
                # Проверяем наличие маркера описания
                if desc_marker.lower() in first_item.lower():
                    description = first_item.split(desc_marker, 1)[1].strip()
                else:
                    description = first_item.strip()

        # Случай 3: Строковое значение
        elif isinstance(value, str):
            description = value.split('\n')[0].strip()

        if description:  # Добавляем только непустые описания
            key_descriptions[key] = description

    return key_descriptions


def clean_text(json_text: str) -> str:
    """
    Очищает текст из JSON строки от специальных символов и форматирует его.

    Функция выполняет:
    1. Парсинг JSON строки
    2. Извлечение всех строк из словаря и списков
    3. Очистку от специальных символов
    4. Форматирование пробелов

    Args:
        json_text: JSON строка для обработки

    Returns:
        Очищенный и отформатированный текст

    Example:
        >>> text = '{"key1": ["item1", "item2"], "key2": "value"}'
        >>> clean_text(text)
        'item1\nitem2\nvalue'
    """
    # Шаг 1: Парсинг JSON
    try:
        data: Dict[str, Union[List[str], str]] = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return ""

    # Шаг 2: Извлечение строк
    content_list: List[str] = []
    for value in data.values():
        if isinstance(value, list):
            content_list.extend(str(item) for item in value)
        else:
            content_list.append(str(value))

    # Шаг 3: Очистка строк
    cleaned_items: List[str] = [
        # Удаляем спецсимволы и лишние пробелы
        re.sub(r'\s+', ' ',
               re.sub(r'[{}"\\]', '', item)
               ).strip()
        for item in content_list
        if item.strip()  # Пропускаем пустые строки
    ]

    # Объединение и возврат результата
    return '\n'.join(cleaned_items)


def get_nested_data(data: Dict[str, Any], keys: List[str]) -> Any:
    """
    Рекурсивно извлекает данные из словаря по списку ключей.

    Args:
        data (Dict[str, Any]): Словарь, из которого нужно извлечь данные.
        keys (List[str]): Список ключей для доступа в словаре к вложенным данным.

    Returns:
        Any: Значение, расположенное по указанному пути ключей.
    """
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            # Если ключ не найден или текущие данные не являются словарем, возвращаем текущие данные
            return data
    return data
