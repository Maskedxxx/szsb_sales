"""
Маппинг ключей продуктов для каждого JSON файла meat отрасли.
Следует структуре универсальной архитектуры Tool Calling.
"""

# Маппинг ключей продуктов для каждого файла мясной отрасли
MEAT_KEYS_MAPPING = {
    "additives.json": {
        "file_description": "Функциональные и вкусо-ароматические добавки для производства колбасных изделий в разных технологиях",
        "product_keys": {
            "name": {
                "description": "Название добавки",
                "filter_impact": "Позволяет искать по названию продукта, бренду (ГОСАРОМ®, DEL'AR®) и типу добавки",
                "data_type": "string"
            },
            "application": {
                "description": "Область применения добавки",
                "filter_impact": "Позволяет фильтровать по типу колбасных изделий и ценовому сегменту",
                "data_type": "array"
            },
            "dosage": {
                "description": "Дозировка добавки",
                "filter_impact": "Позволяет фильтровать по диапазону дозировок (г/кг)",
                "data_type": "object"
            },
            "gost": {
                "description": "Соответствие ГОСТ",
                "filter_impact": "Позволяет отфильтровать добавки по соответствию стандарту ГОСТ",
                "data_type": "boolean"
            },
            "is_halal": {
                "description": "Халяльность продукта",
                "filter_impact": "Позволяет фильтровать халяльные добавки",
                "data_type": "boolean"
            }
        }
    },
    "cultures_and_casings.json": {
        "file_description": "Микробиологические стартовые культуры для ферментированных мясных продуктов и колбасные оболочки",
        "product_keys": {
            "name": {
                "description": "Название культуры или оболочки",
                "filter_impact": "Позволяет искать по названию продукта и бренду (Startline®, Golden Line®)",
                "data_type": "string"
            },
            "application": {
                "description": "Область применения продукта",
                "filter_impact": "Позволяет фильтровать по типу производимых изделий и технологическим процессам",
                "data_type": "array"
            },
            "composition": {
                "description": "Микробиологический состав стартовых культур",
                "filter_impact": "Позволяет фильтровать по типу микроорганизмов и штаммов",
                "data_type": "array"
            },
            "advantages": {
                "description": "Технологические преимущества использования",
                "filter_impact": "Позволяет фильтровать по функциональным свойствам и эффектам",
                "data_type": "array"
            },
            "is_halal": {
                "description": "Халяльная сертификация",
                "filter_impact": "Позволяет фильтровать продукты с халяльной сертификацией",
                "data_type": "boolean"
            }
        }
    },
    "fillings.json": {
        "file_description": "Начинки и наполнители для мясных изделий: сыры, фруктовые, овощные, кремовые начинки",
        "product_keys": {
            "name": {
                "description": "Название начинки или сырного продукта",
                "filter_impact": "Позволяет искать по типу начинки, вкусу и бренду продукта",
                "data_type": "string"
            },
        }
    },
    "flavorings.json": {
        "file_description": "Вкусо-ароматические добавки, моноспеции и гастрономические системы для мясной промышленности",
        "product_keys": {
            "name": {
                "description": "Название вкусо-ароматической добавки или пряности",
                "filter_impact": "Позволяет искать по названию продукта и типу ароматизатора",
                "data_type": "string"
            },
            "flavor_profile": {
                "description": "Профиль вкуса и аромата продукта",
                "filter_impact": "Позволяет фильтровать по вкусовым характеристикам и ароматическим нотам",
                "data_type": "string"
            },
            "purpose": {
                "description": "Назначение и область применения",
                "filter_impact": "Позволяет фильтровать по сфере применения и назначению (только для моноспеций)",
                "data_type": "string"
            },
            "ratio_to_natural_spice": {
                "description": "Соотношение к натуральной пряности",
                "filter_impact": "Позволяет фильтровать по концентрации относительно натуральных аналогов",
                "data_type": "string"
            },
            "dosage": {
                "description": "Рекомендуемая дозировка применения",
                "filter_impact": "Позволяет фильтровать по диапазону дозировок (г/кг)",
                "data_type": "object"
            },
            "is_halal": {
                "description": "Халяльная сертификация продукта",
                "filter_impact": "Позволяет фильтровать халяльные ароматизаторы",
                "data_type": "boolean"
            },
            "is_e_free": {
                "description": "Продукт без пищевых добавок с индексами E",
                "filter_impact": "Позволяет фильтровать натуральные продукты без синтетических добавок",
                "data_type": "boolean"
            },
            "is_vegan": {
                "description": "Веганский продукт",
                "filter_impact": "Позволяет фильтровать продукты подходящие для веганского питания",
                "data_type": "boolean"
            }
        }
    },
    "mixes_and_batters.json": {
        "file_description": "Сухие кулинарные основы и покрытия для термообработки: смеси для супов и соусов, панировки и кляры",
        "product_keys": {
            "name": {
                "description": "Название смеси, панировки или кляра",
                "filter_impact": "Позволяет искать по названию продукта, бренду (DEL'AR®, DENFAI®, Millgri®) и типу смеси",
                "data_type": "string"
            },
            "flavor_profile": {
                "description": "Профиль вкуса и аромата панировочных смесей",
                "filter_impact": "Позволяет фильтровать по вкусовым характеристикам и составу специй",
                "data_type": "string"
            },
            "is_halal": {
                "description": "Халяльная сертификация продукта",
                "filter_impact": "Позволяет фильтровать халяльные смеси",
                "data_type": "boolean"
            },
            "is_e_free": {
                "description": "Продукт без пищевых добавок с индексами E",
                "filter_impact": "Позволяет фильтровать натуральные смеси без синтетических добавок",
                "data_type": "boolean"
            }
        }
    },
    "preservatives_and_additives.json": {
        "file_description": "Консерванты, антиоксиданты, улучшители теста и пищевые красители для мясной промышленности",
        "product_keys": {
            "name": {
                "description": "Название консерванта, улучшителя или красителя",
                "filter_impact": "Позволяет искать по названию продукта и бренду (AiBi®, DEL'AR®, DENFAI®, Esco®)",
                "data_type": "string"
            },
            "dosage_percentage": {
                "description": "Дозировка в процентном выражении",
                "filter_impact": "Позволяет фильтровать по уровню концентрации в процентах",
                "data_type": "string"
            },
            "application": {
                "description": "Область применения продукта",
                "filter_impact": "Позволяет фильтровать по типу производства и назначению (для улучшителей теста)",
                "data_type": "string"
            },
            "is_halal": {
                "description": "Халяльная сертификация продукта",
                "filter_impact": "Позволяет фильтровать халяльные консерванты и добавки",
                "data_type": "boolean"
            },
            "is_e_free": {
                "description": "Продукт без пищевых добавок с индексами E (чистая этикетка)",
                "filter_impact": "Позволяет фильтровать натуральные консерванты без синтетических добавок",
                "data_type": "boolean"
            }
        }
    },
    "processing_aids.json": {
        "file_description": "Технологические вспомогательные средства: агенты инъектирования, добавки для гриль-колбас и маринады",
        "product_keys": {
            "name": {
                "description": "Название технологического средства",
                "filter_impact": "Позволяет искать по названию продукта и типу технологического решения",
                "data_type": "string"
            },
            "dosage": {
                "description": "Структурированная дозировка с минимальными и максимальными значениями",
                "filter_impact": "Позволяет фильтровать по диапазону дозировок (г/кг)",
                "data_type": "object"
            },
            "application": {
                "description": "Область технологического применения",
                "filter_impact": "Позволяет фильтровать по типу производственного процесса",
                "data_type": "string"
            },
            "ingredients": {
                "description": "Состав ингредиентов продукта",
                "filter_impact": "Позволяет фильтровать по составу и компонентам (для жидких маринадов)",
                "data_type": "string"
            },
            "is_halal": {
                "description": "Халяльная сертификация продукта",
                "filter_impact": "Позволяет фильтровать халяльные технологические средства",
                "data_type": "boolean"
            },
            "is_e_free": {
                "description": "Продукт без пищевых добавок с индексами E",
                "filter_impact": "Позволяет фильтровать натуральные средства без синтетических добавок",
                "data_type": "boolean"
            }
        }
    },
    "semifinished.json": {
        "file_description": "Комплексные пряные смеси для полуфабрикатов и регуляторы вкуса и кислотности",
        "product_keys": {
            "name": {
                "description": "Название пряной смеси или регулятора вкуса",
                "filter_impact": "Позволяет искать по названию продукта и бренду (DEL'AR®)",
                "data_type": "string"
            },
            "application": {
                "description": "Область применения и ценовые сегменты",
                "filter_impact": "Позволяет фильтровать по типу полуфабрикатов и ценовой категории",
                "data_type": "array"
            },
            "application_area": {
                "description": "Область применения регуляторов вкуса",
                "filter_impact": "Позволяет фильтровать по сфере использования (только для регуляторов)",
                "data_type": "string"
            },
            "flavor_profile": {
                "description": "Профиль вкуса регулятора",
                "filter_impact": "Позволяет фильтровать по вкусовым характеристикам (только для регуляторов)",
                "data_type": "string"
            },
            "dosage": {
                "description": "Структурированная дозировка с минимальными и максимальными значениями",
                "filter_impact": "Позволяет фильтровать по диапазону дозировок (г/кг)",
                "data_type": "object"
            },
            "is_halal": {
                "description": "Халяльная сертификация продукта",
                "filter_impact": "Позволяет фильтровать халяльные пряные смеси и регуляторы",
                "data_type": "boolean"
            },
            "is_e_free": {
                "description": "Продукт без пищевых добавок с индексами E",
                "filter_impact": "Позволяет фильтровать натуральные смеси линейки Naturel",
                "data_type": "boolean"
            }
        }
    },
    "systems.json": {
        "file_description": "Функциональные системы для мясной и частично молочной промышленности: инъекционные системы, стабилизаторы, желирующие и эмульсионные продукты",
        "product_keys": {
            "name": {
                "description": "Название функциональной системы",
                "filter_impact": "Позволяет искать по названию и бренду (Гелеон®, DEL'AR®, Golden Line®, Startline®, Denmilk®, Miligri®)",
                "data_type": "string"
            },
            "application": {
                "description": "Конкретная область применения системы",
                "filter_impact": "Позволяет фильтровать по типу производственного процесса",
                "data_type": "string"
            },
            "flavor_profile": {
                "description": "Профиль вкуса и аромата декораторов",
                "filter_impact": "Позволяет фильтровать по вкусовым характеристикам и ароматам",
                "data_type": "string"
            },
            "is_halal": {
                "description": "Соответствие халяльным требованиям",
                "filter_impact": "Позволяет фильтровать продукты для экспортных и специальных рынков",
                "data_type": "boolean"
            },
            "is_e_free": {
                "description": "Продукт без пищевых добавок с индексами E (чистая этикетка)",
                "filter_impact": "Позволяет фильтровать натуральные системы без синтетических добавок",
                "data_type": "boolean"
            }
        }
    }
}

# Маппинг selected_key к файлам для субключей (если есть сложные структуры)
KEY_TO_FILE_MAPPING = {
    # Субключи для additives.json
    "gost_sausages": "additives.json",
    "cooked_sausages_tu": "additives.json", 
    "smoked_cured_sausages": "additives.json",
    # Субключи для cultures_and_casings.json
    "starter_cultures": "cultures_and_casings.json",
    "sausage_casings": "cultures_and_casings.json",
    # Субключи для fillings.json
    "cheeses": "fillings.json",
    "fruit_stuffings": "fillings.json",
    "vegetable_stuffings": "fillings.json",
    "cream_stuffings": "fillings.json",
    "condensed_milk_stuffings": "fillings.json",
    # Субключи для flavorings.json
    "mono_spices": "flavorings.json",
    "meat_profile_additives": "flavorings.json",
    "gastronomic_additives": "flavorings.json",
    # Субключи для preservatives_and_additives.json
    "natural_preservatives_aibi": "preservatives_and_additives.json",
    "other_preservatives": "preservatives_and_additives.json",
    "dough_improvers": "preservatives_and_additives.json",
    "food_colorings": "preservatives_and_additives.json",
    # Субключи для processing_aids.json
    "injection_agents": "processing_aids.json",
    "bbq_sausage_additives": "processing_aids.json",
    "dry_marinades": "processing_aids.json",
    "liquid_marinades": "processing_aids.json",
    # Субключи для semifinished.json
    "spice_mixes": "semifinished.json",
    "flavor_regulators": "semifinished.json",
    # Субключи для systems.json
    "injection_aids_poultry": "systems.json",
    "injection_aids_beef_pork": "systems.json",
    "ham_additives": "systems.json",
    "nitrite_salt_replacements": "systems.json",
    "stabilizers": "systems.json",
    "flavor_decorators": "systems.json",
    "minced_meat_stabilizers": "systems.json",
    "cottage_cheese_products": "systems.json",
    "jelly_products": "systems.json",
    "emulsion_products": "systems.json",
    "thermostable_fillings": "systems.json",
    "dry_milk_products": "systems.json",
    # Субключи для mixes_and_batters.json
    "soup_mixes": "mixes_and_batters.json",
    "sauce_mixes": "mixes_and_batters.json",
    "breading_products": "mixes_and_batters.json",
    "batter_products": "mixes_and_batters.json"
}

# Обязательный экспорт для универсального загрузчика IndustryMappingsLoader
keys_mapping = MEAT_KEYS_MAPPING
