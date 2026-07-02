---
type: Summary
title: 'A Lightweight High-Throughput Collective-Capable NoC for Large-Scale ML Accelerators'
description: FlooNoC 扩展：multicast/归约/barrier + DCA 借 Snitch FPU；router +16.9% 面积，4×4 mesh 上 multicast 5.3×、reduction 2.8×，SUMMA GEMM 最高 3.8×
tags:
- noc
- collective
- multicast
- reduction
- accelerator
- mesh
- gemm
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf
---

# A Lightweight High-Throughput Collective-Capable NoC for Large-Scale ML Accelerators

**Authors:** Luca Colagrande, Lorenzo Leone, Chen Wu, Tim Fischer, Raphael Roth, Luca Benini (ETH Zurich) | **Venue:** MLSys 2026 | **arXiv:** [2603.26438](https://arxiv.org/abs/2603.26438) | **Code:** [FlooNoC v0.8.0](https://github.com/pulp-platform/FlooNoC/releases/tag/v0.8.0), [picobello](https://github.com/pulp-platform/picobello)

## 一句话总结

在开源 FlooNoC + Snitch tile mesh 上，用 **AXI 多地址 mask**、**XY fork 组播**、**并行/宽归约** 与 **Direct Compute Access（互连借 FPU）** 实现片上 collective；router 仅 **+16.9%** 面积，相对高度优化软件基线在 1–32 KiB 传输上 **multicast 5.3× / reduction 2.8×**，SUMMA GEMM 最高 **3.8×**、能效 **1.17×**。

## 核心贡献

1. **Collective-capable NoC**：AXI4 合规；AWUSER 携带 mask + opcode；NI 做 address↔XY mask 翻译
2. **三层归约**：CollectB/SelectAW（AXI 耦合）、LsbAnd（barrier）、wide reduction + **DCA**
3. **DCA 范式**（详见 [Collective-Capable NoC](/concepts/collective-capable-noc.md#direct-compute-access-dca)）：Router offload → 8× Snitch FPU 并行 512b 浮点归约；类比 DMA 直连 memory，DCA 直连 FPU；core 可 idle，full tile <1% 面积
4. **TSMC 7nm 实现**：full collective router +16.9%；full tile **< 1%** 面积增量，1 GHz 无时序退化
5. **建模 + 对比**：对 seq/tree 软件 multicast/reduction 建立解析模型，RTL cycle-accurate 验证

## 关键数字

| 指标 | 值 |
|------|-----|
| Router 面积开销（full collective） | **16.9%** |
| Full tile 面积开销 | **< 1%** |
| Multicast speedup（4×4，1–32 KiB） | **5.3×** geomean |
| Reduction speedup（4×4，1–32 KiB） | **2.8×** geomean |
| Hardware vs software barrier slope | **1.3** vs **3.3** cycles/cluster |
| SUMMA GEMM speedup（256×256 mesh） | **3.8×** |
| FusedConcatLinear reduction speedup | **2.4×** |
| SUMMA 能效（256×256） | **1.17×** |

## DCA 范式（摘要）

**Direct Compute Access**：互连 fabric 直连 cluster FPU 做 wide in-network reduction，无需 core 发指令。Router 仅 2-input merge + sync/hdr buffer；512b beat 拆 8×64b 送各 FPU（8× DP 或 64× FP8/cycle）。相对 seq/tree 软件 reduction **2.8×**；FCL 能效 **1.13×**（少 DMA + core 可 low-power）。完整机制见 [Collective-Capable NoC — DCA](/concepts/collective-capable-noc.md#direct-compute-access-dca)。

## 与 wiki 交叉引用

- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 架构与 DCA 机制
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — Router 微架构基线
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 2-D mesh collective 前提
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — WSE mesh reduce/multicast 对照
- [Cerebras WSE](/entities/cerebras-wse.md) — 晶圆级 mesh collective 另一路径
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — 硬件 barrier 规模分界

# Citations

[1] [raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf](raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf) — Colagrande et al. (2026)
