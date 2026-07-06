---
type: Summary
title: 'TileLoom: Automatic Dataflow Planning for Tile-Based Languages'
description: MLIR 编译框架：Triton/Helion → spatiotemporal dataflow planning + df 硬件模型；Tenstorrent Wormhole/Blackhole 上 FlashAttention ~2× TTNN、Mamba Scan 最高 27× unfused
tags:
- compiler
- dataflow
- mlir
- triton
- tenstorrent
- noc
- spatial-accelerator
timestamp: '2026-07-06T00:00:00Z'
created: 2026-07-06
sources:
- raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf
---

# TileLoom: Automatic Dataflow Planning for Tile-Based Languages on Spatial Dataflow Accelerators

**Authors:** Wei Li, Zhenyu Bai, Heru Wang, et al. (NUS + ASU/Google + Lumai) | **arXiv:** [2512.22168v2](https://arxiv.org/abs/2512.22168) (May 2026) | **PDF:** [raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf](raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf) | **Code:** https://github.com/ecolab-nus/loom-dataflow

## 一句话总结

TileLoom 是 **MLIR 端到端编译器**：把 **Triton/Helion tile kernel** 降到 **dataflow-agnostic MLIR**，经 **spatiotemporal mapping + reuse/broadcast 分析 + df dialect 性能模型** 生成 **dataflow-aware IR**，再降至 **TT-Metalium**；在 Tenstorrent **Wormhole/Blackhole** 上 **FlashAttention ~2× TTNN**、**GEMM 0.95–1.10×** 高度优化 vendor 库、**Mamba Chunk Scan 10×–55×** unfused baseline。

## 核心贡献

1. **Scale-out dataflow planning**：在固定 per-core 微架构下，搜索 tile 在 2-D mesh 上的时空分布（GPU 上由 runtime/scheduler 做的事前移到编译期）
2. **df MLIR dialect**：编码 interconnect、分层 memory、core 算力 → 可移植 performance model + mapping pass
3. **Dataflow-agnostic → aware IR 管线**：affine/linalg 统一前端；broadcast/ reuse 注解；top-k 模型筛选 + 可选真机 profile
4. **Tenstorrent 实证**：两世代 card；对比 **TTNN** vendor 库与 unfused 实现

## 编译栈

| 阶段 | 输入/输出 |
|------|-----------|
| Front-end | Triton (triton-shared + affinization) / Helion Device IR → **dataflow-agnostic MLIR** |
| Planning | 枚举 spatial/temporal tiling；reuse + broadcast；capacity prune |
| Model | df.interconnects + compute/memory 成本 → **top-k** mappings |
| Back-end | dataflow-aware MLIR → lifetime → **TT-Metalium** → per-core executable |

**设计空间三轴**：(1) parallel dim → 0+ spatial dims；(2) 多 spatial dim 的 tiling 顺序；(3) 剩余 dim → temporal wave 顺序。

## 关键数字（Table 2，geo mean vs TTNN）

| Kernel | TT-Wormhole | TT-Blackhole |
|--------|-------------|--------------|
| FlashAttention | **1.94×** | **1.98×** |
| Flash Decode | 0.84× | 0.87× |
| GEMM | 0.95× | **1.10×** |
| Mamba Chunk Scan (unfused) | **27.23×** | **16.27×** |

- FlashAttention：**1.88–2.06×**（KV tile reuse 降 DRAM traffic）
- Flash Decode：**~85%** TTNN（query len=1，mapping 空间小；vendor 特化强）
- GEMM：Wormhole compute-bound → 降 traffic 收益有限；Blackhole 更高算力/带宽比 → **1.10×**

**硬件（Table 1）**：Wormhole 8×8 core、108 MB SRAM、288 GB/s DRAM、64 TFLOPS FP16；Blackhole 12×10、180 MB SRAM、512 GB/s、162 TFLOPS FP16。

## 与 wiki 交叉引用

- [TileLoom Compiler](/concepts/tileloom-compiler.md) — 机制与对比 SpaDA/Plasticine
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 侧 spatial DSL + placement（不同 target）
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Tenstorrent 2-D mesh 目标拓扑
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 2-D tile mesh 加速器谱系
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — PE 级 co-design 对照
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 显式 dataflow vs cache hierarchy

# Citations

[1] [raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf](raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf) — Li et al. (2026)
