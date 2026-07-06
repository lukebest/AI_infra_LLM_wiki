---
type: Concept
title: TileLoom Compiler
description: NUS TileLoom：MLIR 端到端 dataflow planning，Triton/Helion → spatiotemporal mapping + df 硬件模型；Tenstorrent 2-D mesh 上 FlashAttention ~2× TTNN
tags:
- compiler
- dataflow
- mlir
- triton
- tenstorrent
- noc
- spatial-accelerator
- attention
timestamp: '2026-07-06T00:00:00Z'
created: 2026-07-06
sources:
- raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf
---

# TileLoom Compiler

**TileLoom**（Li et al., arXiv 2512.22168, 2026）面向 **空间数据流加速器**（Tenstorrent Wormhole/Blackhole、Cerebras、Graphcore 等）的 **MLIR 编译框架**：在 **tile-based DSL**（Triton、Helion）之上自动做 **scale-out dataflow planning**——决定 tile 实例如何映射到 2-D mesh core、如何利用 NoC/分布式 scratchpad 复用数据，而非仅优化单 core 内 tile 代码。

**Authors:** Wei Li, Zhenyu Bai, et al. (NUS) | **arXiv:** [2512.22168](https://arxiv.org/abs/2512.22168) | **Code:** https://github.com/ecolab-nus/loom-dataflow

## 为何需要 TileLoom

| 层次 | GPU 习惯 | 空间 dataflow |
|------|----------|---------------|
| 单 tile 内 | CUDA/Triton 编译器 | Triton/Helion 已覆盖 |
| **跨 core 分布** | 硬件 scheduler + L2 | **编译器/placement 必须显式** |
| 失败模式 | SM 空闲 | NoC 拥塞、DRAM 重复读、core 空转 |

Vendor 库（如 TTNN）性能好但**不可移植、难定制**；TileLoom 把 mapping 决策 **compile-time 化**并 **参数化硬件**（df dialect）。

## 三阶段管线

```
Triton / Helion (tile shape autotune)
    ↓  triton-shared / Helion lowering + affinization
Dataflow-agnostic MLIR  (affine + linalg + scf + arith)
    ↓  spatiotemporal mapping · reuse · broadcast · capacity
Dataflow-aware MLIR
    ↓  performance model (top-k) · optional HW profile
TT-Metalium per-core executable
```

**df dialect** 描述 scale-out（mesh 拓扑、NoC、DRAM）与 scale-in（matrix/vector 吞吐），供 mapping pass 与 analytical model 共用。

## Spatiotemporal mapping

原始 `grid_dim_x/y/z` 等 parallel 维可：

1. **Spatialize** → 绑定 mesh 索引（如 8×8 core），引入 outer `affine.parallel`
2. **Temporalize** → 剩余维变为 wave 循环（`affine.for`），分批占用 core 阵列
3. **Tiling 顺序** → 影响 spatial layout 与 NoC traffic

**Reuse analysis**：对每个 affine 访问，区分 purely intra-core vs 需 inter-core 通信；可插入 **1D/ND broadcast** 降 global load。

**Selection**：performance model 排名 top-k → 可选真机 profile 修正模型误差（专有微架构细节不全时）。

## Tenstorrent 评测摘要

| vs TTNN | Wormhole 8×8 | Blackhole 12×10 |
|---------|--------------|-----------------|
| FlashAttention | **~1.94×** | **~1.98×** |
| GEMM | 0.95× | **1.10×** |
| Flash Decode | ~0.85× | ~0.87× |
| Mamba Chunk Scan | **27×** (unfused) | **16×** |

FlashAttention 增益来自 **K/V tile 跨 Q/V wave 复用**；GEMM 在 compute-bound Wormhole 上接近 vendor ceiling；Blackhole 更高 FP16/DRAM 比使 dataflow 优化更值钱。

## 与 SpaDA / Plasticine / TileLang 区分

| | TileLoom | [SpaDA](/concepts/spada-programming-language.md) | [Plasticine](/concepts/plasticine-accelerator.md) |
|--|----------|------------------|---------------------|
| **输入** | Triton/Helion | GT4Py / SpaDA IR | DHDL parallel patterns |
| **Target** | Tenstorrent（实证） | Cerebras WSE / CSL | 可重构 CGRA |
| **规划粒度** | **Core + NoC tile 分布** | place/stream + color/task | PE + network co-design |
| **硬件假设** | Intra-core 固定 | 电路交换 mesh + color | 合成 overlay |

**注意**：论文引用的 tile DSL 生态含 Triton、[TileLang [66]](https://arxiv.org/abs/2504.12984) 等；与 wiki 中 DeepSeek **[TileLang DSL](/concepts/tilelang.md)**（V4 kernel 开发）是**不同项目**，勿混淆。

## 与 WSE / NoC 研究

- Tenstorrent 与 [Cerebras WSE](/entities/cerebras-wse.md) 同属 **2-D mesh + local scratchpad + packet NoC**（见 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)）
- TileLoom 的 **df 性能模型 + placement search** 可类比 WSE 上 **SME/SpaDA placement**——但 TileLoom 从 **Triton 语义** 出发，SpaDA 从 **stream/async** 出发
- FlashAttention mapping 与 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) 中 KV/带宽 bound 一致：降 DRAM 重复读是 scale-out 主杠杆

## 相关页面

- [papers/tileloom-automatic-dataflow-planning.md](/papers/tileloom-automatic-dataflow-planning.md) — 论文 digest
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE spatial 编译对照
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — ML tile mesh collective 扩展
- [Deterministic Execution](/concepts/deterministic-execution.md) — 编译期 spatial 编排范式
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — Spatial/PE 级 co-design 文献线
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 显式 dataflow vs cache

# Citations

[1] [raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf](raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf) — Li et al. (2026)
[2] [raw/papers/tileloom-automatic-dataflow-planning.md](raw/papers/tileloom-automatic-dataflow-planning.md) — OKF raw digest
