---
type: Concept
title: Virtual Memory and TLB
description: 虚拟内存四作用、页表与 TLB、巨页与 TLB Shootdown、AMAT 含地址转换、WSE 无 MMU 的工程权衡
tags:
- architecture
- memory
- cpu
- virtualization
- wse
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-15.md
---

# Virtual Memory and TLB（虚拟内存与 TLB）

程序使用**虚拟地址**；硬件经 **MMU + 页表** 转为物理地址。**TLB** 是地址转换的 Cache——在访问路径上位于 Cache **之前**，TLB Miss 时 Cache 都不查。

## 虚拟内存的四个作用

| 作用 | 含义 | WSE 需求 |
|------|------|----------|
| **保护** | 页级 R/W/X 权限 | 低（单租户 wafer） |
| **隔离** | 每进程独立地址空间 | 低 |
| **扩展** | Demand paging、换页 | 无（数据常驻 SRAM） |
| **共享** | 共享库、COW fork | 低 |

WSE 单工作负载 + 显式数据放置 → (1)(2)(4) 需求大降；(3) 不适用。

## 地址转换与页表

典型 2 级页表（Sv32）：VPN 索引 → **2 次额外访存** 得 PPN。无 TLB 时每次 load/store 延迟约 **×3**。

**多级页表**：按需分配——64 KB 工作集可能只需 ~8 KB 页表 vs 单级 4 MB。

## TLB 结构

| 层级 | 典型大小 | Hit 时间 |
|------|----------|----------|
| L1 TLB | 32–128 项 | ~1 cycle |
| L2 TLB | 256–2048 项 | 5–10 cycles |
| Page Walk | — | 30–100 cycles |
| Page Fault | — | 10⁶+ cycles |

典型 TLB 缺失率 1–2%，但单次 Page Walk 代价极高。

## 含 TLB 的 AMAT

```
AMAT ≈ TLB_Hit_Time + TLB_Hit_Rate × Cache_AMAT
     + TLB_Miss_Rate × Page_Walk_Time
```

TLB 在路径前端——对 AI 大工作集，TLB 压力可超过 L3 Miss。

## 巨页 (Huge Pages)

| 页大小 | 32 GB 工作集页数 | 128 项 TLB 覆盖 |
|--------|------------------|-----------------|
| 4 KB | 8M | ~512 KB (0.0016%) |
| 2 MB | 16K | ~256 MB (0.78%) |
| 1 GB | 32 | ~128 GB |

LLM 训练（参数 + 优化器 + 梯度 数十 GB）**必须** 2 MB/1 GB 巨页；THP 常带来 **5–15%** 提升。AI 训练倾向启动时预分配、运行中少 mmap。

## TLB Shootdown

多核共享页表时，一核改 PTE → 其他核 TLB  stale → **IPI 广播 flush**。64 核单次可达 50–100 μs；系统调用密集 workload 可占 **5–10%** 时间。众核/WSE 规模下传统 IPI 方案不可行。

## WSE：无 MMU/TLB 的权衡

```
传统:  VA → TLB → PA → Cache → 数据
WSE:  编译器/CSL → 物理地址 → SRAM（必然命中）
```

**Software-Managed Everything (SME)**：malloc/分支/Cache 猜测 → 编译时静态映射 + 数据流图。

| 放弃 | 获得 |
|------|------|
| 进程隔离、COW、动态 malloc | 零地址转换开销、确定性访存 |
| 通用指针追逐 | 可建模延迟（[WSE Performance Model](/concepts/wse-performance-model.md)） |
| | 省 MMU/TLB 面积；NoC 无 coherence/shootdown traffic |

NoC 无需 Cache coherence、TLB shootdown IPI、共享内存 ordering——协议大幅简化。

## 相关页面

- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — Cache 层与完整访存路径
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — CPU 武器 vs WSE 矩阵
- [Deterministic Execution](/concepts/deterministic-execution.md) — 显式地址管理
- [Cerebras WSE](/entities/cerebras-wse.md) — 无虚拟内存实例

# Citations

[1] [raw/articles/arch-study-30d-day-15.md](raw/articles/arch-study-30d-day-15.md) — H&P Ch.2.8 虚拟内存（Day 15）
