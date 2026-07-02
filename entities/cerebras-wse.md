---
type: Entity
title: Cerebras WSE
description: Cerebras 晶圆级 AI 加速器，24 color 确定性路由，900K 核心
tags:
- cerebras
- wse
- accelerator
- deterministic
- inference
- mesh
timestamp: '2026-05-29T00:00:00Z'
created: 2026-04-16
sources:
- raw/papers/Near-optimal_wafer-scale_reduce.pdf
- raw/articles/interconn-study-21d-day-01.md
- raw/articles/interconn-study-21d-day-02.md
- raw/articles/interconn-study-21d-day-03.md
- raw/articles/interconn-study-21d-day-04.md
- raw/articles/arch-study-30d-day-02.md
- raw/articles/arch-study-30d-day-13.md
- raw/articles/arch-study-30d-day-14.md
- raw/articles/arch-study-30d-day-15.md
- raw/articles/arch-study-30d-day-16.md
- raw/articles/arch-study-30d-day-17.md
- raw/articles/memory-fence-hardware-2026-06-28.md
---

# Cerebras WSE (Wafer-Scale Engine)

晶圆级 AI 加速器。WSE-3 为最新代：900K 核心，44 GB SRAM，214 Pbit/s fabric 带宽。

## 与通用 CPU 体系结构的差异

| 维度 | 通用 OoO CPU | WSE |
|------|-------------|-----|
| ILP | 硬件 Tomasulo + 分支预测 | 编译器静态调度（[Deterministic Execution](/concepts/deterministic-execution.md)） |
| 内存 | L1/L2/L3 + DRAM/HBM | **44 GB 片上 SRAM**，无 DRAM（[DRAM and Memory System](/concepts/dram-memory-system.md)、[Memory Hierarchy](/concepts/memory-hierarchy-cache.md)） |
| 地址 | MMU + TLB + 虚拟内存 | **无 MMU/TLB**，物理/SRAM 直寻（[Virtual Memory and TLB](/concepts/virtual-memory-tlb.md)） |
| 互连 | 片外总线/NoC + coherence | 晶圆级 2D Mesh + 虫孔，无 coherence/shootdown |
| 同步 | MFENCE + coherence 链 | PE barrier / 显式消息（[Memory Consistency Model](/concepts/memory-consistency-model.md)、[Memory Fence and Barrier](/concepts/memory-fence-barrier.md)） |
| 经济 | 小 die 高良率 | 整晶圆良率约束（[Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md)） |

完整能力/代价矩阵见 [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)。

## 2D Mesh 拓扑

WSE-3 ~900K PE 排列为 **~949×949 2D Mesh**，每 PE **4 端口**（上下左右）：

| 度量 | 值 |
|------|-----|
| 度 | 4 |
| 直径 | ≈ 2×948 = **1896** hops |
| 平均距离 | ≈ **632** hops（d̄，见 [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md)） |
| 二分带宽 B_b | ≈ **949** 条链路（~3.8 TB/s @ 4 GB/s/link） |

相对 N 节点全连接，Mesh 以多跳换低端口数——约 **145×** 链路节省。**未选 Torus**：环绕长 wire 在晶圆上不可行（[Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md)）。满注入带宽 vs B_b 差 **~947×** → 必须算子融合与通信局部性（[Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md)）。

## 虫孔交换与流量匹配

WSE 采用 **wormhole routing 变体**（非电路交换）：

- LLM 推理 traffic 为**短突发消息**（activation、gradient）+ 高并发 collective
- 电路交换：建路/拆路开销 >> 数据本身；N 跳通路独占沿途全部链路 → 并发度崩溃
- 虫孔：单 flit 注入、小 buffer、与 AllReduce 等 collective 天然契合

## 确定性路由
- 24 个 color（虚拟通道），编译时静态路由
- 每跳 ~0.4ns，color 之间互不阻塞
- 与 [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) 的 plesiosynchronous C2C 是不同路径实现确定性
- Color 机制详见 [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md)

## 与 Groq LPU 的对比
| 维度 | Cerebras WSE | Groq 3 LPU |
|------|-------------|------------|
| 核心 | 900K 简单 PE | 256 复杂 LPU |
| 内存 | 44 GB 片上 SRAM | 128 GB 片上 SRAM |
| 路由 | 24 color 静态 | 96 C2C plesiosynchronous |
| 编程 | CSL（数据流） | Compiler spatial |
| 模型 | 分布式内存 | 分布式内存 |

## Reduce/AllReduce Collective
- HPDC 2024 论文建立了 WSE 上 Reduce/AllReduce 的性能模型和算法体系
- Auto-Gen Reduce 距下界 ≤1.4×，比 vendor 方案快 3.27×
- 详见 [Wse Performance Model](/concepts/wse-performance-model.md)、[Wse Reduce Algorithms](/concepts/wse-reduce-algorithms.md)、[Near Optimal Wafer Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md)

## 相关页面
- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) — 无 MMU/TLB
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — SLA vs Golden Cove 矩阵
- [Cache Coherence](/concepts/cache-coherence.md) — 900K PE 无 MESI/Directory
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — 无共享内存、PE barrier 近似 SC
- [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) — 无 coherence 时 fence 退化
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 无 DRAM、21 PB/s SRAM 带宽
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — place/dataflow/compute 高级 CSL 抽象
- [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md) — 数据流架构历史（Dennis & Misunas 1975）
- [Deterministic Execution](/concepts/deterministic-execution.md) — 共同使用的确定性范式
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 无 L1/L2/L3 的设计对比
- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — 暗硅、良率、专用 PE
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — WSE 不采用 OoO 的对比
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — 对比参照
- [Lpu Architecture](/concepts/lpu-architecture.md) — LPU 架构
- [Wse Nom Contradiction Analysis](/analyses/wse-nom-contradiction-analysis.md) — 矛盾论六步框架分析 NoW
- [Cerebras Wse Vs Groq Network Comparison](/analyses/cerebras-wse-vs-groq-network-comparison.md) — WSE vs Groq 全面对比
- [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) — Color 虚拟通道机制
- [Noc Router Microarchitecture](/concepts/noc-router-microarchitecture.md) — WSE NoC Router 理论基础
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 通用 tile mesh 片上 collective 对照（FlooNoC/DCA）
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — Mesh 度量与 Torus 对比
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 延迟与 B_b 瓶颈
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 四层设计空间
- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — NI 与协议栈
- [Switching Principles](/concepts/switching-principles.md) — 虫孔 vs 电路交换

# Citations

[1] [raw/papers/Near-optimal_wafer-scale_reduce.pdf](raw/papers/Near-optimal_wafer-scale_reduce.pdf)
[2] [raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf](raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf) — SpaDA 语言与编译器（Gianinazzi et al. 2026）
[3] [raw/articles/interconn-study-21d-day-01.md](raw/articles/interconn-study-21d-day-01.md) — WSE Mesh 引入（互连 Day 1）
[4] [raw/articles/interconn-study-21d-day-02.md](raw/articles/interconn-study-21d-day-02.md) — WSE 虫孔选型（互连 Day 2）
[5] [raw/articles/interconn-study-21d-day-03.md](raw/articles/interconn-study-21d-day-03.md) — Mesh 拓扑度量（互连 Day 3）
[6] [raw/articles/interconn-study-21d-day-04.md](raw/articles/interconn-study-21d-day-04.md) — 成本/延迟模型（互连 Day 4）
[7] [raw/articles/arch-study-30d-day-02.md](raw/articles/arch-study-30d-day-02.md) — 功耗/良率（体系结构 Day 2）
[8] [raw/articles/arch-study-30d-day-14.md](raw/articles/arch-study-30d-day-14.md) — 无 Cache 对比（Day 14）
[9] [raw/articles/arch-study-30d-day-15.md](raw/articles/arch-study-30d-day-15.md) — 无 MMU/TLB（Day 15）
[10] [raw/articles/arch-study-30d-day-16.md](raw/articles/arch-study-30d-day-16.md) — DSA 能力矩阵（Day 16）
