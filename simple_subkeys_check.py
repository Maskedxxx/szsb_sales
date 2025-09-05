#!/usr/bin/env python3
"""
Простой скрипт для проверки синхронизации субключей между enums.py и keys.py
без импорта зависимостей проекта.
"""

import re
from pathlib import Path

def extract_subkeys_from_enums_file(file_path):
    """Извлекаем субключи из enums.py файла через regex"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем структуру: "filename.json": { "subkey": {
    pattern = r'"([^"]+\.json)":\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
    
    subkeys_by_json = {}
    
    # Находим все JSON файлы в DRINKS_ENUM_MAPPING
    json_matches = re.findall(pattern, content, re.DOTALL)
    
    for json_file, json_content in json_matches:
        # Ищем субключи внутри каждого JSON файла: "subkey_name": {
        subkey_pattern = r'"([^"]+)":\s*\{\s*#\s*Субключ'
        subkeys = re.findall(subkey_pattern, json_content)
        subkeys_by_json[json_file] = subkeys
    
    return subkeys_by_json

def extract_subkeys_from_keys_file(file_path):
    """Извлекаем субключи из keys.py через KEY_TO_FILE_MAPPING"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем KEY_TO_FILE_MAPPING = { ... }
    mapping_pattern = r'KEY_TO_FILE_MAPPING\s*=\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
    mapping_match = re.search(mapping_pattern, content, re.DOTALL)
    
    if not mapping_match:
        return {}
    
    mapping_content = mapping_match.group(1)
    
    # Ищем пары "subkey": "filename.json"
    pair_pattern = r'"([^"]+)":\s*"([^"]+\.json)"'
    pairs = re.findall(pair_pattern, mapping_content)
    
    subkeys_by_json = {}
    for subkey, json_file in pairs:
        if json_file not in subkeys_by_json:
            subkeys_by_json[json_file] = []
        subkeys_by_json[json_file].append(subkey)
    
    return subkeys_by_json

def compare_and_report(enums_subkeys, keys_subkeys):
    """Сравниваем и выводим отчет"""
    print("🔍 АНАЛИЗ СИНХРОНИЗАЦИИ СУБКЛЮЧЕЙ")
    print("="*80)
    
    all_json_files = set(enums_subkeys.keys()) | set(keys_subkeys.keys())
    
    total_errors = 0
    total_matches = 0
    
    for json_file in sorted(all_json_files):
        print(f"\n📁 {json_file}")
        print("-" * 50)
        
        enums_subs = set(enums_subkeys.get(json_file, []))
        keys_subs = set(keys_subkeys.get(json_file, []))
        
        # Проверки
        if json_file not in enums_subkeys:
            print(f"❌ ОШИБКА: Файл отсутствует в DRINKS_ENUM_MAPPING!")
            total_errors += 1
            continue
            
        if json_file not in keys_subkeys:
            print(f"⚠️  Файл отсутствует в KEY_TO_FILE_MAPPING!")
            continue
        
        # Различия
        only_in_enums = enums_subs - keys_subs
        only_in_keys = keys_subs - enums_subs
        common = enums_subs & keys_subs
        
        if only_in_enums:
            print(f"❌ Только в enums.py ({len(only_in_enums)}):")
            for subkey in sorted(only_in_enums):
                print(f"   - {subkey}")
            total_errors += len(only_in_enums)
        
        if only_in_keys:
            print(f"❌ Только в keys.py ({len(only_in_keys)}):")
            for subkey in sorted(only_in_keys):
                print(f"   - {subkey}")
            total_errors += len(only_in_keys)
        
        if common:
            print(f"✅ Совпадает ({len(common)}):")
            for subkey in sorted(list(common)[:5]):  # Показываем первые 5
                print(f"   - {subkey}")
            if len(common) > 5:
                print(f"   ... и еще {len(common) - 5}")
            total_matches += len(common)
        
        # Статистика по файлу
        total_file = max(len(enums_subs), len(keys_subs))
        if total_file > 0:
            match_percent = len(common) / total_file * 100
            print(f"📊 Соответствие: {len(common)}/{total_file} ({match_percent:.1f}%)")

    # Общая статистика
    print("\n" + "="*80)
    print("📈 ИТОГОВАЯ СТАТИСТИКА")
    print("="*80)
    
    total_enums = sum(len(subs) for subs in enums_subkeys.values())
    total_keys = sum(len(subs) for subs in keys_subkeys.values())
    
    print(f"JSON файлов в enums.py: {len(enums_subkeys)}")
    print(f"JSON файлов в keys.py: {len(keys_subkeys)}")
    print(f"Всего субключей в enums.py: {total_enums}")
    print(f"Всего субключей в keys.py: {total_keys}")
    print(f"Совпадающих субключей: {total_matches}")
    print(f"Найдено ошибок: {total_errors}")
    
    if max(total_enums, total_keys) > 0:
        success_rate = total_matches / max(total_enums, total_keys) * 100
        print(f"Общий процент соответствия: {success_rate:.1f}%")
        
        if success_rate >= 95:
            print("🎉 ОТЛИЧНО: Высокий уровень синхронизации!")
        elif success_rate >= 80:
            print("⚠️  ХОРОШО: Требуются незначительные исправления")
        else:
            print("❌ КРИТИЧНО: Требуются существенные исправления")

def main():
    print("🚀 ПРОВЕРКА СИНХРОНИЗАЦИИ СУБКЛЮЧЕЙ DRINKS")
    print("="*80)
    
    # Пути к файлам
    base_path = Path("/Users/mask/Documents/Проеты_2025/szsb_sales/app/core/tool_calling/drinks/mappings")
    enums_file = base_path / "enums.py"
    keys_file = base_path / "keys.py"
    
    # Проверяем существование файлов
    if not enums_file.exists():
        print(f"❌ Файл не найден: {enums_file}")
        return
    
    if not keys_file.exists():
        print(f"❌ Файл не найден: {keys_file}")
        return
    
    print(f"📂 Анализируем: {enums_file}")
    print(f"📂 Анализируем: {keys_file}")
    
    # Извлекаем данные
    try:
        enums_subkeys = extract_subkeys_from_enums_file(enums_file)
        print(f"✅ Из enums.py извлечено: {len(enums_subkeys)} JSON файлов")
        
        keys_subkeys = extract_subkeys_from_keys_file(keys_file)
        print(f"✅ Из keys.py извлечено: {len(keys_subkeys)} JSON файлов")
        
        # Сравниваем
        compare_and_report(enums_subkeys, keys_subkeys)
        
    except Exception as e:
        print(f"❌ Ошибка при анализе: {e}")

if __name__ == "__main__":
    main()