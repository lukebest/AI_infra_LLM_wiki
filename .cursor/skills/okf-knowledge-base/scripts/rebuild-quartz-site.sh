#!/usr/bin/env bash
# Sync OKF wiki work layer into Quartz and rebuild.
# Usage: .cursor/skills/okf-knowledge-base/scripts/rebuild-quartz-site.sh [--deploy]
set -euo pipefail

WIKI="${WIKI:-/home/luke/wiki}"
QUARTZ="${QUARTZ:-/home/luke/workspace/ai-infra-wiki-quartz}"
DEPLOY=0
[[ "${1:-}" == "--deploy" ]] && DEPLOY=1

if [[ ! -d "$QUARTZ" ]]; then
  echo "Quartz project not found at $QUARTZ" >&2
  exit 1
fi

cd "$QUARTZ"
rm -rf content
mkdir -p content
rsync -a \
  "$WIKI/concepts" "$WIKI/entities" "$WIKI/papers" "$WIKI/analyses" "$WIKI/summaries" \
  "$WIKI/SCHEMA.md" "$WIKI/log.md" "$WIKI/README.md" \
  content/

cat > content/index.md <<'EOF'
---
title: AI Infra LLM Wiki
description: Open Knowledge Format 知识库 — AI 基础设施、互连网络、晶圆级加速器与 LLM 推理系统
---

# AI Infra LLM Wiki

面向 **AI 基础设施** 的可编译知识库：互连网络 / NoC、晶圆级加速器（WSE）、LLM 推理、DSA 与编译器。

由 OKF 概念页持续沉淀；本站提供 **图谱浏览、全文搜索、反向链接、页面预览**。

## 浏览入口

- [[concepts/index|Concepts]] — 机制、架构与方法论
- [[entities/index|Entities]] — 产品、芯片与组织
- [[papers/index|Papers]] — 论文摘要
- [[analyses/index|Analyses]] — 深度分析
- [[summaries/index|Summaries]] — 综述
- [[log|Update Log]] — 变更历史

## 源仓库

[github.com/lukebest/AI_infra_LLM_wiki](https://github.com/lukebest/AI_infra_LLM_wiki)
EOF

python3 <<'PY'
from pathlib import Path
for name, title, desc in [
    ("content/SCHEMA.md", "Schema", "OKF wiki schema and tag taxonomy"),
    ("content/log.md", "Update Log", "Bundle update history"),
    ("content/README.md", "About", "About this OKF knowledge wiki"),
]:
    p = Path(name)
    text = p.read_text(encoding="utf-8")
    if text.startswith("---"):
        continue
    p.write_text(f"---\ntitle: {title}\ndescription: {desc}\n---\n\n{text}", encoding="utf-8")
PY

npx quartz build -d content -o public
echo "Built → $QUARTZ/public"

if [[ "$DEPLOY" -eq 1 ]]; then
  TMP=$(mktemp -d)
  git clone --depth 1 git@github.com:lukebest/lukebest.github.io.git "$TMP"
  cd "$TMP"
  find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
  cp -a "$QUARTZ/public/." .
  touch .nojekyll
  git add -A
  git commit -m "Update Quartz site from AI_infra_LLM_wiki" || {
    echo "No changes to deploy"
    exit 0
  }
  git push origin HEAD
  echo "Deployed → https://lukebest.github.io/"
fi
