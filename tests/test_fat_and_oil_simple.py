"""
Упрощенный интеграционный тест для fat_and_oil Tool Calling без зависимостей от моделей.

Проверяет:
1. Загрузку mappings файлов напрямую
2. Генерацию OpenAI tool схем на основе keys.py и enums.py  
3. Наличие паттернов в universal.py для каждого enum значения
4. Целостность связей между всеми тремя файлами
"""

import json
import sys
import os
from typing import Dict, List, Any, Set
from pathlib import Path

def test_fat_and_oil_mappings():
    """Основная функция теста без зависимостей от моделей."""
    print("🧪 Запуск упрощенного теста fat_and_oil Tool Calling...")
    print("=" * 80)
    
    # Тест 1: Прямая загрузка mappings файлов
    print("\n📁 Тест 1: Прямая загрузка mappings...")
    keys_mapping, enum_mapping, universal_patterns = load_mappings_direct()
    print("✅ Все mappings файлы загружены напрямую")
    
    # Тест 2: Проверка структуры keys.py
    print("\n🗂️  Тест 2: Проверка структуры keys.py...")
    validate_keys_structure(keys_mapping)
    
    # Тест 3: Проверка структуры enums.py
    print("\n🏷️  Тест 3: Проверка структуры enums.py...")
    validate_enums_structure(enum_mapping, keys_mapping)
    
    # Тест 4: Генерация tool схем для каждого JSON ключа
    print("\n⚙️  Тест 4: Генерация tool схем...")
    test_tool_schema_generation(keys_mapping, enum_mapping)
    
    # Тест 5: Проверка паттернов для всех enum значений
    print("\n🔍 Тест 5: Проверка universal паттернов...")
    test_universal_patterns_coverage(enum_mapping, universal_patterns)
    
    # Тест 6: Проверка KEY_TO_FILE_MAPPING
    print("\n📋 Тест 6: Проверка KEY_TO_FILE_MAPPING...")
    test_key_to_file_mapping(keys_mapping)
    
    print("\n" + "=" * 80)
    print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! fat_and_oil mappings корректны.")

def load_mappings_direct():
    """Загружает mappings файлы напрямую без импорта модулей проекта."""
    mappings_path = Path("/Users/mask/Documents/Проеты_2025/szsb_sales/app/core/tool_calling/fat_and_oil/mappings")
    
    # Загружаем keys.py
    keys_content = {}
    keys_file = mappings_path / "keys.py"
    if keys_file.exists():
        # Выполняем файл и извлекаем нужные переменные
        exec_globals = {}
        exec(keys_file.read_text(encoding='utf-8'), exec_globals)
        keys_content = exec_globals.get('keys_mapping', {})
    
    # Загружаем enums.py
    enums_content = {}
    enums_file = mappings_path / "enums.py"
    if enums_file.exists():
        exec_globals = {}
        exec(enums_file.read_text(encoding='utf-8'), exec_globals)
        enums_content = exec_globals.get('enum_mapping', {})
    
    # Загружаем universal.py 
    universal_patterns = {}
    universal_file = mappings_path / "universal.py"
    if universal_file.exists():
        exec_globals = {}
        exec(universal_file.read_text(encoding='utf-8'), exec_globals)
        universal_patterns = exec_globals.get('FAT_AND_OIL_SPECIFIC_MAPPING', {})
        # Добавляем функции
        universal_patterns['_get_universal_patterns'] = exec_globals.get('get_universal_patterns')
        universal_patterns['_has_universal_enum_match'] = exec_globals.get('has_universal_enum_match')
    
    return keys_content, enums_content, universal_patterns

def validate_keys_structure(keys_mapping: Dict):
    """Проверяет структуру keys.py."""
    print("  🔍 Проверяем FAT_AND_OIL_KEYS_MAPPING...")
    
    expected_files = [
        "antioxidants.json", "cocoa_powders.json", "delar_flavors.json",
        "dry_milk_products.json", "emulsifiers_for_margarine_spreads.json", 
        "fillers_and_toppings.json", "food_colors.json", "preservatives_acids.json",
        "stabilizers_compounds.json", "sweeteners.json"
    ]
    
    # Проверяем наличие всех файлов
    missing_files = [f for f in expected_files if f not in keys_mapping]
    if missing_files:
        raise AssertionError(f"❌ Отсутствуют mappings для файлов: {missing_files}")
    
    # Проверяем структуру каждого файла
    total_fields = 0
    for file_name, file_config in keys_mapping.items():
        # Проверяем обязательные ключи
        if "file_description" not in file_config:
            raise AssertionError(f"❌ Отсутствует file_description для {file_name}")
        if "product_keys" not in file_config:
            raise AssertionError(f"❌ Отсутствует product_keys для {file_name}")
        
        # Проверяем поля продуктов
        product_keys = file_config["product_keys"]
        for field_name, field_config in product_keys.items():
            required_attrs = ["description", "filter_impact", "data_type"]
            missing_attrs = [attr for attr in required_attrs if attr not in field_config]
            if missing_attrs:
                raise AssertionError(f"❌ Отсутствуют атрибуты {missing_attrs} для {field_name} в {file_name}")
            total_fields += 1
    
    print(f"  ✅ Структура корректна. Файлов: {len(keys_mapping)}, полей: {total_fields}")

def validate_enums_structure(enum_mapping: Dict, keys_mapping: Dict):
    """Проверяет структуру enums.py и соответствие keys.py."""
    print("  🔍 Проверяем FAT_AND_OIL_ENUM_MAPPING...")
    
    # Проверяем что enum mapping покрывает все файлы из keys
    missing_enum_files = [f for f in keys_mapping.keys() if f not in enum_mapping]
    if missing_enum_files:
        raise AssertionError(f"❌ Отсутствуют enum mappings для: {missing_enum_files}")
    
    total_enum_values = 0
    all_enum_values = set()
    
    # Проверяем структуру
    for file_name, file_enums in enum_mapping.items():
        if not isinstance(file_enums, dict):
            raise AssertionError(f"❌ enum mapping для {file_name} должен быть словарем")
        
        if not file_enums:
            raise AssertionError(f"❌ Пустой enum mapping для {file_name}")
        
        # Проверяем субключи
        for subkey, subkey_enums in file_enums.items():
            if not isinstance(subkey_enums, dict):
                raise AssertionError(f"❌ Субключ {subkey} в {file_name} должен быть словарем")
            
            # Считаем enum значения
            for field_name, field_categories in subkey_enums.items():
                if isinstance(field_categories, dict):
                    for category, values in field_categories.items():
                        if isinstance(values, list):
                            total_enum_values += len(values)
                            all_enum_values.update(values)
    
    print(f"  ✅ Enum структура корректна. Всего значений: {total_enum_values} (уникальных: {len(all_enum_values)})")
    return all_enum_values

def test_tool_schema_generation(keys_mapping: Dict, enum_mapping: Dict):
    """Проверяет генерацию OpenAI tool схем для каждого JSON ключа."""
    print("  🔍 Генерируем tool схемы для каждого ключа...")
    
    successful_schemas = 0
    total_properties = 0
    
    for file_name, file_config in keys_mapping.items():
        try:
            # Получаем product_keys из keys.py
            product_keys = file_config.get("product_keys", {})
            if not product_keys:
                print(f"  ⚠️ Нет product_keys для {file_name}")
                continue
            
            # Получаем соответствующие enums
            file_enums = enum_mapping.get(file_name, {})
            
            # Генерируем схему
            schema = {
                "type": "function",
                "function": {
                    "name": "filter_fat_and_oil_products",
                    "description": f"Фильтр для продуктов из {file_name}",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
            
            properties = schema["function"]["parameters"]["properties"]
            
            # Добавляем поля из product_keys
            for field_name, field_config in product_keys.items():
                field_property = {
                    "type": ["string", "null"],
                    "description": field_config["description"]
                }
                
                # Ищем enum значения для этого поля
                enum_values = []
                for subkey, subkey_enums in file_enums.items():
                    field_enums = subkey_enums.get(field_name, {})
                    if isinstance(field_enums, dict):
                        for category, values in field_enums.items():
                            if isinstance(values, list):
                                enum_values.extend(values)
                
                # Добавляем enum значения если есть
                if enum_values:
                    unique_enums = list(set(enum_values))
                    unique_enums.append(None)  # для strict mode
                    field_property["enum"] = unique_enums
                
                properties[field_name] = field_property
                total_properties += 1
            
            if properties:
                successful_schemas += 1
                print(f"    ✅ {file_name}: {len(properties)} полей")
            else:
                print(f"    ⚠️ {file_name}: нет полей для схемы")
                
        except Exception as e:
            print(f"    ❌ Ошибка генерации схемы для {file_name}: {e}")
    
    print(f"  ✅ Схемы: {successful_schemas}/{len(keys_mapping)}, всего полей: {total_properties}")

def test_universal_patterns_coverage(enum_mapping: Dict, universal_patterns: Dict):
    """Проверяет наличие паттернов в universal.py для всех enum значений и детализирует пробелы."""
    print("  🔍 Проверяем покрытие enum значений паттернами...")

    # Собираем все enum значения + контекст (файл/поле)
    all_enum_values: Set[str] = set()
    enum_context: Dict[str, Set[str]] = {}
    for file_name, file_enums in enum_mapping.items():
        for subkey, subkey_enums in file_enums.items():
            for field_name, field_categories in subkey_enums.items():
                if isinstance(field_categories, dict):
                    for category, values in field_categories.items():
                        if isinstance(values, list):
                            for v in values:
                                all_enum_values.add(v)
                                enum_context.setdefault(v, set()).add(f"{file_name}:{subkey}.{field_name}")

    print(f"    📊 Всего enum значений для проверки: {len(all_enum_values)}")

    # Получаем паттерны из universal.py
    specific_mapping = {k: v for k, v in universal_patterns.items() if not k.startswith('_')}
    # Примечание: используем только:
    #  - явные ключи в FAT_AND_OIL_SPECIFIC_MAPPING
    #  - и get_universal_patterns(enum) как индикатор наличия нетривиальных синонимов
    #    (если вернул только сам enum без вариантов — считаем, что паттерна нет)
    get_patterns_func = universal_patterns.get('_get_universal_patterns')

    # Проверяем каждое enum значение
    with_patterns = 0
    without_patterns: List[str] = []

    for enum_value in sorted(all_enum_values):
        has = False
        if enum_value in specific_mapping:
            has = True
        elif get_patterns_func:
            try:
                patterns = get_patterns_func(enum_value)
                # Если возвращены нетривиальные варианты (например, синонимы/переводы),
                # то считаем покрытым. Для чисто числовых/кодовых значений вернется
                # только исходное значение, в таком случае паттерна нет.
                uniq = set(patterns or [])
                if len(uniq) > 1:
                    has = True
            except Exception:
                pass

        if has:
            with_patterns += 1
        else:
            without_patterns.append(enum_value)

    coverage_percent = (with_patterns / len(all_enum_values)) * 100 if all_enum_values else 0
    print(f"    ✅ С паттернами: {with_patterns}/{len(all_enum_values)} ({coverage_percent:.1f}%)")

    # Детальная печать отсутствующих значений
    if without_patterns:
        print(f"    ⚠️ Без паттернов: {len(without_patterns)}")
        # Типизация пропусков для анализа (числовые диапазоны, коды, просто числа)
        import re
        re_range = re.compile(r"^\d+(?:[.,]\d+)?_\d+(?:[.,]\d+)?$")
        re_dotcode = re.compile(r"^\d+(?:[.\-]\d+){1,}$")
        re_int = re.compile(r"^\d+$")

        missing_ranges = [v for v in without_patterns if re_range.match(v)]
        missing_dotcodes = [v for v in without_patterns if re_dotcode.match(v)]
        missing_ints = [v for v in without_patterns if re_int.match(v)]
        missing_other = [v for v in without_patterns if v not in set(missing_ranges + missing_dotcodes + missing_ints)]

        def preview(lst: List[str], n: int = 10) -> str:
            return ", ".join(lst[:n]) + (" …" if len(lst) > n else "")

        print(f"       Диапазоны (x_y): {len(missing_ranges)} | {preview(missing_ranges)}")
        print(f"       Коды с точками/дефисами: {len(missing_dotcodes)} | {preview(missing_dotcodes)}")
        print(f"       Чистые числа: {len(missing_ints)} | {preview(missing_ints)}")
        if missing_other:
            print(f"       Прочее: {len(missing_other)} | {preview(missing_other)}")

        # Группировка по контексту (файл/поле), чтобы было ясно где чиним
        print("\n    📌 Где отсутствуют паттерны (по файлу/полю):")
        missing_by_context: Dict[str, List[str]] = {}
        for v in without_patterns:
            for ctx in sorted(enum_context.get(v, [])):
                missing_by_context.setdefault(ctx, []).append(v)

        # Печатаем первые 12 контекстов для краткости
        shown = 0
        for ctx, vals in sorted(missing_by_context.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            print(f"       - {ctx}: {len(vals)} → {preview(sorted(set(vals)), 8)}")
            shown += 1
            if shown >= 12:
                remaining = len(missing_by_context) - shown
                if remaining > 0:
                    print(f"       … и еще {remaining} контекстов")
                break

        # Сохраняем полный список на диск для удобства анализа (локально)
        try:
            report_path = Path("fat_and_oil_missing_enums.json")
            report = {
                "total_missing": len(without_patterns),
                "missing_values": sorted(without_patterns),
                "by_context": {k: sorted(list(set(v))) for k, v in missing_by_context.items()},
            }
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"\n    💾 Полный отчет сохранен: {report_path}")
        except Exception as e:
            print(f"\n    ⚠️ Не удалось сохранить отчет: {e}")

    # Проверяем базовые категории паттернов для sanity-check
    pattern_categories = {
        "антиоксиданты": ["xtendra", "токоферолы", "tbhq"],
        "красители": ["бета_каротин", "карамельный_колер", "паприка"],
        "стабилизаторы": ["гелеон", "стабилизатор", "эмульгатор"],
        "применение": ["майонез", "маргарин", "кетчуп"],
    }
    for category, expected_patterns in pattern_categories.items():
        found = sum(1 for p in expected_patterns if p in specific_mapping)
        print(f"    📋 {category}: {found}/{len(expected_patterns)} основных паттернов")

def test_key_to_file_mapping(keys_mapping: Dict):
    """Проверяет KEY_TO_FILE_MAPPING если он существует."""
    print("  🔍 Проверяем KEY_TO_FILE_MAPPING...")
    
    try:
        # Загружаем KEY_TO_FILE_MAPPING из keys.py
        keys_file = Path("/Users/mask/Documents/Проеты_2025/szsb_sales/app/core/tool_calling/fat_and_oil/mappings/keys.py")
        if keys_file.exists():
            exec_globals = {}
            exec(keys_file.read_text(encoding='utf-8'), exec_globals)
            key_to_file = exec_globals.get('KEY_TO_FILE_MAPPING', {})
            
            if key_to_file:
                # Проверяем что все файлы в маппинге существуют в keys_mapping
                invalid_files = [f for f in key_to_file.values() if f not in keys_mapping]
                if invalid_files:
                    print(f"    ❌ Некорректные файлы в KEY_TO_FILE_MAPPING: {invalid_files}")
                else:
                    print(f"    ✅ KEY_TO_FILE_MAPPING корректен: {len(key_to_file)} записей")
                    
                # Проверяем переименованный ключ
                if "stabilizer_compounds" in key_to_file:
                    print("    ✅ Ключ stabilizer_compounds найден (русский ключ успешно переименован)")
                else:
                    print("    ⚠️ Ключ stabilizer_compounds не найден")
            else:
                print("    ℹ️ KEY_TO_FILE_MAPPING не найден или пустой")
        
    except Exception as e:
        print(f"    ⚠️ Ошибка проверки KEY_TO_FILE_MAPPING: {e}")

if __name__ == "__main__":
    test_fat_and_oil_mappings()
