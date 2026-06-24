#!/usr/bin/env python3
"""Convert Karpathy-style LLM wiki to OKF v0.1 bundle."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import yaml

FRONTMATTER_DELIM = "---"
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
WORK_DIRS = ("entities", "concepts", "papers", "summaries", "analyses", "comparisons", "queries")

TYPE_MAP = {
    "entity": "Entity",
    "concept": "Concept",
    "comparison": "Comparison",
    "query": "Query",
    "summary": "Summary",
    "paper": "Paper",
}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return {}, text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            end_idx = i
            break
    if end_idx is None:
        return {}, text
    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1 :])
    if body.startswith("\n"):
        body = body[1:]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}
    return (fm if isinstance(fm, dict) else {}), body


def serialize_frontmatter(fm: dict, body: str) -> str:
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).rstrip()
    body = body if body.endswith("\n") else body + "\n"
    return f"{FRONTMATTER_DELIM}\n{fm_text}\n{FRONTMATTER_DELIM}\n\n{body}"


def build_slug_map(wiki_root: Path) -> dict[str, str]:
    """Map page slug (stem) to bundle-relative path like entities/foo.md."""
    slug_map: dict[str, str] = {}
    for subdir in WORK_DIRS:
        dir_path = wiki_root / subdir
        if not dir_path.is_dir():
            continue
        for md in dir_path.glob("*.md"):
            slug = md.stem
            rel = f"{subdir}/{md.name}"
            if slug in slug_map:
                print(
                    f"Warning: duplicate slug '{slug}': {slug_map[slug]} vs {rel}",
                    file=sys.stderr,
                )
            slug_map[slug] = rel
    return slug_map


def load_index_descriptions(wiki_root: Path) -> dict[str, str]:
    """Parse index.md one-liners: [[slug]] — description."""
    index_path = wiki_root / "index.md"
    if not index_path.exists():
        return {}
    desc: dict[str, str] = {}
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^-\s*\[\[([^\]|]+)\]\]\s*[—–-]\s*(.+)$", line.strip())
        if m:
            desc[m.group(1)] = m.group(2).strip()
    return desc


def convert_wikilinks(body: str, slug_map: dict[str, str]) -> str:
    def repl(m: re.Match[str]) -> str:
        slug = m.group(1).strip()
        display = m.group(2) or slug.replace("-", " ").title()
        if slug in slug_map:
            return f"[{display}](/{slug_map[slug]})"
        return f"[{display}](#{slug})"  # broken link placeholder

    return WIKILINK_RE.sub(repl, body)


def wiki_type_to_okf(wiki_type: str, subdir: str) -> str:
    if subdir == "analyses":
        return "Analysis"
    return TYPE_MAP.get(wiki_type.lower(), wiki_type.capitalize() if wiki_type else "Concept")


def to_iso_timestamp(date_str: str) -> str:
    if not date_str:
        return datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")
    if "T" in date_str:
        return date_str
    return f"{date_str}T00:00:00Z"


def first_paragraph_description(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line[:200]
    return ""


def convert_page(
    src: Path,
    subdir: str,
    out_root: Path,
    slug_map: dict[str, str],
    index_desc: dict[str, str],
) -> Path | None:
    text = src.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    slug = src.stem

    okf_fm: dict = {
        "type": wiki_type_to_okf(str(fm.get("type", "")), subdir),
        "title": fm.get("title") or slug.replace("-", " ").title(),
        "description": index_desc.get(slug) or first_paragraph_description(body),
        "tags": fm.get("tags") or [],
        "timestamp": to_iso_timestamp(str(fm.get("updated") or fm.get("created") or "")),
    }

    # Preserve wiki-specific keys as extensions
    for key in ("created", "sources", "confidence", "contested", "contradictions"):
        if key in fm:
            okf_fm[key] = fm[key]

    body = convert_wikilinks(body, slug_map)

    # Append Citations from sources if not already present
    sources = fm.get("sources")
    if sources and "# Citations" not in body:
        body = body.rstrip() + "\n\n# Citations\n\n"
        for i, src_ref in enumerate(sources, 1):
            body += f"[{i}] [{src_ref}]({src_ref})\n"

    out_path = out_root / subdir / src.name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(serialize_frontmatter(okf_fm, body), encoding="utf-8")
    return out_path


def generate_indexes(bundle_root: Path) -> None:
    for directory in sorted(bundle_root.rglob("*")):
        if not directory.is_dir():
            continue
        entries: list[tuple[str, str, str, str]] = []
        for child in sorted(directory.iterdir()):
            if child.name == "index.md" or not child.is_file() or child.suffix != ".md":
                continue
            fm, _ = parse_frontmatter(child.read_text(encoding="utf-8"))
            title = str(fm.get("title") or child.stem)
            desc = str(fm.get("description") or "")
            typ = str(fm.get("type") or "Other")
            entries.append((typ, title, child.name, desc))

        if not entries:
            continue

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

        (directory / "index.md").write_text(
            "\n\n".join(sections) + "\n", encoding="utf-8"
        )


def copy_raw_sources(wiki_root: Path, out_root: Path) -> None:
    raw_src = wiki_root / "raw"
    if not raw_src.is_dir():
        return
    raw_dst = out_root / "references" / "raw"
    shutil.copytree(raw_src, raw_dst, dirs_exist_ok=True)

    # Add OKF frontmatter to raw files that lack it
    for md in raw_dst.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm.get("type"):
            continue
        okf_fm = {
            "type": "Raw Source",
            "title": md.stem.replace("-", " ").replace("_", " "),
            "description": f"Immutable source material from wiki raw/{md.relative_to(raw_dst)}",
            "timestamp": to_iso_timestamp(str(fm.get("ingested") or "")),
        }
        if fm.get("source_url"):
            okf_fm["resource"] = fm["source_url"]
        for key in ("source_url", "ingested", "sha256"):
            if key in fm:
                okf_fm[key] = fm[key]
        md.write_text(serialize_frontmatter(okf_fm, body), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert LLM wiki to OKF bundle")
    parser.add_argument("--wiki", type=Path, required=True, help="Wiki root (e.g. ~/wiki)")
    parser.add_argument("--out", type=Path, required=True, help="Output OKF bundle path")
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Copy raw/ sources to references/raw/",
    )
    args = parser.parse_args()

    wiki_root = args.wiki.expanduser().resolve()
    out_root = args.out.expanduser().resolve()

    if not wiki_root.is_dir():
        print(f"Error: wiki path {wiki_root} not found", file=sys.stderr)
        return 1

    out_root.mkdir(parents=True, exist_ok=True)
    slug_map = build_slug_map(wiki_root)
    index_desc = load_index_descriptions(wiki_root)

    converted = 0
    for subdir in WORK_DIRS:
        dir_path = wiki_root / subdir
        if not dir_path.is_dir():
            continue
        for md in sorted(dir_path.glob("*.md")):
            convert_page(md, subdir, out_root, slug_map, index_desc)
            converted += 1

    generate_indexes(out_root)
    if args.include_raw:
        copy_raw_sources(wiki_root, out_root)

    # Root index
    generate_indexes(out_root)

    print(f"Converted {converted} pages → {out_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
