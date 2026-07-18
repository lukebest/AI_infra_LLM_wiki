---
type: Summary
title: 'CosMoS: Architectural Support for Cost-Effective Data Movement in a Disaggregated Memory Systems'
description: ACM JETCAS 2025 — 解耦内存系统硬件热页预测/调度迁移，+20% vs SOTA、+86% vs 基线；保护关键路径 cache miss
tags:
- memory
- virtualization
- infrastructure
- optimization
- scheduling
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/CosMoS_Disaggregated_Memory_Data_Movement_2025.pdf
---

# CosMoS: Architectural Support for Cost-Effective Data Movement in a Disaggregated Memory Systems

**ACM JETCAS 2025** | DOI [10.1145/3725218](https://doi.org/10.1145/3725218)  
Puri, Jose, Tamarapalli（IIT Guwahati）

**Disaggregated Memory System (DMS)** 的硬件页迁移架构：预测热页、调度迁移顺序，并在迁移进行时**不阻塞关键路径上的 remote cache miss**。

## 核心贡献

1. **Workload 特征化**：页访问频率分布宽；多数页 criticality 在生命周期内稳定
2. **硬件热页预测 + 调度**：避免 OS 方案 ping-pong 与带宽浪费
3. **Early response**：迁移与常规 remote cache-line 访问解耦

## 关键数字

| 指标 | 值 |
|------|-----|
| CXL remote vs local | **3–4×** 延迟（**170–250 ns**） |
| 4KB 页迁移 | **1.2–1.5 µs** |
| vs SOTA / baseline | **+20%** / **+86%** |

## 与 wiki 交叉

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 解耦内存数据移动
- [DRAM Memory System](/concepts/dram-memory-system.md) — tiered / remote memory 背景

# Citations

[1] [raw/papers/CosMoS_Disaggregated_Memory_Data_Movement_2025.pdf](raw/papers/CosMoS_Disaggregated_Memory_Data_Movement_2025.pdf)
[2] [raw/papers/cosmos-disaggregated-memory-data-movement.md](raw/papers/cosmos-disaggregated-memory-data-movement.md) — 结构化摘录
