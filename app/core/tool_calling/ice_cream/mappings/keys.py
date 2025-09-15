"""
Ice cream industry product keys mapping for Tool Calling.
Определяет структуру полей продуктов мороженого и их описания для фильтрации.
"""

# Mapping структуры полей для каждого JSON файла отрасли мороженого
ICE_CREAM_KEYS_MAPPING = {
    "delar_flavorings_general_list.json": {
        "file_description": "Общий список ароматизаторов Delar для мороженого",
        "product_keys": {
            "name": {
                "description": "Название ароматизатора DEL'AR с артикулом",
                "filter_impact": "Позволяет искать конкретные ароматизаторы по названию и номеру (например, DEL'AR® Ваниль 11.01.125)",
                "data_type": "string"
            },
            "category": {
                "description": "Тип ароматизатора по составу и происхождению",
                "filter_impact": "Фильтрует ароматизаторы по категориям: натуральный, пищевой, инкапсулированный, эмульсионный",
                "data_type": "string"
            },
            "usage": {
                "description": "Применение ароматизатора в конкретных продуктах мороженого",
                "filter_impact": "Позволяет найти ароматизаторы для определенных видов мороженого (пломбир, эскимо, суфле и др.)",
                "data_type": "string"
            },
            "profile": {
                "description": "Детальное описание вкусоароматического профиля",
                "filter_impact": "Фильтрует по характеру вкуса: сладкий, сочный, ванильный, фруктовый, с нотами и послевкусием",
                "data_type": "string"
            }
        }
    },
    "esco_food_colorings_info.json": {
        "file_description": "Информация о пищевых красителях Esco для мороженого",
        "product_keys": {
            "name": {
                "description": "Название пищевого красителя Esco",
                "filter_impact": "Позволяет искать красители по конкретному названию и артикулу",
                "data_type": "string"
            },
            "color": {
                "description": "Цвет, получаемый при использовании красителя",
                "filter_impact": "Фильтрует красители по цвету: желтый, зеленый, красный, коричневый, оранжевый и их оттенки",
                "data_type": "string"
            },
            "dosage": {
                "description": "Рекомендуемая дозировка красителя",
                "filter_impact": "Позволяет найти красители по концентрации применения (г/л или г/т)",
                "data_type": "string"
            }
        }
    },
    "generall_all_list_glazes.json": {
        "file_description": "Общий список всех глазурей для мороженого",
        "product_keys": {
            "name": {
                "description": "Название глазури для мороженого",
                "filter_impact": "Позволяет искать глазури по конкретному названию или бренду",
                "data_type": "string"
            },
            "category": {
                "description": "Категория глазури по основным ингредиентам",
                "filter_impact": "Фильтрует глазури: фруктовая, ягодная, цитрусовая, молочная, коктейльная, экзотическая",
                "data_type": "string"
            },
            "flavor": {
                "description": "Вкус глазури",
                "filter_impact": "Позволяет найти глазури по конкретному вкусу: клубника, малина, апельсин, лимон, банан и др.",
                "data_type": "string"
            },
            "type": {
                "description": "Тип глазури по составу и консистенции",
                "filter_impact": "Фильтрует по типу: шоколадная, ванильная, карамельная, темная, спрей",
                "data_type": "string"
            },
            "ice_cream_type": {
                "description": "Тип мороженого, для которого предназначена глазурь",
                "filter_impact": "Позволяет найти глазури для конкретных видов: Пломбир, Эскимо, Крем-брюле, Лакомка/трубочка",
                "data_type": "string"
            }
        }
    },
    "plbr_esk_cr_br_lka.json": {
        "file_description": "Продукты линейки пломбир, эскимо, крем-брюле и других видов мороженого",
        "product_keys": {
            "name": {
                "description": "Название продукта для мороженого",
                "filter_impact": "Позволяет искать ингредиенты по конкретному названию или бренду",
                "data_type": "string"
            },
            "category": {
                "description": "Категория продукта по функциональному назначению",
                "filter_impact": "Фильтрует по типу: Ароматизатор, Глазурь, Стабилизатор, Топпинг, Шоколад, Ингредиент",
                "data_type": "string"
            },
            "fat_type": {
                "description": "Тип жировой основы в продукте",
                "filter_impact": "Позволяет найти продукты: натуральные или с растительным жиром",
                "data_type": "string"
            },
            "flavor": {
                "description": "Вкус продукта",
                "filter_impact": "Фильтрует по вкусу: ванильная, шоколадная, фруктовые, ягодные и др.",
                "data_type": "string"
            },
            "color": {
                "description": "Цвет продукта",
                "filter_impact": "Позволяет найти продукты по цвету: белая, коричневая",
                "data_type": "string"
            },
            "texture": {
                "description": "Текстура продукта",
                "filter_impact": "Фильтрует по консистенции: гомогенная",
                "data_type": "string"
            },
            "function": {
                "description": "Функциональное назначение продукта в производстве",
                "filter_impact": "Позволяет найти по применению: ароматизация, стабилизация, создание покрытий",
                "data_type": "string"
            }
        }
    }
}

# Маппинг субключей к файлам (если требуется поддержка сложных структур)
KEY_TO_FILE_MAPPING = {
    # Субключи из delar_flavorings_general_list.json
    "vanilla_flavorings": "delar_flavorings_general_list.json",
    "fruit_flavorings": "delar_flavorings_general_list.json", 
    "cream_and_milk_and_cheese_flavorings": "delar_flavorings_general_list.json",
    "chocolate_nutty_and_coffee_flavorings": "delar_flavorings_general_list.json",
    "spice_and_herb_flavorings": "delar_flavorings_general_list.json",
    "dessert_bakery_and_caramel_flavorings": "delar_flavorings_general_list.json",
    "other_flavorings": "delar_flavorings_general_list.json",
    "milk_based_ice_cream_liquid": "delar_flavorings_general_list.json",
    "fruit_based_desserts_liquid": "delar_flavorings_general_list.json",
    "ice_products_liquid": "delar_flavorings_general_list.json",
    "emulsion_flavor_list": "delar_flavorings_general_list.json",
    "juice_milk_based_flavorings": "delar_flavorings_general_list.json",
    "juice_fruit_based_flavorings": "delar_flavorings_general_list.json",
    "juice_ice_products_flavorings": "delar_flavorings_general_list.json",
    "flavorings_info": "delar_flavorings_general_list.json",
    
    # Субключи из esco_food_colorings_info.json
    "only_natural_food_colorings": "esco_food_colorings_info.json",
    "food_colorings": "esco_food_colorings_info.json",
    "fruit_based_desserts": "esco_food_colorings_info.json",
    "food_ice": "esco_food_colorings_info.json",
    "ice_cream_waffles": "esco_food_colorings_info.json",
    
    # Субключи из generall_all_list_glazes.json
    "general_information": "generall_all_list_glazes.json",
    "glazes_only_colored_list": "generall_all_list_glazes.json",
    "glazes_general_all_list": "generall_all_list_glazes.json",
    "ice_cream_glazes_for_plombir_eskimo_lakomka_cremebrulle": "generall_all_list_glazes.json",
    
    # Субключи из plbr_esk_cr_br_lka.json
    "eskimo_ice_cream": "plbr_esk_cr_br_lka.json",
    "creme_brulee_ice_cream": "plbr_esk_cr_br_lka.json",
    "lakomka_ice_cream": "plbr_esk_cr_br_lka.json",
    "plombir_ice_cream": "plbr_esk_cr_br_lka.json"
}

# Экспорт для универсального загрузчика
keys_mapping = ICE_CREAM_KEYS_MAPPING