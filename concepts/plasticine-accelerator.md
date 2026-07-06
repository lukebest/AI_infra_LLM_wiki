---
type: Concept
title: Plasticine Accelerator
description: Stanford ISCA 2017 CGRA：PCU/PMU 空间阵列直接支持 Map/FlatMap/Fold/HashReduce parallel patterns；28nm 112.8mm²、12.3 TFLOPS、相对 FPGA 最高 76.9× Perf/W
tags:
- accelerator
- cgra
- reconfigurable
- dataflow
- parallel-patterns
- compiler
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf
---

# Plasticine Accelerator

**Plasticine**（Stanford, ISCA 2017）是为 **parallel patterns** 专门设计的**粗粒度空间可重构加速器**：用 **Pattern Compute Unit (PCU)** + **Pattern Memory Unit (PMU)** 二维阵列替代 FPGA 的 bit 级可编程互联，在保持高层 **DHDL** 编译（数分钟 vs FPGA 数小时）的同时，对 dense/sparse ML、数据分析、图计算取得相对 Stratix V FPGA 最高 **76.9× Perf/W**。

**Authors:** Prabhakar, Zhang, Koeplinger, Feldman, Zhao, Hadjis, Pedram, Kozyrakis, Olukotun | **Venue:** ISCA 2017 | **Implementation:** Chisel + Synopsys DC/PrimeTime；VCS + DRAMSim2 评估

## 设计动机

| 平台 | 问题 |
|------|------|
| **FPGA** | >60% 面积/功耗在可编程互联；bit 级抽象能效差 |
| **ASIC** | NRE 与迭代成本高 |
| **传统 CGRA** | 低层编程、编译慢、资源异构难映射 |

**Parallel patterns**（Map、FlatMap、Fold、HashReduce）统一表达数据局部性、访存模式与嵌套并行——Plasticine 将 Table 2 中的编程模型需求**硬连线到架构**。

## 编程模型 → 硬件映射

| Pattern | 硬件需求 |
|---------|----------|
| Map / FlatMap | SIMD 流水线 FU；FlatMap 需 cross-lane **valid 字合并** |
| Fold | cross-lane **归约树** |
| HashReduce | 稀疏/稠密 key 累加器 |
| 嵌套 pattern | 可编程 **counter chain** + 分层 control |
| 集合访存 | banked scratchpad、strided/FIFO/line-buffer/duplication 模式 |

示例：GEMM 写为外层 Map(M,P) + 内层 Fold(N) 点积（Figure 1）；TPC-H Q1 风格用 filter(FlatMap) + HashReduce（Figure 2）。

## 架构概览

```
4× DDR ── AG + coalescer ── 16×8 (PCU|PMU) 阵列
              ↑ scalar / vector / control 静态互联
```

### PCU（Pattern Compute Unit）

- 执行**最内层** parallel pattern
- **多段可配置 SIMD 流水线**：32b int/float FU + 流水线寄存器
- **归约树** + **shift network**（stencil 滑动窗口复用）
- Scalar / vector / control IO + 输入 FIFO 解耦 producer/consumer

### PMU（Pattern Memory Unit）

- **Banked scratchpad**（与 PCU lane 数对齐）+ **独立地址计算 datapath**
- 地址逻辑移出 PCU → 避免占用 PCU stage 与输出链路
- Banking：**strided**（线性）、**FIFO**（流式）、**line buffer**（滑窗）、**duplication**（并行 gather 读）
- **N-buffering** 支持 imperfect nest 的粗粒度流水线

### 片外访存

- 每 DDR channel 多 **Address Generator (AG)**：dense burst + sparse gather/scatter
- **Coalescing cache** 合并稀疏地址，多 outstanding 请求

### 控制

三种外层协议：**sequential**（token 同步）、**coarse-grained pipeline**（credit + M-buffer）、**streaming**（FIFO 反压）。外层 controller 映射到 **switch 内 control block**，减轻 PCU 控制热点。

## 规模与能效（28 nm @ 1 GHz）

| 指标 | 值 |
|------|-----|
| 阵列 | **64 PCU + 64 PMU**（16×8，1:1） |
| PCU | 16 SIMD lane × 6 stage × 6 reg/stage |
| PMU | 16×16 KB = **256 KB**/PMU；片上共 **16 MB** |
| 面积 | **112.77 mm²** |
| 峰值 FP32 | **12.3 TFLOPS** |
| 最大功耗 | **49 W** |
| DRAM | 4× DDR3-1600，**51.2 GB/s** |

相对应用专用 ASIC（同性能）面积开销：完全同构 generalized 后 geo-mean **~11×**；可重构异构基线约 **2.8×**。

## 相对 FPGA 与固定 DNN 加速器

| 对比 | Plasticine | Stratix V FPGA | [Eyeriss](/concepts/eyeriss-accelerator.md) |
|------|------------|----------------|---------------------------------------------|
| 抽象 | Parallel patterns + DHDL | RTL/VHDL | 固定 RS CNN dataflow |
| CNN | 95.1× 快（映射为 3D conv PCU） | 基准 | AlexNet 流片 benchmark |
| GEMM | 33× / 24.4× Perf/W | 基准 | 非目标 workload |
| 编译 | **数分钟** | 数小时 | 层间 scan chain |
| 可重构粒度 | 字级 CGRA | Bit 级 | CNN shape 映射参数 |

与 [FEATHER](/concepts/feather-accelerator.md) 同属「可重构换利用率」，但 Plasticine 面向 **general parallel patterns**（含稀疏图），FEATHER 面向 DNN **(dataflow, layout) co-switch**。

## 编译器（DHDL）

Pipeline 层次 → virtual PCU/PMU → 贪心划分 physical unit → 控制层次生成 → placement/routing → 静态 bitstream。Prior work [36] 可从 parallel patterns 自动生成 DHDL；亦曾用于 FPGA [20]。

## 谱系与 wiki 关系

- [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md) — 数据驱动执行历史；Plasticine 为现代 **spatial dataflow + pattern DSL**
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 同为高层 dataflow 抽象；SpaDA 绑 WSE NoC/CSL，Plasticine 绑 PCU/PMU CGRA
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — 固定 core + NoC tile 规划（Timeloop/Plasticine 为 PE 级 co-design）
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 可重构 vs 固定 ASIC 杠杆
- [Deterministic Execution](/concepts/deterministic-execution.md) — 静态配置、可建模延迟

## 相关页面

- [papers/plasticine-reconfigurable-parallel-patterns.md](/papers/plasticine-reconfigurable-parallel-patterns.md) — 论文摘要
- [FEATHER Accelerator](/concepts/feather-accelerator.md) — DNN 可重构 dataflow-layout
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — 固定 CNN dataflow 流片对照

# Citations

[1] [raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf](raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf) — Prabhakar et al., ISCA 2017
