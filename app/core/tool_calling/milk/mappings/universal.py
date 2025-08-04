"""
Универсальный промежуточный маппинг enum → реальные данные для молочной отрасли.

Расширяет базовые универсальные паттерны специфичными для молочной отрасли.
Использует regex для числовых значений и текстовые паттерны для остальных.
"""

import re
from typing import List, Dict, Callable

# Импортируем базовые универсальные функции
from ...horeca.mappings.universal import (
    has_universal_enum_match,
    get_universal_patterns,
    UNIVERSAL_KBGU_CHECKERS,
    PACKAGING_CHECKERS,
    SHELF_LIFE_CHECKERS
)

# ===================== СПЕЦИФИЧНЫЕ ДЛЯ МОЛОЧНОЙ ОТРАСЛИ ПАТТЕРНЫ =====================

# Специфичные маппинги для молочной отрасли
MILK_SPECIFIC_MAPPING: Dict[str, List[str]] = {
    
    # ========== МОЛОЧНЫЕ БЕЛКИ ==========
    "концентрат_молочного_белка": ["КОНЦЕНТРАТ МОЛОЧНОГО БЕЛКА", "концентрат молочного белка"],
    "комплексная_пищевая_добавка": ["КОМПЛЕКСНАЯ ПИЩЕВАЯ ДОБАВКА", "комплексная пищевая добавка"],
    "74_процента": ["74,0", "74", "не менее 74"],
    "75_процентов": ["75,0±2,5", "75±2,5", "75"],
    "80_процентов": ["80,0+2,5", "80+2,5", "80"],
    "85_процентов": ["83+3", "85", "83"],
    "ГЕЛЕОН": ["ГЕЛЕОН", "Гелеон"],
    "ZL": ["ZL", "zl"],
    
    # ========== ЗАКВАСОЧНЫЕ КУЛЬТУРЫ ==========
    "PROFILINE": ["PROFILINE®", "PROFILINE", "Profiline"],
    "GOLDEN_TIME": ["GOLDEN TIME®", "GOLDEN TIME", "Golden Time"],
    "SMARTLINE": ["SMARTLINE", "Smartline"],
    "YO": ["YO", "yo"],
    "RZ": ["RZ", "rz"],
    "KE": ["KE", "ke"],
    "CC": ["CC", "cc"],
    "LOW": ["LOW", "low"],
    "F": ["F", " F"],
    "F2": ["F2", "f2"],
    "R5": ["R5", "r5"],
    "D": ["D", " D"],
    "SWEET": ["SWEET", "sweet"],
    "GOLDEN_LINE": ["GOLDEN LINE®", "GOLDEN LINE", "Golden Line"],
    
    # ========== КРАСИТЕЛИ ==========
    "бета_каротин": ["БЕТА-КАРОТИН", "бета-каротин", "BETA-CAROTENE"],
    "кармин": ["КАРМИН", "кармин", "CARMINE"],
    "азорубин": ["АЗОРУБИН", "азорубин", "AZORUBINE"],
    "сахарный_колер": ["САХАРНЫЙ КОЛЕР", "сахарный колер"],
    "солнечный_закат": ["СОЛНЕЧНЫЙ ЗАКАТ", "солнечный закат"],
    "диоксид_титана": ["ДИОКСИД ТИТАНА", "диоксид титана", "TITANIUM DIOXIDE"],
    "куркумин": ["КУРКУМИН", "куркумин", "CURCUMIN"],
    "ESCO": ["ESCO", "Esco"],
    "WSC": ["WSC", "wsc"],
    "жидкий": ["ЖИДКИЙ", "жидкий", "Жидкий"],
    "порошок": ["ПОРОШОК", "порошок", "Порошок"],
    "в_растительном_масле": ["В РАСТИТЕЛЬНОМ МАСЛЕ", "в растительном масле"],
    "водорастворимый": ["10%", "водорастворимый", "WSC"],
    "натуральный": ["НАТУРАЛЬНЫЙ", "натуральный", "Натуральный"],
    "синтетический": ["синтетический", "Синтетический"],
    
    # ========== КАКАО ==========
    "алкализованный": ["алкализованный", "Алкализованный", "АЛКАЛИЗОВАННЫЙ"],
    "TULIP": ["TULIP", "Tulip"],
    "GOLDEN_HARVEST": ["GOLDEN HARVEST", "Golden Harvest"],
    "ДЕНКАКАО": ["ДЕНКАКАО", "Денкакао", "ДЕНКАКАО-А"],
    "400": ["400"],
    "А": ["А", "-А"],
    
    # ========== ГЛАЗУРИ И МАССЫ ==========
    "масса_кондитерская": ["МАССА КОНДИТЕРСКАЯ", "масса кондитерская"],
    "глазурь_кондитерская": ["ГЛАЗУРЬ КОНДИТЕРСКАЯ", "глазурь кондитерская"],
    "темная": ["ТЕМНАЯ", "темная", "Темная"],
    "молочная": ["МОЛОЧНАЯ", "молочная", "Молочная"],
    "светло_коричневый": ["Светло-коричневый", "светло-коричневый"],
    "042": ["042"],
    "920": ["920"],
    "145": ["145"],
    "805": ["805"],
    "капли": ["КАПЛИ", "капли", "(КАПЛИ)"],
    
    # ========== ЦВЕТА ==========
    "желтый": ["Желтый", "желтый", "ЖЕЛТЫЙ", "оттенки желтого"],
    "оранжевый": ["Оранжевый", "оранжевый", "ОРАНЖЕВЫЙ"],
    "красный": ["Красный", "красный", "яркий красный", "темно-красный"],
    "коричневый": ["Коричневый", "коричневый", "яркий коричневый"],
    "зеленый": ["Зеленый", "зеленый", "яркий зеленый"],
    "белый": ["Белый", "белый", "БЕЛЫЙ"],
    "фиолетовый": ["фиолетовый", "темно-фиолетовый"],
    "яркий": ["яркий", "Яркий"],
    "темный": ["темный", "Темный", "темно"],
    "насыщенный": ["насыщенный", "Насыщенный"],
    "естественный": ["естественный", "Естественный"],
    "цвет_вишни": ["цвет спелой вишни", "Цвет спелой вишни"],
    "цвет_ряженки": ["цвет ряженки", "Цвет ряженки"],
    "лимонный": ["лимонный", "Лимонный", "темно-желтый"],
    
    # ========== ДОЗИРОВКИ ==========
    "низкая_до_1": ["0.02-0.08", "0,2-0,5", "0,2-0,4", "0,2-0,7"],
    "средняя_1_10": ["1-5", "5-30", "2-10"],
    "высокая_свыше_10": ["15-40", "свыше 10"],
    "процент": ["%", "процент", "процентов"],
    "кг_на_тонну": ["кг/т", "кг на тонну"],
    "мг_на_кг": ["мг/кг", "мг на кг"],
    "0_3_процента": ["0,3%", "0.3%"],
    "10_процентов": ["10%"],
    
    # ========== УПАКОВКИ ==========
    "50": ["50"],
    "250": ["250"],
    "150": ["150"],
    "малая_упаковка_50": ["50"],
    "средняя_упаковка_150_250": ["150", "250"],
    "комбинированная_упаковка": ["50, 250", "250, 50"],
    
    # ========== ФРУКТЫ И ЯГОДЫ ==========
    "черничная": ["Черничная", "черничная", "ЧЕРНИЧНАЯ"],
    "чернослив": ["Чернослив", "чернослив", "ЧЕРНОСЛИВ"],
    "вишневая": ["Вишневая", "вишневая", "ВИШНЕВАЯ", "Вишня"],
    "клубничная": ["Клубничная", "клубничная", "КЛУБНИЧНАЯ", "Клубники"],
    "абрикосовая": ["Абрикосовая", "абрикосовая", "АБРИКОСОВАЯ"],
    "апельсиновый": ["Апельсиновый", "апельсиновый", "АПЕЛЬСИНОВЫЙ"],
    "ананасовый": ["Ананасовый", "ананасовый", "АНАНАСОВЫЙ"],
    "банановая": ["Банановая", "банановая", "БАНАНОВАЯ"],
    "брусника_клюква": ["Брусника-Клюква", "брусника-клюква"],
    "денкрим": ["Денкрим", "ДЕНКРИМ"],
    "с_ягодой": ["с ягодой", "(с ягодой)"],
    "с_кусочками": ["с кусочками", "(с кусочками)"],
    "с_цедрой": ["с цедрой", "(с цедрой)"],
    "с_орехом": ["с грецким орехом", "с орехом"],
    "со_вкусом": ["со вкусом", "со вкусами"],
    "Nat": ["Nat", "NAT"],
    "1_2_мм": ["1-2 мм", "1-2мм"],
    "3_5_мм": ["3-5 мм", "3-5мм"],
    
    # ========== ФОСФАТЫ ==========
    "ДЕНФОС": ["ДЕНФОС", "Денфос"],
    "ДЕНФОСФАТ": ["ДЕНФОСФАТ", "Денфосфат"],
    "120": ["120"],
    "2070": ["2070"],
    "12_РІ": ["12 РІ", "12РІ"],
    "76_SL": ["76 SL", "76SL"],
    "85": ["85"],
    "пастообразные_сыры": ["пастообразных плавленых сыров", "пастообразные"],
    "ломтевые_сыры": ["ломтевых плавленых сыров", "ломтевые"],
    "моцарелла_пицца": ["моцареллы для пиццы", "моцарелла для пиццы"],
    "имитационные_сыры": ["имитационных плавленых сыров", "имитационные"],
    "кремовый_эффект": ["кремовый эффект", "высокий кремовый эффект"],
    "гомогенная_эмульсия": ["гомогенную эмульсию", "гомогенная эмульсия"],
    
    # ========== КОНСЕРВАНТЫ ==========
    "глюкоза_ферментированная": ["ГЛЮКОЗА ФЕРМЕНТИРОВАННАЯ", "глюкоза ферментированная"],
    "AIBI": ["ΑΙΒΙ", "AIBI"],
    "DEL_AR": ["DEL'AR", "DEL AR", "DELAR"],
    "лактовас": ["LАCТOВАС", "ЛАКТОВАС"],
    "сорбиновая": ["СОРБИНОВАЯ", "сорбиновая"],
    "лимонная": ["ЛИМОННАЯ", "лимонная"],
    "сорбат_калия": ["СОРБАТ КАЛИЯ", "сорбат калия"],
    "бензоат_натрия": ["БЕНЗОАТ НАТРИЯ", "бензоат натрия"],
    "цитрат_натрия": ["ЦИТРАТ НАТРИЯ", "цитрат натрия", "НАТРИЙ ЛИМОННОКИСЛЫЙ"],
    "кислота": ["КИСЛОТА", "кислота"],
    "соль": ["соль", "Соль", "СОЛЬ"],
    "комплексная_добавка": ["КОМПЛЕКСНАЯ ПИЩЕВАЯ ДОБАВКА", "комплексная добавка"],
    "жидкая": ["ЖИДКАЯ", "жидкая"],
    "сухая": ["сухая", "Сухая", "СУХАЯ"],
    "КИТАЙ": ["КИТАЙ", "(КИТАЙ)"],
    
    # ========== ОБЛАСТИ ПРИМЕНЕНИЯ КОНСЕРВАНТОВ ==========
    "сметанные_продукты": ["Сметанный продукт", "сметанные продукты"],
    "кисломолочные": ["кисломолочные продукты", "кисломолочные"],
    "творожные": ["Творожный продукт", "творожные продукты", "творожные изделия"],
    "сгущенное_молоко": ["Сгущенное молоко", "сгущенное молоко"],
    "сыры": ["сыры", "Сыры"],
    "плавленые_сыры": ["плавленые сыры", "Плавленые сыры"],
    "спреды": ["спреды", "Спреды"],
    "молоко_стерилизованное": ["Молоко стерилизованное", "молоко стерилизованное"],
    "сливки": ["сливки", "Сливки"],
    
    # ========== ПРОЦЕНТНЫЕ ДИАПАЗОНЫ КОНСЕРВАНТОВ ==========
    "0_01": ["0,01", "0.01"],
    "0_05_0_40": ["0,05-0,40", "0.05-0.40"],
    "0_1_0_15": ["0,1-0,15", "0.1-0.15"],
    "0_2_0_25": ["0,2-0,25", "0.2-0.25"],
    "0_2_2_0": ["0,2-2,0", "0.2-2.0"],
    "0_5_1_0": ["0,5-1,0", "0.5-1.0"],
    "0_7_1_0": ["0,7-1,0", "0.7-1.0"],
    "0_8_1_0": ["0,8-1,0", "0.8-1.0"],
    "1_0": ["1,0", "1.0"],
    "1_0_2_0": ["1,0-2,0", "1.0-2.0"],
    "2_3": ["2-3", "2,0-3,0"],
    
    # ========== МУЛЬТИФУНКЦИОНАЛЬНЫЕ СИСТЕМЫ ==========
    "стабилизация": ["стабилизация", "Стабилизация"],
    "текстурирование": ["текстурирование", "Текстурирование"],
    "вкусокоррекция": ["вкусокоррекция", "коррекция вкуса"],
    "консервирование": ["консервирование", "Консервирование"],
    "молочные_напитки": ["молочные напитки", "Молочные напитки"],
    "кисломолочные_продукты": ["кисломолочные продукты", "Кисломолочные продукты"],
    "творожные_продукты": ["творожные продукты", "Творожные продукты"],
    "мороженое": ["мороженое", "Мороженое"],
    "простая_система": ["простая система", "Простая система"],
    "комплексная_система": ["комплексная система", "Комплексная система"],
    "специализированная_система": ["специализированная система", "Специализированная система"],
    
    # ========== АРОМАТИЗАТОРЫ DEL'AR ==========
    "фруктовый": ["фруктовый", "Фруктовый"],
    "ванильный": ["ванильный", "Ванильный", "ванили"],
    "шоколадный": ["шоколадный", "Шоколадный"],
    "карамельный": ["карамельный", "Карамельный"],
    "ореховый": ["ореховый", "Ореховый"],
    "легкий": ["легкий", "Легкий"],
    "средний": ["средний", "Средний"],
    "интенсивный": ["интенсивный", "Интенсивный"],
    "очень_интенсивный": ["очень интенсивный", "Очень интенсивный"],
    "эмульсия": ["эмульсия", "Эмульсия"],
    "порошкообразный": ["порошкообразный", "Порошкообразный"],
}

# ===================== СПЕЦИАЛЬНЫЕ REGEX ФУНКЦИИ ДЛЯ МОЛОЧНОЙ ОТРАСЛИ =====================

# Regex для процентного содержания белка
PROTEIN_CONTENT_REGEX = re.compile(r"белка.*?(\d+(?:,\d+)?)", re.IGNORECASE)

# Regex для дозировки
DOSAGE_REGEX = re.compile(r"(\d+(?:,\d+)?(?:-\d+(?:,\d+)?)?)\s*(?:%|кг/т|мг/кг)", re.IGNORECASE)

# Regex для размера упаковки
PACKAGE_SIZE_REGEX = re.compile(r"\b(\d+)\b", re.IGNORECASE)


def check_protein_content_milk(text: str, enum_value: str) -> bool:
    """
    Проверяет процентное содержание белка в молочных продуктах.
    
    Args:
        text: Текст с характеристиками продукта
        enum_value: Enum значение содержания белка
        
    Returns:
        True если содержание белка соответствует, False иначе
    """
    match = PROTEIN_CONTENT_REGEX.search(text)
    if not match:
        return False
    
    try:
        protein_content = float(match.group(1).replace(',', '.'))
        
        if enum_value == "белка_не_менее_74":
            return protein_content >= 74.0
        elif enum_value == "белка_75_плюс_минус_2_5":
            return 72.5 <= protein_content <= 77.5
        elif enum_value == "белка_80_плюс_2_5":
            return 77.5 <= protein_content <= 82.5
        elif enum_value == "белка_83_плюс_3":
            return 80.0 <= protein_content <= 86.0
        
    except (ValueError, IndexError):
        pass
    
    return False


def check_dosage_range_milk(text: str, enum_value: str) -> bool:
    """
    Проверяет диапазон дозировки для молочных продуктов.
    
    Args:
        text: Текст с дозировкой
        enum_value: Enum значение диапазона дозировки
        
    Returns:
        True если дозировка в диапазоне, False иначе
    """
    match = DOSAGE_REGEX.search(text)
    if not match:
        return False
    
    try:
        dosage_str = match.group(1).replace(',', '.')
        if '-' in dosage_str:
            # Диапазон дозировки
            min_dose, max_dose = map(float, dosage_str.split('-'))
            avg_dose = (min_dose + max_dose) / 2
        else:
            # Одиночное значение
            avg_dose = float(dosage_str)
        
        if enum_value == "низкая_до_1":
            return avg_dose < 1.0
        elif enum_value == "средняя_1_10":
            return 1.0 <= avg_dose <= 10.0
        elif enum_value == "высокая_свыше_10":
            return avg_dose > 10.0
        
    except (ValueError, IndexError):
        pass
    
    return False


def check_package_size_milk(text: str, enum_value: str) -> bool:
    """
    Проверяет размер упаковки для молочных продуктов.
    
    Args:
        text: Текст с размером упаковки
        enum_value: Enum значение размера упаковки
        
    Returns:
        True если размер соответствует, False иначе
    """
    matches = PACKAGE_SIZE_REGEX.findall(text)
    if not matches:
        return False
    
    package_sizes = [int(match) for match in matches]
    
    if enum_value == "50":
        return 50 in package_sizes
    elif enum_value == "250":
        return 250 in package_sizes
    elif enum_value == "150":
        return 150 in package_sizes
    elif enum_value == "малая_упаковка_50":
        return 50 in package_sizes
    elif enum_value == "средняя_упаковка_150_250":
        return any(size in [150, 250] for size in package_sizes)
    elif enum_value == "комбинированная_упаковка":
        return len(set(package_sizes) & {50, 150, 250}) >= 2
    
    return False


# Regex для процентных диапазонов фосфатов
PHOSPHATE_PERCENTAGE_REGEX = re.compile(r"(\\d+(?:,\\d+)?(?:-\\d+(?:,\\d+)?)?)\s*%", re.IGNORECASE)

# Regex для характеристик фруктовых наполнителей
DRY_MATTER_REGEX = re.compile(r"сухих\\s+веществ[^:]*:(\\d+(?:,\\d+)?)\\s*(?:±|\\+/-|\\+-)(\\d+(?:,\\d+)?)\\s*%", re.IGNORECASE)
PH_REGEX = re.compile(r"pH[^:]*:(\\d+(?:,\\d+)?)-?(\\d+(?:,\\d+)?)", re.IGNORECASE)

def check_phosphate_percentage_milk(text: str, enum_value: str) -> bool:
    """
    Проверяет процентный диапазон для фосфатов.
    
    Args:
        text: Текст с процентным содержанием
        enum_value: Enum значение процентного диапазона
        
    Returns:
        True если процент в диапазоне, False иначе
    """
    match = PHOSPHATE_PERCENTAGE_REGEX.search(text)
    if not match:
        return False
    
    try:
        percentage_str = match.group(1).replace(',', '.')
        if '-' in percentage_str:
            # Диапазон процентов
            min_pct, max_pct = map(float, percentage_str.split('-'))
            avg_pct = (min_pct + max_pct) / 2
        else:
            # Одиночное значение
            avg_pct = float(percentage_str)
        
        if enum_value == "0_1_0_5":
            return 0.1 <= avg_pct <= 0.5
        elif enum_value == "1_0_1_4":
            return 1.0 <= avg_pct <= 1.4
        elif enum_value == "1_1_1_5":
            return 1.1 <= avg_pct <= 1.5
        elif enum_value == "1_4_2_0":
            return 1.4 <= avg_pct <= 2.0
        elif enum_value == "1_5_2_0":
            return 1.5 <= avg_pct <= 2.0
        elif enum_value == "1_8_2_0":
            return 1.8 <= avg_pct <= 2.0
        
    except (ValueError, IndexError):
        pass
    
    return False


def check_dry_matter_milk(text: str, enum_value: str) -> bool:
    """
    Проверяет массовую долю сухих веществ.
    
    Args:
        text: Текст с характеристиками
        enum_value: Enum значение сухих веществ
        
    Returns:
        True если соответствует, False иначе
    """
    match = DRY_MATTER_REGEX.search(text)
    if not match:
        return False
    
    try:
        base_value = float(match.group(1).replace(',', '.'))
        tolerance = float(match.group(2).replace(',', '.'))
        
        if enum_value == "68_плюс_минус_2_процента":
            return abs(base_value - 68.0) <= tolerance and tolerance == 2.0
            
    except (ValueError, IndexError):
        pass
    
    return False


def check_ph_range_milk(text: str, enum_value: str) -> bool:
    """
    Проверяет диапазон pH.
    
    Args:
        text: Текст с pH характеристиками
        enum_value: Enum значение pH диапазона
        
    Returns:
        True если pH в диапазоне, False иначе
    """
    match = PH_REGEX.search(text)
    if not match:
        return False
    
    try:
        min_ph = float(match.group(1).replace(',', '.'))
        max_ph = float(match.group(2).replace(',', '.')) if match.group(2) else min_ph
        
        if enum_value == "3_6_4_2":
            return min_ph == 3.6 and max_ph == 4.2
            
    except (ValueError, IndexError):
        pass
    
    return False


# Специальные проверки для молочной отрасли
MILK_SPECIFIC_CHECKERS: Dict[str, Callable[[str, str], bool]] = {
    # Белковое содержание
    "белка_не_менее_74": check_protein_content_milk,
    "белка_75_плюс_минус_2_5": check_protein_content_milk,
    "белка_80_плюс_2_5": check_protein_content_milk,
    "белка_83_плюс_3": check_protein_content_milk,
    
    # Дозировки
    "низкая_до_1": check_dosage_range_milk,
    "средняя_1_10": check_dosage_range_milk,
    "высокая_свыше_10": check_dosage_range_milk,
    
    # Упаковки
    "50": check_package_size_milk,
    "250": check_package_size_milk,
    "150": check_package_size_milk,
    "малая_упаковка_50": check_package_size_milk,
    "средняя_упаковка_150_250": check_package_size_milk,
    "комбинированная_упаковка": check_package_size_milk,
    
    # Процентные диапазоны фосфатов
    "0_1_0_5": check_phosphate_percentage_milk,
    "1_0_1_4": check_phosphate_percentage_milk,
    "1_1_1_5": check_phosphate_percentage_milk,
    "1_4_2_0": check_phosphate_percentage_milk,
    "1_5_2_0": check_phosphate_percentage_milk,
    "1_8_2_0": check_phosphate_percentage_milk,
    
    # Характеристики фруктовых наполнителей
    "68_плюс_минус_2_процента": check_dry_matter_milk,
    "3_6_4_2": check_ph_range_milk,
}

# ===================== ОСНОВНЫЕ ФУНКЦИИ =====================

def get_milk_patterns(enum_value: str) -> List[str]:
    """
    Возвращает паттерны поиска для enum значения из молочных маппингов.
    
    Args:
        enum_value: Значение enum из milk_enum_mapping.py
        
    Returns:
        Список паттернов для поиска в реальных данных
    """
    # Сначала ищем в специфичных молочных паттернах
    milk_patterns = MILK_SPECIFIC_MAPPING.get(enum_value, [])
    if milk_patterns:
        return milk_patterns
    
    # Если не найдено, используем универсальные паттерны
    universal_patterns = get_universal_patterns(enum_value)
    return universal_patterns


def has_milk_enum_match(text: str, enum_value: str, field_key: str = None) -> bool:
    """
    Универсальная проверка совпадения enum значения с текстом для молочной отрасли.
    
    Args:
        text: Текст для поиска
        enum_value: Значение enum
        field_key: Ключ поля для специальной обработки
        
    Returns:
        True если найдено совпадение, False иначе
    """
    if not text or not enum_value:
        return False
    
    # Специальная обработка для молочных характеристик
    if field_key == "characteristics" and enum_value in MILK_SPECIFIC_CHECKERS:
        checker_func = MILK_SPECIFIC_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    # Специальная обработка для дозировок
    if field_key == "dosage" and enum_value in MILK_SPECIFIC_CHECKERS:
        checker_func = MILK_SPECIFIC_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    # Специальная обработка для упаковок
    if field_key == "packaging" and enum_value in MILK_SPECIFIC_CHECKERS:
        checker_func = MILK_SPECIFIC_CHECKERS[enum_value] 
        return checker_func(text, enum_value)
    
    # Используем универсальные проверки для КБЖУ, веса, срока хранения
    if field_key == "kbgu" and enum_value in UNIVERSAL_KBGU_CHECKERS:
        checker_func = UNIVERSAL_KBGU_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    if field_key == "packaging" and enum_value in PACKAGING_CHECKERS:
        checker_func = PACKAGING_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    if field_key == "shelf_life" and enum_value in SHELF_LIFE_CHECKERS:
        checker_func = SHELF_LIFE_CHECKERS[enum_value]
        return checker_func(text, enum_value)
    
    # Обычный текстовый поиск с приоритетом молочных паттернов
    patterns = get_milk_patterns(enum_value)
    text_lower = text.lower()
    
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return True
    
    # Fallback на универсальную функцию
    return has_universal_enum_match(text, enum_value, field_key)


# ===================== ТЕСТИРОВАНИЕ =====================

if __name__ == "__main__":
    print("=== ТЕСТ МОЛОЧНЫХ ПАТТЕРНОВ ===")
    print(f"'концентрат_молочного_белка' паттерны: {get_milk_patterns('концентрат_молочного_белка')}")
    print(f"'PROFILINE' паттерны: {get_milk_patterns('PROFILINE')}")
    print(f"'бета_каротин' паттерны: {get_milk_patterns('бета_каротин')}")
    
    print("\n=== ТЕСТ ТЕКСТОВЫХ СОВПАДЕНИЙ ===")
    print(f"'КОНЦЕНТРАТ МОЛОЧНОГО БЕЛКА 75 ZL' содержит 'концентрат_молочного_белка': {has_milk_enum_match('КОНЦЕНТРАТ МОЛОЧНОГО БЕЛКА 75 ZL', 'концентрат_молочного_белка')}")
    print(f"'PROFILINE® YO 22.50' содержит 'PROFILINE': {has_milk_enum_match('PROFILINE® YO 22.50', 'PROFILINE')}")
    print(f"'БЕТА-КАРОТИН 0,3%' содержит 'бета_каротин': {has_milk_enum_match('БЕТА-КАРОТИН 0,3%', 'бета_каротин')}")
    
    print("\n=== ТЕСТ ЧИСЛОВЫХ ПРОВЕРОК ===")
    test_protein = "Массовая доля белка в сухом веществе: 75,0±2,5"
    test_dosage = "0,2-0,5 кг/т"
    test_package = "50, 250"
    
    print(f"Белок 75±2.5 -> 'белка_75_плюс_минус_2_5': {has_milk_enum_match(test_protein, 'белка_75_плюс_минус_2_5', 'characteristics')}")
    print(f"Дозировка 0,2-0,5 -> 'низкая_до_1': {has_milk_enum_match(test_dosage, 'низкая_до_1', 'dosage')}")
    print(f"Упаковка 50, 250 -> 'комбинированная_упаковка': {has_milk_enum_match(test_package, 'комбинированная_упаковка', 'packaging')}")
    
    print("\n✅ Молочное тестирование завершено успешно")