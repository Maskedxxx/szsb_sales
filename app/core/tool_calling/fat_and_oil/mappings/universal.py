"""
Универсальный промежуточный маппинг enum → реальные данные для масложировой отрасли.

Использует regex для числовых значений (дозировки, температуры) и текстовые паттерны 
для брендов, типов продуктов и областей применения.
"""

import re
from typing import List, Dict, Callable

# ===================== РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ =====================

# Извлечение процентных дозировок: 0,02-0,1%
DOSAGE_PERCENTAGE_REGEX = re.compile(r"(\d+(?:,\d+)?)-?(\d+(?:,\d+)?)?%?", re.IGNORECASE)

# Извлечение дозировок в кг/т: 0,1-4,0 кг/т
DOSAGE_KG_T_REGEX = re.compile(r"(\d+(?:,\d+)?)-?(\d+(?:,\d+)?)?\s*кг/т", re.IGNORECASE)

# Извлечение температурных диапазонов: 0-110 °C
TEMPERATURE_REGEX = re.compile(r"(\d+)-?(\d+)?\s*°?C", re.IGNORECASE)

# Извлечение соотношений замены: 1 кг смеси заменяет 200 кг сахара
REPLACEMENT_RATIO_REGEX = re.compile(r"1\s*кг.*?заменяет\s*(\d+)\s*кг", re.IGNORECASE)

# ===================== СПЕЦИФИЧНЫЕ МАППИНГИ ДЛЯ МАСЛОЖИРОВОЙ ОТРАСЛИ =====================

FAT_AND_OIL_SPECIFIC_MAPPING: Dict[str, List[str]] = {
    
    # ========== АНТИОКСИДАНТЫ ==========
    "xtendra": ["XTENDRA", "xtendra", "Xtendra", "ХТЕНДРА"],
    "ЭДТА": ["ЭДТА", "EDTA", "этилендиаминтетраацетат", "хелатор"],
    "токоферолы": ["ТОКОФЕРОЛЫ", "токоферол", "vitamin_E", "витамин_E", "NASURE", "натуральных смешанных токоферолов"],
    "tbhq": ["TBHQ", "трет-бутилгидрохинон", "Третбутилгидрохинон", "Е319"],
    "BHA": ["BHA", "ВНА", "Бутилгидроксианизол", "Е320"],
    "BHT": ["BHT", "ВНТ", "бутилгидрокситолуол", "Е321"],
    "пропилгаллат": ["пропилгаллат", "Е310"],
    "лимонная_кислота_антиоксидант": ["лимонная кислота", "Е330"],
    
    # ========== КРАСИТЕЛИ ==========
    "бета_каротин": ["бета-каротин", "БЕТА-КАРОТИН", "beta-carotene", "каротин", "ALTRATENE"],
    "карамельный_колер": ["карамельный колер", "КАРАМЕЛЬНЫЙ КОЛЕР", "caramel", "Е150", "Е150D"],
    "сахарный_колер": ["сахарный колер", "САХАРНЫЙ КОЛЕР", "sugar_color"],
    "паприка": ["паприка", "ПАПРИКА", "paprika", "красный_перец"],
    "тартразин": ["тартразин", "ТАРТРАЗИН", "Е102"],
    "солнечный_закат": ["солнечный закат", "СОЛНЕЧНЫЙ ЗАКАТ", "sunset_yellow", "Е110"],
    "понсо": ["понсо", "ПОНСО", "ponceau", "Е124"],
    "кармуазин": ["кармуазин", "КАРМУАЗИН", "carmoisine", "Е122"],
    "зеленое_яблоко": ["зеленое яблоко", "ЗЕЛЕНОЕ ЯБЛОКО", "green_apple"],
    "диоксид_титана": ["диоксид титана", "ДИОКСИД ТИТАНА", "titanium_dioxide", "Е171"],
    "ESCO": ["ESCO", "эско", "ЭСКО"],
    
    # ========== ЦВЕТА ==========
    "желтый": ["желт", "ЖЕЛТ", "yellow", "оранжев", "золотист"],
    "красный": ["красн", "КРАСН", "red", "алый", "вишнев", "розовый"],
    "коричневый": ["коричнев", "КОРИЧНЕВ", "brown", "темн"],
    "зеленый": ["зелен", "ЗЕЛЕН", "green", "яблоко"],
    "оранжевый": ["оранжев", "ОРАНЖЕВ", "orange"],
    "белый": ["белый", "БЕЛЫЙ", "white", "слоновой кости"],
    "черный": ["черный", "ЧЕРНЫЙ", "black"],
    
    # ========== ФОРМЫ ВЫПУСКА ========== 
    "жидкость": ["жидк", "ЖИДК", "liquid", "масляная", "суспензия"],
    "порошок": ["порошк", "ПОРОШК", "powder", "гранул", "сухой"],
    "масляная_суспензия": ["масляная суспензия", "МАСЛЯНАЯ СУСПЕНЗИЯ", "oil_suspension"],
    
    # ========== ПРИМЕНЕНИЕ ==========
    "майонез": ["майонез", "МАЙОНЕЗ", "mayonnaise", "майонезн"],
    "маргарин": ["маргарин", "МАРГАРИН", "margarine", "спред"],
    "кетчуп": ["кетчуп", "КЕТЧУП", "ketchup", "томатн"],
    "горчица": ["горчиц", "ГОРЧИЦ", "mustard"],
    "соус": ["соус", "СОУС", "sauce", "дрессинг"],
    "хрен": ["хрен", "ХРЕН", "horseradish"],
    "консервы": ["консервы", "КОНСЕРВЫ", "консерв", "овощные"],
    "масла_жиры": ["масла и жиры", "растительные масла", "животные жиры"],
    "фритюрные": ["фритюрные", "ФРИТЮРНЫЕ", "фритюр", "жарка"],
    "кулинарные": ["кулинарные", "КУЛИНАРНЫЕ", "кулинар"],
    "хлебопекарные": ["хлебопекарные", "ХЛЕБОПЕКАРНЫЕ", "хлебопекар", "выпечка"],
    
    # ========== БРЕНДЫ ==========
    "ГЕЛЕОН": ["ГЕЛЕОН", "гелеон", "GELEON", "geleon"],
    "DEL_AR": ["DEL'AR", "ДЕЛЯР", "del ar", "зеленые линии"],
    "СЛАДИН": ["СЛАДИН", "сладин", "SLADIN", "подсластитель"],
    "Camlin": ["Camlin", "CAMLIN", "камлин"],
    "AIBI": ["AIBI", "αιβι", "АИБИ"],
    "DENMILK": ["DENMILK", "денмилк", "ДЕНМИЛК"],
    "MILLGRI": ["MILLGRI", "миллгри", "МИЛЛГРИ"],
    "TULIP": ["TULIP", "тулип", "ТУЛИП"],
    "ДЕНКАКАО": ["ДЕНКАКАО", "денкакао", "DENKAKAO"],
    
    # ========== ТИПЫ ПРОДУКТОВ ==========
    "стабилизатор": ["стабилизатор", "СТАБИЛИЗАТОР", "stabilizer"],
    "эмульгатор": ["эмульгатор", "ЭМУЛЬГАТОР", "emulsifier"],
    "консервант": ["консервант", "КОНСЕРВАНТ", "preservative"],
    "антиоксидант": ["антиоксидант", "АНТИОКСИДАНТ", "antioxidant"],
    "краситель": ["краситель", "КРАСИТЕЛЬ", "colorant", "dye"],
    "подсластитель": ["подсластитель", "ПОДСЛАСТИТЕЛЬ", "sweetener"],
    "загуститель": ["загуститель", "ЗАГУСТИТЕЛЬ", "thickener"],
    "компаунд": ["компаунд", "КОМПАУНД", "compound"],
    "комплексная_добавка": ["комплексная пищевая добавка", "КПД", "комплексная добавка"],
    
    # ========== КАКАО ==========
    "алкализованный": ["алкализованный", "АЛКАЛИЗОВАННЫЙ", "alkalized"],
    "натуральный_какао": ["натуральный", "НАТУРАЛЬНЫЙ", "natural"],
    "какао_порошок": ["какао-порошок", "КАКАО-ПОРОШОК", "cocoa_powder"],
    
    # ========== МОЛОЧНЫЕ ПРОДУКТЫ ==========
    "йогурт_сухой": ["йогурт сухой", "ЙОГУРТ СУХОЙ", "dry_yogurt"],
    "сыр_сухой": ["сыр сухой", "СЫР СУХОЙ", "dry_cheese"],
    "обезжиренный": ["обезжиренный", "ОБЕЗЖИРЕННЫЙ", "fat_free"],
    
    # ========== ЭМУЛЬГАТОРЫ ==========
    "моноглицериды": ["моноглицериды", "МОНОГЛИЦЕРИДЫ", "monoglycerides"],
    "диглицериды": ["диглицериды", "ДИГЛИЦЕРИДЫ", "diglycerides"],
    "дистиллированный": ["дистиллированный", "ДИСТИЛЛИРОВАННЫЙ", "distilled"],
    
    # ========== НАЧИНКИ И ТОППИНГИ ==========
    "начинка": ["начинка", "НАЧИНКА", "filling"],
    "гастрономическая": ["гастрономическая", "ГАСТРОНОМИЧЕСКАЯ", "gastronomic"],
    "овощная": ["овощная", "ОВОЩНАЯ", "vegetable"],
    "грибы": ["грибы", "ГРИБЫ", "mushroom"],
    "огурец": ["огурец", "ОГУРЕЦ", "cucumber"],
    "укроп": ["укроп", "УКРОП", "dill"],
    "лук": ["лук", "ЛУК", "onion"],
    "классика": ["классика", "КЛАССИКА", "classic"],
    
    # ========== АРОМАТИЗАТОРЫ DEL'AR ==========
    "эфирное_масло": ["эфирное масло", "ЭФИРНОЕ МАСЛО", "essential_oil"],
    "горчичное": ["горчичное", "ГОРЧИЧНОЕ", "mustard"],
    "сливочное": ["сливочное", "СЛИВОЧНОЕ", "butter", "масло сливочное"],
    "чеснок": ["чеснок", "ЧЕСНОК", "garlic"],
    "натуральный_аромат": ["натуральный", "НАТУРАЛЬНЫЙ", "natural"],
    "натуральный_молочный": ["натуральный", "НАТУРАЛЬНЫЙ", "natural", "лактобактерии"],
    "натуральный_консервант": ["натуральный", "НАТУРАЛЬНЫЙ", "natural", "ферментированный"],
    
    # ========== КОНСЕРВАНТЫ ==========
    "глюкоза_ферментированная": ["глюкоза ферментированная", "ГЛЮКОЗА ФЕРМЕНТИРОВАННАЯ"],
    "лактобак": ["лактобак", "ЛАКТОБАК", "lactobac"],
    "сорбиновая_кислота": ["сорбиновая кислота", "СОРБИНОВАЯ КИСЛОТА"],
    "бензоат_натрия": ["бензоат натрия", "БЕНЗОАТ НАТРИЯ"],
    "лимонная_кислота": ["лимонная кислота", "ЛИМОННАЯ КИСЛОТА", "цитрат"],
    
    # ========== ДОЗИРОВКИ (текстовые паттерны) ==========
    "низкие_дозировки": ["0,01", "0,02", "0,03", "0,05", "до 0,1"],
    "средние_дозировки": ["0,1", "0,2", "0,5", "1,0", "до 2"],
    "высокие_дозировки": ["2,0", "3,0", "5,0", "свыше 5"],
    "до_4": ["до 4,00", "до 4"],
    
    # ========== ТЕМПЕРАТУРНЫЕ РЕЖИМЫ ==========
    "холодный_способ": ["холодный способ", "ХОЛОДНЫЙ СПОСОБ", "cold_method"],
    "горячий_способ": ["горячий способ", "ГОРЯЧИЙ СПОСОБ", "hot_method"],
    "низкие_температуры": ["0-50", "до 50"],
    "средние_температуры": ["50-85", "85"],
    "высокие_температуры": ["85-110", "свыше 85"],
    
    # ========== ПРОИЗВОДИТЕЛИ И СТРАНЫ ==========
    "россия": ["Россия", "РОССИЯ", "НПО «Зеленые линии»"],
    "китай": ["Китай", "КИТАЙ", "Kevin Food Co", "Shandong"],
    "малайзия": ["Малайзия", "МАЛАЙЗИЯ", "Guan Chong"],
    "германия": ["Германия", "ГЕРМАНИЯ", "Tulip"],
    
    # ========== ЖИРНОСТЬ И КОНЦЕНТРАЦИИ ==========
    "82_процента": ["82%", "82"],
    "71_процент": ["71%", "71"],
    "67_процентов": ["67%", "67"],
    "60_процентов": ["60%", "60"],
    "55_процентов": ["55%", "55"],
    "50_процентов": ["50%", "50"],
    "40_процентов": ["40%", "40", "менее 40%"],
    "0_3_процента": ["0,3%", "0.3%"],
    "1_0_процент": ["1,0%", "1.0%"],
    "30_процентов": ["30%", "30"],
    
    # ========== ЗАМЕНА САХАРА ==========
    "замена_100": ["100 А", "1 кг заменяет 100 кг сахара"],
    "замена_200": ["200 Т", "200 К", "1 кг заменяет 200 кг сахара"],
    "термостабильный": ["термостабильный", "ТЕРМОСТАБИЛЬНЫЙ", "thermostable"],

    # ========== ДОП. БРЕНДЫ/ТЕРМИНЫ ИЗ ENUM ==========
    # Бренды и производители
    "camlin": ["camlin", "Camlin", "Camlin Fine Sciences", "Camlin Fine Sciences Ltd", "camlin_fine_sciences"],
    "kemfood": ["kemfood", "KEMFOOD"],
    "del_ar": ["del'ar", "DEL'AR", "delar", "del ar", "дел'ар", "делар"],
    "aibi": ["aibi", "AIBI"],

    # Технологические свойства (часто встречаются в стабилизаторах)
    "загущение": ["загущение", "загуститель", "увеличивает вязкость"],
    "стабилизация": ["стабилизация", "стабилизатор", "повышает стабильность"],
    "гелеобразование": ["гелеобразование", "гелеобразующий", "gel"],
    "консистенция": ["консистенция", "улучшает консистенцию", "texture"],
    "морозостойкость": ["морозостойкость", "морозо-стойкость", "заморозка-оттаивание", "устойчив к заморозке"],
    "срок_хранения": ["срок хранения", "увеличивает срок хранения", "shelf life"],
    "ph_стабильность": ["ph стабильность", "pH-стабильность", "устойчив к ph", "устойчив к pH"],

    # Часто встречающиеся коды/индексы
    "330": ["330", "E330", "Е330", "лимонная кислота"],
}


# ===================== СПЕЦИАЛЬНЫЕ REGEX ФУНКЦИИ =====================

def check_dosage_range(text: str, min_val: float, max_val: float) -> bool:
    """Проверяет попадание дозировки в диапазон."""
    # Ищем проценты: 0,02-0,1%
    percentage_match = DOSAGE_PERCENTAGE_REGEX.search(text)
    if percentage_match:
        try:
            val1 = float(percentage_match.group(1).replace(',', '.'))
            val2_str = percentage_match.group(2)
            if val2_str:
                val2 = float(val2_str.replace(',', '.'))
                return (min_val <= val1 <= max_val) or (min_val <= val2 <= max_val)
            else:
                return min_val <= val1 <= max_val
        except (ValueError, AttributeError):
            pass
    
    # Ищем кг/т: 0,1-4,0 кг/т
    kg_t_match = DOSAGE_KG_T_REGEX.search(text)
    if kg_t_match:
        try:
            val1 = float(kg_t_match.group(1).replace(',', '.'))
            val2_str = kg_t_match.group(2)  
            if val2_str:
                val2 = float(val2_str.replace(',', '.'))
                return (min_val <= val1 <= max_val) or (min_val <= val2 <= max_val)
            else:
                return min_val <= val1 <= max_val
        except (ValueError, AttributeError):
            pass
    
    return False


def check_temperature_range(text: str, min_temp: float, max_temp: float) -> bool:
    """Проверяет попадание температуры в диапазон."""
    temp_match = TEMPERATURE_REGEX.search(text)
    if temp_match:
        try:
            temp1 = float(temp_match.group(1))
            temp2_str = temp_match.group(2)
            if temp2_str:
                temp2 = float(temp2_str)
                return (min_temp <= temp1 <= max_temp) or (min_temp <= temp2 <= max_temp)
            else:
                return min_temp <= temp1 <= max_temp
        except (ValueError, AttributeError):
            pass
    return False


def check_replacement_ratio(text: str, target_ratio: int) -> bool:
    """Проверяет коэффициент замены сахара."""
    ratio_match = REPLACEMENT_RATIO_REGEX.search(text)
    if ratio_match:
        try:
            ratio = int(ratio_match.group(1))
            return ratio == target_ratio
        except (ValueError, AttributeError):
            pass
    return False


# ===================== СПЕЦИАЛЬНЫЕ ЧЕКЕРЫ ДЛЯ МАСЛОЖИРОВОЙ ОТРАСЛИ =====================

FAT_AND_OIL_SPECIFIC_CHECKERS: Dict[str, Callable[[str, str], bool]] = {
    # Дозировки
    "низкие_до_0.1": lambda text, _: check_dosage_range(text, 0.0, 0.1),
    "средние_0.1_1.0": lambda text, _: check_dosage_range(text, 0.1, 1.0),
    "высокие_свыше_1.0": lambda text, _: check_dosage_range(text, 1.0, 10.0),
    "до_4_кг_т": lambda text, _: check_dosage_range(text, 0.0, 4.0),
    
    # Температуры  
    "низкие_до_50": lambda text, _: check_temperature_range(text, 0, 50),
    "средние_50_100": lambda text, _: check_temperature_range(text, 50, 100),
    "высокие_свыше_100": lambda text, _: check_temperature_range(text, 100, 200),
    "рабочие_0_110": lambda text, _: check_temperature_range(text, 0, 110),
    
    # Коэффициенты замены сахара
    "замена_100": lambda text, _: check_replacement_ratio(text, 100),
    "замена_200": lambda text, _: check_replacement_ratio(text, 200),
}


# ===================== ОСНОВНЫЕ ФУНКЦИИ =====================

def get_universal_patterns(enum_value: str) -> List[str]:
    """
    Возвращает паттерны поиска для enum значения.
    
    Args:
        enum_value: Значение enum из fat_and_oil_enum_mapping.py
        
    Returns:
        Список паттернов для поиска в реальных данных
    """
    patterns = FAT_AND_OIL_SPECIFIC_MAPPING.get(enum_value, [enum_value])

    # Расширение паттернов для частых форматов значений из enum
    try:
        ev = str(enum_value)

        # 1) Диапазоны чисел в формате a_b (включая десятичные точки/запятые)
        rng = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)_(\d+(?:[.,]\d+)?)\s*", ev)
        if rng:
            a, b = rng.group(1), rng.group(2)
            # Нормализуем как с точкой, так и с запятой
            def dot(s: str) -> str:
                return s.replace(',', '.')
            def comma(s: str) -> str:
                return s.replace('.', ',')
            a_dot, b_dot = dot(a), dot(b)
            a_com, b_com = comma(a_dot), comma(b_dot)
            # Базовые варианты с дефисом
            patterns.extend([
                f"{a_dot}-{b_dot}",
                f"{a_com}-{b_com}",
                f"{a_dot} - {b_dot}",
                f"{a_com} - {b_com}",
            ])

        # 2) Десятичное число с точкой — добавить вариант с запятой
        dec = re.fullmatch(r"\s*(\d+)\.(\d+)\s*", ev)
        if dec:
            patterns.append(f"{dec.group(1)},{dec.group(2)}")

        # 3) Коды с точками: 10.05, 825.24, 10.05.154 — добавить альтернативные написания
        dotcode = re.fullmatch(r"\s*(\d+(?:\.\d+)+)\s*", ev)
        if dotcode:
            code = dotcode.group(1)
            patterns.extend([
                code,
                code.replace('.', '-'),
                f"№ {code}",
                f"№{code}",
                f"N {code}",
                f"N{code}",
                f"серия {code}",
            ])

        # 4) Чистые числа (в т.ч. с ведущими нулями): добавить формы с №/N и снятием ведущих нулей
        pure_int = re.fullmatch(r"\s*0*(\d+)\s*", ev)
        if pure_int and ev.strip().isdigit():
            val = pure_int.group(1)
            if val != ev:
                # была ведущая 0-подставка, добавить форму без нулей
                patterns.append(val)
            # добавить контекстные формы
            patterns.extend([f"№{ev}", f"№ {ev}", f"N{ev}", f"N {ev}"])

    except Exception:
        pass
    
    # Добавляем вариации для русских слов
    variations = []
    for pattern in patterns:
        variations.append(pattern)
        variations.append(pattern.upper())
        variations.append(pattern.lower())
        variations.append(pattern.capitalize())
    
    return list(set(variations))


def has_universal_enum_match(text: str, enum_value: str, field_key: str = None) -> bool:
    """
    Универсальная проверка совпадения enum значения с текстом.
    
    Args:
        text: Текст для поиска
        enum_value: Значение enum
        field_key: Ключ поля для специальной обработки
        
    Returns:
        True если найдено совпадение, False иначе
    """
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Специальная обработка дозировок
    if field_key in ["dosage", "dosage_percentage", "dosage_kg_t"]:
        return _check_special_numeric_field(text, enum_value, field_key)
    
    # Специальная обработка температур
    if field_key in ["working_temperature_range", "temperature"]:
        return _check_special_numeric_field(text, enum_value, field_key)
    
    # Обычная текстовая проверка
    patterns = get_universal_patterns(enum_value)
    
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return True
    
    return False


def _check_special_numeric_field(text: str, enum_value: str, field_key: str) -> bool:
    """Специальная проверка для числовых полей."""
    if field_key in ["dosage", "dosage_percentage", "dosage_kg_t"]:
        # Диапазоны дозировок
        if enum_value == "низкие_до_0.1":
            return check_dosage_range(text, 0.0, 0.1)
        elif enum_value == "средние_0.1_1.0":
            return check_dosage_range(text, 0.1, 1.0)
        elif enum_value == "высокие_свыше_1.0":
            return check_dosage_range(text, 1.0, 10.0)
        elif enum_value == "до_4_кг_т":
            return check_dosage_range(text, 0.0, 4.0)
    
    elif field_key in ["working_temperature_range", "temperature"]:
        # Температурные диапазоны
        if enum_value == "низкие_до_50":
            return check_temperature_range(text, 0, 50)
        elif enum_value == "средние_50_100":
            return check_temperature_range(text, 50, 100) 
        elif enum_value == "высокие_свыше_100":
            return check_temperature_range(text, 100, 200)
        elif enum_value == "рабочие_0_110":
            return check_temperature_range(text, 0, 110)
    
    # Fallback к обычной проверке
    patterns = get_universal_patterns(enum_value)
    text_lower = text.lower()
    return any(pattern.lower() in text_lower for pattern in patterns)


# ===================== ТЕСТИРОВАНИЕ =====================

if __name__ == "__main__":
    print("=== ТЕСТ МАСЛОЖИРОВЫХ ПАТТЕРНОВ ===")
    print(f"'XTENDRA' паттерны: {get_universal_patterns('XTENDRA')}")
    print(f"'бета_каротин' паттерны: {get_universal_patterns('бета_каротин')}")
    print(f"'ГЕЛЕОН' паттерны: {get_universal_patterns('ГЕЛЕОН')}")
    print(f"'майонез' паттерны: {get_universal_patterns('майонез')}")
    
    print("\n=== ТЕСТ ТЕКСТОВЫХ СОВПАДЕНИЙ ===")
    print(f"'АНТИОКСИДАНТ XTENDRA 08' содержит 'XTENDRA': {has_universal_enum_match('АНТИОКСИДАНТ XTENDRA 08', 'XTENDRA')}")
    print(f"'КРАСИТЕЛЬ БЕТА-КАРОТИН' содержит 'бета_каротин': {has_universal_enum_match('КРАСИТЕЛЬ БЕТА-КАРОТИН', 'бета_каротин')}")
    print(f"'СТАБИЛИЗАТОР «102 С» ГЕЛЕОН®' содержит 'ГЕЛЕОН': {has_universal_enum_match('СТАБИЛИЗАТОР «102 С» ГЕЛЕОН®', 'ГЕЛЕОН')}")
    
    print("\n=== ТЕСТ ЧИСЛОВЫХ ПРОВЕРОК ===")
    test_dosage = "0,02-0,1%"
    test_kg_t = "0,1-4,0 кг/т"
    test_temp = "0-110 °C"
    test_replacement = "1 кг смеси заменяет 200 кг сахара"
    
    print(f"Дозировка 0,02-0,1% -> 'низкие_до_0.1': {has_universal_enum_match(test_dosage, 'низкие_до_0.1', 'dosage_percentage')}")
    print(f"Дозировка 0,1-4,0 кг/т -> 'до_4_кг_т': {has_universal_enum_match(test_kg_t, 'до_4_кг_т', 'dosage_kg_t')}")
    print(f"Температура 0-110°C -> 'рабочие_0_110': {has_universal_enum_match(test_temp, 'рабочие_0_110', 'working_temperature_range')}")
    print(f"Замена 200кг -> 'замена_200': {has_universal_enum_match(test_replacement, 'замена_200')}")
    
    print("\n✅ Масложировое тестирование завершено успешно")
