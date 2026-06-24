#!/usr/bin/env python3
"""Generate self-contained OKF bundle HTML visualization."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_DELIM = "---"
INDEX_NAME = "index.md"
LINK_RE = re.compile(r"\]\(([^)\s]+\.md)(?:#[A-Za-z0-9_\-]*)?\)")

TYPE_PALETTE = {
    "BigQuery Dataset": "#8b5cf6",
    "BigQuery Table": "#3b82f6",
    "Reference": "#10b981",
    "Entity": "#f59e0b",
    "Concept": "#3b82f6",
    "Paper": "#8b5cf6",
    "Summary": "#06b6d4",
    "Analysis": "#ec4899",
    "Raw Source": "#64748b",
}
DEFAULT_NODE_COLOR = "#94a3b8"

VIEWER_ROOT = Path(__file__).resolve().parents[3] / "workspace/knowledge-catalog/okf/src/reference_agent/viewer"
# Fallback when skill lives outside home layout
if not VIEWER_ROOT.is_dir():
    VIEWER_ROOT = Path("/home/luke/workspace/knowledge-catalog/okf/src/reference_agent/viewer")


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


@dataclass
class Concept:
    id: str
    type: str
    title: str
    description: str
    resource: str
    tags: list[str]
    body: str
    links_to: list[str] = field(default_factory=list)

    def to_node(self) -> dict:
        color = TYPE_PALETTE.get(self.type, DEFAULT_NODE_COLOR)
        return {
            "data": {
                "id": self.id,
                "label": self.title or self.id,
                "type": self.type,
                "description": self.description,
                "resource": self.resource,
                "tags": self.tags,
                "color": color,
                "size": 30 + min(60, len(self.body) // 200),
            }
        }


def resolve_link(target: str, doc_dir: Path, bundle_root: Path) -> str | None:
    if "://" in target:
        return None
    bundle_root = bundle_root.resolve()
    if target.startswith("/"):
        rel_path = target.lstrip("/")
        resolved = (bundle_root / rel_path).resolve()
    else:
        resolved = (doc_dir / target).resolve()
    try:
        rel = resolved.relative_to(bundle_root)
    except ValueError:
        return None
    rel_str = rel.as_posix()
    if rel_str.endswith(".md"):
        rel_str = rel_str[:-3]
    return rel_str or None


def extract_links(body: str, doc_dir: Path, bundle_root: Path) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for m in LINK_RE.finditer(body):
        target_id = resolve_link(m.group(1), doc_dir, bundle_root)
        if target_id and target_id not in seen:
            seen.add(target_id)
            out.append(target_id)
    return out


def walk_concepts(bundle_root: Path) -> list[Concept]:
    concepts: list[Concept] = []
    for md_path in sorted(bundle_root.rglob("*.md")):
        if md_path.name == INDEX_NAME:
            continue
        rel = md_path.relative_to(bundle_root).with_suffix("")
        concept_id = "/".join(rel.parts)
        fm, body = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        if not fm.get("type"):
            continue
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        concepts.append(
            Concept(
                id=concept_id,
                type=str(fm.get("type") or "Unknown"),
                title=str(fm.get("title") or concept_id),
                description=str(fm.get("description") or ""),
                resource=str(fm.get("resource") or ""),
                tags=[str(t) for t in tags],
                body=body,
                links_to=extract_links(body, md_path.parent, bundle_root),
            )
        )
    return concepts


def build_graph(concepts: list[Concept]) -> dict:
    ids = {c.id for c in concepts}
    nodes = [c.to_node() for c in concepts]
    edges: list[dict] = []
    seen_edges: set[tuple[str, str]] = set()
    for c in concepts:
        for target in c.links_to:
            if target == c.id or target not in ids:
                continue
            key = (c.id, target)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append(
                {"data": {"id": f"{c.id}__{target}", "source": c.id, "target": target}}
            )
    return {
        "nodes": nodes,
        "edges": edges,
        "bodies": {c.id: c.body for c in concepts},
        "types": sorted({c.type for c in concepts}),
        "palette": TYPE_PALETTE,
    }


def generate_visualization(bundle_root: Path, out_path: Path, *, bundle_name: str | None = None) -> dict:
    bundle_root = Path(bundle_root)
    out_path = Path(out_path)
    if not bundle_root.is_dir():
        raise FileNotFoundError(f"Bundle not found: {bundle_root}")

    concepts = walk_concepts(bundle_root)
    graph = build_graph(concepts)
    template = (VIEWER_ROOT / "templates" / "viz.html").read_text(encoding="utf-8")
    css = (VIEWER_ROOT / "static" / "viz.css").read_text(encoding="utf-8")
    js = (VIEWER_ROOT / "static" / "viz.js").read_text(encoding="utf-8")
    name = bundle_name or bundle_root.resolve().name

    html = (
        template.replace("/*__VIZ_CSS__*/", css)
        .replace("/*__VIZ_JS__*/", js)
        .replace("__BUNDLE_NAME__", json.dumps(name))
        .replace("__BUNDLE_DATA__", json.dumps(graph))
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return {
        "concepts": len(concepts),
        "edges": len(graph["edges"]),
        "bytes": len(html.encode("utf-8")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate OKF bundle HTML visualization")
    parser.add_argument("bundle", type=Path, help="OKF bundle root")
    parser.add_argument("--out", type=Path, default=None, help="Output path (default: <bundle>/viz.html)")
    parser.add_argument("--name", default=None, help="Display name in viewer header")
    args = parser.parse_args()

    out = args.out or (args.bundle / "viz.html")
    try:
        stats = generate_visualization(args.bundle, out, bundle_name=args.name)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(
        f"Wrote {stats['concepts']} concept(s), "
        f"{stats['edges']} edge(s), "
        f"{stats['bytes']} bytes → {out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
