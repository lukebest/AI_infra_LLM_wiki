---
type: Summary
title: Arch-Study 30d Knowledge Map
description: 体系结构 30 天收束：五阶段知识地图、五个根问题、十大公式；衔接 WSE/NoC/NPU 研究
tags:
- architecture
- methodology
- amdahl
- roofline
- summary
- wse
- noc
timestamp: '2026-07-13T00:00:00Z'
created: 2026-07-13
sources:
- raw/articles/arch-study-30d-day-30.md
---

# Arch-Study 30d Knowledge Map（30 天知识地图）

arch-study **Day 30**：不读新教材——把 Day 1–29 **收束成地图、根问题与公式清单**。完整笔记：[raw/articles/arch-study-30d-day-30.md](raw/articles/arch-study-30d-day-30.md)。

## 五阶段脉络

| 阶段 | Days | 锚点概念（wiki） |
|------|-------|------------------|
| ① 量化基础 | 1–7 | [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) |
| ② 现代 CPU | 8–16 | [CPU Pipeline](/concepts/cpu-pipeline-fundamentals.md)、[OoO](/concepts/out-of-order-execution.md)、[Branch Prediction](/concepts/branch-prediction.md)、[Cache](/concepts/memory-hierarchy-cache.md)、[TLB](/concepts/virtual-memory-tlb.md) |
| ③ 存储 | 17–22 | [DRAM](/concepts/dram-memory-system.md)、[Coherence](/concepts/cache-coherence.md)、[NoC Fundamentals](/concepts/noc-fundamentals-hp-appendix-f.md)、[End-to-End Memory Path](/concepts/end-to-end-memory-data-path.md) |
| ④ 并行 | 23–27 | [Multicore/SMT](/concepts/multicore-smt-nuca.md)、[GPU SIMT](/concepts/gpu-simt-architecture.md)、[Systolic DSA](/concepts/dnn-accelerator-systolic-dataflow.md)、[WSE Quant](/concepts/wse-quantitative-architecture-analysis.md)、[LLM Collectives](/concepts/llm-distributed-training-collectives.md) |
| ⑤ 研究 | 28–30 | [Paper Reading](/concepts/architecture-paper-reading-methodology.md)、[Post-Moore](/concepts/post-moore-architecture-frontiers.md)、本页 |

```
量化基础 → CPU 核心 → 存储/NoC → 并行(GPU/DSA/WSE/分布式)
                                    ↓
                         后摩尔：DSA × Packaging × Novel
```

## 五个根问题

1. **性能从哪来？** — `IC × CPI × T`；三因子互锁（频率↔分支惩罚、并行↔通信）  
2. **瓶颈在哪？** — Roofline + Amdahl；WSE Ridge≈6 → decode 偏 memory  
3. **数据怎么搬？** — 层次延迟差数量级；片上 PB/s vs 片外 TB/s  
4. **并行怎么排？** — ILP/DLP/TLP + 流水/重叠；WSE「反传统武器」换海量 PE  
5. **怎么评价？** — 公平 / 透明 / 可复现（同工艺、同预算、报告 tail 与敏感度）

## 十大公式速查

| # | 公式 | 场景 |
|---|------|------|
| 1 | CPU Time = IC × CPI × T | 任意性能 |
| 2 | Speedup = 1/((1−f)+f/S) | 优化决策 |
| 3 | P = αCV²f | 功耗 |
| 4 | AMAT = Hit + Miss×Penalty | 存储层次 |
| 5 | CPI = Σ freq×cpi | ISA/微架构 |
| 6 | Yield = e^(−D₀A) | 良率/WSE |
| 7 | Attainable = min(Peak, BW×AI) | Roofline |
| 8 | Ridge = Peak/BW | 瓶颈判定 |
| 9 | B_bisect = n（n×n Mesh） | NoC 拓扑 |
| 10 | t_msg ≈ L/B + H×t_hop | 网络延迟 |

## 研究衔接（示例）

| 方向 | 地图位置 |
|------|----------|
| WSE | Day 26 量化 + Day 27 跨 wafer + Day 28 Reduce 论文 |
| NoC | Day 21–22 + Day 29 光/可重构/demand-aware |
| NPU | Day 25 脉动/数据流 + Day 29 稀疏/混合精度 |
| LLM 系统 | Day 27 集体通信 + Prefill/Decode 分歧 |

## 相关页面

- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md)
- [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md)
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)
- [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md)
- [Cerebras WSE](/entities/cerebras-wse.md)

# Citations

[1] [raw/articles/arch-study-30d-day-30.md](raw/articles/arch-study-30d-day-30.md) — 总复习与知识地图（Day 30）
