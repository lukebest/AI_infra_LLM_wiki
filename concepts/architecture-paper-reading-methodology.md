---
type: Concept
title: Architecture Paper Reading Methodology
description: 体系结构论文 5 步精读法 + 四大量化武器（归因/Roofline/敏感性/Pareto）；以 Luczynski HPDC'24 Wafer-Scale Reduce 为范例
tags:
- methodology
- paper
- research
- architecture
- benchmark
- wse
- reduce
timestamp: '2026-07-13T00:00:00Z'
created: 2026-07-13
sources:
- raw/articles/arch-study-30d-day-28.md
---

# Architecture Paper Reading Methodology（体系结构论文阅读方法论）

arch-study **研究篇 Day 28**：把教材式输入转为**从论文挖矿**。范例精读：[Near-Optimal Wafer-Scale Reduce](/concepts/wse-reduce-algorithms.md)（Luczynski et al., HPDC 2024, arXiv:2404.15888）。

**Source:** [raw/articles/arch-study-30d-day-28.md](raw/articles/arch-study-30d-day-28.md)

## 教材 vs 论文

| | 教材 | 论文 |
|--|------|------|
| 目的 | 完整领域知识 | 解决**一个开放问题** |
| 公式 | 可追溯 | 常省略推导 |
| 实验 | 教学例 | 精选 baseline / workload |
| 结论 | 公理式 | 有 marketing 倾向 → 需批判 |

## 5 步精读法

| Step | 焦点 | 红旗 |
|------|------|------|
| **1 Abstract** | 问题 / 方法 / **量化数字** | 无数字几乎是弱文 |
| **2 Intro** | 痛点、局限、insight、贡献清单 | 痛点含糊、insight 陈词 |
| **3 Related** | 前人谱系图 | 只引对自己有利的工作 |
| **4 Method** | 假设、公式来源、复杂度 | 公式凭空出现 |
| **5 Experiments** | baseline 公平、workload、tail、敏感度、真机 vs 模拟 | 仅合成负载、无 sensitivity |

**阅读顺序**：贡献 → 证据 → 方法（不必线性通读）。三遍：鸟瞰（§1+§结论+图）→ 骨架（算法+模型+结果）→ 批判（假设/缺失实验）。

## 四大量化武器

1. **性能归因** — `T = T_compute + T_comm + …`；stacked bar  
2. **Roofline** — compute vs memory/comm-bound；见 [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md)  
3. **敏感性分析** — 单参数扫描（N、D、B、拓扑）  
4. **Pareto 前沿** — 多目标（perf vs 面积/能耗）

## 范例：Wafer-Scale Reduce 读出什么

**Insight**：2D mesh 被传统 Ring/Tree 当成 1D 抽象 → **浪费局部性**。

| 算法 | 要点 |
|------|------|
| **FRED** | 用现有 5 端口路由，沿 2D tree reduce；无额外硬件；大 N 接近下界 |
| **FREDR** | 路由器内嵌小归约单元（边转发边算）；面积 +k% 换延迟 −m% |

相对 Ring：大 N 时 Ring 的 **(N−1)·t_hop** 灾难；FRED 以 **log 直径项 + 带宽项** 主导。完整算法族与数字见 [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)。

**批判清单（可复用）**：baseline 是否同工艺/同色路由资源？消息大小扫了吗？真机还是模拟？与 Day 27 [LLM Collectives](/concepts/llm-distributed-training-collectives.md) 的 Ring 对比是否公平？

## 相关页面

- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — 精读对象
- [WSE Performance Model](/concepts/wse-performance-model.md) — 延迟模型
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — Day 27 集群侧
- [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md) — 几何均值/陷阱
- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — Amdahl/功耗地基
- [Arch-Study 30d Knowledge Map](/summaries/arch-study-30d-knowledge-map.md) — Day 30 收束
- [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md) — NoC 五决策读法（互连 Day 20）

# Citations

[1] [raw/articles/arch-study-30d-day-28.md](raw/articles/arch-study-30d-day-28.md) — 论文方法论 + Luczynski 精读（Day 28）
[2] [raw/papers/Near-optimal_wafer-scale_reduce.pdf](raw/papers/Near-optimal_wafer-scale_reduce.pdf) — Luczynski et al., HPDC 2024
