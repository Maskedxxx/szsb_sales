"""
Маппинг ключей продуктов для каждого JSON файла отрасли напитков (drinks).

Этот файл содержит полный анализ структуры данных всех файлов отрасли напитков
и описания ключей для создания динамических tool схем.
"""

import json
from typing import Dict, Any

# Маппинг ключей продуктов для каждого файла отрасли напитков
DRINKS_KEYS_MAPPING = {
    "colorant_data.json": {
        "file_description": "Красители ESCO® для напитков (натуральные, синтетические порошковые и жидкие)",
        "product_keys": {
            "name_product": {
                "description": "Название красителя или комплексной пищевой добавки",
                "filter_impact": "Позволяет искать по типу красителя (сахарный колер, тартразин, кармуазин), бренду ESCO® и форме (порошок, жидкий)",
                "data_type": "string",
                "examples": ["КРАСИТЕЛЬ «САХАРНЫЙ КОЛЕР» Е150D", "КРАСИТЕЛЬ «ЗЕЛЕНОЕ ЯБЛОКО Е102, Е133» (ПОРОШОК)"]
            },
            "composition": {
                "description": "Состав красителя с указанием E-кодов и вспомогательных веществ",
                "filter_impact": "Позволяет фильтровать по E-кодам красителей (E102, E122, E124, E133, E150D) и составу",
                "data_type": "string",
                "examples": ["Краситель сахарный колер IV", "Красители Е102, E133"]
            },
            "dosage": {
                "description": "Рекомендуемая дозировка применения красителя",
                "filter_impact": "Позволяет фильтровать по уровню дозировки и единицам измерения (кг/т, кг/1000 л)",
                "data_type": "string",
                "examples": ["0,01-3,0 кг/т", "10-30 кг/т", "0,05-0,15 кг/т"]
            },
            "color": {
                "description": "Получаемый цвет готового продукта при использовании красителя",
                "filter_impact": "Позволяет фильтровать по цветовой гамме напитков (зеленый, малиновый, темно-коричневый, синий)",
                "data_type": "string",
                "examples": ["Темно-коричневый", "Зеленый", "Малиновый", "Синий"]
            }
        }
    },

    "flavor_data.json": {
        "file_description": "Коллекция ароматизаторов DEL'AR для напитков (натуральные, цитрусовые, фруктовые, алкогольные)",
        "product_keys": {
            "name_product": {
                "description": "Название ароматизатора DEL'AR с указанием типа и кода продукта",
                "filter_impact": "Позволяет искать по типу аромата (фруктовый, цитрусовый, натуральный), вкусовому профилю и бренду DEL'AR",
                "data_type": "string",
                "examples": ["НАТУРАЛЬНЫЙ ТИП АБРИКОС", "КОЛА (НАТУРАЛЬНЫЙ)", "МОХИТО (НАТУРАЛЬНЫЙ)"]
            },
            "product_code": {
                "description": "Уникальный код продукта DEL'AR для идентификации ароматизатора",
                "filter_impact": "Позволяет точно идентифицировать конкретный ароматизатор по внутреннему коду производителя",
                "data_type": "string",
                "examples": ["11.01.365", "11.04.113", "11.02.206 P"]
            },
            "property": {
                "description": "Специальные свойства продукта или дополнительные характеристики",
                "filter_impact": "Позволяет фильтровать по специальным характеристикам и функциональным свойствам",
                "data_type": "string",
                "examples": ["эти продукты имеют замутнитель жидкостей", "термостабильный", "концентрированный"]
            }
        }
    },

    "sweeteners_data.json": {
        "file_description": "Подсластители SLADIN® комбинированные (без аспартама, с аспартамом, премиум линейка)",
        "product_keys": {
            "name_product": {
                "description": "Название комбинированного подсластителя SLADIN® с указанием коэффициента сладости",
                "filter_impact": "Позволяет искать по коэффициенту сладости (50, 130, 200, 240, 250), наличию аспартама и типу (премиум, стандарт)",
                "data_type": "string",
                "examples": ["ПОДСЛАСТИТЕЛЬ КОМБИНИРОВАННЫЙ 50 S", "ПОДСЛАСТИТЕЛЬ КОМБИНИРОВАННЫЙ 200 A"]
            },
            "sweetness_coefficient": {
                "description": "Коэффициент сладости относительно сахара или эквивалентность по вкусу",
                "filter_impact": "Позволяет фильтровать по уровню сладости и экономичности применения подсластителя",
                "data_type": "string",
                "examples": ["50", "200", "250", "18", "2,5"]
            },
            "composition": {
                "description": "Состав подсластителя с указанием E-кодов компонентов",
                "filter_impact": "Позволяет фильтровать по типу подсластителей (с аспартамом E951, цикламат E952, сахарин E954) и наличию фенилаланина",
                "data_type": "string",
                "examples": ["Подсластители (Е952, Е950)", "Подсластители (Е950, Е951, Е952, Е954). Содержит источник фенилаланина"]
            }
        }
    },

    "juce_recipes.json": {
        "file_description": "Рецепты безалкогольных соковых напитков (тропические, яблочно-грушевые, лесные ягоды, цитрусовые)",
        "product_keys": {
            "recipe_name": {
                "description": "Полное название рецепта напитка с указанием содержания сока",
                "filter_impact": "Позволяет искать по типу напитка (негазированный/газированный), вкусовому профилю и содержанию сока (2,5%, 5%, 30%)",
                "data_type": "string",
                "examples": ["Напиток безалкогольный негазированный «Манго-маракуйя», 2,5% сока", "Напиток безалкогольный газированный «С ароматом апельсина», сок 3,5%"]
            },
            "variants": {
                "description": "Варианты рецепта (на сахаре vs на подсластителе) с технологическими параметрами",
                "filter_impact": "Позволяет фильтровать по способу подслащивания, калорийности и содержанию углеводов",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на Сладин 200 А"]
            },
            "composition": {
                "description": "Состав рецептуры (ингредиенты и добавки с возможными дозировками)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["сахар", "лимонная кислота", "ароматизатор", "краситель"]
            },
            "process_stages": {
                "description": "Технологические этапы производства напитка (сироп и финальный напиток)",
                "filter_impact": "Позволяет искать по технологии производства и составу ингредиентов",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "club_recipes.json": {
        "file_description": "Рецепты безалкогольных клубных коктейлей (мохито, сангрия, пунш, глинтвейн, пина колада)",
        "product_keys": {
            "recipe_name": {
                "description": "Название клубного коктейля или напитка с указанием типа",
                "filter_impact": "Позволяет искать по категории напитка (мохито, сангрия, пунш) и вкусовому профилю (лимон-лайм, клубника, гранат)",
                "data_type": "string",
                "examples": ["Напиток безалкогольный «Мохито с ароматом лимон-лайма»", "Напиток безалкогольный газированный «Сангрия белая»"]
            },
            "variants": {
                "description": "Варианты приготовления коктейля с различным составом подслащивающих веществ",
                "filter_impact": "Позволяет фильтровать по энергетической ценности и способу подслащивания",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на подсластителе Сладин 200"]
            },
            "composition": {
                "description": "Состав рецептуры (ингредиенты и добавки с возможными дозировками)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["сахар", "лимонная кислота", "ароматизатор", "краситель"]
            },
            "process_stages": {
                "description": "Стадии производства клубного напитка включая газацию",
                "filter_impact": "Позволяет искать по технологическим особенностям и составу ароматизаторов",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "energy_recipes.json": {
        "file_description": "Рецепты безалкогольных газированных энергетических напитков (цитрусовые и фруктовые)",
        "product_keys": {
            "recipe_name": {
                "description": "Название энергетического напитка с указанием вкусового профиля",
                "filter_impact": "Позволяет искать по типу энергетика (цитрусовая бомба, bitter lemon, тропический манго) и функциональным добавкам",
                "data_type": "string",
                "examples": ["Напиток безалкогольный газированный энергетический «Цитрусовая бомба»", "НАПИТОК безалкогольный газированный энергетический Bitter Lemon"]
            },
            "variants": {
                "description": "Варианты энергетического напитка по составу подсластителей",
                "filter_impact": "Позволяет фильтровать по калорийности и содержанию энергетических компонентов",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на интенсивном подсластителе"]
            },
            "composition": {
                "description": "Состав рецептуры (ингредиенты и добавки с возможными дозировками)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["женьшень", "L-карнитин", "кофеин", "ароматизатор"]
            },
            "process_stages": {
                "description": "Технологические стадии производства энергетического напитка",
                "filter_impact": "Позволяет искать по составу энергетических добавок (женьшень, L-карнитин) и ароматизаторов",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "cold_tea_recipes.json": {
        "file_description": "Рецепты холодных чайных напитков (черный чай и зеленый чай)",
        "product_keys": {
            "recipe_name": {
                "description": "Название чайного напитка с указанием типа чая и вкусовых добавок",
                "filter_impact": "Позволяет искать по типу чая (черный, зеленый) и вкусовым характеристикам",
                "data_type": "string",
                "examples": ["Напиток чайный холодный черный", "Напиток чайный холодный зеленый"]
            },
            "variants": {
                "description": "Варианты чайного напитка с разными способами подслащивания",
                "filter_impact": "Позволяет фильтровать по калорийности и содержанию сахара",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на подсластителе"]
            },
            "composition": {
                "description": "Состав рецептуры (чайные экстракты, кислоты, ароматизаторы и др.)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["экстракт чая", "лимонная кислота", "ароматизатор"]
            },
            "process_stages": {
                "description": "Этапы производства холодного чая включая заваривание и охлаждение",
                "filter_impact": "Позволяет искать по технологии заваривания и составу чайной основы",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "drink_snaps_recipes.json": {
        "file_description": "Рецепты снап-напитков (ягодные, ванильно-карамельные, фруктовые)",
        "product_keys": {
            "recipe_name": {
                "description": "Название снап-напитка с указанием вкусовой категории",
                "filter_impact": "Позволяет искать по типу снап-напитка и основному вкусовому профилю",
                "data_type": "string",
                "examples": ["Снап-напиток ягодный", "Снап-напиток ванильно-карамельный"]
            },
            "variants": {
                "description": "Варианты снап-напитка с различными подсластителями",
                "filter_impact": "Позволяет фильтровать по энергетической ценности и способу подслащивания",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на подсластителе"]
            },
            "composition": {
                "description": "Состав рецептуры (ингредиенты и добавки с возможными дозировками)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["сахар", "лимонная кислота", "ароматизатор", "краситель"]
            },
            "process_stages": {
                "description": "Стадии производства снап-напитка с особой технологией",
                "filter_impact": "Позволяет искать по специфичной технологии снап-напитков и составу",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "jelly_recipes.json": {
        "file_description": "Рецепты желе-напитков (ягодные, с алоэ и кактусом, цитрусово-травяные)",
        "product_keys": {
            "recipe_name": {
                "description": "Название желе-напитка с указанием основных ингредиентов",
                "filter_impact": "Позволяет искать по типу желе-напитка и функциональным добавкам (алоэ, кактус)",
                "data_type": "string",
                "examples": ["Желе-напиток ягодный", "Желе-напиток с алоэ и кактусом"]
            },
            "variants": {
                "description": "Варианты желе-напитка по составу подслащивающих веществ",
                "filter_impact": "Позволяет фильтровать по калорийности и гелеобразующим свойствам",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на подсластителе"]
            },
            "composition": {
                "description": "Состав рецептуры (ингредиенты и добавки с возможными дозировками)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["сахар", "лимонная кислота", "ароматизатор", "загуститель"]
            },
            "process_stages": {
                "description": "Технологические этапы производства желе-напитка с желирующими агентами",
                "filter_impact": "Позволяет искать по составу желирующих компонентов и технологии гелеобразования",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "kvas_gost_recipes.json": {
        "file_description": "Рецепты кваса по ГОСТ (со специями, яблочный, традиционный, свекольно-ягодный)",
        "product_keys": {
            "recipe_name": {
                "description": "Название кваса с указанием типа и соответствия ГОСТ",
                "filter_impact": "Позволяет искать по типу кваса (традиционный, яблочный, со специями) и соответствию стандартам ГОСТ",
                "data_type": "string",
                "examples": ["Квас традиционный ГОСТ", "Квас яблочный ГОСТ", "Квас со специями"]
            },
            "variants": {
                "description": "Варианты кваса с различными способами брожения и подслащивания",
                "filter_impact": "Позволяет фильтровать по технологии брожения и составу закваски",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на подсластителе"]
            },
            "composition": {
                "description": "Состав рецептуры (ингредиенты и добавки с возможными дозировками)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["солод", "сахар", "закваска", "пряности"]
            },
            "process_stages": {
                "description": "Стадии производства кваса включая брожение и созревание",
                "filter_impact": "Позволяет искать по технологии брожения, составу закваски и времени выдержки",
                "data_type": "object",
                "examples": ["syrup_preparation", "intermediate_stage", "final_drink_preparation"]
            }
        }
    },

    "malt_recipes.json": {
        "file_description": "Рецепты солодовых напитков (с охлаждающим эффектом, ягодные, травяные)",
        "product_keys": {
            "recipe_name": {
                "description": "Название солодового напитка с указанием дополнительных эффектов",
                "filter_impact": "Позволяет искать по типу солодового напитка и функциональным эффектам (охлаждающий, согревающий)",
                "data_type": "string",
                "examples": ["Солодовый напиток с охлаждающим эффектом", "Солодовый напиток ягодный"]
            },
            "variants": {
                "description": "Варианты солодового напитка по составу подсластителей",
                "filter_impact": "Позволяет фильтровать по калорийности и содержанию солодовых экстрактов",
                "data_type": "array",
                "examples": ["Вариант 1 – на сахаре", "Вариант 2 – на подсластителе"]
            },
            "process_stages": {
                "description": "Этапы производства солодового напитка с солодовыми экстрактами",
                "filter_impact": "Позволяет искать по составу солодовых компонентов и технологии экстракции",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "retro_recipes.json": {
        "file_description": "Рецепты ретро напитков (тархун, дюшес, лимонады)",
        "product_keys": {
            "recipe_name": {
                "description": "Название ретро напитка с классическими вкусовыми характеристиками",
                "filter_impact": "Позволяет искать по типу ретро напитка (тархун, дюшес, лимонад) и традиционным рецептурам",
                "data_type": "string",
                "examples": ["Тархун классический", "Дюшес ретро", "Лимонад советский"]
            },
            "variants": {
                "description": "Варианты ретро напитка с современными и традиционными составами",
                "filter_impact": "Позволяет фильтровать по аутентичности рецептуры и способу подслащивания",
                "data_type": "array",
                "examples": ["Вариант 1 – традиционный", "Вариант 2 – современная формула"]
            },
            "process_stages": {
                "description": "Стадии производства ретро напитка с сохранением классической технологии",
                "filter_impact": "Позволяет искать по традиционным технологиям и составу натуральных ароматизаторов",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "vegetable_extract_recipes.json": {
        "file_description": "Рецепты напитков с растительными экстрактами (алгоритмические, травяные, ягодные)",
        "product_keys": {
            "recipe_name": {
                "description": "Название напитка с растительными экстрактами и функциональными добавками",
                "filter_impact": "Позволяет искать по типу растительных экстрактов и функциональному назначению напитка",
                "data_type": "string",
                "examples": ["Напиток с экстрактом алоэ", "Напиток травяной функциональный"]
            },
            "variants": {
                "description": "Варианты напитка с различной концентрацией растительных экстрактов",
                "filter_impact": "Позволяет фильтровать по концентрации активных веществ и способу подслащивания",
                "data_type": "array",
                "examples": ["Вариант 1 – стандартная концентрация", "Вариант 2 – усиленная формула"]
            },
            "composition": {
                "description": "Состав рецептуры (ингредиенты и добавки с возможными дозировками)",
                "filter_impact": "Позволяет фильтровать/искать по ингредиентам и компонентам рецептуры",
                "data_type": "object",
                "examples": ["экстракты трав", "экстракты ягод", "кислоты", "ароматизаторы"]
            },
            "process_stages": {
                "description": "Этапы производства с экстракцией растительных компонентов",
                "filter_impact": "Позволяет искать по технологии экстракции и составу функциональных добавок",
                "data_type": "object",
                "examples": ["syrup_preparation", "final_drink_preparation"]
            }
        }
    },

    "mixture_data.json": {
        "file_description": "Смеси и концентраты для напитков (квасные смеси, напиточные смеси)",
        "product_keys": {
            "name_product": {
                "description": "Название готовой смеси или концентрата для приготовления напитков",
                "filter_impact": "Позволяет искать по типу смеси (квасная, напиточная) и назначению концентрата",
                "data_type": "string",
                "examples": ["КВАС", "Смесь для лимонада", "Концентрат напитка"]
            },
            "composition": {
                "description": "Состав смеси с указанием основных компонентов",
                "filter_impact": "Позволяет фильтровать по составу ингредиентов и типу смеси",
                "data_type": "string",
                "examples": ["Мальтозная основа, дрожжи", "Сахар, лимонная кислота, ароматизатор"]
            },
            "dosage": {
                "description": "Рекомендуемая дозировка применения смеси для получения готового напитка",
                "filter_impact": "Позволяет фильтровать по норме расхода и концентрации смеси",
                "data_type": "string",
                "examples": ["50 кг/т", "20-30 кг/1000 л"]
            }
        }
    },

    "various_data.json": {
        "file_description": "Различные добавки для напитков (консерванты, кислоты, функциональные добавки)",
        "product_keys": {
            "name_product": {
                "description": "Название пищевой добавки или вспомогательного вещества для производства напитков",
                "filter_impact": "Позволяет искать по типу добавки (консервант, кислота, стабилизатор) и функциональному назначению",
                "data_type": "string",
                "examples": ["КИСЛОТА ЛИМОННАЯ", "НАТРИЯ БЕНЗОАТ", "СТАБИЛИЗАТОР"]
            },
            "composition": {
                "description": "Состав пищевой добавки с указанием основных компонентов",
                "filter_impact": "Позволяет фильтровать по составу ингредиентов и активным веществам",
                "data_type": "string",
                "examples": ["Мальтодекстрин, красители", "Пребиотик олигофруктоза", "Лимонная кислота моногидрат"]
            },
            "has_E_code": {
                "description": "Наличие и указание E-кода пищевой добавки согласно европейской классификации",
                "filter_impact": "Позволяет фильтровать по E-кодам добавок и их безопасности для применения",
                "data_type": "string",
                "examples": ["E330", "E211", "E202"]
            },
            "dosage": {
                "description": "Рекомендуемая дозировка применения добавки в производстве напитков",
                "filter_impact": "Позволяет фильтровать по норме внесения и области применения добавки",
                "data_type": "string",
                "examples": ["1,0-3,0 кг/т", "0,1-0,2%", "По потребности"]
            }
        }
    }
}

# Маппинг selected_key к файлам для субключей отрасли напитков
KEY_TO_FILE_MAPPING = {
    # colorant_data.json субключи
    "natural_colorants": "colorant_data.json",
    "synthetic_powder_colorants": "colorant_data.json", 
    "synthetic_liquid_colorants": "colorant_data.json",
    
    # flavor_data.json субключи
    "retro_classic_drink_flavors": "flavor_data.json",
    "natural": "flavor_data.json",
    "juice_bases": "flavor_data.json",
    # Добавляем реально существующие субключи
    "alcohol_flavor": "flavor_data.json",
    "choco_coffee_bakery_aroma": "flavor_data.json",
    "citrus_aroma": "flavor_data.json",
    "fruit_aroma": "flavor_data.json",
    "grape_flavor": "flavor_data.json",
    "herbal_flavor": "flavor_data.json",
    "nut_cereal_flavor": "flavor_data.json",
    "vanilla_creamy_aroma": "flavor_data.json",
    
    # sweeteners_data.json субключи
    "sweeteners_no_aspartame": "sweeteners_data.json",
    "sweeteners_with_aspartame": "sweeteners_data.json",
    "sweeteners_premium": "sweeteners_data.json",
    "sweeteners_sweetness_200": "sweeteners_data.json",
    
    # juce_recipes.json субключи
    "tropical": "juce_recipes.json",
    "apple_pear_peach": "juce_recipes.json",
    "forest_berries": "juce_recipes.json",
    "orange_drinks": "juce_recipes.json",
    "cherry_pomegranate": "juce_recipes.json",
    
    # club_recipes.json субключи
    "mojito": "club_recipes.json",
    "sangria": "club_recipes.json",
    "punch_glintwein_pinacolada": "club_recipes.json",
    "daiquiri_kruchon": "club_recipes.json",
    
    # energy_recipes.json субключи
    "citrus_energy": "energy_recipes.json",
    "fruit_energy": "energy_recipes.json",
    
    # cold_tea_recipes.json субключи
    "black_tea": "cold_tea_recipes.json",
    "green_tea": "cold_tea_recipes.json",
    
    # drink_snaps_recipes.json субключи
    "berry_snaps": "drink_snaps_recipes.json",
    "vanilla_cream_caramel": "drink_snaps_recipes.json",
    "fruit_snaps": "drink_snaps_recipes.json",
    
    # jelly_recipes.json субключи
    "berry_bird_cherry": "jelly_recipes.json",
    "berry_jelly": "jelly_recipes.json",
    "aloe_cactus_grape": "jelly_recipes.json",
    "orange_watermelon_herbs": "jelly_recipes.json",
    
    # kvas_gost_recipes.json субключи
    "with_spices": "kvas_gost_recipes.json",
    "apple": "kvas_gost_recipes.json",
    "traditional": "kvas_gost_recipes.json",
    "beet_berry": "kvas_gost_recipes.json",
    "whey": "kvas_gost_recipes.json",
    
    # malt_recipes.json субключи
    "cooling_effect": "malt_recipes.json",
    "berry_malt": "malt_recipes.json",
    "herbal_malt": "malt_recipes.json",
    
    # retro_recipes.json субключи
    "tarragon": "retro_recipes.json",
    "duchess_pear": "retro_recipes.json",
    "lemonades": "retro_recipes.json",
    "citrus_retro": "retro_recipes.json",
    # Добавляем реально существующие субключи
    "buratino_cream_soda": "retro_recipes.json",
    "cherry_feijoa_activity": "retro_recipes.json",
    "cola": "retro_recipes.json",
    "kolokolchik": "retro_recipes.json",
    "kvas_drinks": "retro_recipes.json",
    
    # vegetable_extract_recipes.json субключи
    "algorithms": "vegetable_extract_recipes.json",
    "herbal_vegetable": "vegetable_extract_recipes.json",
    "berry_vegetable": "vegetable_extract_recipes.json",
    
    # mixture_data.json субключи
    "kvass_mixtures": "mixture_data.json",
    "drink_mixtures": "mixture_data.json",
    
    # various_data.json субключи
    "preservatives_and_acids": "various_data.json",
    # Добавляем реально существующие субключи
    "ferments": "various_data.json",
    "fruit_powders": "various_data.json",
    "oxygen_cocktail": "various_data.json",
    "probiotic_cultures": "various_data.json",
    "vegetable_milk_powder": "various_data.json"
}


def get_drinks_file_specific_keys(file_name: str) -> Dict[str, Any]:
    """
    Возвращает специфичные ключи для конкретного файла отрасли напитков.
    
    Args:
        file_name: Имя файла (например, "colorant_data.json")
        
    Returns:
        Словарь с ключами и их описаниями для файла
    """
    return DRINKS_KEYS_MAPPING.get(file_name, {})


# Экспорт для универсального загрузчика
keys_mapping = DRINKS_KEYS_MAPPING


if __name__ == "__main__":
    # Пример использования
    print("=== ПРИМЕР СПЕЦИФИЧНЫХ КЛЮЧЕЙ ДЛЯ КРАСИТЕЛЕЙ ===")
    colorant_keys = get_drinks_file_specific_keys("colorant_data.json")
    print(json.dumps(colorant_keys, indent=2, ensure_ascii=False))
