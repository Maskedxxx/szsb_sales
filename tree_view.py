#!/usr/bin/env python3
"""
tree_view.py  — универсальный скрипт для печати структуры проекта.

Запуск:
    python tree_view.py [PATH] [-e PATTERN ...] [-d MAX_DEPTH]

Аргументы:
    PATH               Корневая директория (по умолчанию текущая).
    -e / --exclude     Маска (glob) для исключения файлов/папок.
                       Можно указывать несколько раз.
                       Пример: -e "__pycache__" -e "*.pyc"
    -d / --max-depth   Максимальная глубина рекурсии (0 = только корень).
                       По умолчанию без ограничений.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
from pathlib import Path
from typing import Iterable, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print directory tree")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Корень проекта (default: текущая директория)",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Glob-маска для исключения (можно несколько)",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        default=-1,
        metavar="N",
        help="Максимальная глубина рекурсии (-1 = без ограничений)",
    )
    return parser.parse_args()


def should_exclude(name: str, patterns: Iterable[str]) -> bool:
    """Проверяет, подходит ли имя под одну из масок исключения."""
    return any(fnmatch.fnmatch(name, p) for p in patterns)


def build_tree(
    root: Path,
    prefix: str,
    exclude: List[str],
    level: int,
    max_depth: int,
) -> None:
    """Рекурсивно печатает дерево, соблюдая ограничения."""
    if max_depth >= 0 and level > max_depth:
        return

    # Отфильтровываем и сортируем: папки сначала, затем файлы (алфавитно)
    children = [
        child
        for child in sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        if not should_exclude(child.name, exclude)
    ]

    for index, child in enumerate(children):
        connector = "└── " if index == len(children) - 1 else "├── "
        print(f"{prefix}{connector}{child.name}")

        if child.is_dir():
            extension = "    " if index == len(children) - 1 else "│   "
            build_tree(child, prefix + extension, exclude, level + 1, max_depth)


def main() -> None:
    args = parse_args()
    root_path = Path(args.path).resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"Путь '{root_path}' не существует")

    print(root_path.name)
    build_tree(
        root=root_path,
        prefix="",
        exclude=args.exclude,
        level=0,
        max_depth=args.max_depth,
    )


if __name__ == "__main__":
    main()
