"""
Маппинг ключей продуктов для каждого JSON файла selo отрасли.
"""

# Маппинг ключей продуктов для каждого файла
SELO_KEYS_MAPPING = {
    "products.json": {
        "file_description": "Кормовые продукты: биоконсерванты для силосования и пробиотические добавки",
        "product_keys": {
            "product_name": {
                "description": "Название продукта",
                "filter_impact": "Позволяет искать по конкретному названию продукта",
                "data_type": "string"
            }
        }
    }
}

# Маппинг selected_key к файлам для субключей (пустой для простой структуры)
KEY_TO_FILE_MAPPING = {}

# Экспорт для универсального загрузчика
keys_mapping = SELO_KEYS_MAPPING