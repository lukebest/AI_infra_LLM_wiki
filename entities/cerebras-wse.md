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
timestamp: '2026-08-18T00:00:00Z'
created: 2026-04-16
updated: 2026-08-18
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
- raw/articles/arch-study-30d-day-20.md
- raw/reports/superscalar-cpu-final-report.md
- raw/articles/memory-fence-hardware-2026-06-28.md
- raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf
- raw/articles/arch-study-30d-day-26.md
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
| 内存 | 44 GB 片上 SRAM + **memoryX NVMe** | 128 GB 片上 SRAM |
| 路由 | 24 color 静态 | 96 C2C plesiosynchronous |
| 编程 | CSL（数据流） | Compiler spatial |
| 模型 | 分布式内存 | 分布式内存 |

## Reduce/AllReduce Collective
- HPDC 2024 论文建立了 WSE 上 Reduce/AllReduce 的性能模型和算法体系
- Auto-Gen Reduce 距下界 ≤1.4×，比 vendor 方案快 3.27×
- 详见 [Wse Performance Model](/concepts/wse-performance-model.md)、[Wse Reduce Algorithms](/concepts/wse-reduce-algorithms.md)、[Near Optimal Wafer Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md)

## memoryX 外置存储

WSE-3 经 **PCIe Gen5 ×16**（~64 GB/s）连接 **memoryX**：约 **4× NVMe SSD**（~30 TB 顺序读 ~28 GB/s 量级）+ host DRAM 池。片上 **~21 PB/s SRAM** 与 NVMe 带宽差 **~750,000×**——适合 checkpoint/冷加载，不适合 per-token KV 从 SSD 读取。详见 [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md)。

## 相关页面
- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) — 无 MMU/TLB
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — SLA vs Golden Cove 矩阵
- [Cache Coherence](/concepts/cache-coherence.md) — 900K PE 无 MESI/Directory
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — 无共享内存、PE barrier 近似 SC
- [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) — 无 coherence 时 fence 退化
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 无 DRAM、21 PB/s SRAM 带宽
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — memoryX NVMe tier
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — place/dataflow/compute 高级 CSL 抽象
- [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md) — 数据流架构历史（Dennis & Misunas 1975）
- [Deterministic Execution](/concepts/deterministic-execution.md) — 共同使用的确定性范式
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 无 L1/L2/L3 的设计对比
- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — 暗硅、良率、专用 PE
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — WSE-aware Constabulary、控制核 vs PE 无 BP/OoO
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — WSE 不采用 OoO 的对比
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — 对比参照
- [Lpu Architecture](/concepts/lpu-architecture.md) — LPU 架构
- [Wse Nom Contradiction Analysis](/analyses/wse-nom-contradiction-analysis.md) — 矛盾论六步框架分析 NoW
- [Cerebras Wse Vs Groq Network Comparison](/analyses/cerebras-wse-vs-groq-network-comparison.md) — WSE vs Groq 全面对比
- [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) — Color 虚拟通道机制
- [Noc Router Microarchitecture](/concepts/noc-router-microarchitecture.md) — WSE NoC Router 理论基础
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 通用 tile mesh 片上 collective 对照（FlooNoC/DCA）
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — Mesh 度量与 Torus 对比
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — ~949×949 2-D Mesh 选型
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — 为何未用 CMesh/Express/Hypercube
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — 分布式 XY 路由与 collective 延迟
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md) — 为何 WSE 倾向 DOR 而非拥塞自适应
- [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md) — Mesh 单 VC、为何不用 Torus（Day 13）
- [Duato Escape VC Deadlock-Free Routing](/concepts/duato-escape-vc-deadlock-free-routing.md) — 逃逸 VC；WSE 倾向避免而非恢复（Day 14）
- [WaferLLM System](/concepts/waferllm-system.md) — PLMR 模型、MeshGEMM/V、KV shift（WSE-2 E2E LLM）
- [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md) — Amdahl/Roofline/Mesh/良率量化（Day 26）
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 训练集体通信；多 wafer 限制（Day 27）
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Chiplet vs wafer 路径（Day 29）
- [Arch-Study 30d Knowledge Map](/summaries/arch-study-30d-knowledge-map.md) — 30 天知识地图（Day 30）
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — TPU 脉动 vs SLA PE（Day 25）
- [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) — 6 个未解瓶颈 + MLIR pass 设计
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 延迟与 B_b 瓶颈
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 四层设计空间
- [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md) — H&P App.F 五问（Day 21）
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 存储+NoC 全景（Day 22）
- [Multicore SMT and NUCA](/concepts/multicore-smt-nuca.md) — 900K PE 扩展哲学（Day 23）
- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — NI 与协议栈
- [Switching Principles](/concepts/switching-principles.md) — 虫孔 vs 电路交换
- [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md) — Flit/WH/HoL（互连 Day 15）
- [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md) — VC + Credit（互连 Day 16）
- [NoC Router Pipeline and Allocators](/concepts/noc-router-pipeline-allocators.md) — 五级流水（互连 Day 17）
- [NoC Router Pipeline Optimizations](/concepts/noc-router-pipeline-optimizations.md) — 跳延迟优化动机（互连 Day 18）
- [Network Interface and System-Level Design](/concepts/network-interface-and-system-design.md) — 极简 PE NI（互连 Day 19）
- [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md) — Polaris/WSE 反推（互连 Day 20）
- [Interconn-Study 21d Knowledge Map](/summaries/interconn-study-21d-knowledge-map.md) — 21 天收束（互连 Day 21）
- [TPU v4 OCS Reconfigurable Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) — 4096-chip 可重构 vs 单晶圆 Mesh
- [Layout-Aware NoC and Flexible Dataflow Accelerators](/concepts/layout-aware-noc-flexible-dataflow.md) — MAERI/SIGMA/FEATHER/Venus 5 类技术路线
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — GPU fat-tree 对照
- [Paper Deep-Dive Map](/summaries/paper-deepdive.md) — 精读 Day 1–8
- [Network-on-Wafer](/concepts/network-on-wafer.md) — WSE 是 field stitching 均匀 mesh；对照 WoW「同层不能直连」
- [WoW Network Design](/papers/network-design-wafer-scale-wow-hybrid-bonding.md) — SoIC-WoW 第三条 WSI 路线

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
[11] [raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf](raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf) — WaferLLM PLMR/MeshGEMM（He et al. 2025）
[12] [raw/articles/arch-study-30d-day-26.md](raw/articles/arch-study-30d-day-26.md) — WSE 量化综合（Day 26）
[13] [raw/articles/arch-study-30d-day-25.md](raw/articles/arch-study-30d-day-25.md) — DSA/脉动 vs SLA（Day 25）
[14] [raw/articles/interconn-study-21d-day-13.md](raw/articles/interconn-study-21d-day-13.md) — CDG/Dally、Mesh vs Torus（Day 13）
[15] [raw/articles/interconn-study-21d-day-14.md](raw/articles/interconn-study-21d-day-14.md) — Duato / 逃逸 VC（Day 14）
