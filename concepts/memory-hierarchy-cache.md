---
type: Concept
title: Memory Hierarchy and Cache
description: 内存墙、存储层次、Cache 映射与 3C 模型、AMAT 优化框架、与 WSE SRAM-only 设计的对比
tags:
- architecture
- memory
- cache
- sram
- memory-bandwidth
- wse
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-13.md
- raw/articles/arch-study-30d-day-14.md
- raw/articles/arch-study-30d-day-15.md
---

# Memory Hierarchy and Cache（存储层次与 Cache）

**内存墙 (Memory Wall)**：CPU 算力增速 >> DRAM 延迟改善（~7%/年）→ Cache 层次是过去 30 年 CPU 设计的核心。

## 完整访存路径（含 TLB）

```
虚拟地址 → TLB → 物理地址 → L1 → L2 → L3 → DRAM
```

TLB 在 Cache **之前**；详见 [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md)。AI 大工作集需巨页，否则 TLB Miss 代价可超过 L3 Miss。

## 存储层次（典型延迟量级）

| 层级 | 延迟 | 容量 |
|------|------|------|
| Register | < 1 ns | ~KB |
| L1 | ~1–2 ns | 32–64 KB |
| L2 | ~3–10 ns | 256 KB–1 MB |
| L3/LLC | ~10–20 ns | 8–64 MB |
| DRAM | ~80–100 ns | GB 级 |
| SSD | μs 级 | TB 级 |

理论基础：[Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) 中的**局部性原理**。

## Cache 基础

- **映射**：直接映射 / 组相联 / 全相联
- **写策略**：Write-through vs Write-back
- **替换**：LRU 近似
- **Cache Line**：通常 64 B，利用空间局部性

## 3C Miss 模型

```
Miss Rate = Compulsory + Capacity + Conflict
```

| 类型 | 原因 | 对策 |
|------|------|------|
| Compulsory | 首次访问 | 预取 |
| Capacity | 工作集 > Cache | 增大容量 |
| Conflict | 映射冲突 | 提高相联度 |

## AMAT 优化总框架

```
AMAT = Hit Time + Miss Rate × Miss Penalty
```

多层递归：L1 miss → L2 → L3 → DRAM。

三类优化方向：

1. **降低 Hit Time** — 小而简单 L1、流水线访问
2. **降低 Miss Rate** — 容量、相联度、预取、编译器布局
3. **降低 Miss Penalty** — 多级 Cache、非阻塞 Cache、读优先

## WSE「无传统 Cache」对比

| | 传统 CPU | [Cerebras WSE](/entities/cerebras-wse.md) |
|--|----------|-------------------------------------------|
| 层次 | Register → L1/L2/L3 → DRAM | PE + **片上 SRAM**，无 L1/L2/L3 |
| 动机 | 隐藏 DRAM 延迟 | 44 GB SRAM + 编译器 placement |
| 代价 | Cache 一致性、AMAT 调优复杂 | SRAM 容量上限、编程模型约束 |

理解 CPU Cache 优化「工具箱」，才能评估 **SRAM-first**（[LPU](/concepts/lpu-architecture.md)、WSE）放弃 Cache 的权衡。

## 相关页面

- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) — 地址转换层
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — CPU vs WSE 能力矩阵
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — DRAM 带宽与 NoC
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — memory-bound decode
- [Reasoning Cliff](/concepts/reasoning-cliff.md) — KV/HBM 饱和

# Citations

[1] [raw/articles/arch-study-30d-day-13.md](raw/articles/arch-study-30d-day-13.md) — H&P Ch.2 存储层次（Day 13）
[2] [raw/articles/arch-study-30d-day-14.md](raw/articles/arch-study-30d-day-14.md) — AMAT 与 Cache 优化（Day 14）
[3] [raw/articles/arch-study-30d-day-15.md](raw/articles/arch-study-30d-day-15.md) — TLB 与访存路径（Day 15）
