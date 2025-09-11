"""
Структура полей для semi_finished отрасли.
Следует универсальной архитектуре Tool Calling.
"""

# Маппинг ключей для каждого JSON файла semi_finished отрасли
SEMI_FINISHED_KEYS_MAPPING = {
    "chees.json": {
        "file_description": "Сыры и сырные продукты",
        "product_keys": {},
    },
    "colorants.json": {
        "file_description": "Красители для полуфабрикатов",
        "product_keys": {},
    },
    "dry_dairy_products_ready_meal_mixes.json": {
        "file_description": "Сухие молочные продукты и готовые смеси для блюд",
        "product_keys": {},
    },
    "filling.json": {
        "file_description": "Начинки для полуфабрикатов",
        "product_keys": {},
    },
    "industry_products.json": {
        "file_description": "Промышленные продукты для производства полуфабрикатов",
        "product_keys": {},
    },
    "marinades.json": {
        "file_description": "Маринады для полуфабрикатов",
        "product_keys": {},
    },
    "recipes.json": {
        "file_description": "Рецептуры и технологические решения",
        "product_keys": {},
    },
    "semi_finished_questions.json": {
        "file_description": "Часто задаваемые вопросы по полуфабрикатам",
        "product_keys": {},
    },
    "stabilizers_preservatives.json": {
        "file_description": "Стабилизаторы и консерванты для полуфабрикатов",
        "product_keys": {},
    },
}

# Маппинг ключей к файлам (для субключей)
KEY_TO_FILE_MAPPING = {
    # TODO: Будет заполнено при необходимости поддержки субключей
}