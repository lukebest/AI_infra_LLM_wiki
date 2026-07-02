---
type: Summary
title: Optimization of Collective Reduction Operations
description: Rabenseifner ICCS 2004：MPI Reduce/AllReduce 五算法（tree、doubling、RHD、binary blocks、ring）与 (p,n) 选择；占 MPI 时间 >40%；长向量相对 vendor 最高 100×
tags:
- mpi
- collective
- allreduce
- reduce
- hpc
- communication
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf
---

# Optimization of Collective Reduction Operations

**Author:** Rolf Rabenseifner (HLRS, University of Stuttgart) | **Venue:** ICCS 2004, LNCS 3036 | **PDF:** [raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf](raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf)

## 一句话总结

针对 MPI 中 **Allreduce/Reduce 占 >40% MPI 时间** 且 **25% 运行非 2 的幂进程数** 的现状，Rabenseifner 给出 **五种带宽/延迟优化算法**（二叉树、recursive doubling、**halving & doubling**、binary blocks、**ring**），按 **(p, 向量长度)** 自适应选择；长向量相对当年 vendor 实现加速 **3×–100×**，RHD 已纳入 **MPICH-2**。

## 核心贡献

1. **统一 α+nβ 代价模型** 比较五种协议（双向/单向因子 f_α, f_β）
2. **Recursive halving & doubling**：reduce-scatter + allgather，长向量 **~2nβ** 级带宽；非 POT 预处理
3. **Binary blocks**：非 POT 进程数块分解，降低 RHD 额外开销
4. **Ring**：pairwise reduce-scatter + ring allgather，中等非 POT 长向量
5. **运行时算法选择** heatmap（Cray T3E、IBM SP 实测）

## 关键数字

| 指标 | 值 |
|------|-----|
| MPI 时间 in Allreduce+Reduce | **40.7%**（T3E profiling） |
| 非 POT 进程占比 | **25%** runtime |
| vs vendor (long vector) | **3×** IBM sum — **100×** Cray maxloc |
| IBM SP bandwidth gain | **1.5–5×** (8 KB–8 MB) |
| Ring Allreduce steps | **2(p−1)** |
| RHD (POT) bandwidth term | **≈ 2nβ** |

## 与 wiki 交叉引用

- [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) — 五算法机制与选择
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — Ring / reduce-scatter+allgather 在 WSE 上的扩展
- [Linear and Ring Topology](/concepts/linear-ring-topology.md) — Ring AllGather 逻辑环
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — α/β 通信代价
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 硬件归约 offload
- [Near-Optimal Wafer-Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md) — 2024 WSE 归约算法系统研究

# Citations

[1] [raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf](raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf) — Rabenseifner (2004)
