#!/usr/bin/env python3
"""Validate OKF v0.1 bundle conformance."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

RESERVED = {"index.md", "log.md"}
FRONTMATTER_DELIM = "---"


def parse_frontmatter(text: str) -> dict | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            end_idx = i
            break
    if end_idx is None:
        return None
    fm_text = "\n".join(lines[1:end_idx])
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def validate_bundle(bundle_root: Path, *, strict: bool = False) -> list[str]:
    errors: list[str] = []
    required_strict = ("type", "title", "description", "timestamp")

    for md in sorted(bundle_root.rglob("*.md")):
        if md.name in RESERVED:
            continue
        rel = md.relative_to(bundle_root)
        try:
            text = md.read_text(encoding="utf-8")
        except OSError as e:
            errors.append(f"{rel}: cannot read — {e}")
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: missing or unparseable YAML frontmatter")
            continue

        if not fm.get("type"):
            errors.append(f"{rel}: missing required frontmatter key 'type'")

        if strict:
            missing = [k for k in required_strict if not fm.get(k)]
            if missing:
                errors.append(
                    f"{rel}: missing strict keys: {', '.join(missing)}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OKF bundle")
    parser.add_argument("bundle", type=Path, help="Path to OKF bundle root")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also require title, description, timestamp (reference agent mode)",
    )
    args = parser.parse_args()

    if not args.bundle.is_dir():
        print(f"Error: {args.bundle} is not a directory", file=sys.stderr)
        return 1

    errors = validate_bundle(args.bundle, strict=args.strict)
    if errors:
        print(f"FAIL: {len(errors)} issue(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1

    n = len(list(args.bundle.rglob("*.md")))
    print(f"OK: bundle conforms to OKF v0.1 ({n} markdown files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
