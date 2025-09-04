#!/usr/bin/env python3
"""
Скрипт валидации соответствий между keys.py, enums.py, universal.py и JSON файлами 
для отрасли drinks (Напитки).

Проверяет:
1. Соответствие DRINKS_KEYS_MAPPING структуре JSON файлов
2. Полноту KEY_TO_FILE_MAPPING для всех субключей
3. Наличие enums в DRINKS_ENUM_MAPPING для всех ключей/субключей
4. Покрытие universal patterns в DRINKS_SPECIFIC_MAPPING для всех enum значений

Автор: Claude Code
Дата: 2025-09-04
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
from datetime import datetime

# Цвета для консольного вывода
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Пути к файлам
BASE_DIR = Path(__file__).parent
DRINKS_MAPPINGS_DIR = BASE_DIR / "app" / "core" / "tool_calling" / "drinks" / "mappings"
JSON_DIR = BASE_DIR / "app" / "routes" / "drinks"

class DrinksValidationReport:
    """Класс для сбора и форматирования результатов валидации."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.stats: Dict[str, Any] = {}
        
    def add_error(self, message: str):
        self.errors.append(message)
        
    def add_warning(self, message: str):
        self.warnings.append(message)
        
    def add_info(self, message: str):
        self.info.append(message)
        
    def add_stats(self, category: str, data: Any):
        self.stats[category] = data
        
    def get_summary(self) -> str:
        """Генерирует итоговый отчет."""
        lines = []
        lines.append(f"\n{Colors.BOLD}=== ОТЧЕТ ВАЛИДАЦИИ DRINKS MAPPINGS ==={Colors.END}")
        lines.append(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Статистика
        if self.stats:
            lines.append(f"{Colors.BLUE}📊 СТАТИСТИКА:{Colors.END}")
            for category, data in self.stats.items():
                if isinstance(data, dict):
                    lines.append(f"  {category}:")
                    for key, value in data.items():
                        lines.append(f"    {key}: {value}")
                else:
                    lines.append(f"  {category}: {data}")
            lines.append("")
        
        # Ошибки
        if self.errors:
            lines.append(f"{Colors.RED}{Colors.BOLD}❌ ОШИБКИ ({len(self.errors)}):{Colors.END}")
            for i, error in enumerate(self.errors, 1):
                lines.append(f"  {i}. {error}")
            lines.append("")
        
        # Предупреждения
        if self.warnings:
            lines.append(f"{Colors.YELLOW}{Colors.BOLD}⚠️  ПРЕДУПРЕЖДЕНИЯ ({len(self.warnings)}):{Colors.END}")
            for i, warning in enumerate(self.warnings, 1):
                lines.append(f"  {i}. {warning}")
            lines.append("")
        
        # Информация
        if self.info:
            lines.append(f"{Colors.CYAN}{Colors.BOLD}ℹ️  ИНФОРМАЦИЯ ({len(self.info)}):{Colors.END}")
            for i, info in enumerate(self.info, 1):
                lines.append(f"  {i}. {info}")
            lines.append("")
        
        # Итоговая оценка
        total_issues = len(self.errors) + len(self.warnings)
        if total_issues == 0:
            lines.append(f"{Colors.GREEN}{Colors.BOLD}✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!{Colors.END}")
            quality = "ОТЛИЧНО"
        elif len(self.errors) == 0:
            lines.append(f"{Colors.YELLOW}{Colors.BOLD}⚠️  ЕСТЬ ПРЕДУПРЕЖДЕНИЯ, НО КРИТИЧЕСКИХ ОШИБОК НЕТ{Colors.END}")
            quality = "ХОРОШО"
        elif len(self.errors) < 5:
            lines.append(f"{Colors.RED}{Colors.BOLD}❌ ОБНАРУЖЕНЫ КРИТИЧЕСКИЕ ОШИБКИ{Colors.END}")
            quality = "ТРЕБУЕТ ИСПРАВЛЕНИЯ"
        else:
            lines.append(f"{Colors.RED}{Colors.BOLD}💀 МНОЖЕСТВЕННЫЕ КРИТИЧЕСКИЕ ОШИБКИ{Colors.END}")
            quality = "КРИТИЧЕСКОЕ СОСТОЯНИЕ"
        
        lines.append(f"{Colors.BOLD}Общая оценка качества: {quality}{Colors.END}")
        lines.append(f"Всего ошибок: {len(self.errors)}, предупреждений: {len(self.warnings)}")
        
        return "\n".join(lines)

def load_mappings() -> Tuple[Dict, Dict, Dict]:
    """Загружает все mapping файлы."""
    print(f"{Colors.BLUE}🔄 Загружаем mapping файлы...{Colors.END}")
    
    # Добавляем путь к mappings для импорта
    sys.path.insert(0, str(DRINKS_MAPPINGS_DIR))
    
    try:
        import keys
        import enums 
        import universal
        
        keys_mapping = keys.DRINKS_KEYS_MAPPING
        key_to_file_mapping = keys.KEY_TO_FILE_MAPPING
        enum_mapping = enums.DRINKS_ENUM_MAPPING
        universal_mapping = universal.DRINKS_SPECIFIC_MAPPING
        
        print(f"{Colors.GREEN}✅ Загружены все mapping файлы{Colors.END}")
        return keys_mapping, key_to_file_mapping, enum_mapping, universal_mapping
        
    except ImportError as e:
        print(f"{Colors.RED}❌ Ошибка импорта: {e}{Colors.END}")
        sys.exit(1)
    except AttributeError as e:
        print(f"{Colors.RED}❌ Ошибка атрибута: {e}{Colors.END}")
        sys.exit(1)

def load_json_files() -> Dict[str, Dict]:
    """Загружает все JSON файлы из директории drinks."""
    print(f"{Colors.BLUE}🔄 Загружаем JSON файлы...{Colors.END}")
    
    json_files = {}
    json_pattern = JSON_DIR / "*.json"
    
    for json_path in JSON_DIR.glob("*.json"):
        filename = json_path.name
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_files[filename] = json.load(f)
            print(f"  📄 {filename}")
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка чтения {filename}: {e}{Colors.END}")
    
    print(f"{Colors.GREEN}✅ Загружено {len(json_files)} JSON файлов{Colors.END}")
    return json_files

def validate_keys_mapping(keys_mapping: Dict, json_files: Dict[str, Dict], report: DrinksValidationReport):
    """Проверяет соответствие DRINKS_KEYS_MAPPING структуре JSON файлов."""
    print(f"\n{Colors.BLUE}🔍 1. Проверка соответствия DRINKS_KEYS_MAPPING...{Colors.END}")
    
    files_in_keys = set(keys_mapping.keys())
    files_in_json = set(json_files.keys())
    
    # Проверяем покрытие файлов
    missing_files = files_in_json - files_in_keys
    extra_files = files_in_keys - files_in_json
    
    for missing in missing_files:
        report.add_error(f"Файл {missing} есть в JSON, но отсутствует в DRINKS_KEYS_MAPPING")
    
    for extra in extra_files:
        report.add_error(f"Файл {extra} описан в DRINKS_KEYS_MAPPING, но JSON файл не найден")
    
    # Проверяем структуру ключей для каждого файла
    valid_files = files_in_keys & files_in_json
    
    for filename in valid_files:
        json_data = json_files[filename]
        keys_data = keys_mapping[filename]
        
        if 'product_keys' not in keys_data:
            report.add_error(f"{filename}: отсутствует раздел 'product_keys'")
            continue
            
        expected_keys = set(keys_data['product_keys'].keys())
        
        # Ищем реальные ключи в JSON данных
        actual_keys = set()
        sample_product = None
        
        # Ищем sample product в субключах или напрямую в product_list
        for key, value in json_data.items():
            if key in ['description', 'keywords']:
                continue
                
            if isinstance(value, dict):
                if 'product_list' in value:
                    try:
                        # Берем первый продукт как образец
                        first_product_str = value['product_list'][0]
                        sample_product = json.loads(first_product_str)
                        actual_keys.update(sample_product.keys())
                        break
                    except (IndexError, json.JSONDecodeError):
                        continue
        
        if not actual_keys:
            report.add_warning(f"{filename}: не удалось извлечь структуру продуктов")
            continue
            
        # Сравниваем ключи
        missing_keys = actual_keys - expected_keys
        extra_keys = expected_keys - actual_keys
        
        for missing in missing_keys:
            report.add_error(f"{filename}: ключ '{missing}' есть в JSON, но отсутствует в DRINKS_KEYS_MAPPING")
        
        for extra in extra_keys:
            report.add_warning(f"{filename}: ключ '{extra}' описан в DRINKS_KEYS_MAPPING, но отсутствует в JSON")
    
    report.add_stats("Файлы", {
        "Всего JSON файлов": len(files_in_json),
        "Файлов в KEYS_MAPPING": len(files_in_keys),
        "Корректно описанных": len(valid_files),
        "Отсутствующих в mapping": len(missing_files),
        "Лишних в mapping": len(extra_files)
    })
    
    print(f"{Colors.GREEN}✅ Проверка KEYS_MAPPING завершена{Colors.END}")

def validate_key_to_file_mapping(key_to_file_mapping: Dict, json_files: Dict[str, Dict], report: DrinksValidationReport):
    """Проверяет полноту KEY_TO_FILE_MAPPING для всех субключей."""
    print(f"\n{Colors.BLUE}🔍 2. Проверка KEY_TO_FILE_MAPPING...{Colors.END}")
    
    # Собираем все субключи из JSON файлов
    actual_subkeys = set()
    subkey_to_file = {}
    
    for filename, json_data in json_files.items():
        for key, value in json_data.items():
            if key not in ['description', 'keywords'] and isinstance(value, dict):
                actual_subkeys.add(key)
                subkey_to_file[key] = filename
    
    mapped_subkeys = set(key_to_file_mapping.keys())
    
    # Проверяем покрытие
    missing_subkeys = actual_subkeys - mapped_subkeys
    extra_subkeys = mapped_subkeys - actual_subkeys
    
    for missing in missing_subkeys:
        source_file = subkey_to_file.get(missing, "неизвестно")
        report.add_error(f"Субключ '{missing}' из {source_file} отсутствует в KEY_TO_FILE_MAPPING")
    
    for extra in extra_subkeys:
        mapped_file = key_to_file_mapping.get(extra)
        report.add_warning(f"Субключ '{extra}' в KEY_TO_FILE_MAPPING указывает на {mapped_file}, но не найден в JSON")
    
    # Проверяем корректность маппинга
    correct_mappings = 0
    for subkey, mapped_file in key_to_file_mapping.items():
        if subkey in subkey_to_file:
            if subkey_to_file[subkey] == mapped_file:
                correct_mappings += 1
            else:
                report.add_error(f"Субключ '{subkey}': маппинг указывает на {mapped_file}, но реально в {subkey_to_file[subkey]}")
    
    report.add_stats("Субключи", {
        "Всего субключей в JSON": len(actual_subkeys),
        "Субключей в mapping": len(mapped_subkeys), 
        "Корректных маппингов": correct_mappings,
        "Отсутствующих": len(missing_subkeys),
        "Лишних": len(extra_subkeys)
    })
    
    print(f"{Colors.GREEN}✅ Проверка KEY_TO_FILE_MAPPING завершена{Colors.END}")

def validate_enum_mapping(enum_mapping: Dict, keys_mapping: Dict, key_to_file_mapping: Dict, report: DrinksValidationReport):
    """Проверяет наличие enums для всех ключей/субключей."""
    print(f"\n{Colors.BLUE}🔍 3. Проверка DRINKS_ENUM_MAPPING...{Colors.END}")
    
    # Собираем все файлы и субключи из keys_mapping и key_to_file_mapping
    expected_coverage = {}
    
    # Из key_to_file_mapping собираем структуру file -> subkeys
    for subkey, filename in key_to_file_mapping.items():
        if filename not in expected_coverage:
            expected_coverage[filename] = set()
        expected_coverage[filename].add(subkey)
    
    # Проверяем покрытие enum_mapping
    files_in_enum = set(enum_mapping.keys())
    files_expected = set(expected_coverage.keys())
    
    missing_files = files_expected - files_in_enum
    extra_files = files_in_enum - files_expected
    
    for missing in missing_files:
        report.add_error(f"Файл {missing} отсутствует в DRINKS_ENUM_MAPPING")
    
    for extra in extra_files:
        report.add_warning(f"Файл {extra} в DRINKS_ENUM_MAPPING, но не используется")
    
    # Проверяем субключи и их enums
    total_subkeys = 0
    covered_subkeys = 0
    total_field_enums = 0
    
    for filename in files_expected & files_in_enum:
        expected_subkeys = expected_coverage[filename]
        enum_subkeys = set(enum_mapping[filename].keys())
        
        missing_subkeys = expected_subkeys - enum_subkeys
        extra_subkeys = enum_subkeys - expected_subkeys
        
        for missing in missing_subkeys:
            report.add_error(f"{filename}: субключ '{missing}' отсутствует в DRINKS_ENUM_MAPPING")
        
        for extra in extra_subkeys:
            report.add_warning(f"{filename}: субключ '{extra}' в DRINKS_ENUM_MAPPING не найден в JSON")
        
        # Проверяем enums для полей в каждом субключе
        valid_subkeys = expected_subkeys & enum_subkeys
        for subkey in valid_subkeys:
            total_subkeys += 1
            covered_subkeys += 1
            
            # Получаем ожидаемые поля из keys_mapping
            if filename in keys_mapping and 'product_keys' in keys_mapping[filename]:
                expected_fields = set(keys_mapping[filename]['product_keys'].keys())
                enum_fields = set(enum_mapping[filename][subkey].keys())
                
                missing_fields = expected_fields - enum_fields
                for missing_field in missing_fields:
                    report.add_warning(f"{filename}.{subkey}: поле '{missing_field}' не имеет enums")
                
                # Считаем общее количество enum категорий
                for field_name, field_enums in enum_mapping[filename][subkey].items():
                    if isinstance(field_enums, dict):
                        total_field_enums += len(field_enums)
    
    report.add_stats("Enums", {
        "Файлов с enums": len(files_in_enum & files_expected),
        "Субключей покрыто": covered_subkeys,
        "Всего enum категорий": total_field_enums,
        "Файлов без enums": len(missing_files),
        "Лишних файлов": len(extra_files)
    })
    
    print(f"{Colors.GREEN}✅ Проверка ENUM_MAPPING завершена{Colors.END}")

def validate_universal_patterns(universal_mapping: Dict, enum_mapping: Dict, report: DrinksValidationReport):
    """Проверяет покрытие universal patterns для всех enum значений."""
    print(f"\n{Colors.BLUE}🔍 4. Проверка DRINKS_SPECIFIC_MAPPING (universal patterns)...{Colors.END}")
    
    # Собираем все enum значения из enum_mapping
    all_enum_values = set()
    enum_sources = {}  # enum_value -> [(filename, subkey, field)]
    
    for filename, file_enums in enum_mapping.items():
        for subkey, subkey_enums in file_enums.items():
            for field, field_enums in subkey_enums.items():
                if isinstance(field_enums, dict):
                    for enum_category, enum_list in field_enums.items():
                        if isinstance(enum_list, list):
                            for enum_value in enum_list:
                                all_enum_values.add(enum_value)
                                if enum_value not in enum_sources:
                                    enum_sources[enum_value] = []
                                enum_sources[enum_value].append((filename, subkey, field, enum_category))
    
    # Проверяем покрытие universal patterns
    patterns_available = set(universal_mapping.keys())
    
    missing_patterns = all_enum_values - patterns_available
    extra_patterns = patterns_available - all_enum_values
    
    # Группируем отсутствующие паттерны по частоте использования
    missing_by_frequency = []
    for missing in missing_patterns:
        frequency = len(enum_sources.get(missing, []))
        missing_by_frequency.append((missing, frequency))
    
    missing_by_frequency.sort(key=lambda x: x[1], reverse=True)
    
    # Добавляем ошибки для наиболее используемых отсутствующих паттернов
    for enum_value, frequency in missing_by_frequency[:20]:  # Топ 20
        sources = enum_sources.get(enum_value, [])
        source_info = ", ".join([f"{f}.{s}.{field}" for f, s, field, cat in sources[:3]])
        if len(sources) > 3:
            source_info += f" и еще {len(sources) - 3}"
        report.add_error(f"Enum '{enum_value}' (используется {frequency} раз в {source_info}) не имеет universal pattern")
    
    # Добавляем предупреждения для остальных
    for enum_value, frequency in missing_by_frequency[20:]:
        if frequency > 1:  # Только для тех, что используются больше 1 раза
            report.add_warning(f"Enum '{enum_value}' (используется {frequency} раз) не имеет universal pattern")
    
    # Информация о лишних паттернах (могут быть полезными синонимами)
    for extra in sorted(extra_patterns)[:10]:  # Топ 10 лишних
        report.add_info(f"Universal pattern '{extra}' не используется в enums (возможно, полезный синоним)")
    
    report.add_stats("Universal Patterns", {
        "Всего enum значений": len(all_enum_values),
        "Паттернов в mapping": len(patterns_available),
        "Покрытых enum": len(all_enum_values & patterns_available),
        "Отсутствующих паттернов": len(missing_patterns),
        "Лишних паттернов": len(extra_patterns),
        "% покрытия": round(len(all_enum_values & patterns_available) / len(all_enum_values) * 100, 1) if all_enum_values else 0
    })
    
    print(f"{Colors.GREEN}✅ Проверка Universal Patterns завершена{Colors.END}")

def main():
    """Основная функция валидации."""
    print(f"{Colors.BOLD}{Colors.CYAN}🔍 ВАЛИДАЦИЯ DRINKS MAPPINGS{Colors.END}")
    print(f"Проверяем соответствия между keys.py, enums.py, universal.py и JSON файлами")
    print("=" * 70)
    
    # Проверяем существование директорий
    if not DRINKS_MAPPINGS_DIR.exists():
        print(f"{Colors.RED}❌ Директория mappings не найдена: {DRINKS_MAPPINGS_DIR}{Colors.END}")
        sys.exit(1)
        
    if not JSON_DIR.exists():
        print(f"{Colors.RED}❌ Директория JSON не найдена: {JSON_DIR}{Colors.END}")
        sys.exit(1)
    
    # Создаем отчет
    report = DrinksValidationReport()
    
    try:
        # Загружаем данные
        keys_mapping, key_to_file_mapping, enum_mapping, universal_mapping = load_mappings()
        json_files = load_json_files()
        
        # Выполняем проверки
        validate_keys_mapping(keys_mapping, json_files, report)
        validate_key_to_file_mapping(key_to_file_mapping, json_files, report)
        validate_enum_mapping(enum_mapping, keys_mapping, key_to_file_mapping, report)
        validate_universal_patterns(universal_mapping, enum_mapping, report)
        
        # Генерируем и сохраняем отчет
        report_content = report.get_summary()
        print(report_content)
        
        # Сохраняем в файл
        report_file = BASE_DIR / "drinks_mappings_validation_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            # Удаляем цветовые коды для файла
            clean_content = report_content
            for color in [Colors.GREEN, Colors.RED, Colors.YELLOW, Colors.BLUE, Colors.CYAN, Colors.WHITE, Colors.BOLD, Colors.END]:
                clean_content = clean_content.replace(color, '')
            f.write(clean_content)
        
        print(f"\n{Colors.CYAN}📄 Отчет сохранен в: {report_file}{Colors.END}")
        
        # Возвращаем код выхода
        if report.errors:
            sys.exit(1)  # Есть критические ошибки
        elif report.warnings:
            sys.exit(2)  # Есть предупреждения
        else:
            sys.exit(0)  # Все отлично
        
    except Exception as e:
        print(f"{Colors.RED}💀 Критическая ошибка: {e}{Colors.END}")
        import traceback
        print(f"{Colors.RED}{traceback.format_exc()}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()