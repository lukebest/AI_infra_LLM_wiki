---
type: Summary
title: Optimizing the Parallelism of Communication and Computation in Distributed Training Platform
description: ICA3PP 2023 — Torus-Ring 分层训练平台上重叠通信与计算，ResNet50 +23.8–25.6%，Transformer +11.7–12.8%
tags:
- training
- training-system
- parallelism
- communication
- optimization
- benchmark
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Optimizing_Comm_Comp_Parallelism_Distributed_Training_2024.pdf
---

# Optimizing the Parallelism of Communication and Computation in Distributed Training Platform

**ICA3PP 2023** (LNCS 14487) | DOI [10.1007/978-981-97-0834-5_20](https://doi.org/10.1007/978-981-97-0834-5_20)  
Hou, Yuan, Ma, Xu, Wang, et al.（国防科技大学）

在 **hierarchical Torus-Ring** 分布式训练平台上，通过调度重叠计算与 collective 通信，分别削减 data parallelism 的**通信暴露**和 model parallelism 的**计算暴露**。

## 核心贡献

1. **Data parallelism**：weight-gradient Ring AllReduce 与 activation 计算并行
2. **Model parallelism**：activation AllGather 与 weight-gradient 计算并行
3. **基于 Ring All-Reduce** 的通信-计算联合调度

## 关键数字

| 模型 | 训练加速（5 iter） |
|------|-------------------|
| ResNet50 | **+23.77–25.64%** |
| Transformer | **+11.66–12.83%** |

## 与 wiki 交叉

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — AllReduce/AllGather 语义
- [MPI Reduce / AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) — Ring AllReduce 算法

# Citations

[1] [raw/papers/Optimizing_Comm_Comp_Parallelism_Distributed_Training_2024.pdf](raw/papers/Optimizing_Comm_Comp_Parallelism_Distributed_Training_2024.pdf)
[2] [raw/papers/optimizing-comm-comp-parallelism-training.md](raw/papers/optimizing-comm-comp-parallelism-training.md) — 结构化摘录
