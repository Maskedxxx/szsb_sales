"""
Структура полей для semi_finished отрасли.
Следует универсальной архитектуре Tool Calling.
"""

# Маппинг ключей для каждого JSON файла semi_finished отрасли
SEMI_FINISHED_KEYS_MAPPING = {
    "chees.json": {
        "file_description": "Сыры и сырные продукты",
        "product_keys": {
            "name": {
                "description": "Полное коммерческое название сырного продукта включая бренд, тип сыра и характеристики жирности",
                "filter_impact": "Фильтрует продукты по подстрокам в названии: типу сыра, бренду, характеристикам упаковки",
                "data_type": "string"
            },
            "properties": {
                "description": "Текстовое описание ключевых свойств сыра таких как натуральность, тягучесть при нагревании, отсутствие сои",
                "filter_impact": "Фильтрует по ключевым характеристикам: натуральность продукта, поведение при нагревании, состав",
                "data_type": "string"
            }
        },
    },
    "colorants.json": {
        "file_description": "Красители для полуфабрикатов",
        "product_keys": {
            "name": {
                "description": "Коммерческое название пищевого красителя с указанием типа, цвета и производителя",
                "filter_impact": "Фильтрует красители по названию, типу окрашивания, цветовой гамме и бренду",
                "data_type": "string"
            },
            "properties": {
                "description": "Описание функциональных свойств красителя включая интенсивность окрашивания и область применения",
                "filter_impact": "Фильтрует по характеристикам окрашивания, стабильности цвета, совместимости с продуктами",
                "data_type": "string"
            },
            "dosage": {
                "description": "Рекомендуемые нормы внесения красителя в граммах или процентах от массы готового продукта",
                "filter_impact": "Фильтрует по диапазонам дозировок для подбора оптимального количества внесения",
                "data_type": "string"
            }
        },
    },
    "dry_dairy_products_ready_meal_mixes.json": {
        "file_description": "Сухие молочные продукты и готовые смеси для блюд",
        "product_keys": {
            "name": {
                "description": "Коммерческое наименование сухого молочного продукта или готовой смеси с указанием назначения и характеристик",
                "filter_impact": "Фильтрует по типу продукта, назначению смеси, вкусовым характеристикам и бренду",
                "data_type": "string"
            },
            "properties": {
                "description": "Текстовое описание функциональных и органолептических свойств продукта включая растворимость и вкус",
                "filter_impact": "Фильтрует по функциональным характеристикам, способу приготовления, вкусовым особенностям",
                "data_type": "string"
            },
            "dosage": {
                "description": "Нормы внесения продукта в рецептуру указанные в граммах на литр готового изделия или в процентах",
                "filter_impact": "Фильтрует по диапазонам рекомендуемых дозировок для технологического процесса",
                "data_type": "string"
            },
            "e_free": {
                "description": "Булево значение отсутствия синтетических пищевых добавок с индексом E в составе продукта",
                "filter_impact": "Фильтрует продукты строго по наличию или отсутствию E-добавок в составе",
                "data_type": "boolean"
            }
        },
    },
    "filling.json": {
        "file_description": "Начинки для полуфабрикатов",
        "product_keys": {
            "name": {
                "description": "Полное коммерческое название начинки с указанием вкуса, типа продукта и производителя",
                "filter_impact": "Фильтрует начинки по вкусовому профилю, типу основы, назначению и бренду",
                "data_type": "string"
            },
            "properties": {
                "description": "Описание характеристик начинки включая консистенцию, вкусовые особенности и область применения",
                "filter_impact": "Фильтрует по текстурным свойствам, органолептическим характеристикам, способу использования",
                "data_type": "string"
            }
        },
    },
    "industry_products.json": {
        "file_description": "Промышленные продукты для производства полуфабрикатов",
        "product_keys": {
            "name": {
                "description": "Коммерческое название промышленного продукта с указанием функционального назначения и бренда производителя",
                "filter_impact": "Фильтрует по типу промышленного продукта, функциональному назначению, бренду",
                "data_type": "string"
            },
            "properties": {
                "description": "Описание функциональных свойств промышленного продукта включая стабилизацию, эмульгирование и технологические функции",
                "filter_impact": "Фильтрует по технологическим функциям, области применения, особенностям использования",
                "data_type": "string"
            },
            "composition": {
                "description": "Детальный состав промышленного продукта с перечислением основных компонентов и добавок",
                "filter_impact": "Фильтрует по конкретным ингредиентам, типу основы, наличию специальных добавок",
                "data_type": "string"
            },
            "dosage": {
                "description": "Нормы внесения промышленного продукта в технологический процесс указанные в граммах на килограмм основы",
                "filter_impact": "Фильтрует по диапазонам рекомендуемых дозировок для оптимального технологического процесса",
                "data_type": "string"
            },
            "properties_and_dosage": {
                "description": "Комбинированное описание объединяющее функциональные свойства продукта с рекомендуемыми нормами внесения",
                "filter_impact": "Фильтрует одновременно по технологическим характеристикам и применяемым дозировкам",
                "data_type": "string"
            }
        },
    },
    "marinades.json": {
        "file_description": "Маринады для полуфабрикатов",
        "product_keys": {
            "name": {
                "description": "Коммерческое название маринада с указанием вкусового профиля, типа маринада и назначения",
                "filter_impact": "Фильтрует маринады по вкусовому направлению, типу продукта, целевому назначению, бренду",
                "data_type": "string"
            },
            "properties": {
                "description": "Описание функциональных свойств маринада включая способ применения и особенности воздействия на продукт",
                "filter_impact": "Фильтрует по способу применения, воздействию на продукт, особенностям использования",
                "data_type": "string"
            },
            "dosage": {
                "description": "Рекомендуемые нормы внесения маринада на килограмм обрабатываемого мясного сырья или полуфабриката",
                "filter_impact": "Фильтрует по диапазонам норм внесения для оптимального маринования сырья",
                "data_type": "string"
            },
            "e_free": {
                "description": "Булево значение отсутствия синтетических пищевых добавок с E-индексом в составе маринада",
                "filter_impact": "Фильтрует маринады строго по наличию или отсутствию E-добавок для натуральности продукта",
                "data_type": "boolean"
            }
        },
    },
    "recipes.json": {
        "file_description": "Рецептуры и технологические решения",
        "product_keys": {
            "product_name": {
                "description": "Наименование готового продукта",
                "filter_impact": "high",
                "data_type": "string"
            },
            "category": {
                "description": "Категория продукта",
                "filter_impact": "high",
                "data_type": "string"
            },
            "description": {
                "description": "Описание рецептуры",
                "filter_impact": "medium",
                "data_type": "string"
            },
            "ingredients": {
                "description": "Ингредиенты рецептуры",
                "filter_impact": "medium",
                "data_type": "string"
            },
            "technology": {
                "description": "Технология приготовления",
                "filter_impact": "medium",
                "data_type": "string"
            },
            "total_output_kg": {
                "description": "Общий выход в килограммах",
                "filter_impact": "low",
                "data_type": "number"
            }
        },
    },
    "stabilizers_preservatives.json": {
        "file_description": "Стабилизаторы и консерванты для полуфабрикатов",
        "product_keys": {
            "name": {
                "description": "Наименование стабилизатора или консерванта",
                "filter_impact": "high",
                "data_type": "string"
            },
            "properties": {
                "description": "Свойства добавки",
                "filter_impact": "medium",
                "data_type": "string"
            },
            "dosage": {
                "description": "Дозировка применения",
                "filter_impact": "medium",
                "data_type": "string"
            },
            "e_free": {
                "description": "Отсутствие E-добавок",
                "filter_impact": "high",
                "data_type": "boolean"
            }
        },
    },
}

# Маппинг ключей к файлам (для субключей)
KEY_TO_FILE_MAPPING = {
    # chees.json
    "cheeses": "chees.json",
    
    # colorants.json
    "colorants": "colorants.json",
    
    # dry_dairy_products_ready_meal_mixes.json
    "dry_dairy_products": "dry_dairy_products_ready_meal_mixes.json",
    "ready_meal_mixes": "dry_dairy_products_ready_meal_mixes.json",
    
    # filling.json
    "fillings": "filling.json",
    
    # industry_products.json
    "baking_aids": "industry_products.json",
    "batters_breading": "industry_products.json",
    "dough_improvers": "industry_products.json",
    "flavoring_additives": "industry_products.json",
    "meat_seasonings": "industry_products.json",
    "ready_meal_mixess": "industry_products.json",
    
    # marinades.json
    "marinades": "marinades.json",
    
    # recipes.json
    "dumpling_dough_recipes": "recipes.json",
    "meat_product_recipes": "recipes.json",
    "pancake_recipes": "recipes.json",
    "pastry_recipes": "recipes.json",
    
    # stabilizers_preservatives.json
    "preservatives": "stabilizers_preservatives.json",
    "stabilizers": "stabilizers_preservatives.json",
}

keys_mapping = SEMI_FINISHED_KEYS_MAPPING