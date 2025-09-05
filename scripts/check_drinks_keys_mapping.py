"""
Проверка соответствия JSON-файлов из `app/routes/drinks/` ключам
`DRINKS_KEYS_MAPPING` с наглядным print-выводом.

Запуск из корня репозитория:
    python scripts/check_drinks_keys_mapping.py

Скрипт не использует pytest и не импортирует пакет `app`,
чтобы избежать побочных зависимостей — маппинг подгружается
напрямую по пути файла через importlib.
"""

from __future__ import annotations

import sys
from pathlib import Path
import importlib.util
from typing import Dict, Any, Set, List


def load_drinks_keys_mapping(repo_root: Path) -> Dict[str, Any]:
    mapping_path = repo_root / "app" / "core" / "tool_calling" / "drinks" / "mappings" / "keys.py"
    if not mapping_path.is_file():
        print(f"[ERR] Не найден файл маппинга: {mapping_path}")
        sys.exit(2)

    spec = importlib.util.spec_from_file_location("drinks_keys_mapping", str(mapping_path))
    if not spec or not spec.loader:
        print("[ERR] Не удалось создать spec для keys.py")
        sys.exit(2)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

    try:
        return getattr(module, "DRINKS_KEYS_MAPPING")
    except AttributeError:
        print("[ERR] В модуле keys.py отсутствует DRINKS_KEYS_MAPPING")
        sys.exit(2)


def main() -> int:
    # Корень репозитория = родительская директория скрипта
    repo_root = Path(__file__).resolve().parents[1]
    drinks_routes_dir = repo_root / "app" / "routes" / "drinks"

    print("=== Проверка DRINKS_KEYS_MAPPING против app/routes/drinks/*.json ===")
    print(f"Repo root: {repo_root}")
    print(f"Routes dir: {drinks_routes_dir}")

    if not drinks_routes_dir.is_dir():
        print(f"[ERR] Нет директории: {drinks_routes_dir}")
        return 2

    route_json_files: List[str] = sorted(p.name for p in drinks_routes_dir.glob("*.json"))
    if not route_json_files:
        print("[ERR] В app/routes/drinks нет JSON-файлов.")
        return 2

    drinks_keys_mapping = load_drinks_keys_mapping(repo_root)
    mapping_keys: Set[str] = set(drinks_keys_mapping.keys())

    print(f"Найдено файлов в routes/drinks: {len(route_json_files)}")
    print(f"Ключей в DRINKS_KEYS_MAPPING: {len(mapping_keys)}")
    print("\n— Проверка покрытия по каждому файлу:")

    missing: List[str] = []
    for name in route_json_files:
        if name in mapping_keys:
            print(f"  ✔ {name} — OK")
        else:
            print(f"  ✖ {name} — MISSING в DRINKS_KEYS_MAPPING")
            missing.append(name)

    extra: List[str] = sorted(k for k in mapping_keys if k not in route_json_files)
    if extra:
        print("\n— Лишние ключи в DRINKS_KEYS_MAPPING (нет таких файлов в routes/drinks):")
        for k in extra:
            print(f"  • {k}")

    print("\n— Итог:")
    if not missing:
        print("RESULT: SUCCESS — все файлы покрыты ключами DRINKS_KEYS_MAPPING")
        return 0
    else:
        print("RESULT: FAILED — отсутствуют соответствия для:")
        for m in missing:
            print(f"  • {m}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

