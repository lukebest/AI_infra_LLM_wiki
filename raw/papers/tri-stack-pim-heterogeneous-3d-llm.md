---
type: Raw Source
title: "Tri-Stack-PIM: A Heterogeneous Multi-Die 3D-Integrated Processing-in-Memory Architecture for Efficient LLM Inference"
source_url: https://arxiv.org/abs/2611.13644
pdf: Tri_Stack_PIM_3D_LLM_Inference_2026.pdf
retrieved: 2026-11-12
ingested: 2026-11-12
org: Beijing University of Posts and Telecommunications / Fudan University
venue: ICCAD 2026
---

# Abstract (verbatim gist, arXiv:2611.13644)

Large language model (LLM) inference during autoregressive decoding is fundamentally memory-bandwidth-bound. Existing three-dimensional (3D) stacked processing-in-memory (PIM) architectures alleviate the off-chip bandwidth wall, yet remain constrained by several limitations: physical layer (PHY), controllers, and direct memory access (DMA) engines compete with arithmetic units for advanced-node base-die area; hybrid-bonding keep-out zones fragment the base-die floorplan and impede physical design; compute tiles built in a dynamic random access memory (DRAM) process are restricted to low logic density, capping achievable throughput; and nonlinear operations offloaded to the host reintroduce a communication bottleneck. We present Tri-Stack-PIM, a heterogeneous three-die architecture that resolves these tensions by dedicating a top DRAM die to storage, a middle buffer die on a mature process node to PHYs, DMA engines, and near-memory compute units, and a bottom base die on an advanced node exclusively to single-instruction-multiple-data (SIMD) multiply-accumulate (MAC) arrays. We further introduce a Unified Buffer-Aware Ready-based (UBAR) hardware out-of-order micro-operation scheduler that enforces cross-die dependency correctness at runtime while maximizing issue-slot utilization through a multi-term priority function, recovering up to 90% of the cycles that an in-order policy would forfeit. A joint architecture-dataflow co-exploration identifies Pareto-optimal configurations that reduce the energy-delay product (EDP) by 33-66× over naïve parameter selection. Evaluated across multi-head, grouped-query, and multi-query attention (MHA, GQA, MQA) mechanisms with batch sizes 1-32, Tri-Stack-PIM achieves geometric-mean speedups of 4.95×, 2.57×, and 1.68× across all three attention mechanisms and batch sizes over a graphics processing unit (GPU) baseline, AttAcc, and H2-LLM, respectively.

# Excerpts / key facts

- Authors: Shuao Jia, Zichao Ling, Kang Zhao, Jianwang Zhai*（BUPT）；Chen Bai（Fudan）。*Corresponding。ICCAD ’26，2026-11-08–12，San Jose；ACM ISBN 979-8-4007-2873-0/2026/11；doi 10.1145/3831252.3834022。arXiv:2611.13644，cs.AR。
- 三层混合键合：顶层 DRAM 存储；中层成熟节点 buffer die 承担 host PHY、DMA、近存计算（含非线性）与 UBAR 调度；底层先进节点 base die 专给 SIMD MAC。把 PHY/控制从先进节点搬走，避开 HB keep-out 对计算 floorplan 的切割，并把 softmax 等非 GEMM 留在栈内。
- 评测（§4.1）：OPT-6.7B（MHA 32/32）、LLaMA3-8B（GQA 32/8）、PaLM-8B（MQA 16/1）；batch {1,4,8,16,32}；长度对 (128,64)、(512,256)、(1024,64)、(1024,16)。Base die：ASAP7，0.5–1.5 GHz，16–256 MACs/tile（73.1–4614.5 µm²/block，0.15–41.2 fJ/MAC）。Buffer die SRE：NanGate 45 nm，0.1–1.0 GHz，0.47 mm²，1.1–9.5 pJ/softmax op。HB 链路 0.88 pJ/bit（H2-LLM 模型）。周期精确仿真扩展 Ramulator 2。
- 对照：GPU-Only 为代表性边缘 GPU + 4 通道 LPDDR5X **30.7 GB/s**（不是数据中心 GPU）；AttAcc；H2-LLM。几何均值加速（全部三种 attention × 全部 batch）：相对 GPU **4.95×**、AttAcc **2.57×**、H2-LLM **1.68×**（摘要 / 贡献列表）。
- UBAR 回收 in-order 会放弃的周期最多 **90%**。联合架构–数据流探索相对朴素参数选择把 EDP 降 **33–66×**。7 nm base die 晶圆成本 $9,346、45 nm buffer die $2,000，仅 PHY 一项单位晶圆成本降 **4.7×**。热仿真峰值约 63.74 / 63.75 / 62.63 °C（DRAM / buffer / base）。
