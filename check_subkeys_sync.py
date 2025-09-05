#!/usr/bin/env python3
"""
Скрипт для проверки синхронизации субключей между enums.py и keys.py
в отрасли напитков (drinks).
"""

import sys
import os
from pathlib import Path

# Добавляем путь к проекту
project_path = Path("/Users/mask/Documents/Проеты_2025/szsb_sales")
sys.path.append(str(project_path))

def load_drinks_mappings():
    """Загружаем маппинги из файлов drinks отрасли"""
    try:
        # Импортируем маппинги
        from app.core.tool_calling.drinks.mappings.enums import DRINKS_ENUM_MAPPING
        from app.core.tool_calling.drinks.mappings.keys import KEY_TO_FILE_MAPPING
        
        return DRINKS_ENUM_MAPPING, KEY_TO_FILE_MAPPING
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return None, None

def extract_subkeys_from_enums(enum_mapping):
    """Извлекаем все субключи из DRINKS_ENUM_MAPPING"""
    subkeys_by_json = {}
    
    for json_file, subkeys_dict in enum_mapping.items():
        subkeys_by_json[json_file] = list(subkeys_dict.keys())
    
    return subkeys_by_json

def extract_subkeys_from_key_mapping(key_mapping):
    """Извлекаем все субключи из KEY_TO_FILE_MAPPING"""
    subkeys_by_json = {}
    
    for subkey, json_file in key_mapping.items():
        if json_file not in subkeys_by_json:
            subkeys_by_json[json_file] = []
        subkeys_by_json[json_file].append(subkey)
    
    return subkeys_by_json

def compare_subkeys(enums_subkeys, keys_subkeys):
    """Сравниваем субключи между двумя источниками"""
    print("🔍 АНАЛИЗ СИНХРОНИЗАЦИИ СУБКЛЮЧЕЙ\n")
    print("="*80)
    
    # Все JSON файлы из обоих источников
    all_json_files = set(enums_subkeys.keys()) | set(keys_subkeys.keys())
    
    errors_found = False
    warnings_found = False
    
    for json_file in sorted(all_json_files):
        print(f"\n📁 {json_file}")
        print("-" * 50)
        
        enums_subs = set(enums_subkeys.get(json_file, []))
        keys_subs = set(keys_subkeys.get(json_file, []))
        
        # Проверяем отсутствие файла в одном из источников
        if json_file not in enums_subkeys:
            print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: Файл отсутствует в DRINKS_ENUM_MAPPING!")
            errors_found = True
            continue
            
        if json_file not in keys_subkeys:
            print(f"⚠️  ВНИМАНИЕ: Файл отсутствует в KEY_TO_FILE_MAPPING!")
            warnings_found = True
            continue
        
        # Субключи только в enums.py
        only_in_enums = enums_subs - keys_subs
        if only_in_enums:
            print(f"❌ Только в enums.py ({len(only_in_enums)}):")
            for subkey in sorted(only_in_enums):
                print(f"   - {subkey}")
            errors_found = True
        
        # Субключи только в keys.py  
        only_in_keys = keys_subs - enums_subs
        if only_in_keys:
            print(f"❌ Только в KEY_TO_FILE_MAPPING ({len(only_in_keys)}):")
            for subkey in sorted(only_in_keys):
                print(f"   - {subkey}")
            errors_found = True
        
        # Общие субключи
        common_subs = enums_subs & keys_subs
        if common_subs:
            print(f"✅ Общие субключи ({len(common_subs)}):")
            for subkey in sorted(common_subs):
                print(f"   - {subkey}")
        
        # Статистика
        print(f"\n📊 Статистика для {json_file}:")
        print(f"   enums.py: {len(enums_subs)} субключей")
        print(f"   keys.py:  {len(keys_subs)} субключей")
        print(f"   Соответствие: {len(common_subs)}/{max(len(enums_subs), len(keys_subs))} "
              f"({len(common_subs)/max(len(enums_subs), len(keys_subs))*100:.1f}%)")

def print_summary_stats(enums_subkeys, keys_subkeys):
    """Выводим общую статистику"""
    print("\n" + "="*80)
    print("📈 ОБЩАЯ СТАТИСТИКА")
    print("="*80)
    
    total_enums = sum(len(subs) for subs in enums_subkeys.values())
    total_keys = sum(len(subs) for subs in keys_subkeys.values())
    
    print(f"JSON файлов в enums.py: {len(enums_subkeys)}")
    print(f"JSON файлов в keys.py: {len(keys_subkeys)}")
    print(f"Всего субключей в enums.py: {total_enums}")
    print(f"Всего субключей в KEY_TO_FILE_MAPPING: {total_keys}")
    
    # Подсчет совпадений
    common_files = set(enums_subkeys.keys()) & set(keys_subkeys.keys())
    total_matches = 0
    for json_file in common_files:
        enums_subs = set(enums_subkeys[json_file])
        keys_subs = set(keys_subkeys[json_file])
        total_matches += len(enums_subs & keys_subs)
    
    print(f"Совпадающих субключей: {total_matches}")
    if max(total_enums, total_keys) > 0:
        match_percent = total_matches / max(total_enums, total_keys) * 100
        print(f"Общий процент соответствия: {match_percent:.1f}%")

def main():
    print("🚀 ЗАПУСК ПРОВЕРКИ СИНХРОНИЗАЦИИ СУБКЛЮЧЕЙ")
    print("="*80)
    
    # Загружаем маппинги
    enum_mapping, key_mapping = load_drinks_mappings()
    
    if not enum_mapping or not key_mapping:
        print("❌ Не удалось загрузить маппинги!")
        return
    
    # Извлекаем субключи
    print("📤 Извлечение субключей из DRINKS_ENUM_MAPPING...")
    enums_subkeys = extract_subkeys_from_enums(enum_mapping)
    
    print("📤 Извлечение субключей из KEY_TO_FILE_MAPPING...")
    keys_subkeys = extract_subkeys_from_key_mapping(key_mapping)
    
    # Сравниваем
    compare_subkeys(enums_subkeys, keys_subkeys)
    
    # Общая статистика
    print_summary_stats(enums_subkeys, keys_subkeys)
    
    print("\n✅ Проверка завершена!")

if __name__ == "__main__":
    main()