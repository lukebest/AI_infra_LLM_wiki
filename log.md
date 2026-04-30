# Wiki Log

> 按时间顺序记录所有 wiki 操作。仅追加。
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-16] create | Wiki initialized
- Domain: AI 基础设施（scale-up 网络、加速器架构、确定性执行、推理系统）
- Structure created with SCHEMA.md, index.md, log.md

## [2026-04-16] ingest | NVIDIA Groq 3 LPX Blog Article
- Source: raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- Created: entities/nvidia-groq-3-lpx.md, entities/nvidia-vera-rubin-nvl72.md, entities/cerebras-wse.md, concepts/deterministic-execution.md, concepts/lpu-architecture.md, concepts/heterogeneous-inference.md
## [2026-04-16] ingest | MegaScale-Infer + 3 analyses
- Ingest: papers/megascale-infer-2504.02263.md
- Created: analyses/wse-nom-contradiction-analysis.md (矛盾论六步)
- Created: analyses/cerebras-wse-vs-groq-network-comparison.md (全面对比)
- Updated: index.md (10 pages total)
- 使用《矛盾论》六步框架系统性分析 WSE Network-on-Wafer
- Created: analyses/wse-nom-contradiction-analysis.md
- 主要矛盾：物理均匀性 vs 通信异构性（通信异构性是主要方面）
- 关键洞察：color routing 是调和性缓解，非根本解决

## [2026-04-17] ingest | MegaScale-Infer 概念提取
- Created: concepts/disaggregated-inference.md, concepts/m2n-communication.md
- Updated: papers/megascale-infer-2504.02263.md (添加交叉引用)
- Updated: index.md (8 pages total)
## [2026-04-20] ingest | 信息论视角下的 AI Agent 价值模型
- Source: raw/papers/information-theory-ai-agents-2026-04.md
- Created: concepts/information-theoretic-value-model.md
- Updated: index.md (9 pages total)
- Topic: 互信息 I(S;K) 作为 Agent 价值的核心度量，有效性条件 I(S;K)/H(S) > 0.5 (α=2)，悖论区间，工程策略

## [2026-04-17] ingest | AI Tools Weekly Report (manual run)
- Report: notes/projects/ai-tools-weekly-2026-04-17.md
- Email sent: liuyingxyzabc@live.com (Foxmail SMTP, fixed From address)
- Topics: OpenClaw 2026.4.12, Cursor 3, Windsurf/Cognition, Claude Code rebuild, Opus 4.7

## [2026-04-28] ingest | DeepSeek-V4 Technical Report
- Source: DeepSeek_V4 PDF (54 pages)
- Files created:
  - entities/deepseek-v4.md — Model entity page
  - concepts/csa-hca.md — Hybrid attention architecture
  - concepts/mhc.md — Manifold-Constrained Hyper-Connections
  - concepts/muon-optimizer.md — Muon optimizer with Hybrid Newton-Schulz
  - concepts/fp4-qat.md — FP4 Quantization-Aware Training
  - concepts/megamoe-kernel.md — Expert Parallelism communication-computation overlap
  - concepts/tilelang.md — TileLang DSL for kernel development
  - concepts/dsec-sandbox.md — DSec sandbox platform
  - summaries/deepseek-v4.md — Paper summary with wiki cross-links
- Updated: index.md (22 pages total)
- Note: Merged from workspace wiki into ~/wiki/
