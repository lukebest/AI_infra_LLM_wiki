---
type: Summary
title: 'SpaDA: A Spatial Dataflow Architecture Programming Language'
description: 空间数据流语言 place/dataflow/compute + GT4Py→CSL 优化编译；WSE-2 14× 减码、collective 1.04× 手写 CSL、260 TFlop/s stencil、82× GEMV vs A100
tags:
- cerebras
- wse
- compiler
- dataflow
- hpc
- stencil
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf
---

# SpaDA: A Spatial Dataflow Architecture Programming Language

**Authors:** Lukas Gianinazzi⋆, Tal Ben-Nun⋆, Torsten Hoefler | **Affiliations:** Noeda Research; LLNL; ETH Zurich | **PDF:** [raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf](raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf) | **arXiv:** 2511.09447v2

## 一句话总结

SpaDA 用 **place / dataflow / compute** 三构造 + **async/await** 抽象 WSE 的 color 路由与 task 调度，经 checkerboard 路由、task fusion/recycling、copy elimination 等 pass 降至 CSL，在 WSE-2 上以 **14× 更少代码**实现接近手写 collective（1.04×）、**260 TFlop/s** stencil 与 **82× GEMV** vs A100。

## 核心贡献

1. **语言设计**：显式 PE 网格数据放置、relative_stream 通信、phase + meta-for 结构化异步
2. **GT4Py 前端**：Stencil IR 解耦 domain 语义与 spatial codegen（CSCS/MeteoSwiss 生产 DSL）
3. **CSL backend**：自动 routing（checkerboard）、task graph 优化、DSD 向量化、memory/I/O mapping
4. **WSE-2 评测**：Collectives / Stencil / GEMV 三类，对比 HPDC'24 手写 CSL 与 A100 baseline

## 语言要点

```text
place   →  PE 子网格上 f32[K] 等局部存储
dataflow → relative_stream(dx,dy) 声明有向流（可 multicast）
compute → await send/receive/foreach；completion 依赖管理
phase   → 本地顺序 scope；跨 PE 异步推进
```

Tree reduce 示例（Figure 1a）：meta-for 每 stage 一 phase，`relative_stream(-(1<<stage), 0)` 构建二叉归约树。

## 编译优化（相对 raw CSL）

| Pass | 效果 |
|------|------|
| Checkerboard decomposition | 单跳 stream 无 color 冲突 |
| Task fusion + recycling | tree-reduce 等大 kernel 可编译；task 利用率最高 **2×** |
| Copy elimination | PE SRAM 占用最高 **−50%** |

## 实验摘要

| Kernel | SpaDA vs baseline |
|--------|-------------------|
| 2D Reduce (Chain/Tree/Two-Phase) | **1.04×** vs Luczynski HPDC'24 CSL（harmonic mean） |
| 1D Broadcast | 30–100% overhead vs 手写 |
| UVBKE stencil (746×990×80) | **>260 TFlop/s**；vs A100 GT4Py **400×+**；**4.5×** perf/W |
| GEMV (1.5D partitioned) | **82.9×** vs CUBLAS A100；Two-Phase **1.9×** vs Chain |

**代码量（Table II harmonic mean）：** SpaDA/CSL = **14.09×**；GT4Py Laplacian → CSL = **616×**。

## 与 wiki 交叉引用

- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 机制与编译管线
- [Cerebras WSE](/entities/cerebras-wse.md) — 目标硬件
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — collective baseline 论文
- [Deterministic Execution](/concepts/deterministic-execution.md) — 编译时 spatial 编排范式
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — Triton/Helion scale-out planning（Tenstorrent；对照 WSE SpaDA）

# Citations

[1] [raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf](raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf) — Gianinazzi et al. (2026)
