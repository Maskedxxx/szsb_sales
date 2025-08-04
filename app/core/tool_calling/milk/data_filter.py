"""
Функция фильтрации данных молочной отрасли с использованием промежуточного маппинга enum → реальные данные.

Использует готовые маппинги для точного поиска по паттернам и regex для числовых значений.
"""

import json
import pandas as pd
import logging
from typing import List

# Импортируем универсальный промежуточный маппинг
from .mappings.universal import has_milk_enum_match

# Настройка логирования
logger = logging.getLogger(__name__)


def filter_milk_products_smart(
    product_list: List[str],
    filter_key: str,
    enum_value: str
) -> List[str]:
    """
    Фильтрует JSON строки продуктов молочной отрасли используя промежуточный маппинг enum → реальные данные.
    
    Args:
        product_list: Список JSON строк из product_list файла молочной отрасли
        filter_key: Ключ для фильтрации ("name", "properties", "dosage", "color", "packaging", "characteristics")
        enum_value: Значение enum из milk_enum_mapping.py
        
    Returns:
        Список отфильтрованных JSON строк продуктов
    """
    logger.info(f"Умная фильтрация {len(product_list)} продуктов по ключу '{filter_key}' со значением '{enum_value}'")
    
    # Парсим все JSON строки в DataFrame для удобства
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
    
    # Умная фильтрация: используем универсальный промежуточный маппинг с паттернами и regex
    try:
        mask = df[filter_key].apply(lambda x: has_milk_enum_match(x, enum_value, filter_key))
        filtered_df = df[mask]
        
        logger.info(f"Найдено совпадений: {len(filtered_df)} из {len(df)}")
        
        # Возвращаем оригинальные JSON строки
        result = filtered_df['original_json'].tolist()
        
        if not result:
            logger.info(f"Фильтрация по '{filter_key}={enum_value}' не дала результатов")
        
        return result
        
    except Exception as e:
        logger.error(f"Ошибка при применении фильтра: {str(e)}")
        # При ошибке возвращаем исходные данные
        return product_list