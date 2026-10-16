---
type: Paper
title: "CacheSmith: Adaptive KV Reuse for RAG under Latency SLOs"
description: "POSTECH/MSR — RAG 上下文缓存的选择性重算拆成 WarmUp/Probe/Patch；SLO 感知调度 + 预算规划；quality-gated SLO 达成率最高 +27.5%，P99 TTFT 最高 −86%"
tags:
- kv-cache
- inference
- serving
- prefill
- latency
- serving-system
- gpu
- nvidia
created: 2026-10-16
updated: 2026-10-16
timestamp: '2026-10-16T00:00:00Z'
paper_author: [Xinyue Ma, Damin Lee, Aashaka Shah, Myeongjae Jeon]
year: 2026
arxiv: '2610.18925'
sources:
  - raw/papers/CacheSmith_Adaptive_KV_Reuse_RAG_SLO_2026.pdf
  - raw/papers/cachesmith-adaptive-kv-reuse-rag-slo.md
---

# CacheSmith：RAG 上下文缓存的自适应 KV 重用

## 一句话结论
按 chunk 预计算的 KV 缺跨 chunk attention。静态「固定层 + 固定覆盖率」的选择性重算跟不上请求异质与排队后剩余 TTFT。CacheSmith 把重算拆成 **WarmUp / Probe / Patch**，用 SLO 感知批处理与预算带规划，最大化「既达标又够准」的请求比例。

## 动机（论文数字）
- PassageRetrieval 上 CacheBlend@15% 准确率随段落数从 10→40 由 **65%→39%**；p90 所需覆盖率从 20 段的 **35%** 升到 40 段的 **65%**。
- 加深 warm-up（前 5 层全算）把 40 段组的中位最小覆盖率从 **20%→10%**、p90 **65%→30%**，CacheBlend@15% 准确率 **39%→63%**。
- QCI（ProphetKV）与 KV-dev（CacheBlend）在不同任务上互有胜负；探测本身也吃 TTFT。

## 方案
| 部件 | 做法 |
|---|---|
| 抽象 | 配置 (S, w, p, r)：信号、warm-up 深度、probe 长度、patch 覆盖率 |
| Planner | 预算内选 rank depth 与 (w,p)，再按需求分布分覆盖率；输出 **budget band** |
| Scheduler | 按 deadline×长度分桶组批；在 band 内抬预算；瞬态突发可 partial KV 滑窗 |
| Runtime | 相位感知 KV 预取；传输滞后时重规划 |

## 效果（仅论文数字；vLLM 0.10.2，RTX PRO 6000）
- 四任务 × 多种到达/SLO，共 96 设置：相对 BestStatic 在 **93/96** 胜出；quality-gated SLO attainment 提高 **2–27.5%**（最高 **27.5%**）。
- 相对四基线（EPIC / ProphetKV / CacheBlend / FusionRAG）：P99 TTFT 最高砍 **86%**。
- PR 上可达约 **97%** attainment × **89%** accuracy 组合，基线任一覆盖率达不到。
- 链路 10→3 GB/s：基线 stall **12–72%** 服务时间；CacheSmith **3–7%**；PR 准确率随变慢链路升至 **92%**（规划更深 WarmUp 掩盖传输）。

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 在 vLLM 上实现的 prefill 侧重算层
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 复用 KV 的质量–延迟权衡
- [Lachesis](/papers/lachesis-lifetime-aware-kv-hbm-hbf.md)、[Adaptive DHiSparse](/papers/adaptive-dhisparse-speculative-hierarchical-kv.md) — 同属 KV 放置/复用族

## 局限
- 主评测 8B/32B；rank–accuracy 曲线轻量重标定后迁到 Qwen3-32B。
- QCI 路径共享未调优 Triton，相对原论文延迟偏悲观。

# Citations
- Ma et al., "CacheSmith: Accurate RAG Serving under Latency SLOs with Adaptive KV Reuse", arXiv:2610.18925. [raw](/raw/papers/cachesmith-adaptive-kv-reuse-rag-slo.md) · [PDF](/raw/papers/CacheSmith_Adaptive_KV_Reuse_RAG_SLO_2026.pdf)
