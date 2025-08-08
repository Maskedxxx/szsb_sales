"""
Маппинг ключей продуктов для каждого JSON файла молочной отрасли.

Этот файл содержит полный анализ структуры данных всех файлов молочной отрасли
и описания ключей для создания динамических tool схем.
"""

import json
from typing import Dict, List, Any

# Маппинг ключей продуктов для каждого файла молочной отрасли
MILK_KEYS_MAPPING = {
    "milk_protein.json": {
        "file_description": "Молочнобелковые концентраты для получения натуральных молочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название молочнобелкового концентрата или комплексной пищевой добавки",
                "filter_impact": "Позволяет искать по типу концентрата (молочный белок, комплексная добавка) и процентному содержанию белка",
                "data_type": "string",
                "examples": ["КОМПЛЕКСНАЯ ПИЩЕВАЯ ДОБАВКА 112 С-С ГЕЛЕОН", "КОНЦЕНТРАТ МОЛОЧНОГО БЕЛКА 75 ZL"]
            },
            "properties": {
                "description": "Свойства и состав концентрата",
                "filter_impact": "Позволяет фильтровать по основным компонентам (концентрат молочного белка, сывороточного белка, обезжиренное молоко)",
                "data_type": "string",
                "examples": ["Концентрат молочного белка, концентрат сывороточного белка", "Пастеризованное обезжиренное молоко"]
            },
            "characteristics": {
                "description": "Технические характеристики и дозировка",
                "filter_impact": "Позволяет фильтровать по массовой доле белка, жира, лактозы и рекомендуемой дозировке",
                "data_type": "string",
                "examples": ["Массовая доля белка не менее 74,0\\nКазеиновый белок не менее 45,0"]
            }
        }
    },

    "starter_cultures.json": {
        "file_description": "Лиофилизированные культуры прямого внесения Golden Line® для производства кисломолочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название заквасочной культуры",
                "filter_impact": "Позволяет искать по линейке продуктов (PROFILINE, GOLDEN TIME, SMARTLINE), типу культуры (YO, RZ, KE, CC) и бренду",
                "data_type": "string",
                "examples": ["КУЛЬТУРА БАКТЕРИАЛЬНАЯ КОНЦЕНТРИРОВАННАЯ ЗАКВАСОЧНАЯ PROFILINE® YO 22.50 LOW GOLDEN LINE®"]
            },
            "packaging": {
                "description": "Размер упаковки заквасочной культуры",
                "filter_impact": "Позволяет фильтровать по размеру упаковки (50, 250, 150 единиц)",
                "data_type": "string",
                "examples": ["50", "250", "50, 250", "150"]
            }
        }
    },

    "dyes.json": {
        "file_description": "Натуральные и синтетические красители для окрашивания молочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название красителя или комплексной пищевой добавки",
                "filter_impact": "Позволяет искать по типу красителя (бета-каротин, кармин, куркумин), бренду (ESCO) и форме (жидкий, порошок)",
                "data_type": "string",
                "examples": ["КОМПЛЕКСНАЯ ПИЩЕВАЯ ДОБАВКА «КРАСИТЕЛЬ БЕТА-КАРОТИН 0,3% В РАСТИТЕЛЬНОМ МАСЛЕ»"]
            },
            "dosage": {
                "description": "Рекомендуемая дозировка применения красителя",
                "filter_impact": "Позволяет фильтровать по уровню дозировки (низкая, средняя, высокая) и единицам измерения",
                "data_type": "string",
                "examples": ["0.02-0.08\\n0,2-2,0%", "0,2-0,5 кг/т", "5-30 мг/кг"]
            },
            "color": {
                "description": "Получаемый цвет при использовании красителя",
                "filter_impact": "Позволяет фильтровать по цветовой гамме (желтый, красный, коричневый, зеленый) и оттенкам",
                "data_type": "string",
                "examples": ["Оттенки желтого", "Яркий красный", "Цвет спелой вишни"]
            }
        }
    },

    "fruit_fillings.json": {
        "file_description": "Термостабильные фруктовые наполнители Denfruit® для молочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название фруктового наполнителя с указанием вкуса и консистенции",
                "filter_impact": "Позволяет искать по типу фрукта/ягоды (черника, вишня, клубника, абрикос, ананас), консистенции (с ягодой, с кусочками, с цедрой) и номеру рецептуры",
                "data_type": "string",
                "examples": ["Черничная N 755.00 (с ягодой)", "Абрикосовая N 702.00 (с кусочками)", "Денкрим со вкусом Ванили Т"]
            },
            "characteristics": {
                "description": "Технические характеристики наполнителя (сухие вещества и pH)",
                "filter_impact": "Позволяет фильтровать по массовой доле сухих веществ (68±2%) и кислотности (pH 3,6-4,2)",
                "data_type": "string",
                "examples": ["Массовая доля сухих веществ: 68±2 %. pH: 3,6-4,2"]
            }
        }
    },

    "vegetable_fillings.json": {
        "file_description": "Овощные наполнители и начинки для молочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название овощного наполнителя",
                "filter_impact": "Позволяет искать по типу овоща, консистенции и назначению продукта",
                "data_type": "string",
                "examples": ["Грибы белые", "Грибы с розмарином", "Итальянский с травами"]
            },
            "application_areas": {
                "description": "Области применения овощного наполнителя в молочных продуктах",
                "filter_impact": "Позволяет фильтровать по типу конечного продукта (кисломолочные напитки, сыры, творожные изделия)",
                "data_type": "array",
                "examples": ["кисломолочные напитки, молочные коктейли", "сыры плавленые", "творожные изделия"]
            }
        }
    },

    "confectionery_glaze.json": {
        "file_description": "Кондитерские глазури и покрытия «КЛАССИКА» на основе заменителей какао-масла лауринового типа",
        "product_keys": {
            "name": {
                "description": "Название кондитерской массы, глазури или шоколада",
                "filter_impact": "Позволяет искать по типу продукта (масса, глазурь, шоколад), цвету (темная, молочная, белая) и номеру рецептуры",
                "data_type": "string",
                "examples": ["МАССА КОНДИТЕРСКАЯ «042 ТЕМНАЯ» «КЛАССИКА»", "ГЛАЗУРЬ КОНДИТЕРСКАЯ «145» «КЛАССИКА»", "ШОКОЛАД БЕЛЫЙ 735 «КЛАССИКА»"]
            },
            "color": {
                "description": "Цвет кондитерской массы или глазури",
                "filter_impact": "Позволяет фильтровать по цвету (коричневый, светло-коричневый, белый)",
                "data_type": "string",
                "examples": ["Коричневый", "Светло-коричневый", "Белый"]
            },
            "characteristics": {
                "description": "Технические характеристики продукта (вязкость и дисперсность)",  
                "filter_impact": "Позволяет фильтровать по вязкости (Па*с) и дисперсности (процент)",
                "data_type": "string",
                "examples": ["Вязкость: 3,6-4,8 Па*с\\nДисперсность: не менее 93,5%", "Вязкость: 6,0-7,0 Па*с\\nДисперсность: не менее 93,5%"]
            }
        }
    },

    "cocoa_powder.json": {
        "file_description": "Какао порошки от ведущих мировых производителей для молочных продуктов и напитков",
        "product_keys": {
            "name": {
                "description": "Название какао порошка с указанием типа и бренда",
                "filter_impact": "Позволяет искать по типу какао (алкализованный, натуральный), бренду (TULIP, GOLDEN HARVEST, ДЕНКАКАО) и номеру продукта",
                "data_type": "string",
                "examples": ["Какао-порошок алкализованный TULIP 400", "КАКАО-ПОРОШОК НАТУРАЛЬНЫЙ «GOLDEN HARVEST»"]
            },
            "color": {
                "description": "Цвет какао порошка",
                "filter_impact": "Позволяет фильтровать по цветовой характеристике какао продукции",
                "data_type": "string",
                "examples": ["Коричневый"]
            },
            "composition": {
                "description": "Состав и тип обработки какао порошка",
                "filter_impact": "Позволяет фильтровать по методу обработки (алкализованный или натуральный)",
                "data_type": "string",
                "examples": ["Какао-порошок алкализованный", "Какао-порошок натуральный"]
            }
        }
    },

    "phosphates.json": {
        "file_description": "Соли-плавители Денфос® для производства плавленых сыров от Aditya Birla Chemicals",
        "product_keys": {
            "name": {
                "description": "Название комплексной пищевой добавки на основе фосфатов",
                "filter_impact": "Позволяет искать по номеру рецептуры (120, 2070, 12 РІ, 76 SL, 85), бренду (ДЕНФОС, ДЕНФОСФАТ) и назначению",
                "data_type": "string",
                "examples": ["КОМПЛЕКСНАЯ ПИЩЕВАЯ ДОБАВКА 120 ДЕНФОС", "КОМПЛЕКСНАЯ ПИЩЕВАЯ ДОБАВКА 2070 ДЕНФОСФАТ"]
            },
            "dosage": {
                "description": "Рекомендуемая дозировка применения фосфатов",
                "filter_impact": "Позволяет фильтровать по процентному содержанию (0,1-2,0%) и области применения (плавленые сыры, моцарелла)",
                "data_type": "string",
                "examples": ["1,1-1,5% для пастообразных плавленых сыров.\\n1,5-2,0% для ломтевых плавленых сыров", "1,0-1,4% для моцареллы для пиццы"]
            },
            "description": {
                "description": "Подробное описание свойств и эффектов фосфата",
                "filter_impact": "Позволяет фильтровать по функциональным свойствам (кремовый эффект, эмульгирующие свойства, стабилизация pH)",
                "data_type": "string",
                "examples": ["Имеет высокий кремовый эффект и формирует гомогенную эмульсию с короткой однородной структурой"]
            }
        }
    },

    "preservatives_antioxidants.json": {
        "file_description": "Консерванты, антиоксиданты и эмульгирующие соли для продления срока хранения молочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название консерванта, кислоты или комплексной добавки",
                "filter_impact": "Позволяет искать по типу вещества (глюкоза ферментированная, кислоты, соли), бренду (AIBI, DEL'AR) и происхождению (натуральный, синтетический)",
                "data_type": "string",
                "examples": ["ГЛЮКОЗА ФЕРМЕНТИРОВАННАЯ «1.50» ΑΙΒΙ", "КИСЛОТА СОРБИНОВАЯ (КИТАЙ)", "КОМПЛЕКСНАЯ ПИЩЕВАЯ ДОБАВКА «LАCТOВАС» DEL'AR"]
            },
            "dosage": {
                "description": "Рекомендуемая дозировка консерванта для различных продуктов",
                "filter_impact": "Позволяет фильтровать по процентному содержанию (0,01-3,0%) и области применения (сыры, сметана, творог, сгущенное молоко)",
                "data_type": "string",
                "examples": ["Сметанный продукт, кисломолочные продукты: 0,1-0,15% после ферментации", "Сыры: 1,0; плавленые сыры: 1,0-2,0; спреды: 1,0"]
            }
        }
    },

    "multifunctional_systems.json": {
        "file_description": "Мультифункциональные системы для комплексного улучшения молочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название мультифункциональной системы ГЕЛЕОН",
                "filter_impact": "Позволяет искать по бренду (ГЕЛЕОН, ДЕНСАЙС), номеру продукта и функциональному назначению",
                "data_type": "string",
                "examples": ["КАРРАГИНАН 201 М ГЕЛЕОН", "3.01.003 ΓЕЛЕОН", "СТАБИЛИЗАТОР 110 С ГЕЛЕОН"]
            },
            "intended_use": {
                "description": "Функциональное назначение системы",
                "filter_impact": "Позволяет фильтровать по основной функции (стабилизатор, загуститель, структурообразователь)",
                "data_type": "string",
                "examples": ["Структурообразователь", "Стабилизатор", "Загуститель"]
            },
            "dosage": {
                "description": "Рекомендуемая дозировка для различных молочных продуктов",
                "filter_impact": "Позволяет фильтровать по диапазону дозировки и типу продукта",
                "data_type": "string",
                "examples": ["Плавленые сыры: 0,25-0,4. Сгущенный молочный продукт: 0,05-0,2", "Йогурт: 1,8-2,0"]
            },
            "composition": {
                "description": "Состав мультифункциональной системы",
                "filter_impact": "Позволяет искать по основным компонентам (стабилизаторы, загустители, желатин, крахмал)",
                "data_type": "string",
                "examples": ["Стабилизаторы (Е407а), декстроза, желирующий агент (Е508)", "Желатин говяжий пищевой, концентрат молочного белка"]
            }
        }
    },

    "delar_flavor_collection.json": {
        "file_description": "Коллекция ароматизаторов DEL'AR для молочных продуктов",
        "product_keys": {
            "name": {
                "description": "Название ароматизатора DEL'AR",
                "filter_impact": "Позволяет искать по типу аромата (фруктовый, ванильный, шоколадный, мясной), интенсивности и бренду DEL'AR",
                "data_type": "string",
                "examples": ["Натуральный Базилик (11.01.461 Η)", "Ветчина (10.06.163)", "Абрикос (10.04.120 Ин)"]
            },
            "flavor_profile": {
                "description": "Профиль вкуса и аромата",
                "filter_impact": "Позволяет фильтровать по характеристикам вкуса (интенсивность, вкусовые ноты, профиль)",
                "data_type": "string",
                "examples": ["Свежая трава базилика", "Мясной, легкая нота копчености", "Натуральный фруктовый"]
            },
            "application_areas": {
                "description": "Области применения ароматизатора в молочной продукции",
                "filter_impact": "Позволяет фильтровать по типу конечного продукта (плавленные сыры, молочные десерты, напитки)",
                "data_type": "array",
                "examples": ["плавленные сыры", "молочные десерты, пудинги, кремы", "молочные напитки"]
            }
        }
    }
}

# Маппинг selected_key к файлам для сложных структур молочной отрасли
KEY_TO_FILE_MAPPING = {
    # delar_flavor_collection.json
    "aromatic_emulsions": "delar_flavor_collection.json",
    "flavor_bases": "delar_flavor_collection.json", 
    "gastronomic_flavors": "delar_flavor_collection.json",
    "juice_containing_flavors": "delar_flavor_collection.json",
    "spread_flavorings": "delar_flavor_collection.json",
    "sweet_flavors": "delar_flavor_collection.json",
    
    # fruit_fillings.json
    "nonthermostable_homogeneous_fillings": "fruit_fillings.json",
    "thermostable_homogeneous_fillings": "fruit_fillings.json",
    
    # starter_cultures.json
    "probiotic_cultures": "starter_cultures.json",
    "protective_cultures": "starter_cultures.json", 
    "thermophilic_starter_cultures": "starter_cultures.json",
    "mesophilic_starter_cultures": "starter_cultures.json",
    "yogurt_starter_cultures": "starter_cultures.json",
    "kefir_starter_cultures": "starter_cultures.json",
    "sour_cream_starter_cultures": "starter_cultures.json",
    "cheese_starter_cultures": "starter_cultures.json",
    
    # vegetable_fillings.json  
    "nonthermostable_homogeneous_vegetable_fillings": "vegetable_fillings.json",
    "thermostable_homogeneous_vegetable_fillings": "vegetable_fillings.json",
    
    # Остальные файлы с прямым соответствием
    "milk_protein": "milk_protein.json",
    "multifunctional_systems": "multifunctional_systems.json",
    "cocoa_powder": "cocoa_powder.json",
    "confectionery_glaze": "confectionery_glaze.json",
    "dyes": "dyes.json",
    "phosphates": "phosphates.json",
    "preservatives_antioxidants_emulsifying_salts": "preservatives_antioxidants.json"
}


def get_milk_file_specific_keys(file_name: str) -> Dict[str, Any]:
    """
    Возвращает специфичные ключи для конкретного файла молочной отрасли.
    
    Args:
        file_name: Имя файла (например, "milk_protein.json")
        
    Returns:
        Словарь с ключами и их описаниями для файла
    """
    return MILK_KEYS_MAPPING.get(file_name, {})


if __name__ == "__main__":
    # Пример использования
    print("=== ПРИМЕР СПЕЦИФИЧНЫХ КЛЮЧЕЙ ДЛЯ МОЛОЧНЫХ БЕЛКОВ ===")
    protein_keys = get_milk_file_specific_keys("milk_protein.json")
    print(json.dumps(protein_keys, indent=2, ensure_ascii=False))