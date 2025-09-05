"""
Проверка соответствия «подключей» (топ-уровневые ключи JSON, кроме
description/keywords) из `app/routes/drinks/*.json` маппингу
`KEY_TO_FILE_MAPPING` в `app/core/tool_calling/drinks/mappings/keys.py`.

Требование: для каждого подклуча в файле должен быть ключ в
`KEY_TO_FILE_MAPPING`, где значение — имя этого JSON-файла.

Также выводятся «лишние» ключи `KEY_TO_FILE_MAPPING`, которые указывают на
существующий файл в routes/drinks, но такого подклуча в файле нет.

Запуск из корня репозитория:
    python scripts/check_drinks_subkeys_mapping.py
"""

from __future__ import annotations

import sys
import json
from pathlib import Path
import importlib.util
from typing import Dict, Any, Set, List, Tuple


def load_keys_module_attr(repo_root: Path, attr_name: str):
    mapping_path = repo_root / "app" / "core" / "tool_calling" / "drinks" / "mappings" / "keys.py"
    if not mapping_path.is_file():
        print(f"[ERR] Не найден файл: {mapping_path}")
        sys.exit(2)

    spec = importlib.util.spec_from_file_location("drinks_keys_mapping", str(mapping_path))
    if not spec or not spec.loader:
        print("[ERR] Не удалось создать spec для keys.py")
        sys.exit(2)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

    try:
        return getattr(module, attr_name)
    except AttributeError:
        print(f"[ERR] В keys.py отсутствует {attr_name}")
        sys.exit(2)


def collect_file_subkeys(json_path: Path) -> List[str]:
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"  [ERR] Не удалось прочитать {json_path.name}: {e}")
        return []

    if not isinstance(data, dict):
        print(f"  [WARN] {json_path.name}: верхний уровень не dict — пропускаю")
        return []

    # Подключи — все топ-уровневые ключи, кроме служебных
    return [k for k in data.keys() if k not in ("description", "keywords")]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    drinks_routes_dir = repo_root / "app" / "routes" / "drinks"

    print("=== Проверка KEY_TO_FILE_MAPPING для подключей в routes/drinks ===")
    print(f"Repo root: {repo_root}")
    print(f"Routes dir: {drinks_routes_dir}")

    if not drinks_routes_dir.is_dir():
        print(f"[ERR] Нет директории: {drinks_routes_dir}")
        return 2

    json_files: List[Path] = sorted(drinks_routes_dir.glob("*.json"))
    if not json_files:
        print("[ERR] Нет JSON-файлов в routes/drinks")
        return 2

    key_to_file: Dict[str, str] = load_keys_module_attr(repo_root, "KEY_TO_FILE_MAPPING")

    print(f"Файлов: {len(json_files)}  |  Пары в KEY_TO_FILE_MAPPING: {len(key_to_file)}")

    has_errors = False

    # Проверяем, что каждый подклуч из файла правильно отражён в KEY_TO_FILE_MAPPING
    for jf in json_files:
        fname = jf.name
        subkeys = collect_file_subkeys(jf)
        print(f"\n— {fname}: найдено подключей: {len(subkeys)}")
        if not subkeys:
            print("   [INFO] Подключи не найдены (возможен простой формат файла)")
        for sk in subkeys:
            mapped = key_to_file.get(sk)
            if mapped is None:
                print(f"   ✖ {sk} — MISSING в KEY_TO_FILE_MAPPING")
                has_errors = True
            elif mapped != fname:
                print(f"   ✖ {sk} — WRONG_TARGET ⇒ {mapped} (ожидалось: {fname})")
                has_errors = True
            else:
                print(f"   ✔ {sk} — OK")

    # Лишние ключи (указывает на существующий файл, но такого подклуча нет в файле)
    existing_files = {p.name for p in json_files}
    file_to_subkeys: Dict[str, Set[str]] = {}
    for jf in json_files:
        file_to_subkeys[jf.name] = set(collect_file_subkeys(jf))

    extras: List[Tuple[str, str]] = []  # (subkey, target_file)
    for sk, target in key_to_file.items():
        if target in existing_files and sk not in file_to_subkeys.get(target, set()):
            extras.append((sk, target))

    if extras:
        print("\n— Лишние ключи в KEY_TO_FILE_MAPPING (не найдены как подключи соответствующего файла):")
        for sk, target in sorted(extras, key=lambda x: (x[1], x[0])):
            print(f"   • {sk} ⇒ {target}")
        has_errors = True

    print("\n— Итог:")
    if has_errors:
        print("RESULT: FAILED — есть несоответствия подключей и KEY_TO_FILE_MAPPING")
        return 1
    else:
        print("RESULT: SUCCESS — все подключи корректно отражены в KEY_TO_FILE_MAPPING и нет лишних записей")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

