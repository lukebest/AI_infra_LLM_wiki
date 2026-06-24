---
name: okf-knowledge-base
description: >-
  Generate and maintain Open Knowledge Format (OKF) bundles from raw source
  documents. Converts LLM wikis, ingests articles/PDFs/specs into structured
  markdown concepts. Use when the user mentions OKF, knowledge bundles, Open
  Knowledge Format, or wants to convert/build a knowledge base from source files.
---

# OKF Knowledge Base

Generate **Open Knowledge Format (OKF) v0.1** bundles — directories of markdown files with YAML frontmatter. OKF is the interchange format from [Google Knowledge Catalog](https://github.com/google/knowledge-catalog); this skill covers authoring bundles from raw sources without requiring BigQuery or cloud tooling.

## Quick Reference

| Term | Meaning |
|------|---------|
| **Knowledge Bundle** | Directory tree of `.md` files — the unit of distribution |
| **Concept** | One `.md` file = one knowledge unit (table, entity, playbook, reference…) |
| **Concept ID** | File path without `.md` (e.g. `entities/cerebras-wse`) |
| **Reserved files** | `index.md` (directory listing), `log.md` (update history) — never use for concepts |

Full spec summary: [references/okf-spec-summary.md](references/okf-spec-summary.md)

## When to Use

- User asks to create an OKF bundle or convert sources to OKF
- User wants to export an LLM wiki (`~/wiki`) to OKF format
- User provides raw documents (articles, PDFs, specs) to compile into a knowledge base
- User mentions OKF, Knowledge Catalog, or metadata-as-code for agents

## Bundle Layout

Organize by domain, not by rigid taxonomy:

```
my-bundle/
├── index.md                    # Auto-generated directory listing
├── log.md                      # Optional update history
├── entities/                   # Named things (products, orgs, models)
│   ├── index.md
│   └── cerebras-wse.md
├── concepts/                   # Topics, mechanisms, architectures
├── references/                 # External source mirrors, glossaries, metrics
│   ├── index.md
│   └── metrics/
└── playbooks/                  # Procedures, runbooks (if applicable)
```

Type values are **freeform strings** — pick descriptive names: `Entity`, `Concept`, `Reference`, `BigQuery Table`, `Playbook`.

## Concept Document Template

```markdown
---
type: Entity
title: Cerebras WSE
description: Wafer-scale AI accelerator with deterministic 24-color routing.
tags: [cerebras, wse, accelerator, deterministic]
timestamp: 2026-05-29T00:00:00Z
---

Body prose and structured sections follow.

# Related

Links to [deterministic execution](/concepts/deterministic-execution.md).

# Citations

[1] [Near-optimal wafer-scale reduce](raw/papers/Near-optimal_wafer-scale_reduce.pdf)
```

**Required (OKF spec):** `type` only.

**Recommended (for agent consumption):** `title`, `description`, `tags`, `timestamp` (ISO 8601).

**Extensions:** Preserve any extra keys (`sources`, `confidence`, `created`) — OKF allows arbitrary frontmatter.

### Conventional Body Sections

| Heading | Use for |
|---------|---------|
| `# Schema` | Structured field/column descriptions |
| `# Examples` | Usage examples (fenced code blocks) |
| `# Citations` | Numbered external sources |

### Cross-linking

Prefer bundle-relative absolute links:

```markdown
See [Cerebras WSE](/entities/cerebras-wse.md) for the deterministic routing model.
```

Relative links also work: `[neighbor](../concepts/other.md)`.

## Workflows

### 1. Generate OKF from Raw Source Files

Use when the user provides URLs, PDFs, pasted text, or a directory of documents.

**Step 1 — Orient**

1. Ask or infer the bundle domain (e.g. "AI infrastructure", "sales analytics")
2. Choose output path (default: `./okf-bundle/` or user-specified)
3. Read [references/okf-spec-summary.md](references/okf-spec-summary.md) if unfamiliar with OKF

**Step 2 — Capture sources**

Save immutable originals under `references/raw/` (or a sibling `raw/` directory):

```yaml
---
source_url: https://example.com/article
ingested: 2026-06-24
---
```

Name files: lowercase, hyphens, descriptive (`references/raw/nvidia-groq3-lpx-blog-2026-04.md`).

**Step 3 — Synthesize concepts**

For each source, create or update concept pages when:

- An entity/concept appears in **2+ sources**, OR
- It is **central** to a single source

Per concept:

1. Write frontmatter (`type`, `title`, `description`, `tags`, `timestamp`)
2. Structure body with headings, lists, tables — not freeform prose only
3. Cross-link to at least 2 other concepts via markdown links
4. Add `# Citations` pointing to raw sources

**Step 4 — Generate indexes**

```bash
python scripts/generate_indexes.py /path/to/bundle
```

Or manually write `index.md` per directory (group by `type`, bullet list with descriptions).

**Step 5 — Validate**

```bash
python scripts/validate_bundle.py /path/to/bundle
```

Fix any reported missing `type` or unparseable frontmatter.

**Step 6 — Log changes**

Append to `log.md` at bundle root:

```markdown
## 2026-06-24
* **Creation**: Added [Cerebras WSE](/entities/cerebras-wse.md) from wafer-scale reduce paper.
* **Update**: Enriched [deterministic execution](/concepts/deterministic-execution.md) with color routing details.
```

### 2. Convert LLM Wiki → OKF

Use when the user has a Karpathy-style LLM wiki (e.g. `/home/luke/wiki`) and wants an OKF bundle.

**Feasibility:** Direct conversion is mechanical. Main transforms:

| Wiki | OKF |
|------|-----|
| `[[wikilinks]]` | Markdown links `[title](/dir/slug.md)` |
| `type: entity` | `type: Entity` |
| `updated: YYYY-MM-DD` | `timestamp: YYYY-MM-DDT00:00:00Z` |
| `index.md` one-liners | `description` in frontmatter |
| `sources:` frontmatter | Keep as extension key or move to `# Citations` |
| `raw/` immutable layer | Copy to `references/raw/` as `type: Raw Source` concepts |
| `SCHEMA.md` | Optional bundle-root concept or README — not required by OKF |

**Run conversion:**

```bash
python scripts/wiki_to_okf.py \
  --wiki /home/luke/wiki \
  --out /path/to/okf-bundle \
  --include-raw
```

Then validate and review link resolution (wikilinks without matching pages become broken links — OKF tolerates this).

**Manual review checklist:**

- [ ] Wikilinks resolved to correct paths
- [ ] `description` populated (from index or first paragraph)
- [ ] `timestamp` set from `updated` field
- [ ] Tags preserved
- [ ] Extension keys (`confidence`, `contradictions`, `created`) retained if useful
- [ ] `index.md` regenerated in OKF format

### 3. Enrich Existing OKF Bundle

When adding new sources to an existing bundle:

1. Read bundle `index.md` and scan concept directories — avoid duplicates
2. Read recent `log.md` entries for context
3. Ingest source → update or create concepts
4. Regenerate indexes, validate, append log entry

## Type Mapping (Wiki → OKF)

| Wiki `type` | OKF `type` |
|-------------|------------|
| `entity` | `Entity` |
| `concept` | `Concept` |
| `comparison` | `Comparison` |
| `query` | `Query` |
| `summary` | `Summary` |
| `paper` | `Paper` |
| (analyses dir) | `Analysis` |
| raw source | `Raw Source` |

## Index File Format

No frontmatter. Group by concept type:

```markdown
# Entity

* [Cerebras WSE](entities/cerebras-wse.md) - Wafer-scale AI accelerator with 900K cores.
* [Groq 3 LPX](entities/nvidia-groq-3-lpx.md) - Rack-scale low-latency inference accelerator.

# Concept

* [Deterministic execution](concepts/deterministic-execution.md) - Compiler-controlled timing paradigm.
```

## Pitfalls

- **Don't use `index.md` or `log.md` as concept filenames** — reserved by OKF
- **Always set `type`** — the only strictly required frontmatter field
- **Prefer structured markdown** over walls of prose — aids agent retrieval
- **Preserve unknown frontmatter keys** on round-trip — don't strip wiki-specific metadata
- **Broken links are OK** per spec — they may represent not-yet-written knowledge
- **Don't require BigQuery** — OKF is format-only; the reference agent in knowledge-catalog is one producer, not the only path

## Related Resources

- OKF spec (authoritative): `/home/luke/workspace/knowledge-catalog/okf/SPEC.md`
- Example bundles: `/home/luke/workspace/knowledge-catalog/okf/bundles/`
- Reference agent (BigQuery + web): `/home/luke/workspace/knowledge-catalog/okf/`
- LLM wiki skill: `/home/luke/.openclaw/plugin-skills/llm-wiki/SKILL.md`

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `scripts/validate_bundle.py` | Check OKF conformance (frontmatter, required `type`) |
| `scripts/wiki_to_okf.py` | Convert LLM wiki directory to OKF bundle |
| `scripts/generate_viz.py` | Generate self-contained interactive `viz.html` graph viewer |

Run from this skill directory or with full paths.
