# OKF v0.1 Spec Summary

Condensed from `/home/luke/workspace/knowledge-catalog/okf/SPEC.md`. Read the full spec for normative details.

## Core Model

- **Bundle** = directory tree of UTF-8 markdown files
- **Concept** = one `.md` file (except reserved names)
- **Concept ID** = relative path without `.md`

## Reserved Filenames

| File | Purpose |
|------|---------|
| `index.md` | Directory listing (progressive disclosure) |
| `log.md` | Update history |

## Frontmatter

```yaml
---
type: <required string>       # Only required field for conformance
title: <display name>         # Recommended
description: <one-line summary>
resource: <canonical URI>     # For assets bound to external systems
tags: [tag1, tag2]
timestamp: <ISO 8601 datetime>
# ... arbitrary extension keys preserved by consumers
---
```

## Body Conventions

| Section | Purpose |
|---------|---------|
| `# Schema` | Field/column definitions |
| `# Examples` | Usage examples |
| `# Citations` | Numbered external sources |

## Links

**Recommended:** bundle-relative absolute paths:

```markdown
[customers table](/tables/customers.md)
```

**Also valid:** relative paths (`./other.md`, `../datasets/foo.md`).

Link semantics are conveyed by surrounding prose, not link syntax.

## Index Files

- No frontmatter
- Sections grouped by heading (typically concept `type`)
- Entries: `* [Title](relative-path) - description`

## Log Files

Optional at any level. Newest first:

```markdown
## 2026-05-22
* **Update**: Added [Customer Metrics](/tables/customer-metrics.md).
* **Creation**: Established [Dataplex Playbook](/playbooks/dataplex.md).
```

## Conformance (v0.1)

A bundle is conformant if:

1. Every non-reserved `.md` file has parseable YAML frontmatter
2. Every frontmatter has non-empty `type`

Consumers MUST NOT reject bundles for missing optional fields, unknown types, or broken links.

## Relationship to LLM Wiki

OKF §10 acknowledges LLM wiki repos (markdown + frontmatter + wikilinks) as a close cousin. OKF adds:

- Formal interchange rules (required `type`, reserved filenames, index/log conventions)
- Standard markdown links instead of wikilinks
- ISO 8601 timestamps and `description` for machine-readable catalogs

Conversion between formats is mechanical with wikilink resolution and frontmatter mapping.

## Reference Agent Stricter Validation

The Python reference agent in knowledge-catalog additionally requires:
`type`, `title`, `description`, `timestamp` — this is implementation choice, not spec requirement.
