---
type: Paper
title: "Entwine: Tiled Computation and Fine-Grained GPU Communication"
description: 中科院 — tile 顺序×细粒度 SM 通信×资源预算；GEMM–RS vs cuBLAS+NCCL geomean 1.232×（最高 1.433×），vs SOTA overlap +3.1–9.8%
tags:
- gpu
- communication
- collective
- parallelism
- interconnect
- fabric
- throughput
- latency
- distributed
- nvidia
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/papers/Entwine_Tiled_Computation_Fine_Grained_GPU_Comm_2026.pdf
- raw/papers/entwine-tiled-computation-fine-grained-gpu-comm.md
---

# Entwine: Coordinating Tiled Computation and Fine-Grained Communication across GPUs

**Authors:** Kai Ma, Quanfeng Lv, Jingguo Ge, Bowei Dai, Kefan Ruan  
**Affiliation:** 中科院信息工程研究所 / 国科大 / 中科院微电子所  
**arXiv:** [2609.11562](https://arxiv.org/abs/2609.11562)（2026-09-10，cs.DC；列表 cross cs.AR）  
**Venue:** 预印本。  
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.11562)

相对 [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) 谈域规模上的 barrier τ，Entwine 卡在 **单 NVLink 节点内** GEMM tile 产出节奏与 ReduceScatter 消费节奏的匹配，以及通信核抢 SM 的副作用。

## 动机

高性能 GEMM 按 tile 完成，本可边算边传；但（1）通信可能无数据可发或突发堆积，（2）通信核占用 SM/带宽会拖慢 GEMM，抵消 overlap。FlashOverlap / Async-TP / FLUX / CoCoNet 等已做分解与融合，但 tile 顺序、释放粒度与资源预算未系统联合。

## 方案

面向 **GEMM–ReduceScatter**（TP 常见）：

1. **交错 tile 产出顺序**，让各目的 GPU 的贡献更均匀到达。
2. **细粒度 SM 通信核** 低延迟消费已完成 tile（非整波次才启动）。
3. **通信预算 / SM 分配** 与 GEMM 配置一起按端到端延迟离线选型，避免「通信越猛、总时间反而更差」。

测试床：单节点 2/4/8× **A800-SXM4-80GB**（默认 8），CUDA 12.1 / NCCL 2.21.5；主套件含 Llama 3 70B / 3.1 405B 宽度等。

## 效果（仅论文数字）

- vs 顺序 cuBLAS+NCCL：geomean **1.232×**，最高 **1.433×**。
- vs SOTA overlap 基线：geomean 再高 **3.1–9.8%**。
- 文示顺序执行上通信暴露可占端到端 **11.0–40.2%**。

## 与 wiki 概念的关系

- [LLM Collectives](/concepts/llm-distributed-training-collectives.md) — TP 路径上 GEMM–RS 的 tile 级重叠工程。
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 单节点 NVLink 域内细粒度通信，不是跨 IB 的 scale-out。
- [REACT](/papers/react-tuning-collective-patterns-shared-clusters.md) — 集群拥塞改写集体；本文是算子内 tile/SM 协同。

## 开放问题

1. 多节点 / 跨 NVLink 域（NCCL 树/环混合）时，tile 协议如何切段？
2. 与 FlashMoE / DeepEP 类 MoE 集体叠加时，SM 预算怎么分？
3. 动态形状（变长 batch）下离线选型是否仍稳？

# Related

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md)
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md)
- [REACT](/papers/react-tuning-collective-patterns-shared-clusters.md)
- [BASP](/papers/basp-batch-aware-sequence-parallelism.md)

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.11562) — Ma et al., arXiv:2609.11562  
[2] [raw/papers/entwine-tiled-computation-fine-grained-gpu-comm.md](raw/papers/entwine-tiled-computation-fine-grained-gpu-comm.md) — ingest stub
