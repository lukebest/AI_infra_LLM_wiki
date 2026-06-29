---
type: Concept
title: Memory Fence and Barrier
description: 内存屏障：ISA 顺序语义、Store Buffer/Invalidate Queue 排空、NoC coherence 路径、x86/ARM/RISC-V 变体与 WSE 无 coherence 对照
tags:
- architecture
- cpu
- noc
- protocol
- deterministic
- compiler
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/memory-fence-hardware-2026-06-28.md
---

# Memory Fence and Barrier（内存屏障）

**Memory fence** 是一条同步指令：排空处理器内部缓冲（Store Buffer、Invalidate Queue、Write Combining Buffer），并强制后续访存排在屏障之后。ISA 层 1 条指令，硬件路径却穿透 **ROB → LSQ → SBUF → L1 → Coherence/NoC → Directory → 远端 L1/IQ**——跨核同步链。

## 五种「看不见的缓冲」

[Out-of-Order Execution](/concepts/out-of-order-execution.md) 为填满流水线会异步化访存；fence 约束的对象：

| 缓冲 | 引起的乱序 |
|------|-----------|
| **Store Buffer (SBUF)** | StoreStore、StoreLoad |
| **Load Buffer** | LoadLoad |
| **Invalidate Queue (IQ)** | LoadStore（远端 invalidate 先 ack 后处理） |
| **Write Combining Buffer** | StoreStore（x86 WC） |
| **ROB 推测态** | 跨分支 load 乱序 |

## 四种顺序约束

| 类型 | 约束 | 主要跨越 |
|------|------|----------|
| **StoreStore** | 旧 store 先于新 store 提交 | SBUF 排空 |
| **LoadLoad** | 旧 load 结果先于新 load 可见 | Load Buffer / 推测 |
| **StoreLoad** | store 全局可见后才允许后续 load | SBUF + coherence（TSO 关键） |
| **LoadStore** | load 所见 ≤ 后续 store 影响 | IQ |

x86 **MFENCE** / RISC-V **FENCE rw,rw** 四者全约束；**StoreLoad** 最难——需 store 对其他核可见，不只是本核 L1 更新。

## MFENCE 微架构路径（Skylake 风格）

```
MFENCE 入 ROB → 设 Barrier bit → SBUF drain（stall 新 store）
  → 旧 store 写 L1 或发 ReadEx → NoC → Directory → Invalidate 远端 Owner
  → SBUF 空 → MFENCE retire → 后续 load/store 可发射
```

**Invalidate Ack ≠ 处理完成**：协议常要求低延迟 ack，但远端 IQ 异步处理 tag——ack 回来不保证其他核已看不到旧值。ARM **DSB** 等 outstanding coherence；**DMB** 只排空本核 SBUF/LBUF。

Store Buffer 高性能实现多为 **Speculative + Replay**（地址消歧）；fence 强制 **SBUF drain**——Skylake/Zen 上单条 MFENCE 约 **30–50 cycles**。

## ISA 变体

| ISA | 指令 | 特点 |
|-----|------|------|
| x86 | MFENCE / LFENCE / SFENCE | TSO，store 全局有序 |
| ARM | DMB / DSB | DSB 强于 DMB（含远端 IQ） |
| RISC-V | FENCE pred,succ | 位掩码组合 rw/w/r |
| RISC-V | FENCE.I | I/D cache 一致性（自修改代码） |
| RISC-V | FENCE.VMA | 页表变更 + [TLB Shootdown](/concepts/virtual-memory-tlb.md) |

RISC-V **FENCE.VMA** 路径：排空 outstanding 访存 → TLB shootdown IPI → 等全核 ack——64 核量级 **~30–100 μs**（与 [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) 一致；FENCE.VMA 还可能叠加排空 outstanding 访存的开销）。

## NoC 与多核延迟

| 场景 | 延迟量级 | 关键路径 |
|------|----------|----------|
| 单核 SBUF drain | ~5–20 cycles | ROB → L1 hit |
| 同 socket directory | ~100–500 ns | Directory 双跳 + Owner |
| DSB（最严） | ~500–2000 ns | 远端 IQ + 全局可见 |
| TLB Shootdown（64 核） | ~30–100 μs | IPI + 全核 TLB flush/ack（见 [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md)） |

多核 fence 延迟 ≈ **max(本核 SBUF drain, 最远核 IQ 处理)**；全局 MFENCE 触发 **O(N)** coherence 消息——众核需 **tree barrier** 或硬件聚合。

## WSE / DSA：无 coherence 的退化

[Cerebras WSE](/entities/cerebras-wse.md) 无共享地址空间、无 Cache coherence（[DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)）：

- 无 SBUF/IQ/coherence 链 → 无 x86 式 MFENCE 语义
- 片内同步退化为 **PE barrier / 显式 NoC 消息**（[Deterministic Execution](/concepts/deterministic-execution.md)）
- NoC 无 shootdown、无 memory ordering traffic——协议大幅简化

**开放问题**：CPU↔NPU 异构 fence、coherence-light 混合模型下的屏障语义。

## 相关页面

- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — ROB Barrier、推测与 fence
- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) — FENCE.VMA 与 shootdown
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — coherence miss
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — fence 消息的 NoC 延迟
- [UB Transaction Layer](/concepts/ub-transaction-layer.md) — 事务层 Fence 机制
- [Core Group (DRAM Access Synchronization)](/concepts/core-group-dram-access.md) — 专用同步原语

# Citations

[1] [raw/articles/memory-fence-hardware-2026-06-28.md](raw/articles/memory-fence-hardware-2026-06-28.md) — Memory Fence 深度研究报告（2026-06-28）
