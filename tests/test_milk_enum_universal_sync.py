"""
Sync test: verifies every enum value declared in
app/core/tool_calling/milk/mappings/enums.py has an explicit
support entry in app/core/tool_calling/milk/mappings/universal.py
either as a pattern mapping or a specialized checker.

If gaps are found, the test fails and reports them grouped by
file and section key to make it easy to align mappings.
"""

from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

from app.core.tool_calling.milk.mappings.enums import MILK_ENUM_MAPPING
from app.core.tool_calling.milk.mappings import universal as milk_universal


def _iter_enum_leaves() -> Iterable[Tuple[str, str, str, str]]:
    """
    Yields tuples of (file_name, product_key, section_key, enum_value)
    for each enum value listed under MILK_ENUM_MAPPING.
    """
    for file_name, file_data in MILK_ENUM_MAPPING.items():
        for product_key, product_sections in (file_data or {}).items():
            for section_key, categories in (product_sections or {}).items():
                for _category, values in (categories or {}).items():
                    for enum_value in values or []:
                        yield file_name, product_key, section_key, enum_value


def _supported_universal_keys() -> Set[str]:
    """
    Builds a set of enum identifiers that universal.py explicitly supports,
    via either pattern mappings or specialized checkers.
    """
    supported: Set[str] = set()
    # Explicit pattern mappings
    supported.update((milk_universal.MILK_SPECIFIC_MAPPING or {}).keys())
    # Specialized checkers (characteristics, dosage, packaging, etc.)
    supported.update((milk_universal.MILK_SPECIFIC_CHECKERS or {}).keys())
    supported.update((milk_universal.UNIVERSAL_KBGU_CHECKERS or {}).keys())
    supported.update((milk_universal.PACKAGING_CHECKERS or {}).keys())
    supported.update((milk_universal.SHELF_LIFE_CHECKERS or {}).keys())
    return supported


def test_milk_enums_are_supported_by_universal():
    """
    For each enum value defined in enums.py, assert that universal.py
    has an explicit mapping or a checker key for it. If not, report
    them grouped by (file, section) to guide synchronization work.
    """
    supported = _supported_universal_keys()

    # Collect missing by (file, section)
    missing_by_group: Dict[Tuple[str, str], Set[str]] = defaultdict(set)

    for file_name, _product_key, section_key, enum_value in _iter_enum_leaves():
        if enum_value not in supported:
            missing_by_group[(file_name, section_key)].add(enum_value)

    if missing_by_group:
        # Build readable diff message
        lines: List[str] = []
        lines.append("Found enums in enums.py without explicit support in universal.py:")
        for (file_name, section_key), values in sorted(missing_by_group.items()):
            sample = ", ".join(sorted(values))
            lines.append(f"- {file_name} :: {section_key}: {sample}")
        lines.append(
            "\nHint: add keys either to MILK_SPECIFIC_MAPPING or appropriate *CHECKERS in universal.py."
        )
        raise AssertionError("\n".join(lines))

