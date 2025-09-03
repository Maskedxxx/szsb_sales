"""
Маппинг enum значений для каждого ключа продуктов в файлах масложировой отрасли.

Этот файл содержит конкретные enum значения, которые LLM может выбирать
для фильтрации данных в каждом JSON файле масложировой отрасли.
"""

from typing import Dict, List

# Маппинг enum значений для ключей продуктов в каждом файле масложировой отрасли
FAT_AND_OIL_ENUM_MAPPING = {
    "antioxidants.json": {
        "antioxidants": {
            "name": {
                "antioxidant_types": ["xtendra", "tbhq", "токоферолы", "бутилгидроксианизол", "бутилгидроксытолуол"],
                "brands": ["xtendra", "kemfood", "camlin"],
                "product_numbers": ["08", "14", "57", "1.50", "70_sf", "330"],
                "combinations": ["комплексная_пищевая_добавка", "антиоксидитель", "смешанные_токоферолы"]
            },
            "form": {
                "physical_forms": ["жидкость", "жидкий", "масляная_основа"],
                "colors": ["желтый", "светло_коричневый", "темно_желтый", "коричневый"],
                "consistency": ["вязкая", "текучая"]
            },
            "producer": {
                "companies": ["camlin_fine_sciences", "kevin_food", "kemfood", "wuxi_zuping"],
                "countries": ["индия", "китай", "россия"]
            },
            "application_areas": {
                "product_categories": ["масла_жиры", "маргарины", "консервы", "готовые_продукты"],
                "processing_types": ["промышленная_переработка", "специального_назначения", "фритюрные"],
                "dosage_ranges": ["0.005_0.02", "0.01_0.05", "0.02_0.2"]
            },
            "properties": {
                "solubility": ["жирорастворимый", "маслорастворимый", "не_растворим_в_воде"],
                "functionality": ["замедление_окисления", "увеличение_срока_хранения", "защита_от_прогоркания"]
            },
            "general_application": {
                "end_products": ["маргарины", "майонез", "соусы", "кетчупы", "консервы"],
                "usage_types": ["для_жарки", "для_выпечки", "длительного_хранения"]
            }
        }
    },

    "cocoa_powders.json": {
        "cocoa_powders": {
            "name": {
                "cocoa_types": ["алкализованный", "натуральный_какао"],
                "brands": ["tulip", "денкакао", "golden_harvest", "indcresa"],
                "processing": ["а", "н", "400"],
                "quality_grades": ["премиум", "стандарт"]
            },
            "producer": {
                "companies": ["guan_chong", "indcresa", "tulip_cocoa"],
                "countries": ["малайзия", "испания", "германия"]
            },
            "application_areas": {
                "product_categories": ["маргарины_спреды", "шоколадное_молоко", "десерты", "творожные_изделия"],
                "dosage_ranges": ["1.0_2.5", "2.0_5.0", "3.0_8.0"]
            },
            "advantages": {
                "technical_properties": ["ph_нейтральный", "высокая_степень_помола", "яркий_аромат"],
                "ph_ranges": ["6.9_7.3", "6.8_7.5"],
                "color_characteristics": ["темно_коричневый", "насыщенный", "равномерный"]
            }
        }
    },

    "delar_flavors.json": {
        "flavors_delar_liquid_gastronomic": {
            "name": {
                "gastronomic_flavors": ["горчичное", "чеснок", "хрен", "лук", "укроп", "базилик", "розмарин"],
                "meat_flavors": ["бекон", "ветчина", "салями", "копченое_мясо"],
                "dairy_flavors": ["сливочное_масло", "сыр", "творог", "сметана"]
            },
            "number": {
                "product_codes": ["11.03.142", "11.01.486", "10.06.163", "11.01.165", "11.03.141"],
                "series": ["10", "11", "12"]
            },
            "solubility": {
                "solubility_types": ["ж", "в", "ж_в", "в_о_ж_о", "ж_о_в"],
                "compatibility": ["жировая_фаза", "водная_фаза", "универсальный"]
            },
            "flavor_profile": {
                "intensity": ["легкий", "умеренный", "насыщенный", "интенсивный"],
                "characteristics": ["натуральный_аромат", "концентрированный", "сбалансированный"]
            },
            "oil_and_fat_products": {
                "applications": ["майонез", "спреды", "соусы", "кетчуп", "начинки"],
                "product_types": ["масложировые", "эмульсионные", "соусные"]
            }
        },
        "flavors_delar_liquid_sweet": {
            "name": {
                "fruit_flavors": ["ананас", "банан", "клубника", "вишня", "персик", "яблоко", "лимон"],
                "dessert_flavors": ["ваниль", "карамель", "шоколад", "сливки", "йогурт"],
                "berry_flavors": ["малина", "черника", "ежевика", "смородина"]
            },
            "number": {
                "product_codes": ["10.05.232", "10.05.801", "10.05.154", "10.05.143"],
                "sweet_series": ["10.05", "10.04", "10.03"]
            },
            "solubility": {
                "types": ["ж", "в", "ж_в"],
                "applications": ["молочные_продукты", "кондитерские", "напитки"]
            }
        },
        "flavors_delar_spray_dry_powder_gastronomic": {
            "name": {
                "powder_flavors": ["грибы", "лук", "чеснок", "зелень", "специи"],
                "meat_powders": ["бекон", "ветчина", "копчености"]
            },
            "form": {
                "physical_state": ["порошок", "гранулы", "распылительная_сушка"],
                "particle_size": ["мелкий", "средний", "крупный"]
            }
        },
        "flavors_delar_powder_gastronomic": {
            "name": {
                "powder_types": ["сыр", "сливочное_масло", "специи", "овощи"],
                "dairy_powders": ["пармезан", "чеддер", "моцарелла"]
            }
        },
        "flavor_additives_delar": {
            "name": {
                "additive_types": ["вкусоароматические", "усилители_вкуса", "модификаторы"],
                "categories": ["натуральные", "идентичные_натуральным", "искусственные"]
            }
        },
        "flavor_additives_delar_natural_spice_extract": {
            "name": {
                "spice_extracts": ["перец", "кориандр", "тмин", "анис", "фенхель"],
                "herb_extracts": ["орегано", "тимьян", "майоран", "шалфей"],
                "natural_origin": ["экстракты", "эссенции", "натуральные"]
            }
        }
    },

    "dry_milk_products.json": {
        "dry_milk_products": {
            "name": {
                "product_types": ["йогурт_сухой", "сыр_сухой", "молоко_сухое", "творог_сухой"],
                "fat_content": ["обезжиренный", "38_процентов", "50_процентов", "60_процентов"],
                "brands": ["denmilk", "millgri", "densoy"],
                "processing": ["распылительная_сушка", "сублимационная_сушка"]
            },
            "properties": {
                "characteristics": ["натуральный_молочный", "ферментированный", "лактобактерии", "пробиотический"],
                "taste_profile": ["йогуртный", "сырный", "молочный", "кисломолочный"],
                "functionality": ["белковое_обогащение", "вкусовое_улучшение", "текстурирование"]
            },
            "scope_of_application": {
                "applications": ["майонезы", "соусы", "дрессинги", "спреды"],
                "product_categories": ["эмульсионные", "молочные", "кисломолочные"]
            }
        }
    },

    "emulsifiers_for_margarine_spreads.json": {
        "emulsifiers_for_margarine_spreads": {
            "name": {
                "emulsifier_types": ["моноглицериды", "диглицериды", "дистиллированные", "лецитин"],
                "brands": ["denemul", "kvdmg", "golden_emul"],
                "product_numbers": ["01", "9503а", "02", "03"],
                "chemical_names": ["е471", "е322", "е476"]
            },
            "form": {
                "physical_forms": ["порошок", "гранулы", "хлопья", "пластины"],
                "colors": ["слоновая_кость", "белый", "кремовый", "желтоватый"]
            },
            "scope_of_application": {
                "margarine_types": ["слоеное_тесто", "82_процента", "71_процент", "60_процентов"],
                "applications": ["маргарины", "спреды", "кулинарные_жиры"],
                "fat_content": ["высокожирные", "среднежирные", "низкожирные"]
            },
            "producer": {
                "companies": ["kevin_food", "palsgaard", "corbion"],
                "countries": ["китай", "дания", "нидерланды"]
            },
            "application_areas": {
                "dosage_ranges": ["0.1_1.0", "0.2_0.8", "0.5_2.0"],
                "technical_specs": ["йодное_число_2", "точка_плавления_65_67", "влажность_менее_3"],
                "processing": ["холодный_способ", "горячий_способ", "универсальный"]
            },
            "advantages": {
                "functional_properties": ["стабилизация_эмульсии", "пластичность", "намазываемость", "аэрация"],
                "quality_improvements": ["однородность", "срок_хранения", "консистенция", "вкус"]
            }
        }
    },

    "fillers_and_toppings.json": {
        "vegetable_fillings": {
            "name": {
                "filling_categories": ["гастрономическая", "овощная", "пикантная"],
                "main_ingredients": ["грибы", "огурец", "томат", "лук", "горчица", "хрен"],
                "recipe_numbers": ["825.24", "815.01", "870.15", "845.03", "860.05"],
                "flavor_profiles": ["классика", "острый", "деликатный", "пикантный"]
            },
            "properties": {
                "consistency": ["густая_масса", "кусочки", "намазываемая", "однородная"],
                "texture": ["мелкие_кусочки", "крупные_включения", "пюреобразная"],
                "taste_characteristics": ["яркий_вкус", "насыщенный", "умеренный", "деликатный"],
                "visual": ["с_включениями", "однородная", "цветная"]
            }
        }
    },

    "food_colors.json": {
        "fat_soluble_colors": {
            "name": {
                "colorant_types": ["бета_каротин", "карамельный_колер", "паприка", "аннато"],
                "brands": ["altratene", "esco", "natcol"],
                "e_numbers": ["е160a", "е150c", "е160c", "е160b"],
                "concentrations": ["0.3_процента", "10_процентов", "30_процентов"]
            },
            "form": {
                "physical_forms": ["масляная_суспензия", "порошок", "жидкий", "паста"],
                "base": ["растительное_масло", "подсолнечное_масло", "рапсовое_масло"]
            },
            "color": {
                "color_families": ["желтый", "оранжевый", "красный", "коричневый"],
                "color_shades": ["светло_желтый", "золотистый", "темно_оранжевый", "красно_коричневый"],
                "intensity": ["слабая", "средняя", "интенсивная", "очень_яркая"]
            },
            "dosage_kg_t": {
                "dosage_ranges": ["до_0.1", "0.1_1.0", "1.0_4.0", "4.0_10.0"],
                "economic_levels": ["экономичный", "стандартный", "интенсивный"]
            },
            "application": {
                "product_categories": ["маргарины", "спреды", "майонез", "соусы", "кондитерские"],
                "end_products": ["масложировые", "эмульсионные", "хлебопекарные"]
            }
        },
        "water_soluble_colors": {
            "name": {
                "colorant_types": ["тартразин", "понсо", "кармуазин", "бриллиантовый_синий"],
                "e_numbers": ["е102", "е124", "е122", "е133"],
                "brands": ["esco", "wsc", "natcol"]
            },
            "form": {
                "physical_forms": ["порошок", "жидкий", "гранулы"],
                "solubility": ["водорастворимый", "легко_растворимый"]
            },
            "color": {
                "color_families": ["желтый", "красный", "синий", "зеленый"],
                "bright_shades": ["лимонный", "вишневый", "небесно_синий", "изумрудный"]
            },
            "application": {
                "water_phase_products": ["напитки", "желе", "водные_соусы", "сиропы"]
            }
        }
    },

    "preservatives_acids.json": {
        "preservatives_acids": {
            "name": {
                "preservative_types": ["сорбиновая_кислота", "бензойная_кислота", "лимонная_кислота_антиоксидант", "уксусная"],
                "complex_additives": ["лактобак", "консерфикс", "стабилон"],
                "brands": ["del_ar", "aibi", "натур_консерв"],
                "natural_synthetic": ["натуральный_консервант", "синтетический", "ферментированный"],
                "active_substances": ["глюкоза_ферментированная", "молочная_кислота", "пропионовая"]
            },
            "producer": {
                "companies": ["зеленые_линии", "shandong_reipu", "aibi_tech"],
                "countries": ["россия", "китай", "германия"]
            },
            "properties": {
                "main_functions": ["консервант", "антиоксидант", "регулятор_кислотности", "комплексообразователь"],
                "activity_spectrum": ["против_плесени", "против_дрожжей", "против_бактерий", "универсальный"],
                "ph_regulation": ["подкисление", "буферизация", "стабилизация"]
            },
            "scope_of_application": {
                "product_categories": ["майонез", "соусы", "маргарины", "кетчупы", "дрессинги"],
                "preservation_types": ["краткосрочная", "длительная", "интенсивная"]
            },
            "application_areas": {
                "dosage_ranges": ["0.01_0.05", "0.05_0.2", "0.2_1.0", "1.0_2.0"],
                "specific_applications": ["кисломолочные", "майонезные", "томатные", "горчичные"]
            },
            "advantages": {
                "microbiological": ["подавление_молочнокислых", "защита_от_дрожжей", "антиплесневая"],
                "technological": ["улучшение_консистенции", "стабилизация_цвета", "продление_срока"]
            }
        }
    },

    "sweeteners.json": {
        "sweeteners": {
            "name": {
                "sweetener_types": ["комбинированный", "термостабильный", "интенсивный"],
                "sweetness_ratios": ["100а", "200т", "200к", "300с"],
                "brands": ["сладин", "свитлайн", "натусвит"],
                "replacement_factors": ["1к100", "1к200", "1к300"]
            },
            "properties": {
                "characteristics": ["термостабильный", "без_послевкусия", "низкокалорийный"],
                "stability": ["высокая", "термическая", "ph_стабильный"],
                "functionality": ["замена_сахара", "снижение_калорий", "диетический"]
            },
            "scope_of_application": {
                "applications": ["майонезы", "соусы", "кетчупы", "дрессинги"],
                "diet_products": ["диетические", "низкокалорийные", "для_диабетиков"]
            },
            "form": {
                "physical_forms": ["порошок", "гранулы", "микрогранулы"],
                "colors": ["белый", "кремовый", "слегка_желтоватый"]
            },
            "producer": {
                "companies": ["зеленые_линии", "натурпродукт"],
                "countries": ["россия"]
            },
            "application_areas": {
                "replacement_ratios": ["1кг_заменяет_100кг", "1кг_заменяет_200кг", "1кг_заменяет_300кг"],
                "sweetener_components": ["е954", "е950", "е951", "е955"],
                "synergy": ["ацесульфам_аспартам", "сахарин_цикламат"]
            },
            "advantages": {
                "taste_profile": ["максимально_близко_к_сахару", "без_горечи", "чистый_сладкий"],
                "technological": ["термостабильность", "растворимость", "совместимость"],
                "health_benefits": ["безопасность", "низкая_калорийность", "не_влияет_на_зубы"]
            }
        }
    },

    "stabilizers_compounds.json": {
        "stabilizer_compounds": {
            "name": {
                "product_types": ["стабилизатор", "компаунд", "комплексная_добавка", "эмульгатор"],
                "brands": ["гелеон", "стабилекс", "эмулстаб"],
                "product_numbers": ["102с", "117с", "124м", "140ст", "205к"],
                "functionality": ["для_кетчупа", "для_майонеза", "для_соусов", "универсальный"]
            },
            "producer": {
                "companies": ["зеленые_линии", "гелеон_технологии"],
                "countries": ["россия"]
            },
            "application_areas": {
                "product_categories": ["майонезы", "кетчупы", "соусы", "горчица", "хрен"],
                "dosage_ranges": ["0.01_0.5", "0.5_1.5", "1.0_3.0"],
                "production_methods": ["холодный_способ", "горячий_способ", "универсальный"],
                "working_temperatures": ["0_110", "85_110", "60_95", "комнатная"]
            },
            "advantages": {
                "functional_properties": ["загущение", "стабилизация", "эмульгирование", "гелеобразование"],
                "quality_improvements": ["однородность", "стабильность", "консистенция", "срок_хранения"],
                "processing_benefits": ["простота_применения", "универсальность", "экономичность"],
                "special_properties": ["морозостойкость", "термостабильность", "ph_стабильность"]
            },
            "properties": {
                "main_functions": ["загуститель", "стабилизатор", "эмульгатор", "структурообразователь"],
                "hydrocolloids": ["каррагинан", "ксантан", "гуар", "агар"],
                "composition": ["гидроколлоиды", "эмульгаторы", "белки", "крахмалы"]
            },
            "scope_of_application": {
                "end_products": ["майонез", "кетчуп", "соусы", "дрессинги", "пасты"],
                "processing_compatibility": ["низкий_ph", "высокий_ph", "нейтральный_ph"],
                "shelf_stability": ["краткосрочная", "длительная", "интенсивная"]
            }
        }
    }
}


def get_fat_and_oil_enum_values_for_file_key(file_name: str, key_name: str) -> Dict[str, List[str]]:
    """
    Возвращает enum значения для конкретного ключа в конкретном файле.
    
    Args:
        file_name: Имя файла (например, "antioxidants.json")
        key_name: Имя ключа (например, "name", "form")
        
    Returns:
        Словарь с enum категориями и значениями для данного ключа
    """
    file_data = FAT_AND_OIL_ENUM_MAPPING.get(file_name, {})
    
    # Ищем в субключах (новый формат с субключами)
    for subkey_data in file_data.values():
        if isinstance(subkey_data, dict) and key_name in subkey_data:
            return subkey_data[key_name]
    
    return {}


def get_all_fat_and_oil_enums_for_file(file_name: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Возвращает все enum значения для всех ключей конкретного файла.
    
    Args:
        file_name: Имя файла (например, "antioxidants.json")
        
    Returns:
        Полный словарь с enum'ами для всех ключей файла
    """
    return FAT_AND_OIL_ENUM_MAPPING.get(file_name, {})


# Экспорт для универсального загрузчика
enum_mapping = FAT_AND_OIL_ENUM_MAPPING


if __name__ == "__main__":
    # Пример использования
    import json
    
    print("=== ENUM'Ы ДЛЯ КЛЮЧА 'name' В ФАЙЛЕ АНТИОКСИДАНТОВ ===")
    name_enums = get_fat_and_oil_enum_values_for_file_key("antioxidants.json", "name")
    print(json.dumps(name_enums, indent=2, ensure_ascii=False))
    
    print("\n=== ВСЕ ENUM'Ы ДЛЯ ФАЙЛА КРАСИТЕЛЕЙ (ЖИРОРАСТВОРИМЫЕ) ===")
    color_enums = get_all_fat_and_oil_enums_for_file("food_colors.json")
    print(json.dumps(color_enums, indent=2, ensure_ascii=False))