---
type: Concept
title: FEATHER Accelerator
description: 可重构 DNN 加速器：NEST 2D PE 阵列 + BIRRD 蝶形归约/重排网络，RIR 在归约中隐藏 layout 切换，Layoutloop 联合 dataflow-layout 搜索
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

# FEATHER Accelerator

**FEATHER**（Flexible Engine for Acceleration of Tensors with Hardware Element for Reordering）是 Georgia Tech 提出的可重构 ML 推理加速器：在**每层**切换最优 **(dataflow, layout)** 对，用 **RIR**（Reorder in Reduction）在归约阶段隐式重排片上 buffer 布局，消除 bank conflict 与显式 reorder 延迟。

**Authors:** Jianming Tong, Anirudh Itagi, Prasanth Chatarasi, Tushar Krishna | **arXiv:** [2405.13170](https://arxiv.org/abs/2405.13170) (2024) | **Code:** https://github.com/maeri-project/FEATHER

## 核心问题：dataflow–layout 失配

DNN 层 dataflow 由 loop nest 的 **TOPS** 四维定义：

| 维度 | 含义 |
|------|------|
| **T**iling | 分块适配片上存储 |
| **O**rdering | loop 顺序 / stationarity（input/output/weight） |
| **P**arallelism | 空间并行维度 |
| **S**hape | PE 阵列虚拟分组 |

Timeloop 等框架只建模 buffer **带宽**，忽略 **layout**（inter-line / intra-line 维度顺序）→ 最优 dataflow 在 practice 中可慢 **128×**（bank port 冲突 stall PE）。

```
discordant (dataflow, layout) → 同 cycle 读 > NP 个 bank line → slowdown
concordant → 无 bank conflict
```

片上 buffer 逻辑为 **num_line × line_size** 2D 阵列；TSMC 28nm SRAM 每 bank 最多 **2 port**——并发访问超 port 数即冲突。

## 架构（Fig. 7）

```
StaB/StrB (ping-pong) → NEST (2D PE) → BIRRD → OB → Quantize → StaB (新 layout)
```

| 组件 | 功能 |
|------|------|
| **NEST** | Neural Engine with Spatial forwarding + Temporal reduction；2D PE 阵列，行**时分复用**共享归约网络（vs MAERI/SIGMA 全互联） |
| **BIRRD** | Butterfly Interconnect for Reduction and Reordering in Dataflows；EGG 开关：Pass/Swap/Add-Left/Add-Right |
| **StaB / StrB** | Stationary / Streaming ping-pong buffer |
| **RIR** | 归约输出 oActs 时直接写入**下一层 concordant layout**，非 RAR（Reorder After Reduction） |

### NEST 两阶段

1. **Phase 1**：PE 内 local temporal reduction（partial sum 累加）
2. **Phase 2**：按**行**依次 spatial reduction（BIRRD 时分），同列 PE 共享 output bus 无冲突

结合 ping-pong weight 寄存器，steady state 全 PE 利用。

### BIRRD vs  prior art

| 能力 | SIGMA/MAERI | BIRRD |
|------|-------------|-------|
| 归约 | 全互联 / fat-tree，面积大 | 蝶形网络，**AW×AH 行共享** |
| 重排 | 无 / 片外 / RAR（critical path） | **Arbitrary reorder + RIR** |
| 分发 | 需复杂 multicast NoC | RIR 对齐 layout → **点对点直送 NEST** |

Reorder pattern 谱系：Fixed → Line Rotation → Transpose → Row Reorder → **Arbitrary**（FEATHER）；仅 Arbitrary 扩展 O/P/S 全 concordant 空间。

## Layoutloop

Timeloop 增强版：**物理 storage 建模**（num_line × line_size、conflict depth、NP port）+ layout 评估 + dataflow-layout **co-search**（每层最小 EDP）。

Insight：weights 可 offline reorder；**iActs 须 online reorder**——RIR 在 compute 归约中完成。

## 评估摘要

| 设置 | 结果 |
|------|------|
| Layoutloop vs NVDLA/Eyeriss/SIGMA | 延迟 **1.27–2.89×**，能效 **1.3–6.43×**（ResNet-50、MobileNet-V3） |
| ZCU104 FPGA vs Gemmini / Xilinx DPU | **3.91× / 2.65×** 归一化吞吐；vs Edge TPU **4.56×** geomean |
| vs 固定 dataflow Eyeriss-like | 面积仅 **+6%** |
| (dataflow, layout) co-switch | 能效节省 **27–33%**（含 reorder 开销） |

## 与 wiki 的关系

- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — FEATHER 对比的 **固定 Eyeriss-like RS dataflow** 基线（+6% 面积换 co-switch）；同作者 Krishna
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — 同期 CGRA 路线（parallel patterns）
- [Layout-Aware NoC and Flexible Dataflow Accelerators](/concepts/layout-aware-noc-flexible-dataflow.md) — 5 类柔性 NoC 路线 + 5 篇核心 paper
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 片上 distributed memory / bank 利用率问题同类
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 固定 dataflow（DPU/Gemmini）vs 可重构
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 同为 dataflow 编程抽象，FEATHER 面向 DNN 片上 buffer，SpaDA 面向 WSE NoC
- [Deterministic Execution](/concepts/deterministic-execution.md) — stationarity 与编译时 dataflow 选择

## 相关页面

- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — 固定 RS dataflow 流片基线
- [papers/feather-reconfigurable-accelerator.md](/papers/feather-reconfigurable-accelerator.md) — 论文摘要
- [papers/eyeriss-energy-efficient-cnn-accelerator.md](/papers/eyeriss-energy-efficient-cnn-accelerator.md) — Eyeriss JSSC 2017 摘要
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 片上 SRAM port 约束类比

# Citations

[1] [raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf](raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf) — Tong et al. (2024), arXiv:2405.13170
