---
type: Concept
title: Distributed GEMM Algorithms
description: 分布式内存矩阵乘算法谱系：Cannon（2D mesh ring-shift）、SUMMA（broadcast 外积）、2.5D/3D SUMMA（通信–内存权衡）；α+β 代价模型、SBP 切分 vs 映射放置；T10 rTensor 形式化 Cannon
tags:
- gemm
- distributed-memory
- mpi
- tensor-parallelism
- mesh
- compiler
- communication
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/articles/分布式存储架构下的矩阵乘与编译器.md
---

# Distributed GEMM Algorithms（分布式矩阵乘算法）

在 **分布式内存** 架构上，每个处理器仅直接访问本地内存；GEMM C = A×B 需在 **M/K/N 切分、数据放置、通信原语** 之间联合设计。郑启航（知乎 2024）系统梳理 **Cannon → SUMMA → 3D/2.5D SUMMA** 谱系、LLM **2.5D/3D 张量并行**，以及 Graphcore **T10 rTensor** 对 Cannon 的编译器形式化。

**Source:** [raw/articles/分布式存储架构下的矩阵乘与编译器.md](raw/articles/分布式存储架构下的矩阵乘与编译器.md)（知乎专栏）

## 分布式内存与 TP 切分的局限

| 模式 | 每节点数据 | SBP 式描述 | 问题 |
|------|-----------|-----------|------|
| 1D TP | A[M,K], B[K,N/P] | broadcast × split(1) | 一维无法同时切 M/K/N |
| 2D 切 K | A[M,K/P], B[K/P,N/P] | … → partial_sum → boxing | K 维需 **AllReduce** |
| 2D 切 M,N | split(0),broadcast × broadcast,split(1) | 无冗余 | **仍有一维不可切** → 内存占用高 |

SBP（OneFlow 风格）描述 **静态分片** 且 **计算仅用本地数据**；Cannon 等算法需 **时间维 shift**，不能用纯 SBP 表达，须用 **映射** `[i,j] → [m,k]`。

## 算法谱系（2D √P × √P 处理器网格）

### Cannon（1969）

- **拓扑：** 均匀 **2D mesh**；**M、K、N 全切分**，无冗余存储
- **机制：** 预对齐（align）A/B 分片 → P 步 **matmul 累加** + **ring shift**（A 横向、B 纵向）
- **映射：** A[j,(i+j)%√P]→[m,k]；B[(i+j)%√P,i]→[k,n]
- **通信（α–β 模型，n×n 方阵）：** Cost ≈ **2(√P−1)(α + n²/P · β)**
- **约束：** 处理器数须 **平方数**

### SUMMA（1995, Scalable Universal Matrix Multiplication）

- **机制：** 计算/存储分离；K 维外积迭代，每步 **broadcast** A 的列片与 B 的行片
- **SBP：** (split(0),split(1)) × (split(0),split(1)) = (split(0),split(1))
- **优点：** **非方阵** 处理器网格；实现简单
- **通信：** Cost ≈ **2√P (α log √P + n²/P · β)** — 常数项略高于 Cannon

### 3D SUMMA

- **拓扑：** P = p³ 立方体；A/B/C 在 **三轴切分**（A: split on j,l；B: split on l,j）
- **流程：** Allgather A/B → 本地 GEMM 得 D_ijl → Alltoall 换轴 → 本地 reduce
- **通信：** 相对 2D 少传约 **P^(1/6)** 倍数据；代价是 **3D 拓扑** 与更复杂放置

### 2.5D SUMMA

- **拓扑：** p × p × **d**（1 ≤ d ≤ p）；d=1 退化为 2D，d=p 接近 3D
- **机制：** z=0 层放 A/B → broadcast → 在 z 轴 **重切分 K** → 2D SUMMA 式 broadcast 计算 → z 轴 **Reduce**
- **权衡：** 调节 d 在 **通信量** 与 **A/B 复制内存** 之间插值；SUMMA 改进版支持 **非方阵** 拓扑

## LLM 中的 2.5D / 3D 并行

| 方案 | 要点 |
|------|------|
| **Tesseract** | 训练侧 2.5D 并行；进一步切 A 降 SUMMA 2.5D **额外内存**；拓扑 p×p×d |
| **NUS 3D** | 负载均衡 + GEMM/GEMV 优化；A 切分维与经典 3D SUMMA 论文略有不同 |

与 [Parallelism Transition Point](/concepts/parallelism-transition-point.md) 中 **TP/PP** 选择正交：此处优化 **单次 GEMM 的通信–内存 Pareto 前沿**。

## T10 rTensor：Cannon 的编译器形式化

Graphcore [IPU](/entities/graphcore-ipu.md) 专用编译器 **T10** 提出 **RotatingTensor (rTensor)**，泛化 **空间+时间切分 + ring 旋转**（与 Cannon align + shift 同构）：

```cpp
class RotatingTensor {
  vector<size_t> shape;
  DataType type;
  vector<size_t> spatial_partition_factor;   // 空间切分
  vector<size_t> temporal_partition_factor;  // 时间切分（missing axis）
  vector<size_t> rotating_pace;              // 每步 ring 传输块大小
};
```

| 概念 | 含义 |
|------|------|
| **missing axis** | 某矩阵有一维不参与空间切分但计算全依赖 → 用 **时间维** 切分 |
| **自动搜索** | 由 op 语义推导 (spatial, temporal, rp)；rp 为 ring **圈数**（须整除） |
| **子张量放置** | 全局 align — 与 Cannon **初始分布一致**（3×3 阵列示例） |
| **两级优化** | 算子内 (时间/空间/rp) ↔ 算子间全局内存分配 |

T10 固定 **Cannon 类** 通信模式：通信量 **< SUMMA 2D**、**> SUMMA 3D**；与 [SpaDA](/concepts/spada-programming-language.md)（WSE 空间数据流 DSL）同属 **分布式 GEMM 编译抽象**，目标硬件不同。

## α–β 代价模型

与 [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) 相同：**T = α + nβ**（消息启动 + 每字节）。Flame 等 **Parallel Matrix Multiplication: A Systematic Journey** 用 **切分状态 + MPI 原语变换** 统一推导 2D/3D SUMMA，并给出 **Stationary C / Stationary A** 在 (M,K,N) 尺寸下的选型。

**实践结论（原文）：**

1. 论文常假设方阵；**实际须按 (M,K,N) 尺寸** 选算法
2. 高维 mesh 切分/映射仍开放
3. **RMA** 架构：远端直读 vs broadcast 回落 SUMMA/Cannon — 数据量同阶，性能待测

## 算法选型速查

| 场景 | 倾向 |
|------|------|
| 2D mesh、P 完全平方、内存紧 | **Cannon** |
| 通用 2D 网格、实现简单 | **SUMMA** |
| P 可立方、通信主导 | **3D SUMMA** |
| 通信–内存折中、LLM 训练 | **2.5D / Tesseract** |
| 核间 ring、编译器自动搜索 | **T10 rTensor** |

## 相关页面

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Cannon/SUMMA 的 2D 物理拓扑
- [Linear and Ring Topology](/concepts/linear-ring-topology.md) — Cannon shift 的逻辑 ring
- [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) — α+β 集体通信模型
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 延迟/带宽建模
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — LLM TP/DP 策略
- [Graphcore IPU](/entities/graphcore-ipu.md) — T10 目标平台
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 空间数据流编译
- [summaries/distributed-gemm-and-compiler.md](/summaries/distributed-gemm-and-compiler.md) — 原文摘要

# Citations

[1] [raw/articles/分布式存储架构下的矩阵乘与编译器.md](raw/articles/分布式存储架构下的矩阵乘与编译器.md) — 郑启航, 知乎专栏 (2024)
