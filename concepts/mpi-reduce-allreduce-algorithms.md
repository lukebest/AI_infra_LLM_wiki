---
type: Concept
title: MPI Reduce/AllReduce Algorithms
description: Rabenseifner ICCS 2004 五类 MPI 归约算法：二叉树、recursive doubling、halving&doubling、binary blocks、ring；α+nβ 代价模型与 (p,n) 自适应选择；MPICH-2 长向量基础
tags:
- mpi
- collective
- allreduce
- reduce
- communication
- hpc
- ring
- topology
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf
---

# MPI Reduce/AllReduce Algorithms

Rabenseifner (ICCS 2004) 系统优化 **MPI_Reduce** 与 **MPI_Allreduce**——生产环境 profiling 显示二者占 MPI 时间 **>40%**。论文给出 **五种算法** 及按 **进程数 p** 与 **向量长度 n** 的自适应选择，成为现代 MPI/NCCL 归约实现的经典参照（**recursive halving & doubling** 已进入 MPICH-2）。

**Author:** Rolf Rabenseifner (HLRS, Stuttgart) | **Venue:** ICCS 2004, LNCS 3036

## 代价模型

与 Thakur & Gropp 一致：

| 符号 | 含义 |
|------|------|
| **α + nβ** | 双向消息（latency + per-byte） |
| **α_uni + nβ_uni** | 单向（二叉树常用） |
| **γ** | 每字节归约运算成本；p 进程最优计算 **(p−1)/p · nγ** |

## 五种算法概览

| 算法 | 步数/规模 | 最优区间 | 要点 |
|------|-----------|----------|------|
| **Binary tree** | ⌊lg p⌋ | **短向量** | 每步全向量；后半进程 idle → 负载不均 |
| **Recursive doubling** | ⌊lg p⌋ | **极短向量** | 距离倍增；双端冗余计算同一结果 |
| **Halving & doubling (RHD)** | 2⌊lg p⌋ | **长向量、2 的幂 p** | reduce-scatter + allgather；**~2nβ** 带宽最优级 |
| **Binary blocks** | 块内 RHD | **非 2 的幂、长向量、大 p** | p 分解为 2 的幂块和 |
| **Ring** | 2(p−1) | **中等非 POT、小 p** | 步进 reduce-scatter + 环 allgather |

### Recursive halving & doubling（现代默认基础）

```
Phase 1 — Reduce-scatter:
  递归向量折半 + 距离倍增 → 每进程持 1/p 归约片段

Phase 2 — Allgather:
  递归向量倍增 + 距离折半 → 全进程获完整结果
```

**非 2 的幂：** 先剥离 r = p − 2^⌊lg p⌋ 进程（偶/奇配对交换半向量），再对 p′ = 2^⌊lg p⌋ 进程执行 RHD。

相对 Thakur 的 rank-ordered reduce-scatter：本算法 **不要求 scatter 顺序** → 可优先与近邻交换，利于分层网络。

### Ring AllReduce

与 [Linear and Ring Topology](/concepts/linear-ring-topology.md) 逻辑环一致：

- **Reduce-scatter：** p−1 步，步 i 向 rank+i 发送、从 rank−i 接收对应 chunk 并归约
- **Allgather：** p−1 步，chunk 沿环右传（stride 1）

带宽友好、latency **O(p)** — 仅适合 **小 p** 或非 POT 中等规模。

## 自适应选择

按 **(p, n)** 在运行时切换算法（Cray T3E 900 实测 heatmap）：

| n | 典型选择 |
|---|----------|
| ≤32 B | recursive doubling |
| ≤1 KB | binary tree / vendor / doubling |
| 长、小 p | ring |
| 长、大 p、非 POT | binary blocks |
| 长、POT | halving & doubling |

**25%** 生产任务 **p 非 2 的幂** → binary blocks / ring 不可忽略。

## 实测加速（相对当年 vendor）

| 平台 | 长向量收益 |
|------|-----------|
| Cray T3E | 最高 **~100×**（maxloc）；sum 亦有数倍 |
| IBM SP | **1.5–5×**（8 KB–8 MB）；hybrid MPI/SMP 约 **1.5–3×** |

## 与 ML / 片上互连的关联

| 场景 | 联系 |
|------|------|
| **Tensor Parallel AllReduce** | 训练/推理 TP 梯度或 activation 同步 — 短向量→tree/doubling，长→RHD/ring |
| [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) | 同 **reduce-scatter + allgather** 分解；WSE 另加 Star/Chain/Auto-Gen |
| [Collective-Capable NoC](/concepts/collective-capable-noc.md) | 硬件 offload 归约，避免软件 collective 占互连 |
| [M2N Communication](/concepts/m2n-communication.md) | MoE disagg 用 **M2N** 而非对称 AllReduce |

## 谱系

```
Inverse broadcast / binary tree (短向量)
    → Recursive doubling (极短)
    → Rabenseifner RHD + binary blocks + ring (2004, MPICH-2)
    → Thakur & Gropp MPICH tuning (2003/2004)
    → NCCL/MPI 多算法 runtime 选择
    → [WSE Auto-Gen Reduce](/concepts/wse-reduce-algorithms.md) (模型驱动搜索, 2024)
```

## 相关页面

- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — wafer-scale 归约算法族
- [Linear and Ring Topology](/concepts/linear-ring-topology.md) — Ring AllReduce 逻辑拓扑
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — α/β 延迟带宽模型
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 片上 in-network reduction
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — TP AllReduce 通信开销
- [papers/rabenseifner-collective-reduction-operations.md](/papers/rabenseifner-collective-reduction-operations.md) — 论文摘要

# Citations

[1] [raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf](raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf) — Rabenseifner, ICCS 2004
