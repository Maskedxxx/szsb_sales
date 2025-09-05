"""
Простой тест: собирает имена JSON-файлов из `app/routes/drinks/`
и проверяет, что для каждого из них есть ключ в DRINKS_KEYS_MAPPING.

Важно: модуль с маппингом грузим по пути файла, чтобы избежать
побочных импортов из пакета `app`.
"""

from pathlib import Path
import importlib.util


def _load_drinks_keys_mapping_via_path(repo_root: Path):
    mapping_path = repo_root / "app" / "core" / "tool_calling" / "drinks" / "mappings" / "keys.py"
    assert mapping_path.is_file(), f"Не найден файл маппинга: {mapping_path}"

    spec = importlib.util.spec_from_file_location("drinks_keys_mapping", str(mapping_path))
    assert spec and spec.loader, "Не удалось создать spec для keys.py"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return getattr(module, "DRINKS_KEYS_MAPPING")


def test_drinks_keys_mapping_covers_all_route_jsons():
    # Корень репозитория
    repo_root = Path(__file__).resolve().parents[1]
    drinks_routes_dir = repo_root / "app" / "routes" / "drinks"
    assert drinks_routes_dir.is_dir(), f"Нет директории: {drinks_routes_dir}"

    # Все JSON-файлы в routes/drinks
    route_json_files = sorted(p.name for p in drinks_routes_dir.glob("*.json"))
    assert route_json_files, "В app/routes/drinks нет JSON-файлов."

    # Грузим маппинг из файла (без импорта пакета app)
    drinks_keys_mapping = _load_drinks_keys_mapping_via_path(repo_root)
    mapping_keys = set(drinks_keys_mapping.keys())

    # Какие файлы отсутствуют в маппинге
    missing_in_mapping = [name for name in route_json_files if name not in mapping_keys]

    assert not missing_in_mapping, (
        "Отсутствуют ключи в DRINKS_KEYS_MAPPING для файлов: " + ", ".join(missing_in_mapping)
    )
