"""
Builds two lists for milk tool-calling sync:
- all enum values declared in enums.py
- all explicitly supported keys in universal.py (patterns + checkers)

Prints counts and the differences grouped to highlight gaps.

Usage:
  python tools/check_milk_enum_sync.py
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple
import importlib.util


def _repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def _setup_path() -> None:
    root = _repo_root()
    if root not in sys.path:
        sys.path.insert(0, root)


def _iter_enum_leaves(mapping: Dict) -> Iterable[Tuple[str, str, str, str]]:
    """
    Yields tuples of (file_name, product_key, section_key, enum_value)
    for each enum value listed under MILK_ENUM_MAPPING.
    """
    for file_name, file_data in mapping.items():
        for product_key, product_sections in (file_data or {}).items():
            for section_key, categories in (product_sections or {}).items():
                for _category, values in (categories or {}).items():
                    for enum_value in values or []:
                        yield file_name, product_key, section_key, enum_value


def _supported_universal_keys(universal_module) -> Set[str]:
    supported: Set[str] = set()
    supported.update((universal_module.MILK_SPECIFIC_MAPPING or {}).keys())
    supported.update((universal_module.MILK_SPECIFIC_CHECKERS or {}).keys())
    supported.update((universal_module.UNIVERSAL_KBGU_CHECKERS or {}).keys())
    supported.update((universal_module.PACKAGING_CHECKERS or {}).keys())
    supported.update((universal_module.SHELF_LIFE_CHECKERS or {}).keys())
    return supported


def _load_module(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module {module_name} from {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


def main() -> int:
    _setup_path()

    root = _repo_root()
    enums_path = os.path.join(root, "app", "core", "tool_calling", "milk", "mappings", "enums.py")
    universal_path = os.path.join(root, "app", "core", "tool_calling", "milk", "mappings", "universal.py")

    enums_mod = _load_module("milk_enums_mod", enums_path)
    universal_mod = _load_module("milk_universal_mod", universal_path)

    all_enums: Set[str] = set()
    missing_by_group = defaultdict(set)  # (file, section) -> set[enum]

    for file_name, _product_key, section_key, enum_value in _iter_enum_leaves(enums_mod.MILK_ENUM_MAPPING):
        all_enums.add(enum_value)

    supported = _supported_universal_keys(universal_mod)

    missing_in_universal = all_enums - supported
    extra_in_universal = supported - all_enums

    # Group missing by (file, section) for readability
    for file_name, _product_key, section_key, enum_value in _iter_enum_leaves(enums_mod.MILK_ENUM_MAPPING):
        if enum_value in missing_in_universal:
            missing_by_group[(file_name, section_key)].add(enum_value)

    print("=== Milk Enum ⇄ Universal Support Sync Report ===")
    print(f"Total enum values (enums.py): {len(all_enums)}")
    print(f"Total supported keys (universal.py): {len(supported)}")
    print(f"Missing in universal: {len(missing_in_universal)}")
    print(f"Extra in universal: {len(extra_in_universal)}")

    if missing_by_group:
        print("\n-- Missing by (file :: section) --")
        for (file_name, section_key), values in sorted(missing_by_group.items()):
            items = ", ".join(sorted(values))
            print(f"- {file_name} :: {section_key}: {items}")

    if extra_in_universal:
        print("\n-- Extra keys in universal.py (not present in enums.py) --")
        print(", ".join(sorted(extra_in_universal)))

    print("\nHint: add missing keys to MILK_SPECIFIC_MAPPING or relevant *CHECKERS in universal.py,\n      or trim extra keys if they are obsolete.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
