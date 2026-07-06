---
type: Concept
title: Cache Coherence
description: 多核 Cache 一致性：MESI/MOESI 状态机、Snooping vs Directory、False Sharing，与 WSE 无共享地址空间的对比
tags:
- architecture
- memory
- cache
- cpu
- multicore
- wse
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-18.md
---

# Cache Coherence（Cache 一致性）

多核各自持有 [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) 副本时，**P0 写入何时对 P1 可见**？Coherence 协议保证**同一地址**上的 propagation + serialization（Goodman 1983）。**跨地址顺序**由 [Memory Consistency Model](/concepts/memory-consistency-model.md) + [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) 管辖。

## 问题定义

```
单核：写 L1 → 立即可见
多核：Core0 写 X → Core1 L1 仍持旧值 → 读 X 错误
```

Coherence **只追踪 Cache Line 粒度**（主流 64B）——与 False Sharing 直接相关。

## MESI 状态机

| 状态 | 含义 |
|------|------|
| **M** Modified | 本地独占，dirty |
| **E** Exclusive | 本地独占，clean（与 memory 一致） |
| **S** Shared | 多核共享 clean |
| **I** Invalid | 无效或无副本 |

### 关键转换

| 事件 | 典型转换 | Bus 动作 |
|------|----------|----------|
| I + PrRd（独占） | → **E** | BusRd，无其他 hit |
| I + PrRd（共享） | → **S** | BusRd，其他降为 S |
| I + PrWr | → **M** | BusRdX + invalidate |
| **E + local PrWr** | → **M** | **无 bus 消息**（E 的价值） |
| S + PrWr | → **M** | BusUpgr，其他 → I |
| M + 远端 PrRd | → **S** | write-back，共享读 |

**E vs MSI**：独占读-改-写循环中 E→M 静默升级，避免每次 BusUpgr——OLAP 单线程 update 场景 MESI 比 MSI 快 **15–30%**。

## 协议族对比

| 协议 | 状态 | 特点 | 代表 |
|------|------|------|------|
| MSI | M/S/I | 简单，invalidate 频繁 | 早期 Pentium |
| MESI | +E | 独占静默写 | x86、Apple Silicon |
| MOESI | +O (Owned) | dirty 可直接转读，少 write-back | AMD Zen |

**MOESI 场景**：Core0 持 M，Core1 读同一行——MESI 需 write-back memory（+~100ns）；MOESI 中 Core0→O，Core1 从 O 取数。

## Snooping vs Directory

```
Snooping:  L1 miss → 广播总线 → 所有 cache controller 监听
Directory: L1 miss → 查目录 → 仅通知当前 sharer/owner
```

| 核数 | Snooping | Directory |
|------|----------|-----------|
| ≤8 | ✓ 低延迟（ring bus） | 过重 |
| ~16 | ✓ 仍可（Intel ring） | 可选 |
| 64+ | ✗ 广播饱和 | ✓ 必需（Xeon SP、EPYC） |
| 256+ | ✗✗ | ✓✓ |

Directory 流量 O(sharers)；Snooping O(cores)——64 核时 Directory 总流量约为 Snooping 的 **5–10%**。与 [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) 中 invalidate/NoC 路径、[Linear and Ring Topology](/concepts/linear-ring-topology.md) 有序 snoop 相关。

## False Sharing

两线程写**同一 64B line 内不同字段** → line 在核间 M↔I 反复抖动，单次抖动 ~30–50 ns，吞吐可降 **3–5×**。

```c
struct { int x; char pad[60]; int y; } stats;  // x/y 不同 line
```

Cache 替换算法无法缓解——由**数据布局**决定；与 Row Buffer 被动局部性（[DRAM and Memory System](/concepts/dram-memory-system.md)）形成对比。

## WSE：取消 Coherence

| | 通用多核 | [Cerebras WSE](/entities/cerebras-wse.md) |
|--|----------|-------------------------------------------|
| 地址空间 | 全局共享 | **无共享**；PE 独占 48KB SRAM |
| 协议 | MESI + Directory/Snoop | **无**；显式 NoC 消息 |
| 编程 | pthread 共享变量 | [SpaDA Programming Language](/concepts/spada-programming-language.md) 数据流 |
| 扩展 | 64 核 Directory 极限 | 900K PE |

900K PE × MESI metadata 粗估 **~170 GB** 目录状态 + mesh 广播 → 硬件不可行（[DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)）。

**Hybrid Coherence**（研究前沿）：控制面小范围 coherence + 数据面消息传递——NPU 8 核 Snooping vs 64 核 Directory 的设计分界取决于目标核数。

## 相关页面

- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — Cache 层与 coherence miss
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — SC/TSO/ARM、atomics、MCS 锁
- [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) — coherence 链上的 fence/invalidate
- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) — 无 TLB shootdown/coherence traffic
- [Deterministic Execution](/concepts/deterministic-execution.md) — 无共享内存的数据流替代
- [DRAM and Memory System](/concepts/dram-memory-system.md) — M 态 write-back 到 DRAM
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 一致性决策树与 WSE 无 MESI（Day 22）

# Citations

[1] [raw/articles/arch-study-30d-day-18.md](raw/articles/arch-study-30d-day-18.md) — H&P Ch.5.1–5.3（Day 18）
