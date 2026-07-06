---
type: Summary
title: Superscalar CPU Research (2023-2026)
description: OpenClaw 综述：Constable/Bullseye/Prophet/CVA6S+、旁路子系统范式、OoO 边际饱和、WSE/LLM 关联矩阵与核内同步 Gap；Scout→Critic 8.2-8.4/10
tags:
- architecture
- cpu
- superscalar
- isca
- research-survey
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/reports/superscalar-cpu-final-report.md
- raw/reports/superscalar-cpu-report.md
---

# Superscalar CPU 研究综述 (2023-2026)

**流程:** Scout → Analyst → Writer → Critic → Writer v2 | **评分:** 8.2-8.4/10 | **Raw:** [final](raw/reports/superscalar-cpu-final-report.md) · [report v2](raw/reports/superscalar-cpu-report.md)

## 一句话总结

2023-2026 超标量研究从「堆 ROB/挖 ILP」转向**异构旁路子系统 + 软硬件协同跳过无效访问**；LLM memory-bound 把 **load 消除**（Constable）、**H2P 前端**（Bullseye）、**profile 预取**（Prophet）推上 ISCA 中心；**CVA6S+** 是可 fork 的开源 RISC-V 工业 baseline。

## Top 论文

| 论文 | 会议 | 核心数字 |
|------|------|---------|
| Constable | ISCA'24 Best Paper | +5.1% perf / -3.4% 功耗 |
| CVA6S+ | arXiv'25 | +43.5% IPC vs 标量 CVA6 |
| Bullseye | CBP-2025 | MPKI 3.4045 / 187 KB |
| Prophet | ISCA'25 | +14.23% vs Triangel |
| AVM-BTB ⚠️ | ISCA'24 | 未深分析 |

## 五条 Insight（性质）

- 🔀 **旁路子系统范式** — Constable / Bullseye / Prophet 旁路主表
- 🔁 **CVA6S+ + M1 RE 双轨** — 开源 RTL + 工业参数校准
- 🔀 **前端+内存瓶颈** — OoO 深度边际饱和
- 💡 **WSE LLM 专用 ISA** — 研究提案
- 💡 **微架构透明度** — 战略提案

## Luke 关联 Highlights

| 方向 | 要点 |
|------|------|
| 超标量核 | Constable tracker + fork CVA6S+ + Bullseye HIT |
| WSE | WSE-aware Constabulary；Prophet 片间预取 |
| LLM | KV cache likely-stable；Prophet KV 预取 |
| 核内同步 | **Gap** — Constable 未必适用 LR/SC |

## 优先行动

1. ~~精读 Constable（2-3 h）~~ → [Constable Load Elimination](/concepts/constable-load-elimination.md)（deep-dive 已 ingest）
2. `git clone openhwgroup/cva6s` + gem5 baseline
3. 获取 AVM-BTB ISCA'24 全文
4. gem5 profile LR/SC → 核内同步 proposal

## 与 wiki 交叉引用

- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — 结构化概念页
- [Constable Load Elimination](/concepts/constable-load-elimination.md) — ISCA'24 Best Paper 精读
- [Branch Prediction](/concepts/branch-prediction.md) — Bullseye / TAGE
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — ROB 边际饱和
- [Cerebras WSE](/entities/cerebras-wse.md) — 与超标量控制核对比

# Citations

[1] [raw/reports/superscalar-cpu-final-report.md](raw/reports/superscalar-cpu-final-report.md) — 最终汇总
[2] [raw/reports/superscalar-cpu-report.md](raw/reports/superscalar-cpu-report.md) — 综述 v2
