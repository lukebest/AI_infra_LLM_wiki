---
type: Concept
title: Post-Moore Architecture Frontiers
description: 摩尔/Dennard 之后的体系结构主线：AI 加速器、NoC 新方向、Chiplet、Wafer-Scale；三条路 DSA × Packaging × Novel devices
tags:
- architecture
- moore
- accelerator
- noc
- chiplet
- wse
- photonic
- research
timestamp: '2026-07-13T00:00:00Z'
created: 2026-07-13
sources:
- raw/articles/arch-study-30d-day-29.md
---

# Post-Moore Architecture Frontiers（后摩尔体系结构前沿）

arch-study **研究篇 Day 29**：经典（H&P）之后，**单核主频、单芯片面积、单节点带宽**不再按比例扩展时，研究赌注压在哪里。

**Source:** [raw/articles/arch-study-30d-day-29.md](raw/articles/arch-study-30d-day-29.md)

## 为何「后摩尔」

时间线直觉：Dennard 失效 → 主频墙 → 多核 → Amdahl 墙 → **DSA** → **memory wall**。

物理约束量级：~2 nm 隧穿、~100 W/cm² 功耗密度、~5 GHz 传播、~800 mm² 光罩/良率、引脚限制的片外带宽。固定功耗下 `Perf ∝ 1/(αCV²)` → V 触底后必须换路径。

见 [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md)、[DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)。

## 主题 A：AI 加速器

| 趋势 | 要点 |
|------|------|
| **稀疏** | 跳过零；Sparse Tensor Core / WSE SLA |
| **混合精度** | 训练 BF16+FP32；推理 INT8/4、FP4/6 |
| **软硬协同** | FlashAttention、PagedAttention |
| **训练 vs 推理** | 训练偏算力；推理偏带宽/延迟（WSE/Groq） |

数据复用 WS/OS/RS 见 [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md)。

## 主题 B：NoC 新方向

| 流派 | 思想 |
|------|------|
| **可重构拓扑** | TopoGen / DART 等按负载加长边或改拓扑 |
| **光互连** | 波导/波长；CPO；电光转换代价 |
| **Demand-aware** | 流量驱动路由/拓扑（DC → 片上） |
| **近数据 / PIM** | HBM-PIM、CIM Mesh 减搬运 |

经典底座：[Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)、[Adaptive Routing](/concepts/adaptive-routing-noc.md)。

## 主题 C：Chiplet vs 单片

- **UCIe** 等标准；成本模型（Chiplet Actuary）  
- **CPO** 算力 + 光共封装  
- 对照：小 die 良率 vs [WSE](/entities/cerebras-wse.md) 整晶圆容错  

> 3D / 2.5D 工艺路线细节（TSV / Monolithic / Hybrid Bonding 三路线对 3D NoC 设计的根本含义）见 [Through-Silicon Via Physical Layer](/concepts/tsv-3d-physical-layer.md) 与 [3D Stacking Technologies](/concepts/3d-stacking-technologies.md)。

## 主题 D：Wafer-Scale 未来

- 单 wafer 极限 → **Rack-Scale / 多 wafer fabric**  
- 集体通信：[WSE Reduce](/concepts/wse-reduce-algorithms.md)、[WaferLLM](/concepts/waferllm-system.md)  
- 片上充裕 vs 片外瓶颈：[WSE Quantitative Analysis](/concepts/wse-quantitative-architecture-analysis.md)

## 三条路（收束）

```
(1) 领域专用化 DSA     — 砍通用性换 Perf/W
(2) 封装创新 Packaging — Chiplet / 2.5D / 3D / CPO
(3) 新型器件 Novel     — 光、存算一体、新存储
```

批判框架：每条路的 **核心优势 vs 根本局限**（工艺成熟度、软件栈、可扩展性、良率）。

## 相关页面

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — Day 27
- [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md) — Day 28
- [Arch-Study 30d Knowledge Map](/summaries/arch-study-30d-knowledge-map.md) — Day 30
- [TPU v4 OCS Reconfigurable Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) — 工业光可重构
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 胖链路固定拓扑
- [Cerebras WSE](/entities/cerebras-wse.md) / [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md)

# Citations

[1] [raw/articles/arch-study-30d-day-29.md](raw/articles/arch-study-30d-day-29.md) — 后摩尔四主题综述（Day 29）
