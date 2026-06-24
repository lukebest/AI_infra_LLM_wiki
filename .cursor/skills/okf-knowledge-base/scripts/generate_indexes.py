#!/usr/bin/env python3
"""Regenerate OKF index.md files from concept frontmatter."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml

FRONTMATTER_DELIM = "---"
INDEX_FILE = "index.md"


def parse_frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return {}
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            end_idx = i
            break
    if end_idx is None:
        return {}
    fm_text = "\n".join(lines[1:end_idx])
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return {}
    return fm if isinstance(fm, dict) else {}


def build_index_text(entries: list[tuple[str, str, str, str]]) -> str:
    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for typ, title, link, desc in entries:
        grouped[typ or "Other"].append((title, link, desc))

    sections: list[str] = []
    for typ in sorted(grouped):
        lines = [f"# {typ}", ""]
        for title, link, desc in sorted(grouped[typ], key=lambda e: e[0].lower()):
            suffix = f" - {desc}" if desc else ""
            lines.append(f"* [{title}]({link}){suffix}")
        sections.append("\n".join(lines))
    return "\n\n".join(sections) + "\n"


def regenerate_indexes(bundle_root: Path) -> list[Path]:
    written: list[Path] = []
    dirs = sorted({p.parent for p in bundle_root.rglob("*.md")} | {bundle_root})

    for directory in dirs:
        entries: list[tuple[str, str, str, str]] = []
        for child in sorted(directory.iterdir()):
            if child.name == INDEX_FILE:
                continue
            if child.is_file() and child.suffix == ".md":
                fm = parse_frontmatter(child.read_text(encoding="utf-8"))
                title = str(fm.get("title") or child.stem)
                desc = str(fm.get("description") or "")
                typ = str(fm.get("type") or "")
                entries.append((typ, title, child.name, desc))
            elif child.is_dir() and (child / INDEX_FILE).exists():
                entries.append(
                    ("Subdirectories", child.name, f"{child.name}/{INDEX_FILE}", "")
                )

        if not entries:
            continue

        index_path = directory / INDEX_FILE
        index_path.write_text(build_index_text(entries), encoding="utf-8")
        written.append(index_path)

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate OKF index.md files")
    parser.add_argument("bundle", type=Path, help="OKF bundle root")
    args = parser.parse_args()

    if not args.bundle.is_dir():
        print(f"Error: {args.bundle} is not a directory", file=sys.stderr)
        return 1

    written = regenerate_indexes(args.bundle.resolve())
    print(f"Regenerated {len(written)} index file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
