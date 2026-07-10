#!/usr/bin/env python3
"""Generate a static HTML site from an OKF knowledge bundle for GitHub Pages.

Default output: <bundle>/site/
Designed for deployment at https://lukebest.github.io/ (site root; base_path="").
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import markdown
import yaml

FRONTMATTER_DELIM = "---"
INDEX_NAME = "index.md"
LINK_RE = re.compile(r"\]\(([^)\s]+\.md)(?:#([^)\s]*))?\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]")

# Work-layer dirs to publish (exclude raw/ by default — large PDFs / notes)
PUBLISH_DIRS = ("concepts", "entities", "papers", "analyses", "summaries")
ROOT_PAGES = ("index.md", "log.md", "SCHEMA.md", "README.md")

TYPE_COLORS = {
    "Concept": "#3b82f6",
    "Entity": "#f59e0b",
    "Paper": "#8b5cf6",
    "Summary": "#06b6d4",
    "Analysis": "#ec4899",
    "Comparison": "#10b981",
    "Raw Source": "#64748b",
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
    try:
        fm = yaml.safe_load("\n".join(lines[1:end_idx])) or {}
    except yaml.YAMLError:
        fm = {}
    body = "\n".join(lines[end_idx + 1 :])
    if body.startswith("\n"):
        body = body[1:]
    return (fm if isinstance(fm, dict) else {}), body


@dataclass
class Page:
    rel_md: str  # e.g. concepts/foo.md
    title: str
    description: str
    type: str
    tags: list[str]
    body_md: str
    links_to: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self.rel_md[:-3] if self.rel_md.endswith(".md") else self.rel_md

    @property
    def html_rel(self) -> str:
        if self.rel_md == "index.md":
            return "index.html"
        return self.id + ".html"


def resolve_md_link(target: str, doc_dir: Path, bundle_root: Path) -> str | None:
    if "://" in target or target.startswith("#"):
        return None
    bundle_root = bundle_root.resolve()
    if target.startswith("/"):
        resolved = (bundle_root / target.lstrip("/")).resolve()
    else:
        resolved = (doc_dir / target).resolve()
    try:
        rel = resolved.relative_to(bundle_root)
    except ValueError:
        return None
    return rel.as_posix()


def collect_pages(bundle_root: Path) -> list[Page]:
    pages: list[Page] = []
    paths: list[Path] = []
    for name in ROOT_PAGES:
        p = bundle_root / name
        if p.is_file():
            paths.append(p)
    for d in PUBLISH_DIRS:
        dd = bundle_root / d
        if dd.is_dir():
            paths.extend(sorted(dd.rglob("*.md")))

    for md_path in paths:
        rel = md_path.relative_to(bundle_root).as_posix()
        text = md_path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        title = str(fm.get("title") or md_path.stem.replace("-", " ").title())
        if md_path.name == INDEX_NAME and md_path.parent != bundle_root:
            title = f"{md_path.parent.name.title()} Index"
        elif md_path.name == "index.md":
            title = "AI Infra LLM Wiki"
        elif md_path.name == "README.md":
            title = "About / README"
        elif md_path.name == "SCHEMA.md":
            title = "Schema"
        elif md_path.name == "log.md":
            title = "Update Log"

        page = Page(
            rel_md=rel,
            title=title,
            description=str(fm.get("description") or ""),
            type=str(fm.get("type") or ("Index" if md_path.name == INDEX_NAME else "Page")),
            tags=[str(t) for t in tags],
            body_md=body if fm else text,
        )
        # extract links
        seen: set[str] = set()
        for m in LINK_RE.finditer(page.body_md):
            tgt = resolve_md_link(m.group(1), md_path.parent, bundle_root)
            if tgt and tgt not in seen:
                seen.add(tgt)
                page.links_to.append(tgt)
        pages.append(page)
    return pages


def md_to_html_body(body: str, page: Page, bundle_root: Path, page_index: dict[str, Page], base_path: str) -> str:
    """Rewrite .md links to .html, then render markdown."""
    doc_dir = (bundle_root / page.rel_md).parent

    def repl_md_link(m: re.Match) -> str:
        target = m.group(1)
        anchor = m.group(2)
        full = m.group(0)
        # keep external / non-md
        if "://" in target or not target.endswith(".md"):
            return full
        resolved = resolve_md_link(target, doc_dir, bundle_root)
        if not resolved:
            return full
        # strip leading ./ 
        href = resolved[:-3] + ".html" if resolved.endswith(".md") else resolved
        if resolved == "index.md":
            href = "index.html"
        # relative from current page html location
        from_parts = Path(page.html_rel).parent
        try:
            href = Path(href).as_posix()
            # compute relative path
            cur = Path(page.html_rel)
            target_path = Path(href)
            if cur.parent == Path("."):
                rel_href = target_path.as_posix()
            else:
                rel_href = Path(os_path_rel(cur.parent.as_posix(), target_path.as_posix()))
            if anchor:
                rel_href += f"#{anchor}"
            # rebuild link text from original
            text_m = re.match(r"\[([^\]]*)\]", full)
            link_text = text_m.group(1) if text_m else rel_href
            return f"[{link_text}]({rel_href})"
        except Exception:
            return full

    def repl_wikilink(m: re.Match) -> str:
        name = m.group(1).strip()
        label = (m.group(2) or name).strip()
        # fuzzy: find page whose title or stem matches
        slug = name.lower().replace(" ", "-")
        for p in page_index.values():
            if p.id.endswith(slug) or p.title.lower() == name.lower():
                href = os_path_rel(Path(page.html_rel).parent.as_posix() or ".", p.html_rel)
                return f"[{label}]({href})"
        return label

    text = LINK_RE.sub(repl_md_link, body)
    text = WIKILINK_RE.sub(repl_wikilink, text)

    md = markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "nl2br", "sane_lists"],
        extension_configs={"toc": {"permalink": False}},
    )
    return md.convert(text)


def os_path_rel(from_dir: str, to_path: str) -> str:
    """Relative path from directory from_dir to file to_path (posix)."""
    if from_dir in ("", "."):
        return to_path
    from_parts = Path(from_dir).parts
    to = Path(to_path)
    to_parts = to.parts
    # find common prefix
    i = 0
    while i < len(from_parts) and i < len(to_parts) - 1 and from_parts[i] == to_parts[i]:
        i += 1
    ups = [".."] * (len(from_parts) - i)
    rest = list(to_parts[i:])
    return "/".join(ups + rest) if (ups or rest) else to.name


CSS = """
:root {
  --bg: #0f1419;
  --bg2: #1a2332;
  --bg3: #243044;
  --text: #e7ecf3;
  --muted: #8b9bb4;
  --accent: #5b9fd4;
  --accent2: #7dd3c0;
  --border: #2d3a4f;
  --code-bg: #0a0e14;
  --radius: 8px;
  --font: "IBM Plex Sans", "Noto Sans SC", system-ui, sans-serif;
  --mono: "IBM Plex Mono", "JetBrains Mono", ui-monospace, monospace;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; font-family: var(--font); background: var(--bg); color: var(--text);
  line-height: 1.65; font-size: 16px;
  background-image:
    radial-gradient(ellipse 80% 50% at 10% -10%, rgba(91,159,212,.12), transparent),
    radial-gradient(ellipse 60% 40% at 90% 0%, rgba(125,211,192,.08), transparent);
  min-height: 100vh;
}
a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent2); text-decoration: underline; }
.layout { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }
.sidebar {
  background: var(--bg2); border-right: 1px solid var(--border);
  padding: 1.25rem 1rem; position: sticky; top: 0; height: 100vh; overflow-y: auto;
}
.brand { font-weight: 700; font-size: 1.05rem; letter-spacing: -.02em; margin-bottom: .25rem; }
.brand a { color: var(--text); text-decoration: none; }
.brand-sub { color: var(--muted); font-size: .75rem; margin-bottom: 1.25rem; }
.nav-section { margin-bottom: 1rem; }
.nav-section h3 {
  font-size: .7rem; text-transform: uppercase; letter-spacing: .08em;
  color: var(--muted); margin: 0 0 .4rem; font-weight: 600;
}
.nav-section a {
  display: block; padding: .28rem .5rem; border-radius: 4px;
  color: var(--text); font-size: .85rem; text-decoration: none;
}
.nav-section a:hover, .nav-section a.active { background: var(--bg3); color: var(--accent2); }
.main { padding: 2rem 2.5rem 4rem; max-width: 880px; }
.meta {
  display: flex; flex-wrap: wrap; gap: .5rem; align-items: center;
  margin-bottom: 1.25rem; font-size: .8rem; color: var(--muted);
}
.badge {
  display: inline-block; padding: .15rem .55rem; border-radius: 999px;
  font-size: .72rem; font-weight: 600; background: var(--bg3); color: var(--text);
}
.badge.type { border: 1px solid var(--border); }
.tag { background: transparent; border: 1px solid var(--border); color: var(--muted); }
h1 { font-size: 1.85rem; margin: 0 0 .75rem; letter-spacing: -.03em; line-height: 1.25; }
h2 { font-size: 1.35rem; margin-top: 2rem; border-bottom: 1px solid var(--border); padding-bottom: .35rem; }
h3 { font-size: 1.1rem; margin-top: 1.5rem; }
.desc { color: var(--muted); font-size: 1rem; margin: 0 0 1.5rem; }
.content table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .9rem; }
.content th, .content td { border: 1px solid var(--border); padding: .45rem .65rem; text-align: left; }
.content th { background: var(--bg2); }
.content tr:nth-child(even) td { background: rgba(26,35,50,.5); }
.content code {
  font-family: var(--mono); font-size: .85em; background: var(--code-bg);
  padding: .1em .35em; border-radius: 3px;
}
.content pre {
  background: var(--code-bg); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1rem; overflow-x: auto; font-size: .82rem;
}
.content pre code { background: none; padding: 0; }
.content blockquote {
  border-left: 3px solid var(--accent); margin: 1rem 0; padding: .25rem 1rem;
  color: var(--muted); background: var(--bg2);
}
.content ul, .content ol { padding-left: 1.4rem; }
.content img { max-width: 100%; }
.search-box {
  width: 100%; padding: .5rem .65rem; margin-bottom: 1rem;
  background: var(--bg); border: 1px solid var(--border); border-radius: 6px;
  color: var(--text); font-family: inherit; font-size: .85rem;
}
.search-box:focus { outline: 1px solid var(--accent); }
.home-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem; margin-top: 1.5rem;
}
.card {
  background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1rem 1.1rem; transition: border-color .15s;
}
.card:hover { border-color: var(--accent); }
.card h3 { margin: 0 0 .4rem; font-size: 1rem; }
.card h3 a { color: var(--text); }
.card p { margin: 0; font-size: .82rem; color: var(--muted); }
.footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); font-size: .75rem; color: var(--muted); }
.mobile-toggle { display: none; }
@media (max-width: 800px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar {
    position: fixed; z-index: 20; transform: translateX(-100%);
    transition: transform .2s; width: min(280px, 85vw);
  }
  .sidebar.open { transform: translateX(0); }
  .mobile-toggle {
    display: block; position: fixed; top: .75rem; left: .75rem; z-index: 30;
    background: var(--bg2); border: 1px solid var(--border); color: var(--text);
    padding: .4rem .7rem; border-radius: 6px; font-size: .85rem; cursor: pointer;
  }
  .main { padding: 3.5rem 1.25rem 3rem; }
}
"""

JS = """
(function(){
  const btn = document.getElementById('nav-toggle');
  const side = document.getElementById('sidebar');
  if (btn && side) btn.addEventListener('click', () => side.classList.toggle('open'));
  const q = document.getElementById('site-search');
  const data = window.__SEARCH__ || [];
  const box = document.getElementById('search-results');
  if (!q || !box) return;
  q.addEventListener('input', () => {
    const s = q.value.trim().toLowerCase();
    if (s.length < 2) { box.innerHTML = ''; return; }
    const hits = data.filter(d =>
      d.title.toLowerCase().includes(s) ||
      d.desc.toLowerCase().includes(s) ||
      d.tags.some(t => t.toLowerCase().includes(s)) ||
      d.id.toLowerCase().includes(s)
    ).slice(0, 20);
    box.innerHTML = hits.map(h =>
      `<a href="${h.href}">${h.title}</a>`
    ).join('') || '<span style="color:var(--muted);font-size:.8rem">无结果</span>';
  });
})();
"""


def page_template(
    *,
    title: str,
    description: str,
    body_html: str,
    nav_html: str,
    meta_html: str,
    base_path: str,
    search_json: str,
    rel_home: str,
) -> str:
    bp = base_path.rstrip("/") or ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)} · AI Infra Wiki</title>
<meta name="description" content="{html.escape(description)}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet"/>
<style>{CSS}</style>
</head>
<body>
<button class="mobile-toggle" id="nav-toggle" type="button">菜单</button>
<div class="layout">
<aside class="sidebar" id="sidebar">
  <div class="brand"><a href="{html.escape(rel_home)}">AI Infra Wiki</a></div>
  <div class="brand-sub">OKF knowledge bundle</div>
  <input class="search-box" id="site-search" type="search" placeholder="搜索概念…" autocomplete="off"/>
  <div id="search-results" class="nav-section"></div>
  {nav_html}
</aside>
<main class="main">
  {meta_html}
  <h1>{html.escape(title)}</h1>
  {f'<p class="desc">{html.escape(description)}</p>' if description else ''}
  <div class="content">
  {body_html}
  </div>
  <footer class="footer">
    Generated from <a href="https://github.com/lukebest/AI_infra_LLM_wiki">AI_infra_LLM_wiki</a>
    · <a href="{html.escape(rel_home)}">Home</a>
    · {datetime.now(timezone.utc).strftime("%Y-%m-%d UTC")}
  </footer>
</main>
</div>
<script>window.__SEARCH__ = {search_json};</script>
<script>{JS}</script>
</body>
</html>
"""


def build_nav(pages: list[Page], current: Page) -> str:
    groups: dict[str, list[Page]] = {
        "Home": [],
        "Concepts": [],
        "Entities": [],
        "Papers": [],
        "Analyses": [],
        "Summaries": [],
    }
    for p in pages:
        if p.rel_md in ROOT_PAGES:
            if p.rel_md == "index.md":
                continue
            groups["Home"].append(p)
        elif p.rel_md.endswith("/index.md"):
            continue
        elif p.rel_md.startswith("concepts/"):
            groups["Concepts"].append(p)
        elif p.rel_md.startswith("entities/"):
            groups["Entities"].append(p)
        elif p.rel_md.startswith("papers/"):
            groups["Papers"].append(p)
        elif p.rel_md.startswith("analyses/"):
            groups["Analyses"].append(p)
        elif p.rel_md.startswith("summaries/"):
            groups["Summaries"].append(p)

    parts: list[str] = []
    # section index links
    section_indexes = [
        ("Concepts", "concepts/index.html"),
        ("Entities", "entities/index.html"),
        ("Papers", "papers/index.html"),
        ("Analyses", "analyses/index.html"),
        ("Summaries", "summaries/index.html"),
    ]
    parts.append('<div class="nav-section"><h3>Browse</h3>')
    home_href = os_path_rel(Path(current.html_rel).parent.as_posix() or ".", "index.html")
    parts.append(f'<a href="{html.escape(home_href)}">Home</a>')
    for label, href in section_indexes:
        rh = os_path_rel(Path(current.html_rel).parent.as_posix() or ".", href)
        parts.append(f'<a href="{html.escape(rh)}">{html.escape(label)}</a>')
    parts.append("</div>")

    for label, items in groups.items():
        if not items:
            continue
        items = sorted(items, key=lambda x: x.title.lower())
        # show compact list for large groups — only first-letter? show all but short titles
        parts.append(f'<div class="nav-section"><h3>{html.escape(label)} ({len(items)})</h3>')
        for p in items:
            href = os_path_rel(Path(current.html_rel).parent.as_posix() or ".", p.html_rel)
            cls = " active" if p.rel_md == current.rel_md else ""
            short = p.title if len(p.title) <= 36 else p.title[:34] + "…"
            parts.append(f'<a class="{cls}" href="{html.escape(href)}" title="{html.escape(p.title)}">{html.escape(short)}</a>')
        parts.append("</div>")
    return "\n".join(parts)


def home_body(pages: list[Page]) -> str:
    counts = {
        "concepts": sum(1 for p in pages if p.rel_md.startswith("concepts/") and not p.rel_md.endswith("index.md")),
        "entities": sum(1 for p in pages if p.rel_md.startswith("entities/") and not p.rel_md.endswith("index.md")),
        "papers": sum(1 for p in pages if p.rel_md.startswith("papers/") and not p.rel_md.endswith("index.md")),
        "analyses": sum(1 for p in pages if p.rel_md.startswith("analyses/") and not p.rel_md.endswith("index.md")),
        "summaries": sum(1 for p in pages if p.rel_md.startswith("summaries/") and not p.rel_md.endswith("index.md")),
    }
    cards = [
        ("Concepts", "concepts/index.html", counts["concepts"], "机制、架构与方法论"),
        ("Entities", "entities/index.html", counts["entities"], "产品、芯片与组织"),
        ("Papers", "papers/index.html", counts["papers"], "论文摘要与引用"),
        ("Analyses", "analyses/index.html", counts["analyses"], "深度分析与对比"),
        ("Summaries", "summaries/index.html", counts["summaries"], "综述与阶段总结"),
        ("Update Log", "log.html", "—", "摄取与变更历史"),
    ]
    grid = '<div class="home-grid">'
    for title, href, n, desc in cards:
        nlabel = f"{n} pages" if isinstance(n, int) else n
        grid += f'''<div class="card"><h3><a href="{href}">{html.escape(title)}</a></h3>
        <p>{html.escape(desc)} · {html.escape(str(nlabel))}</p></div>'''
    grid += "</div>"
    intro = """
<p>本站由 <strong>AI_infra_LLM_wiki</strong> OKF 知识库自动生成，覆盖 AI 基础设施：
互连网络 / NoC、晶圆级加速器（WSE）、LLM 推理系统、DSA 与编译器。</p>
<p>源仓库：<a href="https://github.com/lukebest/AI_infra_LLM_wiki">github.com/lukebest/AI_infra_LLM_wiki</a></p>
"""
    return intro + grid


def generate_site(bundle_root: Path, out_dir: Path, base_path: str = "/wiki") -> dict:
    bundle_root = bundle_root.resolve()
    out_dir = out_dir.resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    pages = collect_pages(bundle_root)
    by_md = {p.rel_md: p for p in pages}
    by_id = {p.id: p for p in pages}

    # search index (href relative to site root, with base_path for absolute)
    search = []
    for p in pages:
        if p.rel_md.endswith("index.md") and p.rel_md != "index.md":
            continue
        href = (base_path.rstrip("/") + "/" + p.html_rel).replace("//", "/")
        search.append({
            "id": p.id,
            "title": p.title,
            "desc": p.description,
            "tags": p.tags,
            "href": href if not href.startswith("/") else href,  # absolute from site root
        })
    # For client-side search from nested pages, use path relative to root via base
    # Better: store root-relative paths and prefix with base in JS — use absolute from domain root
    search_json = json.dumps(search, ensure_ascii=False)

    written = 0
    for p in pages:
        if p.rel_md == "index.md":
            body_html = home_body(pages)
            # also append rendered index.md content lightly
            extra = md_to_html_body(p.body_md, p, bundle_root, by_id, base_path)
            body_html += "<h2>Directory</h2>" + extra
        else:
            body_html = md_to_html_body(p.body_md, p, bundle_root, by_id, base_path)

        color = TYPE_COLORS.get(p.type, "#94a3b8")
        badges = [f'<span class="badge type" style="border-color:{color}">{html.escape(p.type)}</span>']
        for t in p.tags[:8]:
            badges.append(f'<span class="badge tag">{html.escape(t)}</span>')
        meta_html = f'<div class="meta">{"".join(badges)}</div>' if p.type not in ("Index", "Page") or p.tags else ""

        nav = build_nav(pages, p)
        rel_home = os_path_rel(Path(p.html_rel).parent.as_posix() or ".", "index.html")

        # Fix search hrefs to be relative from this page
        local_search = []
        for s in search:
            # s href is /wiki/concepts/foo.html — convert to relative
            abs_path = s["href"]
            if abs_path.startswith(base_path):
                root_rel = abs_path[len(base_path.rstrip("/")) :].lstrip("/")
            else:
                root_rel = abs_path.lstrip("/")
            local_search.append({**s, "href": os_path_rel(Path(p.html_rel).parent.as_posix() or ".", root_rel)})
        local_json = json.dumps(local_search, ensure_ascii=False)

        html_out = page_template(
            title=p.title,
            description=p.description or p.title,
            body_html=body_html,
            nav_html=nav,
            meta_html=meta_html,
            base_path=base_path,
            search_json=local_json,
            rel_home=rel_home,
        )
        out_path = out_dir / p.html_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_out, encoding="utf-8")
        written += 1

    # .nojekyll for GitHub Pages
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    # redirect note
    (out_dir / "README.md").write_text(
        f"# AI Infra Wiki (static)\n\nDeployed at `{base_path}/` on lukebest.github.io.\n"
        f"Generated {datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )

    return {"pages": written, "out": str(out_dir)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate static HTML site from OKF bundle")
    ap.add_argument("bundle", type=Path, nargs="?", default=Path("."), help="OKF bundle root")
    ap.add_argument("--out", type=Path, default=None, help="Output directory (default: <bundle>/site)")
    ap.add_argument("--base-path", default="", help="URL base path for GitHub Pages (default: site root)")
    args = ap.parse_args()
    out = args.out or (args.bundle / "site")
    stats = generate_site(args.bundle, out, base_path=args.base_path)
    print(f"Wrote {stats['pages']} page(s) → {stats['out']} (base_path={args.base_path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
