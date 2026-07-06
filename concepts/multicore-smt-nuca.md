---
type: Concept
title: Multicore SMT and NUCA
description: H&P Ch.5.7-5.9：Fine/Coarse/SMT 多线程、SMT 1.2-1.3× 收益、Amdahl+通信/一致性 Overhead、NUCA 非均匀 Cache、WSE 反 Amdahl 哲学
tags:
- architecture
- cpu
- multicore
- smt
- numa
- nuca
- amdahl
- wse
timestamp: '2026-07-06T00:00:00Z'
created: 2026-07-06
sources:
- raw/articles/arch-study-30d-day-23.md
---

# Multicore SMT and NUCA（多核、SMT 与 NUCA）

arch-study **第四阶段（Day 23–27）** 入口：从单核优化转向**多核如何协同**——SMT 复用硬件、Amdahl 限制扩展上限、NUCA 揭示「大 Cache 也不透明」。与 WSE 900K PE 的扩展哲学直接对照。

**Source:** [raw/articles/arch-study-30d-day-23.md](raw/articles/arch-study-30d-day-23.md)（H&P Ch.5.7–5.9，Day 23）

## 多线程三种实现

| 方式 | 切换时机 | 利用率 | 复杂度 |
|------|----------|--------|--------|
| **Fine-grained** | 每条指令 | 高 | 中 |
| **Coarse-grained** | 长 stall | 中 | 低 |
| **SMT** | 同时多发射多线程 | **最高** | 高 |

**SMT 本质**：多线程**共享**执行单元、Cache、功能单元；**独立** PC、寄存器、ROB 项。一线程 Cache miss stall 时，另一线程占用空闲资源。

## SMT 性能

```
SMT_Speedup ≈ (Σ IPC_multithreaded) / (Σ IPC_single_thread)
工业典型：1.2–1.3×（理想 2× 不可达）
```

**达不到 2× 的原因**：执行单元竞争、Cache 污染（两线程工作集干扰）、单线程关键路径不变。

**例题**：单线程 IPC=2.0，双线程联合 IPC=3.2 → **1.6×** 加速，说明 ~40% 硬件在单线程下闲置。

与 [Constable Load Elimination](/concepts/constable-load-elimination.md) 关联：2-way SMT 下 Constable **+8.8%**（noSMT +5.1%）——load 端口更稀缺时 load 消除收益放大。

## Amdahl 定律（多核版）

```
Speedup(N) = 1 / ((1 − f_parallel) + f_parallel/N + Overhead(N))
```

| Overhead 类型 | 增长 | 效应 |
|---------------|------|------|
| 通信 | O(N) 或 O(N log N) | N* 处 Speedup 峰值后下降 |
| 一致性 | O(N²) 流量 | N* 常在 8–32 |

**例题**：f_parallel=95%，64 核理想 Speedup = 1/(0.05+0.95/64) ≈ **15.4×**；实测曲线在 N=64 仅 ~13.5× → 一致性/通信主导。

见 [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md)。

## NUCA (Non-Uniform Cache Access)

现代大 L3 **物理切片**分布芯片各处 → 访问延迟随距离变化：

| 位置 | 典型延迟 |
|------|----------|
| 近端 Cache slice | ~10 cycles |
| 远端 slice | ~50 cycles |
| 平均 | ~25 cycles |

**结论**：Cache 不再「透明」——OS/编译器需 **NUMA-aware / placement** 优化。

## WSE = NUCA 极端形式

| | 传统 NUCA | WSE |
|--|-----------|-----|
| 存储 | 分布式 L3 banks | 每 PE **48 KB 私有 SRAM** |
| 远端访问 | 跨 slice ~50 ns | **NoC 跳数 × ~1 ns** |
| 延迟决定因素 | 片上距离 | [Mesh 拓扑 + XY 路由](/concepts/deterministic-routing-dor.md) |
| 优化 | OS placement | **SME/SpaDA 编译期 placement** |

评估 NoC 时看**延迟分布**（1–2 hop vs 600 hop），而非仅平均值——见 [WSE Performance Model](/concepts/wse-performance-model.md)。

## 多核调度策略

| 策略 | 说明 |
|------|------|
| Symmetric | 同构核，OS 自由调度 |
| AMP (big.LITTLE) | 大小核混合 |
| Dynamic | 硬件负载感知（Thread Director） |
| **Spatial** | 任务位置感知（NUMA/NoC） |

WSE 900K PE 是**极度 Spatial**——[SpaDA](/concepts/spada-programming-language.md) placement 直接决定 NoC 通信开销。

## WSE「反 Amdahl」设计

传统多核瓶颈 → WSE 对策：

| 瓶颈 | 传统 | WSE |
|------|------|-----|
| 串行部分 | Amdahl 上限 | 数据流：PE 独立任务 |
| 一致性 O(N²) | MESI/Directory | **消息传递 + 私有 SRAM** |
| 内存墙 | DRAM 带宽争用 | **43 GB on-chip + 21 PB/s NoC** |
| 同步 | μs 级 barrier | **ns 级硬件 barrier** |

**代价**：非通用 CPU 编程模型（CSL/SME），灵活性换扩展性。见 [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)、[DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)。

## NPU 核设计决策树（Day 23）

```
多核 vs 单核？     → 任务并行度
核间互连？         → Ring(小) / Crossbar(≤16) / Mesh(>16)
缓存？             → 私有+共享 L2/L3 / 全私有消息传递(WSE) / Scratchpad+DMA
一致性？           → 共享编程 → MESI；专用模型 → 不需要
```

## 相关页面

- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — Amdahl 基础
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — SMT 共享 ROB/issue
- [Cache Coherence](/concepts/cache-coherence.md) — 多核一致性（WSE 无）
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — 大规模并行瓶颈
- [Cerebras WSE](/entities/cerebras-wse.md) — 900K PE 扩展实例
- [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md) — 核间互连（Day 21）

# Citations

[1] [raw/articles/arch-study-30d-day-23.md](raw/articles/arch-study-30d-day-23.md) — H&P Ch.5.7–5.9（Day 23）
