---
type: Summary
title: 'PANDA: Adaptive Prefetching and Decentralized Scheduling for Dataflow Architectures'
description: ACM TACO 2025 — 应用自适应 prefetch + PE 去中心化调度；相对 Plasticine 1.90×、REVEL 2.53× geomean 性能
tags:
- accelerator
- dataflow
- scheduling
- spatial-execution
- memory
- cache
- optimization
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/PANDA_Adaptive_Prefetch_Dataflow_Architectures_2025.pdf
---

# PANDA: Adaptive Prefetching and Decentralized Scheduling for Dataflow Architectures

**ACM TACO 2025** | DOI [10.1145/3721288](https://doi.org/10.1145/3721288)  
Qin, Fan, Li, Wang, An, Ye, Fan（中科院计算所）

数据流加速器 **PANDA**：区分 prefetchable / non-prefetchable 数据的自适应预取 + **PE 去中心化动态调度**（task stealing），可重构 SPM/cache 片上存储。

## 核心贡献

1. **Application-adaptive prefetch**：stream 数据预取到 SPM；不规则访问走 cache load/store
2. **Reconfigurable on-chip memory**：SPM 与 cache 共享物理存储，按 ISA 划分
3. **Decentralized scheduling**：PE 自主调度 + 负载均衡，摆脱集中控制器瓶颈

## 关键数字

| vs baseline | geomean 加速 |
|-------------|-------------|
| REVEL | **2.53×** |
| Plasticine | **1.90×** |
| DFU | **1.38×** |
| MTDE | **1.19×** |
| 能效 | 最高 **1.79×** |

## 与 wiki 交叉

- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — 数据流 CGRA 对照 baseline
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 加速器 dataflow 谱系

# Citations

[1] [raw/papers/PANDA_Adaptive_Prefetch_Dataflow_Architectures_2025.pdf](raw/papers/PANDA_Adaptive_Prefetch_Dataflow_Architectures_2025.pdf)
[2] [raw/papers/panda-adaptive-prefetch-dataflow.md](raw/papers/panda-adaptive-prefetch-dataflow.md) — 结构化摘录
