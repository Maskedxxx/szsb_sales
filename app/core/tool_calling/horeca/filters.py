"""
Функции фильтрации для HoReCa данных.

Предоставляет умную фильтрацию продуктов с использованием pandas и маппингов.
"""

import json
import pandas as pd
import logging
from typing import List

from .mappings import has_enum_match

logger = logging.getLogger(__name__)


def filter_products(
    product_list: List[str],
    filter_key: str,
    enum_value: str
) -> List[str]:
    """
    Фильтрует JSON строки продуктов используя умный маппинг enum → реальные данные.
    
    Args:
        product_list: Список JSON строк из product_list файла HoReCa
        filter_key: Ключ для фильтрации ("name", "packaging", "kbgu", "shelf_life")
        enum_value: Значение enum для фильтрации
        
    Returns:
        Список отфильтрованных JSON строк продуктов
    """
    logger.info(f"Фильтрация {len(product_list)} продуктов по ключу '{filter_key}' со значением '{enum_value}'")
    
    # Парсим все JSON строки в DataFrame
    products_data = []
    original_json_strings = []
    
    for product_json in product_list:
        try:
            product = json.loads(product_json)
            products_data.append(product)
            original_json_strings.append(product_json)
        except json.JSONDecodeError as e:
            logger.warning(f"Ошибка парсинга JSON: {e}")
            continue
    
    if not products_data:
        logger.warning("Нет валидных продуктов для фильтрации")
        return []
    
    # Создаем DataFrame
    df = pd.DataFrame(products_data)
    df['original_json'] = original_json_strings
    
    logger.info(f"Успешно обработано {len(df)} продуктов")
    
    # Проверяем наличие ключа
    if filter_key not in df.columns:
        logger.error(f"Ключ '{filter_key}' не найден в продуктах. Доступные ключи: {list(df.columns)}")
        return []
    
    # Умная фильтрация с использованием маппинга
    mask = df[filter_key].apply(lambda x: has_enum_match(x, enum_value, filter_key))
    filtered_df = df[mask]
    
    logger.info(f"Найдено совпадений: {len(filtered_df)} из {len(df)}")
    
    # Возвращаем оригинальные JSON строки
    return filtered_df['original_json'].tolist()