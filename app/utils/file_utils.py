# utils/file_utils.py

import glob
import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Union, Tuple, Set
from .logger import logger

def get_valid_routing_table(dir_path: str, routing_table_path: str) -> Dict[str, Dict[str,Dict[str, Any]]]:
    with open(routing_table_path, 'r', encoding='utf-8') as file:  # Читаем данные из JSON файла
        routing_table = json.load(file)
    
    subsector_dirs = [os.path.basename(f.path) for f in os.scandir(dir_path) if f.is_dir()]
    existing_subsectors = {}
    for subsector, routes in routing_table.items():
        if subsector not in subsector_dirs:
            logger.warning("Subsector %s has no corresponding directory in %s", subsector, dir_path)
            continue

        existing_routes = get_existing_routes(
            subsector = subsector,
            path = os.path.join(dir_path, subsector),
            routes = routes 
        )

        existing_subsectors[subsector] = existing_routes
    
    return existing_subsectors

def get_existing_routes(subsector: str, path: str, routes: Dict[str, List[str]]) -> Dict[str, Dict[str,Any]]:
    subsector_paths = [path for path in glob.glob(path + '/*.json')]
    subsector_filenames = [Path(file_path).stem for file_path in subsector_paths]
    subsector_filepaths = dict(zip(subsector_filenames, subsector_paths))

    existing_routes = {}
    for route_key, utterances in routes.items():
        if route_key not in subsector_filenames:
            logger.warning("Route %s for subsector %s has no corresponding file", route_key, subsector)
            continue
        
        description = get_route_description(subsector_filepaths[route_key])
        if not description:
            logger.warning("Route %s has no file description!", route_key)
            continue

        existing_routes[route_key] = {
            "description": description,
            "utterances": utterances
        }
    
    return existing_routes
    
def get_json_filenames(directory: str) -> List[str]:
    """
    Returns ".json" filenames from given directory path.

    Args:
        directory (str): Path to directory.

    Returns:
        List[str]: Files with ".json" extension.
    """
    path = Path(directory)
    json_files = [file.name for file in path.glob('*.json')]
    logger.info("Найдены JSON файлы в выбранной папке: %s ...", json_files[:5])
    logger.info("Количевство файлов JSON: %d штук", len(json_files))

    return json_files

def get_route_description(path: str) -> str | None:
    """
    Получает описание маршрута из JSON файла.

    Args:
        path: path to file with description

    Returns:
        str: описание маршрута
    """
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    description = data.get('description')
    if description:
        return description
    
    return None

def get_route_description_by_subsector(route_name: str, selected_folder: str) -> str:
    """
    Получает описание маршрута из JSON файла.

    Args:
        route_name: имя маршрута
        selected_folder: выбранная папка

    Returns:
        str: описание маршрута
    """
    file_path = os.path.join(selected_folder, f"{route_name}.json") 
    data = json.loads(Path(file_path).read_text(encoding='utf-8'))
    description = data.get('description')
    if description:
        return description

    raise ValueError(f"Отсутствует описание для маршрута {route_name}")


def read_and_merge(paths: List[str]) -> Dict[str, Any]:
    """
    Reads JSON files from given paths and merges them to a single JSON

    Args:
        paths (List[str]): JSON paths to merge

    Returns:
        Dict[str, Any]: Dict with merged JSONs

    Raises:
        FileNotFoundError: File on path does not exist
        JSONDecodeError: JSON decoding issues
    """
    merged = {}

    logger.info("Reading json files...")
    for p in paths:
        try:
            with open(p, encoding='utf-8') as f:
                d = json.load(f)
            merged.update(d)

        except FileNotFoundError as e:
            logger.info(f"File not found: {p}")
        except json.JSONDecodeError as e:
            logger.info(f"JSON Decoding failed: {p}")
        except Exception as e:
            logger.info(f"Error while reading {p}: {str(e)}")

    return merged


def normalize_dict_descriptions(source: Dict[str, Any],
                             description_key: str = 'description', 
                             exclude_keys: Set[str] = {'description', 'keywords'}
                             ) -> Dict[str, str]:
    """
    The function takes descriptions stored in various formats within a dictionary (nested dictionaries, lists, or direct strings)
    and normalizes them into a consistent structure where each key maps directly to its description as a string.

    3 cases are being processed, where the description-value:
    1. is a Dict with 'description' as a key and the de-facto description-value as value
    2. is a List, where the first item contains the description-value
    3. directly maps to the key

    Args:
        source: Source Dict to be normalized
        description_key: Keyname mapping the description-value
        exclude_keys: Set of keys constrained to the document itself rather to one of the subjects in the document (default {'description', 'keywords'})

    Returns:
        Uniform Dict[str,str], where the key maps directly the description value

    Example:
        >>> source = {
        ...     "item1": {"description": "desc1"},
        ...     "item2": ["Description: desc2"],
        ...     "item3": "desc3"
        ... }
        >>> extract_key_descriptions(source)

        returns 

        >>> {
        ...    'item1': 'desc1',
        ...    'item2': 'desc2',
        ...    'item3': 'desc3'
        >>> }
    """
    logger.info(
        "Normalizing dict with descriptions...")
    
    if not isinstance(source, dict):
        raise TypeError("json_content must be a dictionary")
    
    if not isinstance(description_key, str):
        raise TypeError("description_key must be a string")
    
    normalized = {}
    desc_marker = f"{description_key}:"
    desc_marker_lower = desc_marker.lower()

    for key, value in source.items():
        if key in exclude_keys:
            continue

        # Случай 1: Словарь с ключом описания
        if isinstance(value, dict):
            if description := value.get(description_key):
                normalized[key] = description

        # Случай 2: Список с описанием в первом элементе
        elif isinstance(value, list) and value and isinstance(value[0], str):
            first_item = value[0].strip()
            # Проверяем наличие маркера описания
            if desc_marker_lower in first_item.lower():
                description = first_item.split(desc_marker, 1)[1].strip()
            else:
                description = first_item.strip()

        # Случай 3: Строковое значение
        elif isinstance(value, str):
            description = value.split('\n')[0].strip()

        if description:  # Добавляем только непустые описания
            normalized[key] = description

    return normalized


def clean_json_text(json_text: str) -> str:
    """
    Очищает текст из JSON строки от специальных символов и форматирует его.
    Добавляет нумерацию для продуктов (строк содержащих "name":).
    """
    # Шаг 1: Парсинг JSON
    try:
        data: Dict[str, Union[List[str], str, Dict]] = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return ""

    # Шаг 2: Обработка данных
    result_parts = []
    
    for key, value in data.items():
        if isinstance(value, dict) and "description" in value and "product_list" in value:
            # Обрабатываем специальную структуру с описанием и списком продуктов
            result_parts.append(value["description"])
            
            # Добавляем префикс для списка продуктов
            product_list_prefix = "### ВНИМАНИЕ ЭТО \"список продукции из ассортиментого перечня\" для ответа на вопрос пользователя!, ФОРМИРУЙТЕ ОТВЕТ ИЗ ЭТОГО СПИСКА ЕСЛИ ОН АКТУАЛЕН! ###: "
            
            # Обрабатываем список продуктов с нумерацией
            product_list = value["product_list"]
            if isinstance(product_list, list):
                numbered_products = []
                product_counter = 1
                
                for item in product_list:
                    item_str = str(item)
                    # Проверяем, является ли элемент продуктом
                    if '"name":' in item_str or "'name':" in item_str:
                        # Очищаем строку
                        cleaned_item = re.sub(r'\s+', ' ', re.sub(r'[{}"\\]', '', item_str)).strip()
                        # Добавляем нумерацию
                        numbered_products.append(f"{product_counter}. {cleaned_item}")
                        product_counter += 1
                    else:
                        # Обычная очистка для не-продуктов
                        cleaned_item = re.sub(r'\s+', ' ', re.sub(r'[{}"\\]', '', item_str)).strip()
                        numbered_products.append(cleaned_item)
                
                result_parts.append(f"{product_list_prefix}[\n" + "\n".join(numbered_products) + "\n]")
            else:
                result_parts.append(f"{product_list_prefix}{product_list}")
                
        elif isinstance(value, list):
            # Обычный список
            content_list = [str(item) for item in value]
            cleaned_items = []
            product_counter = 1
            
            for item in content_list:
                if not item.strip():
                    continue
                    
                is_product = '"name":' in item or "'name':" in item
                cleaned_item = re.sub(r'\s+', ' ', re.sub(r'[{}"\\]', '', item)).strip()
                
                if is_product:
                    cleaned_items.append(f"{product_counter}. {cleaned_item}")
                    product_counter += 1
                else:
                    cleaned_items.append(cleaned_item)
            
            result_parts.extend(cleaned_items)
        else:
            # Обычное значение
            result_parts.append(str(value))

    return '\n\n'.join(result_parts)


def get_nested_data(data: Dict[str, Any], keys: List[str]) -> Any:
    """
    Рекурсивно извлекает данные из словаря по списку ключей.
    Если последний ключ равен 'product_list' и в том же словаре присутствует ключ 'description',
    то результатом будет словарь с описанием и данными из 'product_list'.
    
    Args:
        data (Dict[str, Any]): Словарь, из которого нужно извлечь данные.
        keys (List[str]): Список ключей для доступа в словаре к вложенным данным.
    
    Returns:
        Any: Значение, расположенное по указанному пути ключей с объединённым описанием,
             если оно присутствует.
    """
    current = data
    for idx, key in enumerate(keys):
        if isinstance(current, dict) and key in current:
            # Если это последний ключ и он равен "product_list"
            if idx == len(keys) - 1 and key == "product_list":
                description = current.get("description")
                product_data = current[key]
                if description is not None:
                    # Возвращаем структурированные данные, а не JSON строку
                    return {
                        "description": f"### Это описание найденного раздела документа ###: {description}",
                        "product_list": product_data
                    }
                return product_data
            current = current[key]
        else:
            # Если ключ не найден или данные не являются словарем, возвращаем текущие данные
            return current
    return current

def remove_think_tags(text):
    pattern = r'<(think|analysis)>.*?</\1>'
    return re.sub(pattern, '', text, flags=re.DOTALL)