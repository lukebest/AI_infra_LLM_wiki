---
type: Concept
title: DSA Processor Design Tradeoffs
description: 领域专用处理器设计取舍：现代 CPU 传统武器（OoO/Cache/分支预测/TLB）的能力代价矩阵 vs WSE SLA 核
tags:
- architecture
- accelerator
- wse
- cpu
- deterministic
- compiler
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-16.md
---

# DSA Processor Design Tradeoffs（领域专用处理器设计取舍）

H&P 核心篇（Day 8–15）覆盖现代 CPU 的**传统武器**；Day 16 将其与 [Cerebras WSE](/entities/cerebras-wse.md) 的 **「无武器」SLA 核** 对照——体系结构本质是**在关键路径上做杠杆最大的取舍**，而非堆功能。

## 超标量 CPU 完整数据通路

```
前端: I-Cache → 分支预测(TAGE) → µop 译码
  ↓
OoO: 重命名 → ROB/RS → Issue Queue → 调度
  ↓
执行: ALU / MUL / FMA / Load-Store / Branch
  ↓
存储: TLB → L1 → L2 → L3 → DRAM
  ↓
提交: ROB 按序 retire（精确异常）
```

## 能力/代价矩阵

| 机制 | 单核提速（量级） | 面积代价 | WSE SLA |
|------|------------------|----------|---------|
| 流水线 | ~1.5× | 1× | 极浅指令级流水 |
| 乱序执行 | ~1.5× | ~3× | **无** |
| 分支预测 | ~1.2× | ~0.5× | **无**（静态数据流） |
| L1 Cache | ~1.5× | ~1× | **无**（48 KB SRAM 直用） |
| L2/L3 | ~1.3× | ~5× | **无** |
| TLB/MMU | ~1.05× | ~1× | **无**（[Virtual Memory](/concepts/virtual-memory-tlb.md)） |
| Cache 一致性 + Memory Fence | — | ~2× | **无**（无共享地址空间；见 [Cache Coherence](/concepts/cache-coherence.md)、[Memory Fence and Barrier](/concepts/memory-fence-barrier.md)） |

**WSE 交换**：失去通用性与单核峰值 GHz → 获得 **900K PE**、**21 PB/s** 片上带宽、确定性延迟。

## 性能瓶颈金字塔

```
频率 ← 功耗墙（Dennard 终结后停滞）
  ↑ IPC/ILP ← 真实程序 ILP ≈ 2–4
  ↑ 分支预测 ← 98% 易，99.9% 极难
  ↑ Cache 命中 ← AMAT
  ↑ DRAM 带宽 ← AI 真正瓶颈
```

OoO/Cache/预测是为**功耗墙下榨 IPC**；AI workload 上**内存墙**更致命 → WSE 押注 SRAM 而非 DRAM 层次。

## 算力密度对比（Day 16 估算）

| | Intel Golden Cove（估） | WSE-3 PE（估） |
|--|-------------------------|----------------|
| 面积 | ~6 mm² @ 5 GHz | ~0.01 mm² @ 1 GHz |
| 算力密度 | ~0.3 GFLOPS/mm² | ~100 GFLOPS/mm² |

CPU ~80% 面积给 OoO/Cache/预测；PE **100% 给算力**——[Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) 暗硅/专用化逻辑在 DSA 上的极致。

## Software-Managed Everything

| 传统 CPU（隐式） | WSE/DSA（显式） |
|------------------|-----------------|
| malloc + TLB | 编译时 PE 数据映射 |
| 乱序 + 分支预测 | 数据流图 / CSL |
| Cache 定位 + MFENCE | 显式 NoC 消息 / PE barrier |

设计原则：**避免硬件猜测** → 固定可建模延迟 → 复杂性上移到编译器（[Deterministic Execution](/concepts/deterministic-execution.md)）。

## 相关页面

- [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md)
- [Out-of-Order Execution](/concepts/out-of-order-execution.md)
- [Branch Prediction](/concepts/branch-prediction.md)
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md)
- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md)
- [LPU Architecture](/concepts/lpu-architecture.md) — 同类 SME 路径

# Citations

[1] [raw/articles/arch-study-30d-day-16.md](raw/articles/arch-study-30d-day-16.md) — 核心篇阶段总结（Day 16）
