---
type: Summary
title: 分布式存储架构下的矩阵乘与编译器
description: 知乎综述：Cannon/SUMMA/2.5D/3D 分布式 GEMM（MPI 实现+αβ 分析）、LLM Tesseract/NUS 3D 并行、Graphcore T10 rTensor 形式化 Cannon
tags:
- gemm
- distributed-memory
- mpi
- compiler
- tensor-parallelism
- zhihu
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/articles/分布式存储架构下的矩阵乘与编译器.md
---

# 分布式存储架构下的矩阵乘与编译器

**Author:** 郑启航 | **Source:** [知乎专栏](https://zhuanlan.zhihu.com/p/6906641426) | **Raw:** [raw/articles/分布式存储架构下的矩阵乘与编译器.md](raw/articles/分布式存储架构下的矩阵乘与编译器.md)

## 一句话总结

从 **SBP 张量切分** 的局限出发，逐篇实现并 profiling **Cannon、SUMMA、3D SUMMA、2.5D SUMMA**（mpi4py + viztracer），给出 **α–β 通信下界**；延伸到 LLM **Tesseract / NUS 3D** 并行，并解析 Graphcore **T10 rTensor** 如何 **形式化 Cannon**（空间/时间切分 + ring 旋转 + 全局 align）。

## 章节要点

| 节 | 内容 |
|----|------|
| §1 TP 切分 | 1D/2D SBP；总有一维不可切 → 内存高 |
| §2 Cannon | 2D mesh、ring shift、align；Cost ∝ 2(√P−1)(α+n²/P β) |
| §3 SUMMA | broadcast 外积；非方阵网格 |
| §4 3D SUMMA | p³ 拓扑；Allgather+Alltoall；少传 P^(1/6) |
| §5 2.5D | p×p×d；d 调节通信 vs A/B 复制 |
| §6 LLM | Tesseract（切 A 降内存）；NUS 3D 变体 |
| §7 T10 | rTensor；missing axis 时间切分；= Cannon 编译器版 |
| §8 Flame | 切分状态形式化；Stationary C/A |

## 实测配置（文中 profiling）

矩阵 **M:11520, K:7680, N:12288**；Cannon/SUMMA **9 进程** (3×3)，3D **8 进程** (2³)，2.5D **18 进程** (3×3×2)。

## 与 wiki 交叉引用

- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — 结构化概念页
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 2D 处理器网格
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — LLM 并行策略
- [Graphcore IPU](/entities/graphcore-ipu.md) — T10 目标硬件
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 另一空间数据流编译栈

# Citations

[1] [raw/articles/分布式存储架构下的矩阵乘与编译器.md](raw/articles/分布式存储架构下的矩阵乘与编译器.md) — 郑启航 (2024)
