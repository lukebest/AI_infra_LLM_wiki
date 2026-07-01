---
type: Summary
title: 'FEATHER: A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Switching'
description: NEST+BIRRD 可重构加速器，RIR 在归约中做 arbitrary layout reorder；Layoutloop dataflow-layout 联合搜索，ResNet-50 1.27–2.89× 延迟、FPGA 2.65–3.91× 吞吐
tags:
- accelerator
- dataflow
- dnn
- architecture
- compiler
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf
---

# FEATHER: A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Switching

**Authors:** Jianming Tong, Anirudh Itagi, Prasanth Chatarasi, Tushar Krishna | **Affiliations:** Georgia Tech; IBM Research | **PDF:** [raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf](raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf) | **arXiv:** 2405.13170

## 一句话总结

FEATHER 用 **NEST**（2D PE + 行时分共享归约）和 **BIRRD**（蝶形 arbitrary reduce+reorder）实现每层 **(dataflow, layout) co-switch**；**RIR** 在归约阶段隐式写出下一层 concordant layout，消除 Timeloop 忽略 layout 导致的 **128× theory-practice 鸿沟**，面积仅比固定 Eyeriss-like 基线 **+6%**。

## 核心贡献

1. **问题量化**：dataflow 最优 ≠ 实践最优——bank port 冲突可致 **128×** 延迟差距；需 per-layer layout reorder（iActs online）
2. **NEST**：local temporal reduction + 行间时分 spatial reduction，2D 阵列共享低成本归约网
3. **BIRRD + RIR**：蝶形网络同时 arbitrary reduction 与 **Arbitrary Reorder**；reorder 延迟隐藏在 compute reduction 中（非 RAR/off-chip）
4. **Layoutloop**：Timeloop + 物理 buffer 建模 + layout 评估 + dataflow-layout co-search

## 关键机制

### Dataflow (TOPS)

Tiling / Ordering (stationarity) / Parallelism / Shape — 单层设计空间 O(10³⁶)。

### Layout 术语

`CHW W4H2C2` = inter-line 顺序 C→H→W + intra-line (4,2,2) 展平为 W→H→C。

### Reorder 谱系

Fixed → Line Rotation → Transpose → Row Reorder → **Arbitrary**（FEATHER/BIRRD）

| 实现 | 代价 |
|------|------|
| Off-chip | DRAM 往返 + CPU reorder |
| RAR (Medusa/MTIA/TPUv4) | reorder 在 critical path |
| **RIR** | oActs 归约时直接写入新 layout |

## 实验摘要

| 对比 | 结果 |
|------|------|
| Layoutloop: vs NVDLA/Eyeriss/SIGMA | 延迟 **1.27–2.89×**，能效 **1.3–6.43×** |
| ZCU104: vs Gemmini / Xilinx DPU | **3.91× / 2.65×** 归一化吞吐 |
| vs Edge TPU | **4.56×** geomean |
| 面积 vs 固定 Eyeriss-like | **+6%** |
| 最优 (dataflow,layout) co-switch | 能效 **+27–33%** |

## 与 wiki 交叉引用

- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 架构与 Layoutloop
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 片上 memory bank 利用率
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 固定 vs 可重构 dataflow
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 另一 dataflow 抽象层（WSE/CSL）

# Citations

[1] [raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf](raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf) — Tong et al. (2024)
