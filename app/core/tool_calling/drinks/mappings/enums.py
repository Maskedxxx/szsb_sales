"""
Маппинг enum значений для каждого ключа продуктов в файлах отрасли напитков (drinks).

Этот файл содержит конкретные enum значения в новом формате с субключами,
которые LLM может выбирать для фильтрации данных в каждом JSON файле отрасли напитков.

Переписанный в формате Milk отрасли с поддержкой субключей для новой 
универсальной архитектуры Tool Calling.
"""

# Импорты не нужны для статической структуры данных

# Маппинг enum значений для ключей продуктов в каждом файле отрасли напитков (в формате с субключами)
DRINKS_ENUM_MAPPING = {
    "colorant_data.json": {
        "natural_colorants": {  # Субключ для натуральных красителей
            "name_product": {
                "colorant_types": ["краситель", "сахарный_колер", "натуральный"],
                "brands": ["ESCO"],
                "e_codes": ["E150D", "E150A"],
                "product_variants": ["LC", "HS", "SOFT", "купажный"]
            },
            "composition": {
                "composition_types": ["краситель_сахарный_колер_IV", "краситель_сахарный_колер_I_простой"],
                "chemical_types": ["сахарный_колер", "натуральный_краситель"]
            },
            "dosage": {
                "dosage_ranges": ["низкие_0.01_3.0", "средние_0.1_5.0", "сверхнизкие_0.1_0.2"],
                "dosage_units": ["кг_на_тонну"],
                "concentration_levels": ["микро_дозировка", "стандартная_дозировка", "повышенная_дозировка"]
            },
            "color": {
                "color_families": ["коричневый"],
                "color_shades": ["темно_коричневый"],
                "color_intensity": ["темный", "насыщенный"]
            }
        },
        "synthetic_powder_colorants": {  # Субключ для синтетических порошковых красителей
            "name_product": {
                "colorant_types": ["краситель", "зеленое_яблоко", "кармуазин", "солнечный_закат", "понсо_4R", "шоколад_коричневый", "тартразин"],
                "brands": ["ESCO"],
                "e_codes": ["E102", "E133", "E122", "E110", "E124", "E150d", "E120"],
                "form_types": ["порошок", "порошковый"]
            },
            "composition": {
                "composition_types": ["красители_E102_E133", "краситель_E122", "краситель_E110", "краситель_E124", "красители_E102_E110_E122_E133", "краситель_E102"],
                "compound_types": ["мальтодекстрин", "комбинированные_красители"],
                "natural_additives": ["мальтодекстрин_краситель_E150d_E120"]
            },
            "dosage": {
                "dosage_ranges": ["низкие_10_30", "средние_15_30", "высокие_10_50", "сверхнизкие_0.01_5"],
                "dosage_units": ["кг_на_тонну", "кг_на_1000л"],
                "concentration_levels": ["стандартная", "повышенная", "интенсивная"]
            },
            "color": {
                "color_families": ["зеленый", "малиновый", "оранжевый", "красный", "коричневый", "желтый"],
                "color_shades": ["зеленый", "малиновый", "оранжевый", "красный", "темно_коричневый", "золотисто_желтый"],
                "color_descriptions": ["от_серого_до_темно_серого"]
            }
        },
        "synthetic_liquid_colorants": {  # Субключ для синтетических жидких красителей
            "name_product": {
                "colorant_types": ["краситель", "зеленое_яблоко", "лесная_черника", "оранжевый", "бета_каротин", "сочная_клубника", "алтайская_вишня", "синий_B", "солнечный_лимон", "черная_смородина"],
                "brands": ["ESCO"],
                "e_codes": ["E102", "E104", "E131", "E330", "E211", "E122", "E133", "E422", "E433", "E202", "E110", "E124", "E414", "E445", "E160a", "E300", "E307", "E304i"],
                "form_types": ["жидкий", "эмульсионный"]
            },
            "composition": {
                "base_components": ["вода", "вода_питьевая"],
                "preservatives": ["консервант_E211", "консерванты_E202_E211"],
                "emulsifiers": ["эмульгатор_E433", "эмульгатор_E445"],
                "acids": ["регулятор_кислотности_E330"],
                "carriers": ["носитель_E414", "носитель_E422", "масло_подсолнечное"],
                "antioxidants": ["антиокислители_E300_E307_E304i"]
            },
            "dosage": {
                "dosage_ranges": ["сверхнизкие_0.05_0.15", "низкие_0.1_0.3", "средние_0.25_0.6", "высокие_0.3_1.2", "переменные_0.05_1.0", "высокие_0.2_1.0"],
                "dosage_units": ["кг_на_тонну", "кг_на_1000л"],
                "special_dosage": ["по_рецептуре"]
            },
            "color": {
                "color_families": ["зеленый", "фиолетовый", "оранжевый", "красный", "синий", "желтый", "бордовый"],
                "color_shades": ["зеленый", "темно_фиолетовый", "темно_оранжевый", "красно_оранжевый", "темно_красный", "синий", "темно_желтый", "темно_бордовый"],
                "color_ranges": ["от_оранжевого_до_темно_оранжевого", "от_темно_оранжевого_до_красно_оранжевого"]
            }
        }
    },

    "flavor_data.json": {
        "retro_classic_drink_flavors": {  # Субключ для ретро классических напитков
            "name_product": {
                "drink_types": ["буратино", "кола", "колокольчик", "дюшес"],
                "flavor_characteristics": ["натуральный", "натуральный_тип"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_formats": ["11.01.208_ЕС", "11.02.302", "11.02.206_К", "11.02.751_TR"],
                "code_categories": ["11.01", "11.02"],
                "code_types": ["ЕС", "К", "TR"]
            }
        },
        "natural": {  # Субключ для натуральных ароматизаторов
            "name_product": {
                "fruit_flavors": ["абрикос", "апельсин", "банан", "груша", "клубника", "манго", "вишня", "лимон", "лайм", "малина"],
                "berry_flavors": ["брусника", "клюква", "изабелла"],
                "citrus_flavors": ["апельсин", "грейпфрут", "лимон", "лайм", "лимон_лайм", "горький_лимон"],
                "herbal_spice_flavors": ["вермут", "имбирь", "корица", "лаванда", "можжевельник", "кинотто"],
                "flavor_characteristics": ["натуральный", "натуральный_тип"],
                "brands": ["DEL_AR"],
                "special_types": ["тип_швепс", "тип_спрайт"]
            },
            "product_code": {
                "code_categories": ["11.01", "11.02", "11.04", "10.01"],
                "code_formats": ["цифры_точка_цифры", "буквенные_суффиксы"],
                "code_suffixes": ["N", "B", "P", "К", "S"]
            }
        },
        "citrus_aromas": {  # Субключ для цитрусовых ароматов
            "name_product": {
                "citrus_types": ["апельсин", "лимон", "грейпфрут", "лайм", "бергамот"],
                "flavor_effects": ["clouding_эффект", "помутнение"],
                "flavor_characteristics": ["натуральный", "эмульсионный"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["10.02", "11.02", "11.04"],
                "code_types": ["стандартные_коды", "специальные_коды"]
            }
        },
        "grape_berry_flavors": {  # Субключ для виноградно-ягодных вкусов
            "name_product": {
                "grape_varieties": ["виноград", "изабелла", "мускат"],
                "berry_types": ["барбарис", "брусника", "клюква"],
                "flavor_profiles": ["интенсивные", "сбалансированные"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01"],
                "grape_codes": ["специальные_виноградные"]
            }
        },
        "fruit_aromas": {  # Субключ для фруктовых ароматов
            "name_product": {
                "tropical_fruits": ["ананас", "манго", "маракуйя"],
                "stone_fruits": ["абрикос", "персик"],
                "pome_fruits": ["яблоко", "груша"],
                "flavor_profiles": ["сочные", "свежие", "спелые"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "10.01"],
                "fruit_specific_codes": ["тропические", "косточковые", "семечковые"]
            }
        },
        "vanilla_creamy_aromas": {  # Субключ для ванильно-сливочных ароматов
            "name_product": {
                "vanilla_types": ["ваниль", "ванильный"],
                "creamy_types": ["сливочный", "кремовый"],
                "dessert_flavors": ["мороженое", "карамель", "крем_брюле"],
                "texture_profiles": ["мягкий", "округлый"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "11.02"],
                "dessert_codes": ["ванильные", "сливочные"]
            }
        },
        "chocolate_coffee_bakery_aromas": {  # Субключ для шоколадно-кофейно-хлебобулочных ароматов
            "name_product": {
                "chocolate_types": ["шоколад", "какао", "молочный_шоколад"],
                "coffee_types": ["кофе", "эспрессо", "капучино"],
                "bakery_types": ["хлебобулочные", "выпечка"],
                "flavor_intensity": ["богатые", "премиум"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "11.02"],
                "premium_codes": ["шоколадные", "кофейные", "хлебобулочные"]
            }
        },
        "alcohol_flavors": {  # Субключ для алкогольных вкусов
            "name_product": {
                "alcohol_types": ["виски", "амаретто", "ром", "коньяк"],
                "spirit_categories": ["крепкие_напитки", "ликеры"],
                "flavor_applications": ["безалкогольные_аналоги", "экспериментальные"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01"],
                "alcohol_codes": ["крепкий_алкоголь", "ликерные"]
            }
        },
        "herbal_floral_flavors": {  # Субключ для травяно-цветочных ароматов
            "name_product": {
                "herbal_types": ["алоэ", "базилик", "матча", "мята"],
                "floral_types": ["цветочные", "лаванда", "роза"],
                "functional_types": ["здоровые", "функциональные"],
                "application_types": ["wellness_напитки", "craft_концепты"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "11.02"],
                "functional_codes": ["травяные", "цветочные"]
            }
        },
        "nut_cereal_flavors": {  # Субключ для орехово-злаковых ароматов
            "name_product": {
                "nut_types": ["миндаль", "орех", "фундук"],
                "cereal_types": ["злаковые", "овсяные"],
                "sweet_types": ["мед", "медовый"],
                "seasonal_profile": ["осенне_зимние"],
                "application_types": ["craft_концепты"],
                "flavor_characteristics": ["теплые", "слегка_терпкие"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01"],
                "seasonal_codes": ["ореховые", "медовые"]
            }
        },
        "juice_bases": {  # Субключ для соковых основ
            "name_product": {
                "juice_types": ["соковые_основы", "сокосодержащие"],
                "composition_types": ["комплексные", "концентрированный_сок"],
                "application_benefits": ["аромат_и_вкус", "технологическая_эффективность"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["специальные_соковые"],
                "juice_codes": ["концентрированные", "комплексные"]
            }
        },
        "herbal_flavor": {  # Субключ для травяных ароматизаторов
            "name_product": {
                "herbal_types": ["эстрагон", "мята", "базилик", "лаванда"],
                "flavor_characteristics": ["натуральный", "натуральный_тип"],
                "application_types": ["травяные_напитки", "ароматические"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "11.02"],
                "herbal_codes": ["травяные_ароматизаторы"]
            }
        },
        "vanilla_creamy_aroma": {  # Субключ для ванильно-сливочных ароматов
            "name_product": {
                "vanilla_types": ["ваниль", "ванильный_крем"],
                "creamy_types": ["сливочный", "кремовый", "молочный"],
                "dessert_profiles": ["ванильно_сливочный", "кремовый_аромат"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "11.02"],
                "dessert_codes": ["ванильные_ароматы", "сливочные_ароматы"]
            }
        },
        "grape_flavor": {  # Субключ для виноградных вкусов
            "name_product": {
                "grape_varieties": ["виноград", "изабелла", "мускат"],
                "flavor_intensity": ["натуральный_виноградный", "интенсивный_виноградный"],
                "grape_types": ["темный_виноград", "белый_виноград"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01"],
                "grape_codes": ["виноградные_ароматизаторы"]
            }
        },
        "nut_cereal_flavor": {  # Субключ для орехово-злаковых ароматизаторов
            "name_product": {
                "nut_types": ["миндаль", "орех", "фундук", "арахис"],
                "cereal_types": ["злаковые", "овсяные", "пшеничные"],
                "flavor_profiles": ["ореховые", "злаковые", "медовые"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01"],
                "nut_cereal_codes": ["ореховые_ароматизаторы", "злаковые_ароматизаторы"]
            }
        },
        "alcohol_flavor": {  # Субключ для алкогольных ароматизаторов
            "name_product": {
                "alcohol_types": ["виски", "ром", "коньяк", "амаретто"],
                "spirit_categories": ["крепкие_напитки", "ликеры"],
                "flavor_applications": ["безалкогольные_аналоги"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01"],
                "alcohol_codes": ["алкогольные_ароматизаторы"]
            }
        },
        "fruit_aroma": {  # Субключ для фруктовых ароматов
            "name_product": {
                "fruit_types": ["яблоко", "груша", "персик", "абрикос", "манго", "ананас"],
                "tropical_fruits": ["тропические", "экзотические"],
                "stone_fruits": ["косточковые"],
                "pome_fruits": ["семечковые"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "10.01"],
                "fruit_codes": ["фруктовые_ароматы"]
            }
        },
        "citrus_aroma": {  # Субключ для цитрусовых ароматов
            "name_product": {
                "citrus_types": ["лимон", "апельсин", "грейпфрут", "лайм", "бергамот"],
                "citrus_effects": ["clouding_эффект", "помутнение"],
                "flavor_characteristics": ["натуральный", "эмульсионный"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["10.02", "11.02", "11.04"],
                "citrus_codes": ["цитрусовые_ароматы"]
            }
        },
        "choco_coffee_bakery_aroma": {  # Субключ для шоколадно-кофейно-хлебобулочных ароматов
            "name_product": {
                "chocolate_types": ["шоколад", "какао", "молочный_шоколад"],
                "coffee_types": ["кофе", "эспрессо", "капучино"],
                "bakery_types": ["хлебобулочные", "выпечка", "печенье"],
                "brands": ["DEL_AR"]
            },
            "product_code": {
                "code_categories": ["11.01", "11.02"],
                "premium_codes": ["шоколадные_ароматы", "кофейные_ароматы", "хлебобулочные_ароматы"]
            }
        }
    },

    "sweeteners_data.json": {
        "sweeteners_no_aspartame": {  # Субключ для подсластителей без аспартама
            "name_product": {
                "sweetener_types": ["подсластитель_комбинированный"],
                "sweetness_numbers": ["50_S", "130", "200_AN", "240", "200_K", "200_KN", "250_L"],
                "brands": ["SLADIN"],
                "product_characteristics": ["без_аспартама", "комбинированный"]
            },
            "sweetness_coefficient": {
                "sweetness_levels": ["низкие_50", "средние_130_200", "высокие_240_250"],
                "exact_coefficients": ["50", "130", "200", "240", "250"],
                "sweetness_ranges": ["50_раз", "130_раз", "200_раз", "240_раз", "250_раз"]
            },
            "composition": {
                "base_components": ["фруктоза", "мальтодекстрин", "сахар"],
                "e_codes": ["E952", "E950", "E954", "E961", "E955"],
                "sweetener_types": ["цикламат_E952", "ацесульфам_E950", "сахарин_E954", "неотам_E961", "сукралоза_E955"],
                "special_components": ["антислеживающий_агент_E551"],
                "combination_types": ["двухкомпонентные", "трехкомпонентные", "многокомпонентные"]
            }
        },
        "sweeteners_with_aspartame": {  # Субключ для подсластителей с аспартамом
            "name_product": {
                "sweetener_types": ["подсластитель_комбинированный"],
                "sweetness_numbers": ["250_LA", "200_A", "200_AC", "200_L", "280_B"],
                "brands": ["SLADIN"],
                "product_characteristics": ["с_аспартамом", "комбинированный"]
            },
            "sweetness_coefficient": {
                "sweetness_levels": ["высокие_200_280"],
                "exact_coefficients": ["200", "250", "280"],
                "sweetness_ranges": ["200_раз", "250_раз"],
                "special_coefficients": ["соответствующий_9%_раствора_сахарозы"]
            },
            "composition": {
                "base_components": ["сахар"],
                "e_codes": ["E952", "E954", "E961", "E950", "E951"],
                "sweetener_types": ["цикламат_E952", "сахарин_E954", "неотам_E961", "ацесульфам_E950", "аспартам_E951"],
                "special_components": ["антислеживающий_агент_E551", "стевиолгликозиды"],
                "aspartame_warning": ["содержит_источник_фенилаланина"],
                "combination_types": ["с_аспартамом", "премиум_составы"]
            }
        },
        "sweeteners_premium": {  # Субключ для премиум подсластителей
            "name_product": {
                "product_types": ["премиум_подсластители", "натуральные_сиропы"],
                "brands": ["SLADIN"],
                "premium_characteristics": ["улучшенная_функциональность", "награжденный_вкус"]
            },
            "sweetness_coefficient": {
                "premium_levels": ["премиум_категория"],
                "enhanced_properties": ["синергия_вкуса", "улучшенные_характеристики"]
            },
            "composition": {
                "premium_components": ["натуральные_сиропы", "премиум_составы"],
                "quality_certifications": ["ISO_9001", "ISO_22000"],
                "custom_formulations": ["индивидуальные_составы"]
            }
        },
        "sweeteners_sweetness_200": {  # Субключ для подсластителей со сладостью 200
            "name_product": {
                "sweetener_types": ["подсластитель_200"],
                "sweetness_focus": ["200_коэффициент"],
                "brands": ["SLADIN"]
            },
            "sweetness_coefficient": {
                "target_sweetness": ["200"],
                "sweetness_category": ["средне_высокий_уровень"]
            },
            "composition": {
                "specialized_200": ["оптимизированные_для_200"],
                "balanced_formula": ["сбалансированный_состав"]
            }
        }
    },

    "juce_recipes.json": {
        "tropical": {  # Субключ для тропических соковых напитков
            "recipe_name": {
                "drink_types": ["напиток_безалкогольный", "соковый_напиток"],
                "carbonation": ["негазированный", "газированный"],
                "flavor_profiles": ["манго_маракуйя", "тропические"],
                "juice_content": ["2.5%_сока", "3.5%_сока", "5%_сока", "30%_сока"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "sweetener_names": ["Сладин_200_А"],
                "calorie_levels": ["стандартная_калорийность", "низкая_калорийность"]
            },
            "process_stages": {
                "preparation_stages": ["syrup_preparation", "final_drink_preparation"],
                "production_methods": ["двухстадийный_процесс"],
                "volumes": ["200_дм3_сироп", "1000_дм3_напиток"]
            }
        },
        "apple_pear_peach": {  # Субключ для яблочно-грушево-персиковых напитков
            "recipe_name": {
                "drink_types": ["напиток_безалкогольный", "соковый_напиток"],
                "fruit_combinations": ["яблочно_грушевые", "персиковые"],
                "carbonation": ["негазированный", "газированный"],
                "juice_content": ["низкое_содержание_сока", "среднее_содержание_сока"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "sweetener_options": ["Сладин_200_А", "без_подсластителя"]
            },
            "process_stages": {
                "preparation_stages": ["syrup_preparation", "final_drink_preparation"],
                "fruit_processing": ["экстракция_фруктовых_компонентов"]
            }
        },
        "forest_berries": {  # Субключ для лесных ягод
            "recipe_name": {
                "drink_types": ["напиток_безалкогольный"],
                "berry_types": ["лесные_ягоды", "ягодные_смеси"],
                "flavor_intensity": ["интенсивный_ягодный"],
                "juice_content": ["ягодный_сок_присутствует"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "berry_concentration": ["стандартная", "усиленная"]
            },
            "process_stages": {
                "preparation_stages": ["syrup_preparation", "final_drink_preparation"],
                "berry_processing": ["ягодная_экстракция"]
            }
        },
        "orange_drinks": {  # Субключ для апельсиновых напитков
            "recipe_name": {
                "drink_types": ["напиток_безалкогольный"],
                "citrus_types": ["апельсин", "цитрусовые"],
                "flavor_profiles": ["с_ароматом_апельсина"],
                "juice_content": ["3.5%_сока", "апельсиновый_сок"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "citrus_intensity": ["стандартная", "усиленная"]
            },
            "process_stages": {
                "preparation_stages": ["syrup_preparation", "final_drink_preparation"],
                "citrus_processing": ["цитрусовая_экстракция"]
            }
        },
        "cherry_pomegranate": {  # Субключ для вишнево-гранатовых напитков
            "recipe_name": {
                "drink_types": ["напиток_безалкогольный"],
                "fruit_types": ["вишня", "гранат"],
                "flavor_combinations": ["вишнево_гранатовые"],
                "juice_content": ["фруктовый_сок_присутствует"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "fruit_intensity": ["сбалансированная", "интенсивная"]
            },
            "process_stages": {
                "preparation_stages": ["syrup_preparation", "final_drink_preparation"],
                "fruit_processing": ["фруктовая_экстракция"]
            }
        }
    },

    "club_recipes.json": {
        "mojito": {  # Субключ для мохито
            "recipe_name": {
                "drink_types": ["мохито", "напиток_безалкогольный"],
                "flavor_variants": ["лимон_лайм", "клубника", "гранат"],
                "cocktail_category": ["клубные_коктейли"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "sweetener_names": ["Сладин_200_А", "Сладин_200"],
                "calorie_options": ["44_ккал", "36_ккал", "40_ккал", "1_ккал"],
                "carb_content": ["11г_углеводов", "9г_углеводов", "10г_углеводов", "без_углеводов"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "volumes": ["200_дм3_сироп", "166.67_дм3_сироп", "1000_дм3_напиток"],
                "carbonation": ["газация_CO2", "4.15_кг_CO2"]
            }
        },
        "sangria": {  # Субключ для сангрии
            "recipe_name": {
                "drink_types": ["сангрия", "напиток_безалкогольный_газированный"],
                "color_variants": ["белая", "красная"],
                "cocktail_category": ["клубные_коктейли"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "sweetener_names": ["Сладин_200_А"],
                "calorie_options": ["36_ккал", "1_ккал"],
                "carb_content": ["9г_углеводов", "без_углеводов"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "volumes": ["200_дм3_сироп", "1000_дм3_напиток"],
                "fruit_components": ["сок_яблочный_концентрированный", "фруктовые_ароматизаторы"]
            }
        },
        "punch_glintwein_pinacolada": {  # Субключ для пунша, глинтвейна и пина колады
            "recipe_name": {
                "drink_types": ["пунш", "глинтвейн", "пина_колада"],
                "carbonation": ["газированный", "негазированный"],
                "cocktail_category": ["клубные_коктейли"],
                "seasonal_types": ["согревающие", "тропические"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "sweetener_names": ["Сладин_200_А"],
                "calorie_options": ["32_ккал", "40_ккал", "1_ккал", "0.5_ккал"],
                "carb_content": ["8г_углеводов", "10г_углеводов", "без_углеводов"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "volumes": ["200_дм3_сироп", "1000_дм3_напиток"],
                "special_effects": ["охлаждающий_эффект", "согревающий_эффект"],
                "carbonation": ["с_газацией", "без_газации"]
            }
        },
        "daiquiri_kruchon": {  # Субключ для дайкири и кручона
            "recipe_name": {
                "drink_types": ["дайкири", "кручон"],
                "cocktail_category": ["клубные_коктейли"],
                "flavor_profiles": ["фруктовые_коктейли"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "preparation_options": ["классический", "современный"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "cocktail_techniques": ["коктейльные_методы"]
            }
        }
    },

    "energy_recipes.json": {
        "citrus_energy": {  # Субключ для цитрусовых энергетиков
            "recipe_name": {
                "drink_types": ["энергетический", "напиток_безалкогольный_газированный"],
                "flavor_profiles": ["цитрусовая_бомба", "bitter_lemon"],
                "energy_category": ["энергетические_напитки"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_интенсивном_подсластителе"],
                "energy_levels": ["стандартная_энергия", "повышенная_энергия"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "energy_additives": ["женьшень", "L_карнитин", "энергетические_компоненты"]
            }
        },
        "fruit_energy": {  # Субключ для фруктовых энергетиков
            "recipe_name": {
                "drink_types": ["энергетический", "напиток_безалкогольный_газированный"],
                "flavor_profiles": ["тропический_манго", "фруктовые_энергетики"],
                "energy_category": ["энергетические_напитки"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "fruit_intensity": ["тропическая_интенсивность"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "functional_components": ["энергетические_добавки", "фруктовые_экстракты"]
            }
        }
    },

    "cold_tea_recipes.json": {
        "black_tea": {  # Субключ для черного чая
            "recipe_name": {
                "drink_types": ["напиток_чайный_холодный", "черный_чай"],
                "tea_category": ["холодные_чаи"],
                "tea_base": ["черный_чай"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "tea_strength": ["стандартная_крепость", "усиленная_крепость"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "tea_processing": ["заваривание", "охлаждение", "чайная_основа"]
            }
        },
        "green_tea": {  # Субключ для зеленого чая
            "recipe_name": {
                "drink_types": ["напиток_чайный_холодный", "зеленый_чай"],
                "tea_category": ["холодные_чаи"],
                "tea_base": ["зеленый_чай"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "antioxidant_levels": ["стандартные", "повышенные"]
            },
            "process_stages": {
                "preparation_methods": ["двухстадийный_процесс"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "tea_processing": ["деликатное_заваривание", "сохранение_антиоксидантов"]
            }
        }
    },

    "drink_snaps_recipes.json": {
        "berry_snaps": {  # Субключ для ягодных снап-напитков
            "recipe_name": {
                "drink_types": ["снап_напиток", "ягодный"],
                "flavor_profiles": ["ягодные_смеси"],
                "snap_category": ["снап_напитки"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "berry_intensity": ["стандартная", "усиленная"]
            },
            "process_stages": {
                "preparation_methods": ["специальная_технология_снап"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "snap_techniques": ["снап_процессы"]
            }
        },
        "vanilla_cream_caramel": {  # Субключ для ванильно-карамельных снап-напитков
            "recipe_name": {
                "drink_types": ["снап_напиток", "ванильно_карамельный"],
                "flavor_profiles": ["ваниль", "карамель", "сливки"],
                "dessert_category": ["десертные_снапы"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "dessert_intensity": ["мягкая", "интенсивная"]
            },
            "process_stages": {
                "preparation_methods": ["специальная_технология_снап"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "dessert_processing": ["ванильно_карамельная_обработка"]
            }
        },
        "fruit_snaps": {  # Субключ для фруктовых снап-напитков
            "recipe_name": {
                "drink_types": ["снап_напиток", "фруктовый"],
                "fruit_types": ["тропические", "косточковые", "семечковые"],
                "snap_category": ["фруктовые_снапы"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "fruit_intensity": ["натуральная", "усиленная"]
            },
            "process_stages": {
                "preparation_methods": ["специальная_технология_снап"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "fruit_processing": ["фруктовая_снап_обработка"]
            }
        }
    },

    "jelly_recipes.json": {
        "berry_bird_cherry": {  # Субключ для ягодно-черемуховых желе-напитков
            "recipe_name": {
                "drink_types": ["желе_напиток", "ягодный"],
                "berry_types": ["ягоды", "черемуха"],
                "jelly_category": ["желе_напитки"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "gelling_strength": ["стандартная", "усиленная"]
            },
            "process_stages": {
                "preparation_methods": ["желирование"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "gelling_agents": ["желирующие_агенты", "гелеобразование"]
            }
        },
        "berry_jelly": {  # Субключ для ягодных желе-напитков
            "recipe_name": {
                "drink_types": ["желе_напиток", "ягодный"],
                "berry_types": ["смешанные_ягоды"],
                "jelly_category": ["желе_напитки"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "berry_concentration": ["натуральная", "концентрированная"]
            },
            "process_stages": {
                "preparation_methods": ["желирование"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "berry_gelling": ["ягодное_желирование"]
            }
        },
        "aloe_cactus_grape": {  # Субключ для желе с алоэ, кактусом и виноградом
            "recipe_name": {
                "drink_types": ["желе_напиток", "с_алоэ_и_кактусом"],
                "functional_ingredients": ["алоэ", "кактус", "виноград"],
                "functional_category": ["функциональные_желе"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "functional_concentration": ["стандартная", "повышенная"]
            },
            "process_stages": {
                "preparation_methods": ["функциональное_желирование"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "functional_processing": ["алоэ_кактус_обработка"]
            }
        },
        "orange_watermelon_herbs": {  # Субключ для цитрусово-травяных желе
            "recipe_name": {
                "drink_types": ["желе_напиток", "цитрусово_травяной"],
                "flavor_combinations": ["апельсин", "арбуз", "травы"],
                "herbal_category": ["травяные_желе"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "herbal_intensity": ["легкая", "выраженная"]
            },
            "process_stages": {
                "preparation_methods": ["травяное_желирование"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "herbal_processing": ["травяная_экстракция_и_желирование"]
            }
        }
    },

    "kvas_gost_recipes.json": {
        "with_spices": {  # Субключ для кваса со специями
            "recipe_name": {
                "drink_types": ["квас", "со_специями"],
                "gost_compliance": ["ГОСТ"],
                "kvass_category": ["традиционный_квас"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "fermentation_types": ["традиционное_брожение", "современное_брожение"]
            },
            "process_stages": {
                "preparation_methods": ["брожение"],
                "stages": ["syrup_preparation", "intermediate_stage", "final_drink_preparation"],
                "fermentation_processing": ["закваска", "брожение", "созревание"]
            }
        },
        "apple": {  # Субключ для яблочного кваса
            "recipe_name": {
                "drink_types": ["квас", "яблочный"],
                "gost_compliance": ["ГОСТ"],
                "fruit_kvass": ["фруктовый_квас"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "apple_varieties": ["яблочные_сорта"]
            },
            "process_stages": {
                "preparation_methods": ["яблочное_брожение"],
                "stages": ["syrup_preparation", "intermediate_stage", "final_drink_preparation"],
                "apple_fermentation": ["яблочная_закваска"]
            }
        },
        "traditional": {  # Субключ для традиционного кваса
            "recipe_name": {
                "drink_types": ["квас", "традиционный"],
                "gost_compliance": ["ГОСТ"],
                "traditional_category": ["классический_квас"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "traditional_methods": ["аутентичная_рецептура"]
            },
            "process_stages": {
                "preparation_methods": ["традиционное_брожение"],
                "stages": ["syrup_preparation", "intermediate_stage", "final_drink_preparation"],
                "traditional_fermentation": ["классическая_технология"]
            }
        },
        "whey": {  # Субключ для сывороточного кваса
            "recipe_name": {
                "drink_types": ["квас", "сывороточный"],
                "base_ingredients": ["молочная_сыворотка", "сыворотка"],
                "functional_category": ["функциональный_квас"],
                "gost_compliance": ["ГОСТ"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "whey_concentration": ["стандартная", "повышенная"]
            },
            "process_stages": {
                "preparation_methods": ["сывороточное_брожение"],
                "stages": ["syrup_preparation", "intermediate_stage", "final_drink_preparation"],
                "whey_processing": ["сывороточная_технология"]
            }
        },
        "beet_berry": {  # Субключ для свекольно-ягодного кваса
            "recipe_name": {
                "drink_types": ["квас", "свекольно_ягодный"],
                "flavor_combinations": ["свекла", "ягоды"],
                "specialty_kvass": ["специальный_квас"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "beet_berry_ratio": ["сбалансированное", "с_преобладанием_ягод"]
            },
            "process_stages": {
                "preparation_methods": ["свекольно_ягодное_брожение"],
                "stages": ["syrup_preparation", "intermediate_stage", "final_drink_preparation"],
                "specialty_fermentation": ["специальная_закваска"]
            }
        }
    },

    "malt_recipes.json": {
        "cooling_effect": {  # Субключ для солодовых напитков с охлаждающим эффектом
            "recipe_name": {
                "drink_types": ["солодовый_напиток", "с_охлаждающим_эффектом"],
                "functional_effects": ["охлаждающий"],
                "malt_category": ["функциональные_солодовые"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "cooling_intensity": ["легкий", "выраженный"]
            },
            "process_stages": {
                "preparation_methods": ["солодовая_экстракция"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "malt_processing": ["солодовые_экстракты", "охлаждающие_компоненты"]
            }
        },
        "berry_malt": {  # Субключ для ягодных солодовых напитков
            "recipe_name": {
                "drink_types": ["солодовый_напиток", "ягодный"],
                "flavor_combinations": ["солод", "ягоды"],
                "malt_category": ["ягодные_солодовые"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "berry_malt_balance": ["сбалансированный", "с_преобладанием_ягод"]
            },
            "process_stages": {
                "preparation_methods": ["ягодно_солодовая_экстракция"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "berry_malt_processing": ["ягодно_солодовые_компоненты"]
            }
        },
        "herbal_malt": {  # Субключ для травяных солодовых напитков
            "recipe_name": {
                "drink_types": ["солодовый_напиток", "травяной"],
                "herbal_types": ["лечебные_травы", "ароматические_травы"],
                "malt_category": ["травяные_солодовые"]
            },
            "variants": {
                "sugar_types": ["на_сахаре", "на_подсластителе"],
                "herbal_intensity": ["мягкая", "насыщенная"]
            },
            "process_stages": {
                "preparation_methods": ["травяно_солодовая_экстракция"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "herbal_malt_processing": ["травяно_солодовые_экстракты"]
            }
        }
    },

    "retro_recipes.json": {
        "tarragon": {  # Субключ для тархуна
            "recipe_name": {
                "drink_types": ["тархун", "ретро_напиток"],
                "retro_category": ["классические_ретро"],
                "herbal_base": ["эстрагон"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "authenticity_level": ["аутентичный", "модернизированный"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "retro_processing": ["традиционные_технологии", "натуральные_ароматизаторы"]
            }
        },
        "duchess_pear": {  # Субключ для дюшеса
            "recipe_name": {
                "drink_types": ["дюшес", "ретро_напиток"],
                "flavor_base": ["груша"],
                "retro_category": ["классические_ретро"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "pear_intensity": ["классическая", "усиленная"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "pear_processing": ["грушевые_ароматизаторы"]
            }
        },
        "lemonades": {  # Субключ для лимонадов
            "recipe_name": {
                "drink_types": ["лимонад", "ретро_напиток"],
                "citrus_base": ["лимон"],
                "retro_category": ["классические_лимонады"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "citrus_intensity": ["советский_стиль", "современный_стиль"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "citrus_processing": ["классические_цитрусовые_технологии"]
            }
        },
        "cherry_feijoa_activity": {  # Субключ для вишнево-фейхоа напитков
            "recipe_name": {
                "drink_types": ["ретро_напиток", "функциональный"],
                "fruit_combination": ["вишня", "фейхоа"],
                "activity_types": ["тонизирующий", "витаминизированный"],
                "retro_category": ["экзотические_ретро"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "fruit_intensity": ["сбалансированная", "насыщенная"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "fruit_processing": ["экстракция_активных_веществ"]
            }
        },
        "buratino_cream_soda": {  # Субключ для буратино и крем-соды
            "recipe_name": {
                "drink_types": ["буратино", "крем_сода", "ретро_напиток"],
                "flavor_profile": ["сливочный", "ванильный"],
                "retro_category": ["классические_ретро"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "cream_intensity": ["классическая", "усиленная"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "cream_processing": ["сливочная_ароматизация"]
            }
        },
        "kolokolchik": {  # Субключ для колокольчика
            "recipe_name": {
                "drink_types": ["колокольчик", "ретро_напиток"],
                "flavor_profile": ["цветочный", "травяной"],
                "retro_category": ["классические_ретро"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "floral_intensity": ["деликатная", "выраженная"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "floral_processing": ["цветочная_ароматизация"]
            }
        },
        "kvas_drinks": {  # Субключ для квасных напитков
            "recipe_name": {
                "drink_types": ["квасной_напиток", "ретро_напиток"],
                "kvass_base": ["квасная_основа"],
                "retro_category": ["квасные_ретро"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "kvass_intensity": ["легкая", "традиционная"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "kvass_processing": ["квасная_технология"]
            }
        },
        "cola": {  # Субключ для колы
            "recipe_name": {
                "drink_types": ["кола", "ретро_напиток"],
                "flavor_profile": ["кола_классик", "пряный"],
                "retro_category": ["классические_ретро"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "cola_intensity": ["мягкая", "интенсивная"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "cola_processing": ["кола_ароматизация"]
            }
        },
        "citrus_retro": {  # Субключ для цитрусовых ретро-напитков
            "recipe_name": {
                "drink_types": ["ретро_напиток", "газированный"],
                "flavor_profiles": ["bitter_lemon", "с_ароматом_лимона", "с_ароматом_апельсина"],
                "retro_types": ["швепс", "спрайт", "миринда", "фанта"],
                "retro_category": ["классические_ретро"]
            },
            "variants": {
                "sugar_types": ["традиционный", "современная_формула"],
                "citrus_intensity": ["классическая", "усиленная"]
            },
            "process_stages": {
                "preparation_methods": ["классическая_технология"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "citrus_processing": ["ретро_цитрусовые_технологии"]
            }
        }
    },

    "vegetable_extract_recipes.json": {
        "algorithms": {  # Субключ для алгоритмических напитков с экстрактами
            "recipe_name": {
                "drink_types": ["с_растительными_экстрактами", "алгоритмические"],
                "functional_category": ["функциональные_напитки"],
                "extract_types": ["растительные_экстракты"]
            },
            "variants": {
                "sugar_types": ["стандартная_концентрация", "усиленная_формула"],
                "algorithm_complexity": ["базовый", "продвинутый"]
            },
            "process_stages": {
                "preparation_methods": ["экстракция_растительных_компонентов"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "extract_processing": ["технология_экстракции", "функциональные_добавки"]
            }
        },
        "herbal_vegetable": {  # Субключ для травяных напитков с экстрактами
            "recipe_name": {
                "drink_types": ["травяной_функциональный", "с_растительными_экстрактами"],
                "herbal_types": ["лечебные_травы", "ароматические_травы"],
                "functional_category": ["wellness_напитки"]
            },
            "variants": {
                "sugar_types": ["стандартная_концентрация", "усиленная_формула"],
                "herbal_potency": ["стандартная", "повышенная"]
            },
            "process_stages": {
                "preparation_methods": ["травяная_экстракция"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "herbal_processing": ["экстракция_активных_веществ"]
            }
        },
        "berry_vegetable": {  # Субключ для ягодных напитков с экстрактами
            "recipe_name": {
                "drink_types": ["с_растительными_экстрактами", "ягодный"],
                "berry_extracts": ["ягодные_экстракты"],
                "functional_category": ["антиоксидантные_напитки"]
            },
            "variants": {
                "sugar_types": ["стандартная_концентрация", "усиленная_формула"],
                "antioxidant_levels": ["базовые", "усиленные"]
            },
            "process_stages": {
                "preparation_methods": ["ягодная_экстракция"],
                "stages": ["syrup_preparation", "final_drink_preparation"],
                "berry_extract_processing": ["экстракция_антиоксидантов"]
            }
        }
    },

    "mixture_data.json": {
        "kvass_mixtures": {  # Субключ для квасных смесей
            "name_product": {
                "mixture_types": ["квас", "квасная_смесь"],
                "product_applications": ["для_кваса"],
                "base_types": ["мальтозная_основа"]
            },
            "composition": {
                "base_components": ["мальтозная_основа", "дрожжи"],
                "fermentation_agents": ["дрожжи", "закваска"]
            },
            "dosage": {
                "dosage_ranges": ["50_кг_на_тонну"],
                "dosage_units": ["кг_на_тонну"],
                "application_rates": ["для_получения_готового_напитка"]
            }
        },
        "drink_mixtures": {  # Субключ для напиточных смесей
            "name_product": {
                "mixture_types": ["смесь_для_лимонада", "концентрат_напитка", "напиточная_смесь"],
                "product_applications": ["для_лимонада", "для_напитков"],
                "concentrate_types": ["готовые_концентраты"]
            },
            "composition": {
                "base_components": ["сахар", "лимонная_кислота", "ароматизатор"],
                "flavoring_agents": ["ароматизаторы", "вкусовые_добавки"]
            },
            "dosage": {
                "dosage_ranges": ["20_30_кг_на_1000л"],
                "dosage_units": ["кг_на_1000л"],
                "concentration_levels": ["концентрат", "готовая_к_использованию"]
            }
        }
    },

    "various_data.json": {
        "preservatives_and_acids": {  # Субключ для консервантов и кислот
            "name_product": {
                "additive_types": ["кислота_лимонная", "натрия_бензоат", "консервант"],
                "chemical_names": ["лимонная_кислота", "бензоат_натрия"],
                "functional_categories": ["консерванты", "кислоты", "регуляторы_кислотности"]
            },
            "has_E_code": {
                "e_codes": ["E330", "E211", "E202"],
                "safety_classification": ["разрешенные_добавки"],
                "regulatory_status": ["одобрены_для_применения"]
            },
            "dosage": {
                "dosage_ranges": ["1.0_3.0_кг_на_тонну", "0.1_0.2_процента"],
                "dosage_units": ["кг_на_тонну", "процент"],
                "application_flexibility": ["по_потребности"]
            }
        },
        "stabilizers_emulsifiers": {  # Субключ для стабилизаторов и эмульгаторов
            "name_product": {
                "additive_types": ["стабилизатор", "эмульгатор"],
                "functional_categories": ["стабилизаторы", "эмульгаторы", "текстурообразователи"]
            },
            "has_E_code": {
                "e_codes": ["стабилизирующие_E_коды"],
                "functional_e_codes": ["эмульгирующие_добавки"]
            },
            "dosage": {
                "dosage_ranges": ["технологические_нормы"],
                "application_specificity": ["по_технологии"]
            }
        },
        "functional_additives": {  # Субключ для функциональных добавок
            "name_product": {
                "additive_types": ["функциональные_добавки"],
                "health_categories": ["нутрицевтики", "функциональные_ингредиенты"]
            },
            "has_E_code": {
                "regulatory_codes": ["специальные_функциональные_коды"]
            },
            "dosage": {
                "dosage_ranges": ["функциональные_дозировки"],
                "efficacy_levels": ["терапевтические", "профилактические"]
            }
        },
        "vitamins_minerals": {  # Субключ для витаминов и минералов
            "name_product": {
                "nutrient_types": ["витамины", "минералы", "микроэлементы"],
                "fortification_agents": ["витаминные_комплексы"]
            },
            "has_E_code": {
                "vitamin_codes": ["витаминные_E_коды"]
            },
            "dosage": {
                "dosage_ranges": ["витаминные_нормы"],
                "rda_compliance": ["суточные_нормы"]
            }
        },
        "natural_extracts": {  # Субключ для натуральных экстрактов
            "name_product": {
                "extract_types": ["натуральные_экстракты", "растительные_экстракты"],
                "source_materials": ["растительное_сырье"]
            },
            "has_E_code": {
                "natural_codes": ["коды_натуральных_экстрактов"]
            },
            "dosage": {
                "dosage_ranges": ["экстракционные_нормы"],
                "concentration_levels": ["стандартизированные_экстракты"]
            }
        },
        "special_ingredients": {  # Субключ для специальных ингредиентов
            "name_product": {
                "specialty_types": ["специальные_ингредиенты", "инновационные_добавки"],
                "application_specific": ["специализированные_компоненты"]
            },
            "has_E_code": {
                "special_codes": ["специальные_E_коды"]
            },
            "dosage": {
                "dosage_ranges": ["специальные_дозировки"],
                "application_specific_rates": ["по_назначению"]
            }
        },
        "oxygen_cocktail": {  # Субключ для кислородных коктейлей
            "name_product": {
                "cocktail_types": ["кислородный_коктейль", "функциональный_напиток"],
                "oxygen_enriched": ["обогащенный_кислородом"],
                "wellness_category": ["wellness_напитки"]
            },
            "has_E_code": {
                "functional_codes": ["функциональные_добавки"]
            },
            "dosage": {
                "oxygen_levels": ["стандартное_обогащение", "повышенное_обогащение"],
                "application_rates": ["по_технологии"]
            }
        },
        "vegetable_milk_powder": {  # Субключ для растительных молочных порошков
            "name_product": {
                "powder_types": ["растительный_молочный_порошок", "растительное_молоко"],
                "plant_sources": ["соевый", "овсяный", "миндальный", "кокосовый"],
                "functional_category": ["растительные_альтернативы"]
            },
            "has_E_code": {
                "plant_codes": ["растительные_добавки"]
            },
            "dosage": {
                "powder_concentrations": ["стандартная_концентрация", "высокая_концентрация"],
                "reconstitution_ratios": ["1:10", "1:8", "по_рецептуре"]
            }
        },
        "fruit_powders": {  # Субключ для фруктовых порошков
            "name_product": {
                "powder_types": ["фруктовый_порошок", "сублимированные_фрукты"],
                "fruit_sources": ["ягодные", "цитрусовые", "тропические", "косточковые"],
                "processing_types": ["сублимационная_сушка", "распылительная_сушка"]
            },
            "has_E_code": {
                "fruit_codes": ["натуральные_фруктовые"]
            },
            "dosage": {
                "powder_concentrations": ["легкая_ароматизация", "интенсивная_ароматизация"],
                "application_rates": ["5_15_г_на_литр", "по_вкусу"]
            }
        },
        "ferments": {  # Субключ для ферментов
            "name_product": {
                "enzyme_types": ["ферменты", "энзимы"],
                "application_areas": ["брожение", "гидролиз", "осветление"],
                "enzyme_sources": ["микробиальные", "растительные"]
            },
            "has_E_code": {
                "enzyme_codes": ["ферментные_препараты"]
            },
            "dosage": {
                "enzyme_activity": ["стандартная_активность", "высокая_активность"],
                "application_rates": ["по_технологическим_нормам"]
            }
        },
        "probiotic_cultures": {  # Субключ для пробиотических культур
            "name_product": {
                "culture_types": ["пробиотические_культуры", "живые_культуры"],
                "strain_varieties": ["лактобактерии", "бифидобактерии", "молочнокислые"],
                "functional_benefits": ["пищеварение", "иммунитет", "микрофлора"]
            },
            "has_E_code": {
                "probiotic_codes": ["пробиотические_добавки"]
            },
            "dosage": {
                "culture_concentrations": ["стандартная_концентрация", "высокая_концентрация"],
                "cfu_levels": ["10^6_КОЕ", "10^8_КОЕ", "10^9_КОЕ"]
            }
        }
    }
}

# Экспорт для универсального загрузчика
enum_mapping = DRINKS_ENUM_MAPPING