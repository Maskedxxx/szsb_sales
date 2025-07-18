# app/data/final_answer_hints.py

# Подсказки для финального ответа в зависимости от подсектора, роутера и ключа
FINAL_ANSWER_HINTS = {
    # Мясная отрасль (08)
    "08": {
        # Роутер: стабилизаторы и загустители
        "stabilizers_and_thickeners_list": {
            "stabilizers": """
            """,
            "stabilizers_and_thickeners": """
            """,
            "stabilizers_for_ham_only": """
            """
        },
        
        # Роутер: универсальные ароматизаторы и добавки
        "universal_flavors_and_additives_for_meat": {
            "MEAT_PROFILE": """
            """,
            "GASTRONOMIC_FLAVORS": """
            """
        },
        
        # Роутер: колбасы по ТУ и ГОСТ
        "sausage_tu_and_gost": {
            "TU_SAUSAGES": """
            """,
            "GOST_SAUSAGES": """
            """
        }
    },
    
    # Молочная отрасль (04)
    "04": {
        "delar_flavor_collection": {
            "flavor_bases": """
            """
        }
    },
    
    # Мороженое (05)
    "05": {
        "ice_cream_stabilizers": {
            "stabilizer_systems": """
            """
        }
    },
    
    # Напитки (09)
    "09": {
        "drink_stabilizers": {
            "clarity_agents": """
            """,
            "flavor_data": """
            """
        }
    },
    
    # Мучные кондитерские изделия (07)
    "07": {
        "delar_collection": {
        }
    },
    
    # Жировая отрасль (02)
    "02": {
        # Роутер: антиоксиданты
        "antioxidants": {
            "antioxidants": """
            """
        },
        
        # Роутер: какао порошки
        "cocoa_powders": {
            "cocoa_powders": """
            """
        },
        
        # Роутер: ароматизаторы DEL'AR
        "delar_flavors": {
            "flavors": """
            """
        },
        
        # Роутер: сухие молочные продукты
        "dry_milk_products": {
            "milk_products": """
            """
        },
        
        # Роутер: эмульгаторы для маргарина и спредов
        "emulsifiers_for_margarine_spreads": {
            "emulsifiers": """
            """
        },
        
        # Роутер: наполнители и топпинги
        "fillers_and_toppings": {
            "fillers": """
            """
        },
        
        # Роутер: пищевые красители
        "food_colors": {
            "colors": """
            """
        },
        
        # Роутер: консерванты и кислоты
        "preservatives_acids": {
            "preservatives": """
            """
        },
        
        # Роутер: стабилизирующие составы
        "stabilizers_compounds": {
            "stabilizers": """
            """
        },
        
        # Роутер: подсластители
        "sweeteners": {
            "sweeteners": """
            """
        }
    }
}

# Общие подсказки по подсекторам (если нет специфичных для роутера/ключа)
GENERAL_SUBSECTOR_HINTS = {
    "08": """
    """,

    "04": """
    """,
    
    "05": """
    """,
    
    "09": """
    """,
    
    "07": """
    """,
    
    "02": """
    """
}

def get_final_answer_hint(subsector_id: str, route_name: str = None, key_name: str = None) -> str:
    """
    Получает подсказку для финального ответа в зависимости от контекста.
    
    Args:
        subsector_id (str): ID подсектора
        route_name (str, optional): Название роутера
        key_name (str, optional): Название ключа
        
    Returns:
        str: Подсказка для финального ответа
    """
    # Пробуем найти специфичную подсказку
    if (subsector_id in FINAL_ANSWER_HINTS and 
        route_name and route_name in FINAL_ANSWER_HINTS[subsector_id] and
        key_name and key_name in FINAL_ANSWER_HINTS[subsector_id][route_name]):
        return FINAL_ANSWER_HINTS[subsector_id][route_name][key_name]
    
    # Если нет специфичной подсказки, возвращаем общую для подсектора
    return GENERAL_SUBSECTOR_HINTS.get(subsector_id, "")