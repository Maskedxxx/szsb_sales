#!/usr/bin/env python3
"""
Скрипт анализа субключей для drinks mappings
Выводит отсутствующие и лишние субключи в KEY_TO_FILE_MAPPING
"""

import json
import os
from pathlib import Path

def load_json_files():
    """Загружает все JSON файлы из директории drinks"""
    drinks_dir = Path("app/routes/drinks")
    json_files = {}
    
    for json_file in drinks_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                json_files[json_file.name] = data
        except Exception as e:
            print(f"❌ Ошибка загрузки {json_file.name}: {e}")
    
    return json_files

def load_keys_mapping():
    """Загружает KEY_TO_FILE_MAPPING из keys.py"""
    try:
        # Импортируем keys.py
        import sys
        sys.path.append('app/core/tool_calling/drinks/mappings')
        from keys import KEY_TO_FILE_MAPPING
        return KEY_TO_FILE_MAPPING
    except ImportError as e:
        print(f"❌ Не удалось импортировать KEY_TO_FILE_MAPPING: {e}")
        return {}

def extract_subkeys_from_json(json_data):
    """Извлекает все субключи из JSON файла"""
    subkeys = set()
    
    def traverse_dict(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict) and "product_list" in value:
                    # Это субключ с product_list
                    subkeys.add(key)
                elif isinstance(value, dict):
                    # Продолжаем обход
                    traverse_dict(value, f"{path}.{key}" if path else key)
    
    traverse_dict(json_data)
    return subkeys

def main():
    print("🔍 АНАЛИЗ СУБКЛЮЧЕЙ ДЛЯ DRINKS MAPPINGS")
    print("=" * 50)
    
    # Загружаем данные
    json_files = load_json_files()
    keys_mapping = load_keys_mapping()
    
    if not json_files:
        print("❌ Не найдены JSON файлы в app/routes/drinks/")
        return
    
    if not keys_mapping:
        print("❌ Не загружен KEY_TO_FILE_MAPPING")
        return
    
    print(f"📁 Найдено JSON файлов: {len(json_files)}")
    print(f"🗂️ Записей в KEY_TO_FILE_MAPPING: {len(keys_mapping)}")
    print()
    
    # Извлекаем все субключи из JSON файлов
    all_json_subkeys = {}  # filename -> set of subkeys
    for filename, data in json_files.items():
        subkeys = extract_subkeys_from_json(data)
        all_json_subkeys[filename] = subkeys
        print(f"📄 {filename}: {len(subkeys)} субключей")
    
    # Объединяем все субключи из JSON
    all_subkeys_in_json = set()
    subkey_to_files = {}  # subkey -> list of files where it appears
    
    for filename, subkeys in all_json_subkeys.items():
        for subkey in subkeys:
            all_subkeys_in_json.add(subkey)
            if subkey not in subkey_to_files:
                subkey_to_files[subkey] = []
            subkey_to_files[subkey].append(filename)
    
    print(f"\n📊 Всего уникальных субключей в JSON: {len(all_subkeys_in_json)}")
    print(f"📋 Субключей в KEY_TO_FILE_MAPPING: {len(keys_mapping)}")
    
    # Находим отсутствующие субключи (есть в JSON, нет в mapping)
    missing_subkeys = all_subkeys_in_json - set(keys_mapping.keys())
    
    # Находим лишние субключи (есть в mapping, нет в JSON)
    extra_subkeys = set(keys_mapping.keys()) - all_subkeys_in_json
    
    # Находим неправильные маппинги (субключ указывает на файл, где его нет)
    wrong_mappings = []
    for subkey, mapped_file in keys_mapping.items():
        if subkey in subkey_to_files:
            if mapped_file not in subkey_to_files[subkey]:
                wrong_mappings.append((subkey, mapped_file, subkey_to_files[subkey]))
    
    print("\n" + "=" * 50)
    print("❌ ОТСУТСТВУЮЩИЕ СУБКЛЮЧИ (есть в JSON, нет в mapping):")
    print(f"Количество: {len(missing_subkeys)}")
    
    if missing_subkeys:
        for subkey in sorted(missing_subkeys):
            files = subkey_to_files.get(subkey, [])
            print(f"  • {subkey} → найден в: {', '.join(files)}")
    else:
        print("  ✅ Отсутствующих субключей нет")
    
    print("\n" + "=" * 50)
    print("➕ ЛИШНИЕ СУБКЛЮЧИ (есть в mapping, нет в JSON):")
    print(f"Количество: {len(extra_subkeys)}")
    
    if extra_subkeys:
        for subkey in sorted(extra_subkeys):
            mapped_file = keys_mapping.get(subkey, "")
            print(f"  • {subkey} → указывает на: {mapped_file}")
    else:
        print("  ✅ Лишних субключей нет")
    
    print("\n" + "=" * 50)
    print("⚠️ НЕПРАВИЛЬНЫЕ МАППИНГИ:")
    print(f"Количество: {len(wrong_mappings)}")
    
    if wrong_mappings:
        for subkey, wrong_file, correct_files in wrong_mappings:
            print(f"  • {subkey}:")
            print(f"    ❌ Указывает на: {wrong_file}")
            print(f"    ✅ Должен указывать на: {', '.join(correct_files)}")
    else:
        print("  ✅ Неправильных маппингов нет")
    
    print("\n" + "=" * 50)
    print("📈 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"Всего субключей в JSON: {len(all_subkeys_in_json)}")
    print(f"Субключей в mapping: {len(keys_mapping)}")
    print(f"Отсутствующих: {len(missing_subkeys)}")
    print(f"Лишних: {len(extra_subkeys)}")
    print(f"Неправильных маппингов: {len(wrong_mappings)}")
    
    # Рекомендации по исправлению
    print("\n" + "=" * 50)
    print("🔧 РЕКОМЕНДАЦИИ ПО ИСПРАВЛЕНИЮ:")
    
    if missing_subkeys:
        print("\n1️⃣ Добавить в KEY_TO_FILE_MAPPING:")
        for subkey in sorted(missing_subkeys):
            files = subkey_to_files.get(subkey, [])
            if len(files) == 1:
                print(f"    '{subkey}': '{files[0]}',")
            else:
                print(f"    '{subkey}': '{files[0]}',  # также встречается в: {', '.join(files[1:])}")
    
    if extra_subkeys:
        print("\n2️⃣ Удалить из KEY_TO_FILE_MAPPING:")
        for subkey in sorted(extra_subkeys):
            print(f"    '{subkey}': '{keys_mapping[subkey]}',  # <-- удалить эту строку")
    
    if wrong_mappings:
        print("\n3️⃣ Исправить маппинги:")
        for subkey, wrong_file, correct_files in wrong_mappings:
            print(f"    '{subkey}': '{correct_files[0]}',  # было: '{wrong_file}'")

if __name__ == "__main__":
    main()