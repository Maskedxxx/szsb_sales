"""Описание JSON-файлов пекарского направления для маппинга ключей."""

from __future__ import annotations

from typing import Any, Dict


# Наименование ключей соответствует файлам в ``app/routes/bakery``.
BAKERY_KEYS_MAPPING: Dict[str, Dict[str, Any]] = {
    "classic_confectionery_collection.json": {
        "file_description": "The `classic_confectionery_collection.json` file presents foundational semi-finished ingredients such as tempered chocolate, non-tempered glazes, and confectionery masses used to build classic sweets portfolios.",
        "product_keys": {
            "color": {
                "description": "Цветовая группа полуфабриката (темный, молочный, белый, цветной) с указанием визуального результата глазирования.",
                "filter_impact": "Помогает подбирать шоколад и глазурь под требуемую гамму изделия, например выделять белые варианты для фигур или темные для батончиков.",
                "data_type": "string",
            },
            "grinding_degree": {
                "description": "Степень измельчения массы, выраженная как процент прохождения через сито или эквивалентная оценка текстуры.",
                "filter_impact": "Позволяет находить продукты с заданной мелкодисперсной структурой для гладких глазурей либо с пониженной степенью помола.",
                "data_type": "string",
            },
            "name": {
                "description": "Коммерческое название рецептуры (серия «Классика» с порядковыми номерами и пометками, например «без сахара» или «термокапли»).",
                "filter_impact": "Фильтрует ассортимент по конкретным артикулам и модификациям, упрощая выбор нужного полуфабриката.",
                "data_type": "string",
            },
            "type": {
                "description": "Технологический тип изделия: темперируемый шоколад, глазурь на эквиваленте масла какао либо кондитерская масса.",
                "filter_impact": "Сегментирует позиции по режиму применения (формование, покрытие, начинка) и по используемым жирным основам.",
                "data_type": "string",
            },
            "viscosity": {
                "description": "Диапазон пластической вязкости (включая значения по Кассону) либо отметка об отсутствии данных.",
                "filter_impact": "Дает возможность выделять массы с подходящей текучестью для глазирования, формования или работы в капельном формате.",
                "data_type": "string",
            },
        },
    },
    "cocoa_collection.json": {
        "file_description": "The `cocoa_collection.json` file combines cocoa powder substitutes and cocoa-based ingredients that replicate natural and alkalized profiles while supporting fillings, glazes, baked goods, and aerated confectionery.",
        "product_keys": {
            "is_gost_compliant": {
                "description": "Признак соответствия позиции требованиям ГОСТ (True/False).",
                "filter_impact": "Позволяет отделить продукты с подтвержденным соответствием национальному стандарту, что важно для регуляторных или тендерных требований.",
                "data_type": "boolean",
            },
            "name": {
                "description": "Название какао-содержащего ингредиента или комплексной добавки с указанием бренда (TULIP, GOLDEN HARVEST, ZLK, Денмальт).",
                "filter_impact": "Позволяет находить конкретные артикула какао-порошков, масел или заменителей под нужную рецептуру.",
                "data_type": "string",
            },
        },
    },
    "colorant_collection.json": {
        "file_description": "The `colorant_collection.json` file gathers natural, caramel, and synthetic pigments engineered for bakery and confectionery applications where consistent appearance and dosing precision are critical.",
        "product_keys": {
            "dosage": {
                "description": "Рекомендуемый диапазон внесения красителя в готовый продукт (кг на тонну либо аналогичные указания).",
                "filter_impact": "Позволяет сравнивать интенсивность красителей и подобрать варианты с низким расходом или, наоборот, высокую насыщенность.",
                "data_type": "string",
            },
            "name": {
                "description": "Коммерческое название красителя ESCO® или натурального пигмента с указанием формы (порошок, жидкий, эмульсия).",
                "filter_impact": "Фильтрует по конкретным линейкам и разновидностям, облегчая подбор необходимого оттенка или формата.",
                "data_type": "string",
            },
            "sv": {
                "description": "Массовая доля сухих веществ либо пигментная насыщенность, указанная в процентах.",
                "filter_impact": "Даёт возможность отобрать красители с требуемой концентрацией для расчёта дозировок и стабильности оттенка.",
                "data_type": "string",
            },
            "type": {
                "description": "Физическая форма и носитель красителя (порошок, жирорастворимая жидкость, маслянистая система и т.п.).",
                "filter_impact": "Помогает выбирать красители с нужной технологической совместимостью (для жировых глазурей, водных сиропов, аэрозолей).",
                "data_type": "string",
            },
        },
    },
    "delar_collection.json": {
        "file_description": "The `delar_collection.json` file showcases the DELAR® flavor portfolio with gastronomic boosters, fruit and juice tones, emulsions, and sweet profiles tailored to modern pastry product development.",
        "product_keys": {
            "code": {
                "description": "Артикул или код вкусоароматической композиции DELAR® (формат 11.xx.xxx с дополнительными индексами).",
                "filter_impact": "Обеспечивает точный поиск по номенклатуре при подборе конкретного вкуса или при оформлении заказа.",
                "data_type": "string",
            },
            "dosage": {
                "description": "Рекомендуемый диапазон применения композиции в рецептуре (в % от массы или г/кг).",
                "filter_impact": "Позволяет сопоставлять интенсивность ароматов и выбирать решения с подходящей силой вкуса.",
                "data_type": "string",
            },
            "name": {
                "description": "Название вкусоароматической ноты (брынза, ряженка, сливки, специи и т.д.).",
                "filter_impact": "Используется для быстрого подбора вкусовых профилей под целевой продукт (сырный, десертный, специевый).",
                "data_type": "string",
            },
        },
    },
    "denfai_improver_collection.json": {
        "file_description": "The `denfai_improver_collection.json` file enumerates dough improvers aimed at boosting gas retention, loaf volume, crumb softness, and shelf life for industrial bakery formulas.",
        "product_keys": {
            "code": {
                "description": "Каталожный код улучшителя DENFAI® (формат 10.xx или 11.xx с буквенными индексами).",
                "filter_impact": "Уточняет конкретную модификацию при подборе или заказе комплекса для заданной технологии.",
                "data_type": "string",
            },
            "dosage": {
                "description": "Рекомендуемый расход улучшителя на 100 кг муки либо указание «в зависимости от технологии».",
                "filter_impact": "Сравнивает активность продуктов и помогает выбрать смеси с нужной интенсивностью воздействия.",
                "data_type": "string",
            },
            "name": {
                "description": "Название функционального комплекса (Свежесть, Сдоба и слойка, Софт брэд и т.п.).",
                "filter_impact": "Фильтрует решения под требуемый эффект: продление свежести, увеличение объема, работа с замороженным тестом.",
                "data_type": "string",
            },
        },
    },
    "dry_mix_collection.json": {
        "file_description": "The `dry_mix_collection.json` file catalogs dry mixes for donuts, flavored bread, custards, whipped toppings, and fillings that shorten preparation time while keeping microbial safety and quality.",
        "product_keys": {
            "code": {
                "description": "Идентификационный номер сухой смеси (трёхзначные и дробные значения с буквенными индексами).",
                "filter_impact": "Облегчает сопоставление с внутренним ассортиментом и исключает путаницу между похожими названиями.",
                "data_type": "string",
            },
            "dosage": {
                "description": "Нормы внесения смеси относительно муки или теста (проценты, кг на партию).",
                "filter_impact": "Позволяет выбрать решения под желаемую интенсивность вкуса и технологический режим (бисквит, пончики, хлеб).",
                "data_type": "string",
            },
            "name": {
                "description": "Название сухой смеси с указанием назначения (бисквит, пончики, пудра, крем).",
                "filter_impact": "Уточняет сегментацию по типу изделия и вкусовому профилю для быстрого подбора.",
                "data_type": "string",
            },
        },
    },
    "filling_collection.json": {
        "file_description": "The `filling_collection.json` file structures fruit, vegetable, and creamy fillings—including plant-fat and cocoa-butter systems—for thermostable and delicate bakery uses.",
        "product_keys": {
            "CB": {
                "description": "Массовая доля сухих веществ (°Brix) в фруктовой начинке — минимальное значение в процентах.",
                "filter_impact": "Помогает выделить начинки с высоким содержанием сухих веществ для длительной свежести и устойчивости при выпечке.",
                "data_type": "string",
            },
            "code": {
                "description": "Каталожный код начинки или крема (формат K xxx.xx Nat, N xxx.xx и т.п.).",
                "filter_impact": "Позволяет быстро отобрать конкретный рецепт или вкус по внутреннему артикулу.",
                "data_type": "string",
            },
            "dispersity": {
                "description": "Доля измельчённых частиц, проходящих через сито (процент дисперсности).",
                "filter_impact": "Даёт возможность подобрать начинку с нужной текстурой — от гладкой до содержащей заметные включения.",
                "data_type": "string",
            },
            "mass_fraction_fat": {
                "description": "Массовая доля жира в начинке, указанная в процентах.",
                "filter_impact": "Упрощает выбор между более лёгкими фруктовыми вариантами и насыщенными жировыми кремами.",
                "data_type": "string",
            },
            "mass_fraction_solids": {
                "description": "Массовая доля сухих веществ (без жира) с допустимым отклонением.",
                "filter_impact": "Позволяет фильтровать продукты по стабильности и плотности сиропной фазы.",
                "data_type": "string",
            },
            "name": {
                "description": "Название начинки с указанием вкуса и номера рецептуры.",
                "filter_impact": "Используется для выбора вкусовых профилей (грибы, ягоды, орехи, цитрус и др.).",
                "data_type": "string",
            },
            "thermostability": {
                "description": "Отметка о термостабильности: процент сохранения массы после выпечки или отсутствие данных.",
                "filter_impact": "Позволяет отделить начинки, пригодные для высоких температур (до 220 °C), от вариантов для холодного применения.",
                "data_type": "string",
            },
            "viscosity": {
                "description": "Диапазон вязкости начинки в Паскаль-секундах или спецпометка (например, «-» при отсутствии данных).",
                "filter_impact": "Помогает подобрать консистенцию под дозирование: насосное нанесение, отсадка, прослойки.",
                "data_type": "string",
            },
        },
    },
    "structurant_collection_final.json": {
        "file_description": "The `structurant_collection_final.json` file spans agar, pectin, carrageenan, stabilizers, and hydrolyzed collagen that manage gelation, moisture, and texture in layered confectionery and dairy systems.",
        "product_keys": {
            "amino_acids": {
                "description": "Количество аминокислот в составе гидролизованного коллагена (шт.).",
                "filter_impact": "Позволяет выделять коллаген с заданным аминокислотным профилем для функциональных продуктов.",
                "data_type": "string",
            },
            "dosage": {
                "description": "Рекомендуемый уровень применения структурирующего агента (проценты, кг/т и т.п.).",
                "filter_impact": "Помогает подобрать добавку с нужной гелеобразующей силой и экономичностью.",
                "data_type": "string",
            },
            "esterification_degree": {
                "description": "Степень этерификации пектина, указанная в процентах.",
                "filter_impact": "Даёт возможность отобрать пектины высоко- или низкоэтерифицированные в зависимости от желируемой структуры.",
                "data_type": "string",
            },
            "mineral_content": {
                "description": "Содержание минеральных веществ в продукте, %.",
                "filter_impact": "Актуально при выборе коллагена и стабилизаторов с ограничениями по зольности.",
                "data_type": "string",
            },
            "moisture_content": {
                "description": "Массовая доля влаги (процент).",
                "filter_impact": "Позволяет учитывать гигроскопичность и условия хранения структурообразователей.",
                "data_type": "string",
            },
            "name": {
                "description": "Название стабилизатора, агара, пектина или коллагена с брендом.",
                "filter_impact": "Обеспечивает выбор конкретной системы для желирования, стабилизации начинок или укрепления структуры.",
                "data_type": "string",
            },
            "protein_content": {
                "description": "Массовая доля белка, % (характерно для гидролизованного коллагена).",
                "filter_impact": "Помогает отличить белковые структурообразователи от углеводных.",
                "data_type": "string",
            },
            "valence_jelly_strength": {
                "description": "Сила желирования (валентная прочность геля), выраженная в г/см.",
                "filter_impact": "Позволяет подобрать агент с требуемой прочностью геля под конфеты, начинки или десерты.",
                "data_type": "string",
            },
        },
    },
    "technological_aid_collection.json": {
        "file_description": "The `technological_aid_collection.json` file groups technological aids (TVS) that condition dough, improve extensibility, support frozen workflows, and extend freshness in industrial baking.",
        "product_keys": {
            "code": {
                "description": "Артикул технологического вспомогательного средства DENFAI (формат xx.xx).",
                "filter_impact": "Уточняет конкретную формулу комплекса при заказе и в технологических картах.",
                "data_type": "string",
            },
            "dosage": {
                "description": "Рекомендуемый расход на 100 кг муки или теста.",
                "filter_impact": "Позволяет подобрать средство под требуемую степень воздействия на тесто и экономику рецептуры.",
                "data_type": "string",
            },
            "name": {
                "description": "Название вспомогательной добавки (Протеаза, Релакс, Экосвежесть и т.д.).",
                "filter_impact": "Даёт возможность фильтровать продукты по назначению: ферментное смягчение, сохранение свежести, работа с заморозкой.",
                "data_type": "string",
            },
        },
    },
}


# Используется для быстрого определения исходного файла по имени секции.
KEY_TO_FILE_MAPPING: Dict[str, str] = {
    "chocolate": "classic_confectionery_collection.json",
    "glaze": "classic_confectionery_collection.json",
    "confectionery_mass": "classic_confectionery_collection.json",
    "natural": "colorant_collection.json",
    "caramel": "colorant_collection.json",
    "synthetic": "colorant_collection.json",
    "gastronomic_flavors": "delar_collection.json",
    "juice_based_flavors": "delar_collection.json",
    "flavor_bases": "delar_collection.json",
    "aromatic_emulsions": "delar_collection.json",
    "flavor_additives": "delar_collection.json",
    "spice_blends_and_extracts": "delar_collection.json",
    "spices_and_herbs": "delar_collection.json",
    "berries": "delar_collection.json",
    "fruits": "delar_collection.json",
    "effects": "delar_collection.json",
    "coffee_and_dessert_flavors": "delar_collection.json",
    "dairy_products": "delar_collection.json",
    "nut_and_cream_flavors": "delar_collection.json",
    "beverages": "delar_collection.json",
    "vanilla_flavors": "delar_collection.json",
    "chocolate_flavors": "delar_collection.json",
    "caramel_and_cream_flavors": "delar_collection.json",
    "other_dessert_flavors": "delar_collection.json",
    "nuts_and_grains": "delar_collection.json",
    "vegetable": "filling_collection.json",
    "cocoa_substitute_nonlauric": "filling_collection.json",
    "cocoa_substitute_lauric": "filling_collection.json",
    "cream_thermostable": "filling_collection.json",
    "cream_non_thermostable": "filling_collection.json",
    "fruit_thermostable_heterogeneous": "filling_collection.json",
    "fruit_non_thermostable": "filling_collection.json",
    "filling_stabilizers": "structurant_collection_final.json",
    "agars": "structurant_collection_final.json",
    "pectins": "structurant_collection_final.json",
    "carrageenans": "structurant_collection_final.json",
    "collagen": "structurant_collection_final.json",
}
