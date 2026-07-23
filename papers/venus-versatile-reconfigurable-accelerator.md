---
type: Summary
title: 'Venus: A Versatile Deep Neural Network Accelerator Architecture Design for Multiple Applications'
description: DAC 2023 NoC fission/fusion 多 DNN 并行 serving：分布式 buffer + flexible NoC 按 workload 动态 morph；首个 runtime multi-tenancy 适配 layout 工作
tags:
- accelerator
- noc
- fission-fusion
- multi-dnn
- dac
- reconfigurable
- multi-tenant
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- raw/papers/Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf
---

# Venus

**Authors:** Jiaqi Yang et al. (George Washington University, HPCAT lab) | **Venue:** DAC 2023 | **PDF:** [raw/papers/Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf](Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf)

## 一句话总结

**Venus** 首个让 **NoC 按 workload 动态 fission / fusion**：单 DNN 跑时**合并** NoC 提带宽；多 DNN 并行 serving 时**拆分** NoC 给每个 model 独立子网 + 自适应 buffer layout。**layout 适配从"单层"扩展到"runtime 多 DNN 隔离"**。

## 核心创新：NoC Fission / Fusion

**Fission（拆分）**：
- 一个 NoC → 多个 sub-NoC
- 每个 sub-NoC 服务一个 DNN
- **QoS 隔离** + **per-DNN layout 选择**

**Fusion（合并）**：
- 多个 sub-NoC → 一个大 NoC
- 给一个 bandwidth-heavy layer 满带宽
- 提升 bisection bandwidth

```
       Single DNN (FUSION)
       ┌─────────────────┐
       │   PE0 PE1 PE2   │
       │   PE3 PE4 PE5   │
       │   PE6 PE7 PE8   │  ← 整片 NoC
       └─────────────────┘

       Multi-DNN (FISSION)
       ┌──────┐ ┌──────┐
       │ PE0  │ │ PE4  │
       │ PE1  │ │ PE5  │  ← DNN-A  ← DNN-B
       │ PE2  │ │ PE6  │     独立 sub-NoC
       │ PE3  │ │ PE7  │
       └──────┘ └──────┘
```

## Layout / dataflow 能力

- **Distributed buffer**：每 tile 有自己的 buffer，**per-tile layout** 自由选择
- **Reconfigurable systolic array**：可 fission / fusion compute
- **Flexible NoC**：物理数据通路可动态变
- **整体效果**：runtime 选择 **best (topology, layout, schedule)** for current workload

## 数字

- (论文细节未深入抓，主要数据点)
- DAC 2023 acceptance → 论文级别认可

## 与 FEATHER 的关系

| | FEATHER (2024) | Venus (2023) |
|---|-----------------|---------------|
| **layout 适配粒度** | **per-layer**（每层 kernel）| **per-workload**（多 DNN 隔离）|
| **NoC 重构** | BIRRD butterfly（编译期） | **runtime fission/fusion**（硬件层）|
| **适用场景** | 单 DNN 推理 | **多 DNN 并行 serving** |

**Venus 的多租户 layout 隔离** 是 FEATHER 单层 layout 适配的 **正交补充**。

## 与 wiki 已有内容的关联

- [FEATHER Accelerator](/concepts/feather-accelerator.md) — per-layer layout 适配
- [MAERI (paper summary)](/papers/maeri-flexible-dataflow-reconfigurable-interconnects.md) — 灵活 interconnect 原始思想
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — 同样可重构
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 多 DNN serving 视角

# Citations

[1] [raw/papers/Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf](Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf) — Yang et al. DAC 2023