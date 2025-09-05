#!/usr/bin/env python3
"""
Исправленный скрипт для точной проверки синхронизации субключей.
"""

import re
from pathlib import Path

def extract_subkeys_from_enums_file_correct(file_path):
    """Правильно извлекаем субключи из enums.py"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    subkeys_by_json = {}
    
    # Находим начало DRINKS_ENUM_MAPPING
    start_pattern = r'DRINKS_ENUM_MAPPING\s*=\s*\{'
    start_match = re.search(start_pattern, content)
    if not start_match:
        return {}
    
    start_pos = start_match.end()
    
    # Находим JSON файлы в структуре
    json_pattern = r'"([^"]+\.json)":\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}'
    
    # Обрабатываем содержимое после DRINKS_ENUM_MAPPING = {
    mapping_content = content[start_pos:]
    
    # Разбиваем по JSON файлам более точно
    lines = mapping_content.split('\n')
    current_json = None
    current_subkeys = []
    brace_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Считаем скобки для определения уровня вложенности
        brace_level += stripped.count('{') - stripped.count('}')
        
        # Ищем JSON файл (уровень 1)
        json_match = re.match(r'"([^"]+\.json)":\s*\{', stripped)
        if json_match and brace_level == 1:
            # Сохраняем предыдущий JSON если есть
            if current_json and current_subkeys:
                subkeys_by_json[current_json] = current_subkeys.copy()
            
            current_json = json_match.group(1)
            current_subkeys = []
            continue
        
        # Ищем субключи (уровень 2) - содержат комментарий "# Субключ"
        if current_json and brace_level == 2:
            subkey_match = re.match(r'"([^"]+)":\s*\{\s*#\s*Субключ', stripped)
            if subkey_match:
                current_subkeys.append(subkey_match.group(1))
    
    # Сохраняем последний JSON
    if current_json and current_subkeys:
        subkeys_by_json[current_json] = current_subkeys
    
    return subkeys_by_json

def extract_subkeys_from_keys_file(file_path):
    """Извлекаем субключи из KEY_TO_FILE_MAPPING"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем KEY_TO_FILE_MAPPING
    start_pattern = r'KEY_TO_FILE_MAPPING\s*=\s*\{'
    end_pattern = r'^\}'
    
    start_match = re.search(start_pattern, content, re.MULTILINE)
    if not start_match:
        return {}
    
    # Находим содержимое между скобками
    start_pos = start_match.end()
    lines = content[start_pos:].split('\n')
    
    subkeys_by_json = {}
    
    for line in lines:
        if line.strip() == '}':
            break
            
        # Ищем пары "subkey": "filename.json"
        pair_match = re.search(r'"([^"]+)":\s*"([^"]+\.json)"', line)
        if pair_match:
            subkey, json_file = pair_match.groups()
            if json_file not in subkeys_by_json:
                subkeys_by_json[json_file] = []
            subkeys_by_json[json_file].append(subkey)
    
    return subkeys_by_json

def compare_detailed(enums_subkeys, keys_subkeys):
    """Детальное сравнение с улучшенной отчетностью"""
    print("🔍 ДЕТАЛЬНЫЙ АНАЛИЗ СИНХРОНИЗАЦИИ СУБКЛЮЧЕЙ")
    print("="*80)
    
    all_json_files = sorted(set(enums_subkeys.keys()) | set(keys_subkeys.keys()))
    
    total_errors = 0
    total_matches = 0
    perfect_files = 0
    
    for json_file in all_json_files:
        print(f"\n📁 {json_file}")
        print("-" * 60)
        
        enums_subs = set(enums_subkeys.get(json_file, []))
        keys_subs = set(keys_subkeys.get(json_file, []))
        
        if json_file not in enums_subkeys:
            print(f"❌ КРИТИЧНО: Файл полностью отсутствует в DRINKS_ENUM_MAPPING!")
            total_errors += len(keys_subs)
            continue
            
        if json_file not in keys_subkeys:
            print(f"⚠️  ВНИМАНИЕ: Файл отсутствует в KEY_TO_FILE_MAPPING!")
            continue
        
        # Анализ различий
        only_in_enums = enums_subs - keys_subs
        only_in_keys = keys_subs - enums_subs
        common = enums_subs & keys_subs
        
        # Показываем результаты
        if only_in_enums:
            print(f"🔸 Лишние в enums.py ({len(only_in_enums)}):")
            for subkey in sorted(only_in_enums):
                print(f"     - {subkey}")
            total_errors += len(only_in_enums)
        
        if only_in_keys:
            print(f"❌ Отсутствуют в enums.py ({len(only_in_keys)}):")
            for subkey in sorted(only_in_keys):
                print(f"     - {subkey}")
            total_errors += len(only_in_keys)
        
        if common:
            print(f"✅ Синхронизированы ({len(common)}):")
            # Показываем все синхронизированные
            for subkey in sorted(common):
                print(f"     - {subkey}")
            total_matches += len(common)
        
        # Статистика по файлу
        total_expected = len(keys_subs)
        if total_expected > 0:
            match_percent = len(common) / total_expected * 100
            status = "🎯 ИДЕАЛЬНО" if match_percent == 100 else "⚠️ ТРЕБУЕТ ИСПРАВЛЕНИЙ"
            print(f"\n📊 {status}: {len(common)}/{total_expected} ({match_percent:.1f}%)")
            
            if match_percent == 100:
                perfect_files += 1
    
    # Итоговая статистика
    print("\n" + "="*80)
    print("📈 ИТОГОВАЯ СТАТИСТИКА")
    print("="*80)
    
    total_enums = sum(len(subs) for subs in enums_subkeys.values())
    total_keys = sum(len(subs) for subs in keys_subkeys.values())
    total_expected = total_keys
    
    print(f"📁 JSON файлов обработано: {len(all_json_files)}")
    print(f"📁 Файлов с идеальным соответствием: {perfect_files}")
    print(f"📊 Субключей в enums.py: {total_enums}")
    print(f"📊 Субключей ожидалось (из keys.py): {total_expected}")
    print(f"✅ Корректных совпадений: {total_matches}")
    print(f"❌ Найдено проблем: {total_errors}")
    
    if total_expected > 0:
        success_rate = total_matches / total_expected * 100
        print(f"🎯 Общий процент готовности: {success_rate:.1f}%")
        
        if success_rate >= 95:
            print("\n🎉 СТАТУС: ОТЛИЧНО - система практически готова!")
        elif success_rate >= 80:
            print("\n✅ СТАТУС: ХОРОШО - требуются минорные исправления")
        elif success_rate >= 50:
            print("\n⚠️  СТАТУС: УДОВЛЕТВОРИТЕЛЬНО - требуется работа")
        else:
            print("\n❌ СТАТУС: КРИТИЧНО - требуется масштабная доработка")
        
        missing_count = total_expected - total_matches
        if missing_count > 0:
            print(f"🔧 Требуется добавить: {missing_count} субключей в enums.py")

def main():
    print("🚀 ТОЧНАЯ ПРОВЕРКА СИНХРОНИЗАЦИИ СУБКЛЮЧЕЙ")
    print("="*80)
    
    # Пути к файлам
    base_path = Path("/Users/mask/Documents/Проеты_2025/szsb_sales/app/core/tool_calling/drinks/mappings")
    enums_file = base_path / "enums.py"
    keys_file = base_path / "keys.py"
    
    if not all([enums_file.exists(), keys_file.exists()]):
        print("❌ Не все файлы найдены!")
        return
    
    print("📂 Читаем enums.py с улучшенным парсером...")
    enums_subkeys = extract_subkeys_from_enums_file_correct(enums_file)
    print(f"✅ Найдено JSON файлов: {len(enums_subkeys)}")
    
    print("📂 Читаем keys.py...")
    keys_subkeys = extract_subkeys_from_keys_file(keys_file)
    print(f"✅ Найдено JSON файлов: {len(keys_subkeys)}")
    
    # Детальный анализ
    compare_detailed(enums_subkeys, keys_subkeys)

if __name__ == "__main__":
    main()