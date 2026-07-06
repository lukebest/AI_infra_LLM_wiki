---
type: Concept
title: SpaDA Programming Language
description: 空间数据流编程语言：place/dataflow/compute 三构造、async/await、GT4Py→CSL 编译管线与 checkerboard 路由/task 融合优化，WSE-2 上 14× 减码、260 TFlop/s stencil
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

# SpaDA Programming Language

**SpaDA**（Spatial Dataflow Abstraction）是面向 [Cerebras WSE](/entities/cerebras-wse.md) 等空间数据流架构（SDA）的高级编程语言与编译 IR：无共享内存、电路交换 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) NoC、[Color 虚拟通道](/concepts/cerebras-color-mechanism.md) 与异步 task 驱动执行——抽象 CSL 低层细节，同时保留对数据放置与通信结构的显式控制。数据流执行模型谱系见 [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md)（Dennis & Misunas, 1975）。

**Authors:** Lukas Gianinazzi, Tal Ben-Nun, Torsten Hoefler | **arXiv:** [2511.09447](https://arxiv.org/abs/2511.09447) (v2, Apr 2026) | **Code:** https://github.com/spcl/spada/

## 为何需要 SpaDA

CSL 编程需同时编排：

| 硬件机制 | 约束 | CSL 痛点 |
|----------|------|----------|
| **电路交换 NoC** | 每 PE ~24+8 **Color**（虚拟通道） | 并发流须 distinct channel，否则 nondeterministic |
| **异步 task** | 每 PE ≤28 **task ID**（与 color 竞争） | 手写 state machine、task 自阻塞、DSD 寄存器复用 |
| **DSD 向量化** | `@fadd`/`@fmac` 等须 DSD 描述 | 标量 loop 无法峰值利用 |

厂商 25-point stencil 示例 **887 行 CSL**；2D Laplacian GT4Py **4 行 → ~2464 行 CSL**（616× 膨胀）。

## 语言三构造

| 构造 | 作用 | 示例 |
|------|------|------|
| **place** | PE 网格上数据分配 | `place i,j in [0:I, 0:J] { f32[K] loc; }` |
| **dataflow** | 相对偏移通信流 | `stream<f32> w = relative_stream(-1, 0)` |
| **compute** | async/await 数据驱动计算 | `await foreach k, x in receive(w) { loc[k]+=x; }` |

**phase**：PE 本地顺序、跨 PE 异步推进；meta `for` 展开为多 phase（如 tree reduce 每 stage 一 phase）。

**relative_stream(dx, dy)**：发送 (i,j)→(i+dx,j+dy)；接收方向自动反转，支持 pipelined chain。

## 编译管线（GT4Py → SpaDA → CSL）

```
GT4Py Stencil IR → SpaDA → Canonicalization → Routing (checkerboard)
  → Task graph (fusion + recycling) → DSD vectorization → CSL + layout
```

| Pass | 功能 |
|------|------|
| **Checkerboard routing** | 按 PE 奇偶拆分 stream，单跳无路由冲突；自动 color 分配 |
| **Task fusion / recycling** | 合并 post/wait DAG → CSL task；greedy coloring 复用 task ID |
| **Copy elimination** | 消除 48KB SRAM 上的 staging buffer |
| **DSD vectorization** | `map`/`foreach` → `@fmac`/`@mov`；失败则 `@map` callback 或 scalar fallback |

Tree reduce **无 task 优化无法编译**——SpaDA 让 async/await 语义与硬件资源约束解耦。

## 性能与生产力（WSE-2, SDK 1.4.0）

| 类别 | 结果 |
|------|------|
| **代码量** | SpaDA vs 手写 CSL：**4.68–13.13×** 更少；GT4Py→CSL 最高 **616×**（harmonic mean **14.09×**） |
| **Collectives** | Chain/Tree/Two-Phase Reduce vs HPDC'24 手写 CSL：harmonic mean **1.04×** 慢 |
| **Stencil** | UVBKE 天气核 **>260 TFlop/s**（746×990×80，~730K PE）；vs A100 GT4Py **400×+** |
| **GEMV** | 1.5D partitioned + collectives vs CUBLAS A100：**82.9×**；Two-Phase vs Chain **1.9×** |
| **能效** | UVBKE stencil **4.5×** perf/W vs A100 |

## 与 wiki 概念的关系

- [Deterministic Execution](/concepts/deterministic-execution.md) — 编译时确定 placement/routing/task，运行时零动态调度
- [Cache Coherence](/concepts/cache-coherence.md) — SDA 无共享地址空间，SpaDA 显式 stream 替代 MESI
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — SpaDA 复用/对比 Luczynski HPDC'24 near-optimal collectives
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — relative_stream 在 2-D mesh 上路由

SpaDA 同时是**通用 SDA 语言**与 **DSL IR**——架构无关的语言设计，当前 backend 专 targeting WSE/CSL。DNN 片上 buffer 的 dataflow-layout 可重构见 [FEATHER Accelerator](/concepts/feather-accelerator.md)。**Parallel patterns** 驱动的 CGRA 见 [Plasticine Accelerator](/concepts/plasticine-accelerator.md)（ISCA 2017，DHDL → PCU/PMU 映射）。

## 相关页面

- [Cerebras WSE](/entities/cerebras-wse.md) — 730K–900K PE、48KB SRAM、CSL 生态
- [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) — checkerboard pass 分配的 color 资源
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 数据流 vs 通用 CPU 编程模型
- [papers/spada-spatial-dataflow-architecture.md](/papers/spada-spatial-dataflow-architecture.md) — 论文摘要
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — parallel patterns 抽象的另一实现路径
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — Triton/Helion → Tenstorrent scale-out dataflow planning（对照 WSE placement）
- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — 分布式 GEMM 算法与 T10 rTensor 对照

# Citations

[1] [raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf](raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf) — Gianinazzi et al. (2026), arXiv:2511.09447
