"""Enum mappings for bakery tool-calling domain."""

from __future__ import annotations

from typing import Any

# NOTE: Placeholder structure to be populated with enum metadata in subsequent steps.
BAKERY_ENUM_MAPPING: dict[str, dict[str, dict[str, Any]]] = {
    "classic_confectionery_collection.json": {
        "chocolate": {
            "color": {
                "color_families": ["темный", "молочный", "белый"],
            },
            "grinding_degree": {
                "grinding_bands": ["92_93_процента", "95_96_процентов"],
                "grinding_data_flags": ["значение_не_указано"],
            },
            "name": {
                "series_clusters": ["классика_3xx", "классика_4xx", "классика_7xx", "классика_9xx", "классика_14xx"],
                "feature_modifiers": ["без_сахара", "без_эквивалента", "термокапли", "горький_шоколад", "серия_R"],
            },
            "type": {
                "format_types": ["темперируемый_шоколад", "глазурь", "шоколадная_масса"],
                "fat_base_profiles": ["масло_какао", "эквивалент_масла_какао"],
            },
            "viscosity": {
                "viscosity_bands": ["очень_низкая_2_3_3_5", "низкая_4_6", "средняя_6_8", "высокая_8_10", "экстра_высокая_15_plus"],
                "viscosity_flags": ["нет_данных"],
            },
        },
        "glaze": {
            "color": {
                "color_families": ["темный", "белый", "цветной"],
            },
            "grinding_degree": {
                "grinding_bands": ["93_94_процента", "95_процентов"],
                "grinding_data_flags": ["значение_не_указано"],
            },
            "name": {
                "series_clusters": ["классика_0xx", "классика_1xx", "классика_2xx", "классика_6xx", "классика_8xx"],
                "feature_modifiers": ["ГОСТ", "капли", "без_сахара", "GF", "ароматизированная", "цветная"],
            },
            "type": {
                "format_types": ["глазурь_кондитерская", "глазурь_жировая"],
                "fat_base_profiles": ["лауриновый_заменитель", "нетемперируемый_заменитель"],
            },
            "viscosity": {
                "viscosity_bands": ["очень_низкая_2_3_3_5", "низкая_3_5_4_5", "средняя_4_5_6", "повышенная_6_7", "высокая_8_9", "экстра_высокая_15_plus"],
                "viscosity_flags": ["нет_данных", "измерена_секундомером"],
            },
        },
        "confectionery_mass": {
            "color": {
                "color_families": ["темный", "молочный", "белый"],
            },
            "grinding_degree": {
                "grinding_bands": ["93_94_процента", "95_96_процентов"],
                "grinding_data_flags": ["значение_не_указано"],
            },
            "name": {
                "series_clusters": ["классика_0xx", "классика_3xx", "классика_6xx", "классика_7xx", "классика_8xx", "классика_9xx"],
                "feature_modifiers": ["светлая", "термокапли", "йогуртовый_вкус", "без_сахара", "серия_R", "серия_BO", "серия_N", "серия_BS", "серия_T"],
            },
            "type": {
                "format_types": ["масса_кондитерская"],
                "fat_base_profiles": ["эквивалент_масла_какао", "заменитель_масла_какао_лауриновый", "заменитель_масла_какао", "кондитерский_жир"],
            },
            "viscosity": {
                "viscosity_bands": ["очень_низкая_2_3_3_5", "низкая_3_5_4_5", "средняя_4_5_6", "повышенная_6_7", "высокая_7_9", "экстра_высокая_10_plus"],
                "viscosity_flags": ["нет_данных"],
            },
        },
    },
    "cocoa_collection.json": {
        "products": {
            "is_gost_compliant": {
                "compliance_flags": ["соответствует_ГОСТ", "не_соответствует_ГОСТ"],
            },
            "name": {
                "product_types": ["комплексная_добавка", "какао_порошок", "какао_тертое", "масло_какао"],
                "brand_clusters": ["денмальт", "golden_harvest", "tulip", "zlk", "денкакао"],
            },
        },
    },
    "colorant_collection.json": {
        "natural": {
            "dosage": {
                "dosage_bands": ["ультранизкая_0_05_0_2", "низкая_0_2_1", "умеренная_1_3", "повышенная_3_5", "высокая_5_8"],
            },
            "name": {
                "pigment_groups": ["кармин", "куркумин", "бета_каротин", "аннато", "антоциан", "паприка", "хлорофилл", "ягодные_экстракты"],
                "brand_tags": ["esco"],
                "format_modifiers": ["жидкий", "порошок", "маслянистая", "жирорастворимый", "мелкодисперсный", "вязкая"],
            },
            "type": {
                "physical_states": ["жидкий", "маслянистая_жидкость", "маслянистая_мелкодисперсная", "порошок"],
                "texture_modifiers": ["однородный", "мелкогранулированный", "непрозрачная_вязкая"],
            },
        },
        "caramel": {
            "dosage": {
                "dosage_bands": ["низкая_0_15_1", "умеренная_1_5", "высокая_5_10", "смеси_с_процентами"],
            },
            "name": {
                "caramel_styles": ["жженый_сахар", "сахарный_колер"],
                "format_modifiers": ["сироп", "жирорастворимый", "сухой", "порошок"],
                "brand_tags": ["esco"],
            },
            "sv": {
                "solids_bands": ["40_50", "62_74", "65_73", "69_plus", "94_plus"],
                "sv_flags": ["нет_данных"],
            },
            "type": {
                "physical_states": ["жидкий", "жирорастворимый", "сухой", "порошок"],
                "flow_modifiers": ["вязко_текучая"],
            },
        },
        "synthetic": {
            "dosage": {
                "dosage_bands": ["ультранизкая_0_01_0_05", "низкая_0_05_0_3", "умеренная_0_3_1", "повышенная_1_5", "высокая_5_15", "очень_высокая_15_plus"],
            },
            "name": {
                "shade_clusters": ["тартразин", "понсо", "кармуазин", "солнечный_закат", "шоколадный", "красный_бархат", "клюква", "ягодно_фруктовые", "цитрусовые", "ледяные_тона"],
                "format_modifiers": ["жидкий", "жирорастворимый", "порошок"],
                "brand_tags": ["esco"],
            },
            "type": {
                "physical_states": ["жидкий", "жирорастворимый", "порошок"],
            },
        },
    },
    "delar_collection.json": {
        "gastronomic_flavors": {
            "code": {
                "code_prefixes": ["10_01", "10_05", "11_01", "11_02", "100421003"],
                "code_suffixes": ["K", "M", "N", "T", "TR", "caps"],
                "code_special_tags": ["инкапсулированный"],
            },
            "dosage": {
                "dosage_bands": ["ультрамалая_0_1_0_7", "низкая_0_5_1_5", "средняя_1_5_3"],
            },
            "name": {
                "dairy_clusters": ["молоко", "сливки", "ряженка", "сыр", "творог", "сгущенное", "масло"],
                "spice_clusters": ["имбирь", "корица", "перец"],
                "savory_gourmet": ["томат", "жареный_кунжут", "хлебная_корочка"],
                "sweet_aroma_modifiers": ["масляно_ванильный"],
            },
        },
        "juice_based_flavors": {
            "dosage": {
                "dosage_bands": ["низкая_5_7", "средняя_6_10", "высокая_12_17"],
            },
            "name": {
                "fruit_clusters": ["цитрусовые", "ягодные", "косточковые", "тропические", "яблочные"],
                "modifiers": ["миксы", "буква_серия"],
            },
        },
        "flavor_bases": {
            "dosage": {
                "dosage_flags": ["эксп"],
            },
            "name": {
                "botanical_clusters": ["чай", "травы"],
                "taste_modifiers": ["терпкость"],
            },
        },
        "aromatic_emulsions": {
            "dosage": {
                "dosage_bands": ["низкая_0_8_1_2", "средняя_2_3"],
                "dosage_flags": ["эксп"],
            },
            "name": {
                "citrus_clusters": ["лимон", "лайм", "апельсин"],
                "drink_profiles": ["кола", "нейтральный", "персик", "экзотик"],
            },
        },
        "flavor_additives": {
            "code": {
                "code_prefixes": ["10_05"],
                "code_suffixes": ["C", "K", "P"],
            },
            "dosage": {
                "application_contexts": ["готовый_продукт", "масса_муки"],
                "dosage_bands": ["низкая_0_5_2", "средняя_2_3", "высокая_3_6"],
            },
            "name": {
                "savory_clusters": [
                    "лук",
                    "чеснок",
                    "бекон",
                    "ветчина",
                    "укроп",
                    "паприка",
                    "томаты",
                    "огурец",
                    "соус",
                ],
                "cheese_clusters": ["сыр", "пармезан", "чеддер", "четыре_сыра"],
                "mushroom_clusters": ["грибы"],
            },
        },
        "spice_blends_and_extracts": {
            "dosage": {
                "dosage_bands": ["низкая_0_5_1_0", "средняя_1_0_1_5"],
            },
            "name": {
                "spice_clusters": ["имбирь", "перец"],
            },
        },
        "spices_and_herbs": {
            "code": {
                "code_prefixes": ["10_00", "10_01", "11_01", "11_02"],
                "code_suffixes": ["N", "S", "TR"],
                "code_special_tags": ["натуральный"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["микро_0_1_0_4", "низкая_0_4_0_8", "средняя_0_8_1_5", "высокая_1_5_plus"],
            },
            "name": {
                "herbal_clusters": ["лаванда", "роза", "мята", "морковь"],
                "liqueur_clusters": ["амаретто"],
                "bitter_notes": ["горький_компонент"],
            },
        },
        "berries": {
            "code": {
                "code_prefixes": ["10_01", "11_01"],
                "code_suffixes": ["K", "N", "P"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["микро_0_1_0_5", "низкая_0_5_1_5", "средняя_1_5_2_5", "высокая_2_5_plus"],
            },
            "name": {
                "berry_clusters": ["вишня", "малина", "клюква", "смородина", "брусника", "fruitberry"],
            },
        },
        "fruits": {
            "code": {
                "code_prefixes": ["10_01", "10_05", "11_01"],
                "code_suffixes": ["B", "C", "CH", "H", "K", "M", "N", "P", "R"],
                "code_special_tags": ["натуральный"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_bands": ["микро_0_2_0_5", "низкая_0_5_1_5", "средняя_1_5_2_5", "высокая_2_5_plus"],
            },
            "name": {
                "fruit_clusters": ["цитрусовые", "ягодные", "тропические", "косточковые", "экзотические", "яблочные"],
                "special_tones": ["типовые_варианты", "со_сливками", "со_специями"]
            },
        },
        "effects": {
            "code": {
                "code_prefixes": ["11_02"],
            },
            "dosage": {
                "application_contexts": ["confectionery_products", "fillings_and_toppings"],
                "dosage_bands": ["низкая_0_8_1_3", "средняя_1_5_2_0"],
            },
            "name": {
                "effect_types": ["охлаждающий", "согревающий"],
            },
        },
        "coffee_and_dessert_flavors": {
            "code": {
                "code_prefixes": ["11_01"],
                "code_suffixes": ["249", "424"],
            },
            "dosage": {
                "application_contexts": ["confectionery_products", "fillings_and_toppings"],
                "dosage_bands": ["низкая_0_5_0_7", "средняя_0_9_1_3"],
                "dosage_flags": ["эксп"],
            },
            "name": {
                "dessert_clusters": ["мокко", "тирамису"],
            },
        },
        "dairy_products": {
            "code": {
                "code_prefixes": ["10_01", "11_01"],
                "code_suffixes": ["K", "M", "S", "T", "инкапсулированный"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["низкая_0_3_1_0", "средняя_1_0_1_5", "высокая_1_5_2_5"],
            },
            "name": {
                "dairy_clusters": ["молоко", "сливки", "творог", "масло", "сгущенное", "ряженка"],
                "caramelized_notes": ["карамелизованное", "топленое"],
            },
        },
        "nut_and_cream_flavors": {
            "code": {
                "code_prefixes": ["11_01", "11_02"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["средняя_1_2_1_5", "высокая_1_5_plus"],
            },
            "name": {
                "nut_clusters": ["кокос", "кокосовые_сливки"],
            },
        },
        "beverages": {
            "code": {
                "code_prefixes": ["10_01", "11_01"],
                "code_suffixes": ["B", "D", "H", "K", "N"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["низкая_0_4_1_0", "средняя_1_0_1_5", "высокая_1_5_2_0", "очень_высокая_2_0_plus"],
            },
            "name": {
                "alcoholic_profiles": ["коньяк", "ром", "виски", "ликеры", "вермут", "шампанское", "водка"],
                "non_alcoholic_profiles": ["чай", "кофе", "матча", "лимонад", "тархун", "мохито", "кола"],
                "tropical_cocktails": ["пина_колада", "блю_курасао"],
            },
        },
        "vanilla_flavors": {
            "code": {
                "code_prefixes": ["11_01", "11_05"],
                "code_suffixes": ["K", "C", "S", "555", "556", "558", "77", "luxe"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["низкая_0_3_0_8", "средняя_1_0_1_5", "высокая_1_5_2_5", "очень_высокая_2_5_3_0"],
            },
            "name": {
                "vanilla_series": ["ванилин", "ваниль", "ванильно_сливочный", "ваниль_пломбир"],
                "series_modifiers": ["555", "556", "558", "77", "lux", "S", "C"],
            },
        },
        "chocolate_flavors": {
            "code": {
                "code_prefixes": ["10_01", "11_01"],
                "code_suffixes": ["B", "G", "N", "PG", "S"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["низкая_0_4_0_8", "средняя_0_8_1_5", "высокая_1_5_2_5", "очень_высокая_2_5_3_0"],
            },
            "name": {
                "chocolate_profiles": ["шоколад", "шоколадно_ореховый", "горький", "молочный", "печенье"],
                "vanilla_combo_profiles": ["ваниль_шоколад", "фондю", "брауни"],
            },
        },
        "caramel_and_cream_flavors": {
            "code": {
                "code_prefixes": ["10_01", "11_01", "11_02"],
                "code_suffixes": ["A", "K", "TR"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["низкая_0_5_1_2", "средняя_1_0_1_5", "высокая_1_5_2_5", "очень_высокая_2_5_plus"],
            },
            "name": {
                "dessert_clusters": ["крем", "тоффи", "мед", "брюле"],
            },
        },
        "other_dessert_flavors": {
            "code": {
                "code_prefixes": ["10_01", "11_01", "11_02"],
                "code_suffixes": ["TR", "K", "C", "PT"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["микро_0_15_0_9", "низкая_1_0_1_5", "средняя_1_5_2_5"],
            },
            "name": {
                "dessert_clusters": ["баблгам", "бисквит", "кукурузные_палочки", "пломбир", "чизкейк", "тутти_фрутти", "тыква"],
            },
        },
        "nuts_and_grains": {
            "code": {
                "code_prefixes": ["11_01", "11_02"],
                "code_suffixes": ["TR", "PG", "S"],
            },
            "dosage": {
                "application_contexts": ["bakery_products", "confectionery_products", "fillings_and_toppings"],
                "dosage_flags": ["эксп"],
                "dosage_bands": ["низкая_0_5_1_0", "средняя_1_0_1_5", "высокая_1_5_2_5", "очень_высокая_2_5_plus"],
            },
            "name": {
                "nut_clusters": ["миндаль", "арахис", "фисташка", "орех_пекан", "лесной_орех", "горький_миндаль"],
            },
        },
    },
    "denfai_improver_collection.json": {
        "improvers": {
            "code": {
                "code_prefixes": ["10", "11", "13", "15", "17", "18", "20", "21", "22", "23", "26", "28", "61", "70", "71"],
                "code_modifiers": ["П", "В", "N"],
                "code_special_tags": ["массовая_доля_жира_40"]
            },
            "dosage": {
                "dosage_bands": ["микро_0_1_0_3", "низкая_0_3_0_6", "средняя_0_5_1_5", "высокая_1_5_3_0", "очень_высокая_5_10"],
                "dosage_flags": ["зависит_от_технологии"],
            },
            "name": {
                "product_focus": [
                    "кексы",
                    "печенье",
                    "пряники",
                    "круассаны",
                    "хлеб",
                    "макаронные",
                    "слойка",
                    "сдоба",
                    "вафли",
                    "маффины",
                    "лаваш",
                    "бисквит",
                    "сырная",
                    "маргарин",
                ],
                "functional_targets": [
                    "объем",
                    "свежесть",
                    "против_плесени",
                    "разрыхлитель",
                    "софт",
                    "экстра",
                    "мякиш",
                    "классика",
                ],
                "format_modifiers": ["порошок", "комплекс", "жидкий", "люкс"]
            },
        },
    },
    "dry_mix_collection.json": {
        "dry_mixes": {
            "code": {
                "code_prefixes": ["111", "15", "19", "21", "24", "26"],
                "code_suffixes": ["Р", "Т"],
            },
            "dosage": {
                "application_contexts": ["масса_теста", "масса_муки", "рецептура", "восстановление_водой"],
                "dosage_bands": ["низкая_2_5", "средняя_5_10", "высокая_10_15", "очень_высокая_20_50", "соотношение_смесь_вода"],
                "dosage_flags": ["информация_отсутствует"],
            },
            "name": {
                "product_types": [
                    "смесь_для_бисквита",
                    "смесь_для_маффинов",
                    "смесь_для_печенья",
                    "смесь_для_пончиков",
                    "смесь_для_хлеба",
                    "смесь_для_выпечки",
                    "сухая_смесь",
                    "концентрат",
                    "супер_пицца",
                ],
                "flavor_modifiers": ["банан", "лимон", "шоколад", "карамель", "мед", "ваниль", "йогурт", "чесночная", "творог", "сливки", "абрикос"],
                "brand_series": ["классика", "летний_вальс", "максипроф"],
            },
        },
    },
    "filling_collection.json": {
        "vegetable": {
            "code": {
                "code_prefixes": ["N"],
                "code_series": ["805", "810", "815", "820", "825", "830", "870", "876", "885"],
            },
            "name": {
                "vegetable_profiles": ["огурец", "томат", "горчица"],
                "spice_herb_clusters": ["чеснок", "зелень", "базилик", "итальянские_травы", "паприка", "лук", "укроп", "петрушка"],
                "umami_clusters": ["грибы"],
            },
        },
        "cocoa_substitute_nonlauric": {
            "code": {
                "code_series": ["series_200", "series_280", "series_700"],
            },
            "dispersity": {
                "dispersity_levels": ["88%", "95%", "96%"],
            },
            "name": {
                "flavor_clusters": ["ваниль", "шоколад", "орех", "пломбир", "мята", "пина_колада", "клубника"],
                "brand_tags": ["классика"],
            },
            "viscosity": {
                "viscosity_bands": ["низкая_2_5_3_5Па", "средняя_5_6Па", "повышенная_6_8Па", "высокая_8_9Па"],
                "viscosity_flags": ["нет_данных"],
            },
        },
        "cocoa_substitute_lauric": {
            "code": {
                "code_series": ["series_200", "series_700"],
            },
            "dispersity": {
                "dispersity_levels": ["95%", "96%"],
            },
            "name": {
                "flavor_clusters": ["карамель", "пломбир", "шоколадный_трюфель", "классика"],
            },
            "viscosity": {
                "viscosity_bands": ["низкая_2_4_3_7Па", "повышенная_7_8Па"],
            },
        },
        "cream_thermostable": {
            "code": {
                "code_prefixes": ["T", "D", "TN", "ФБ"],
                "code_modifiers": ["Nat", "B", "ч", "серия_200", "серия_201", "серия_202", "серия_205", "серия_217", "серия_220", "серия_265", "серия_270", "серия_325", "серия_875"],
            },
            "mass_fraction_fat": {
                "fat_levels": ["9_2_percent"],
            },
            "mass_fraction_solids": {
                "solids_levels": ["70_plusminus_2"],
            },
            "name": {
                "flavor_clusters": ["ягодные", "фруктовые", "карамельные", "ванильные", "кофейные", "ореховые", "йогуртовые", "экзотические"],
                "format_modifiers": ["Д", "Т", "Nat", "ФБ", "с_кусочками", "с_орехом"],
                "brand_tags": ["классика", "денфрут"],
            },
        },
        "cream_non_thermostable": {
            "CB": {
                "cb_flags": ["минимум_76"],
            },
            "code": {
                "code_prefixes": ["N", "K"],
                "code_modifiers": ["Nat"],
                "code_series": ["series_200", "series_400", "series_500", "series_600", "series_700", "series_900"],
            },
            "name": {
                "flavor_clusters": ["ягодные", "фруктовые", "цитрусовые", "яблочные", "экзотические", "смородина", "клюква", "чернослив"],
                "format_modifiers": ["Nat", "с_кусочками", "с_ягодой"],
            },
        },
        "fruit_thermostable_heterogeneous": {
            "code": {
                "code_prefixes": ["T"],
                "code_modifiers": ["Nat"],
                "code_series": ["series_001_145", "series_200", "series_400", "series_420_450", "series_788"],
            },
            "name": {
                "flavor_clusters": ["ягодные", "косточковые", "цитрусовые", "яблочные", "экзотические"],
                "format_modifiers": ["Nat", "с_кусочками", "с_ягодой", "с_цедрой"],
                "brand_tags": ["денфрут"],
            },
            "thermostability": {
                "thermostability_levels": ["98_100_220c_10мин"],
                "thermostability_flags": ["информация_отсутствует"],
            },
        },
        "fruit_non_thermostable": {
            "CB": {
                "cb_flags": ["минимум_76"],
            },
            "code": {
                "code_prefixes": ["N", "K"],
                "code_modifiers": ["Nat"],
                "code_series": ["series_200", "series_400", "series_500", "series_600", "series_700", "series_900"],
            },
            "name": {
                "flavor_clusters": ["ягодные", "фруктовые", "цитрусовые", "яблочные", "экзотические", "смородина", "клюква", "чернослив"],
                "format_modifiers": ["Nat", "с_кусочками", "с_ягодой"],
            },
            "thermostability": {
                "thermostability_flags": ["информация_отсутствует"],
            },
        },
    },
    "structurant_collection_final.json": {
        "filling_stabilizers": {
            "dosage": {
                "dosage_bands": ["низкая_1_0_1_5"]
            },
            "name": {
                "brand_tags": ["гелеон"],
                "product_types": ["стабилизатор"],
            },
        },
        "agars": {
            "dosage": {
                "dosage_bands": ["7_12_кг_т"],
                "dosage_flags": ["нет_данных"],
            },
            "name": {
                "brand_tags": ["denagar"],
            },
            "valence_jelly_strength": {
                "strength_bands": ["1600_1900", "2100_plus"],
                "strength_flags": ["нет_данных"],
            },
        },
        "pectins": {
            "dosage": {
                "dosage_bands": ["1_2_2_0_percent"],
            },
            "esterification_degree": {
                "esterification_levels": ["58_62_percent"],
            },
            "name": {
                "product_types": ["пектин"],
                "brand_tags": ["мрс_105"],
            },
        },
        "carrageenans": {
            "dosage": {
                "dosage_bands": ["0_4_2_0_percent"],
            },
            "name": {
                "brand_tags": ["гелеон"],
                "product_types": ["комплексная_добавка"],
            },
        },
        "collagen": {
            "amino_acids": {
                "amino_acid_count": ["16"],
            },
            "dosage": {
                "dosage_levels": ["от_3_percent", "от_5_percent"],
            },
            "mineral_content": {
                "mineral_levels": ["2_percent"],
            },
            "moisture_content": {
                "moisture_levels": ["6_percent"],
            },
            "name": {
                "brand_tags": ["классика"],
                "source_profiles": ["говяжий"]
            },
            "protein_content": {
                "protein_levels": ["92_percent"],
            },
        },
    },
    "technological_aid_collection.json": {
        "aids": {
            "code": {
                "code_series": ["10", "11", "13", "17", "18", "22", "30"],
                "code_brand_tags": ["denfai"],
            },
            "dosage": {
                "application_contexts": ["масса_муки", "грамм_на_100кг"],
                "dosage_bands": ["микро_0_1_0_5", "низкая_0_5_1_0", "средняя_1_0_2_0", "высокая_3_15г"],
            },
            "name": {
                "product_focus": ["батон", "булочка", "круассаны", "хлеб", "вафли", "бриошь", "пшеничный"],
                "functional_targets": ["объем", "мягкость", "стабильность", "свежесть", "релакс", "протеаза"],
            },
        },
    },
}

# Alias used by generic loaders that expect `enum_mapping` symbol.
enum_mapping = BAKERY_ENUM_MAPPING
