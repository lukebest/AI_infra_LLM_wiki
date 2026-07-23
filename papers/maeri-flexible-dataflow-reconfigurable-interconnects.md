---
type: Summary
title: 'MAERI: Enabling Flexible Dataflow Mapping over DNN Accelerators via Reconfigurable Interconnects'
description: ASPLOS 2018 首个 flexible interconnect DNN 加速器：ART + Distribution Tree + tiny switches；任何 layout/任意 dataflow 都能映射；8-459% 利用率提升
tags:
- accelerator
- dnn
- dataflow
- noc
- flexible
- reconfigurable
- asplos
- kwon
- krishna
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- raw/papers/MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf
---

# MAERI

**Authors:** Hyoukjun Kwon, Ananda Samajdar, Tushar Krishna (Georgia Tech) | **Venue:** ASPLOS 2018 | **PDF:** [raw/papers/MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf](MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf)

## 一句话总结

**MAERI**（Multi-dimensional Array of Reduced Expandable ISA-Like Reconfigurable Interconnects）是 Georgia Tech 的 ASPLOS 2018 加速器：用 **ART 归约树 + Distribution Tree + tiny switches** 让 **任意 layout/任意 dataflow 都能映射到 PE 阵列**，相对 rigid NoC 加速器利用率提升 **8-459%**。**柔性 NoC 在硬件层面解决 layout 适配问题**的开山之作。

## 核心问题

**DNN layer 之间 layout 需求差异巨大**（图 conv、FC、RNN、pooling、稀疏 LSTM），而 **rigid NoC**（如 systolic、Eyeriss 固定 NoC）只能优化某一种流量模式，**其它 pattern 严重欠利用**。

| 维度 | 现状 | MAERI 的解法 |
|------|------|-------------|
| **NoC 拓扑** | 固定（mesh、systolic、tree）| **可重构**（per-layer 切换）|
| **Distribution** | multicast / unicast 固定模式 | **任意模式**（multicast / scatter / gather 自选）|
| **Reduction** | 固定树 | **tree + ART（前向 forwarding）** |
| **Mapping** | 编译器把 model 硬塞进 fabric | **fabric 适配 model** |

## 三大组件

### 1️⃣ Distribution Tree（反向，从 DRAM 到 PE）

- 把 activations / weights **任意 pattern 分发**到任意 PE 集合
- 用 "tiny switches" 控制每条链路通 / 断
- 树形结构：log(N) latency

### 2️⃣ ART（Augmented Reduction Tree，前向）

- 收集 partial sums
- **前向 forwarding adder network**：中间节点可以把 partial sum 转发给下游节点 → 减少 critical path
- 替代 Eyeriss 的固定 reduction tree

### 3️⃣ PE 阵列 + tiny switches

- 任何 PE 之间都可以被 switches **重新连接**
- 编译器根据 layer 类型，**编译期**配置 switches → 每个 layer 一套连接
- **不是 runtime 重连**——但**编译器**做了相当于 runtime 的事情

## 数字

- **8-459% utilization improvement** vs rigid baselines（Eyeriss-like / systolic）
- +6.5% power overhead vs Eyeriss
- +47% area vs systolic, +49% throughput
- 覆盖：AlexNet, VGG, ResNet, GoogLeNet, RNN, sparse LSTM

## 与 FEATHER 的关系

| | MAERI (2018) | FEATHER (2024) |
|---|--------------|----------------|
| **interconnect 形态** | distribution + reduction tree | **BIRRD butterfly**（更通用）|
| **layout 重排能力** | 任意分发，但归约后是固定 layout | **RIR（归约中重排）→ 任意 layout** |
| **可重构粒度** | 编译期 | **编译期** |
| **layout 转换** | **显式（RAR）** | **隐式（RIR，节省 critical path）**|

**FEATHER 是 MAERI 的继承者**：在归约树里加入 reorder capability，**消除了"reorder after reduction" 的 critical path**。

## 与 wiki 已有内容的关联

- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 直接 successor，RIR 思想从 MAERI 的 switch 扩展而来
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — rigid 对比基线
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — 同期 CGRA 路线
- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — 通用 distributed GEMM 视角
- [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — MAERI 关注 dense GEMM，decode 是 GEMV

# Citations

[1] [raw/papers/MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf](raw/papers/MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf) — Kwon et al. ASPLOS 2018