---
type: Summary
title: 'HyperMR: Efficient Hypergraph-enhanced Matrix Storage on Compute-in-Memory Architecture'
description: SIGMOD 2025 — CIM 矩阵存储超图建模 + 两阶段划分，优化通信/累加成本；100% 矩阵有效优化，合成查询 +29.65%
tags:
- memory
- accelerator
- hardware
- sparse
- optimization
- kernel
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/HyperMR_Hypergraph_Matrix_Storage_CIM_2025.pdf
---

# HyperMR: Efficient Hypergraph-enhanced Matrix Storage on Compute-in-Memory Architecture

**Proc. ACM Manag. Data (SIGMOD) 2025** | DOI [10.1145/3709695](https://doi.org/10.1145/3709695)  
Wu, Chen, Chen, Jiang, Li, Shou（浙江大学）

为 **Compute-in-Memory (CIM)** crossbar 阵列设计矩阵 tile 布局：用超图统一建模矩阵结构与访问模式，优化 MVM 的**通信成本**（列序决定 input vector 分发）和**累加成本**。

## 核心贡献

1. **两个 CIM 专用优化目标**（NP-hard）+ 访问感知超图生成
2. **两阶段超图划分**：不依赖对称/对角块等结构假设
3. **全面优于 SOTA reorder 方案**（GSMR、METIS、GMR、ReSpar 等局限）

## 关键数字

| 指标 | 值 |
|------|-----|
| 有效优化矩阵比例 | **100%** vs baseline **75%** |
| 合成查询 | **+29.65%** |
| 科学图像滤波 | 最高 **+34.9%** |

## 与 wiki 交叉

- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 加速器内存布局优化对照
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 存储布局与数据移动

# Citations

[1] [raw/papers/HyperMR_Hypergraph_Matrix_Storage_CIM_2025.pdf](raw/papers/HyperMR_Hypergraph_Matrix_Storage_CIM_2025.pdf)
[2] [raw/papers/hypermr-hypergraph-matrix-storage-cim.md](raw/papers/hypermr-hypergraph-matrix-storage-cim.md) — 结构化摘录
