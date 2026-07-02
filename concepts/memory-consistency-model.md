---
type: Concept
title: Memory Consistency Model
description: 内存一致性模型：Coherence vs Consistency、SC/TSO/ARM 重排规则、fence 契约、CAS/LL-SC 与 MCS 锁，及 WSE/NPU 同步设计
tags:
- architecture
- memory
- cpu
- multicore
- wse
- deterministic
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-19.md
---

# Memory Consistency Model（内存一致性模型）

[Cache Coherence](/concepts/cache-coherence.md) 保证**单地址** propagation + serialization（「X 最新值是什么？」）。**Consistency** 规定**多地址**访存的相对顺序（「A=1 之后 B=2 是否一定对其他核可见？」）——硬件–软件契约：硬件允许哪些重排，程序员用 [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) / atomics 保证关键顺序。

## Coherence vs Consistency

| | Coherence | Consistency |
|--|-----------|-------------|
| 作用域 | **Per-address** | **Cross-address** |
| 机制 | MESI/MOESI | Store Buffer 规则 + fence |
| 可独立 | 完美 coherence + **弱** consistency ✓ | — |

经典反例（弱模型下可能出现）：

```
Core 0: A=1; print B;
Core 1: B=1; print A;
→ 两核都看到对方变量 = 0
```

## Sequential Consistency (SC)

Lamport (1979)：执行等价于某**全局全序**，且每核操作保持**程序顺序**。

| 重排 | SC |
|------|-----|
| Load→Load | ✗ |
| Load→Store | ✗ |
| Store→Load | ✗ |
| Store→Store | ✗ |

实现代价：每次访存等前序操作**全局可见** → Store Buffer 刷新 stall **50+ ns**。**无商业 CPU 实现纯 SC**。

## TSO（x86）

**Total Store Order** ≈ SC + **Store Buffer**：

| 重排 | TSO |
|------|-----|
| Load→Load | ✗ |
| Load→Store | ✗ |
| Store→Store | ✗ |
| **Store→Load** | **✓**（唯一放宽） |

写对本核立即可见（读自己的写）；对其他核延迟可见直至 fence/flush。**StoreLoad** 是 TSO 与 [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) 的核心。

## ARM / RISC-V（弱序）

默认允许 LL/LS/SS/SL 重排（除显式 fence / acquire-release）。

| 操作 | SC | TSO | ARM/RV |
|------|----|-----|--------|
| Load 后 Store | 必须等 | 必须等 | 可并行 |
| Store 后 Load | 必须等 | **可重排** | 可重排 |
| 日常需 fence | 几乎从不 | 偶尔 | **必须显式** |

x86 lock-free 更简单；ARM/RV 性能上限更高（少无谓 stall）。

## Fence 与 ISA（概要）

| ISA | 代表指令 |
|-----|----------|
| x86 | MFENCE / LFENCE / SFENCE；LOCK 前缀隐含 full fence |
| ARM | DMB / DSB / ISB |
| RISC-V | `fence rw,rw`；`fence.tso`；FENCE.VMA |

详见 [Memory Fence and Barrier](/concepts/memory-fence-barrier.md)。

## 原子原语：CAS vs LL/SC

| | CAS | LL/SC |
|--|-----|-------|
| 代表 | x86 LOCK CMPXCHG | RISC-V LR/SC、ARM LDREX/STREX |
| ABA | **有** | **无**（地址被写过即 SC 失败） |
| NPU | 控制面偶尔 | 数据流友好 |

NPU 统计计数：64 PE 用软件 CAS/LL-SC 串行化 **128–192** 次总线事务 vs **fetch-and-add 硬件 1 次 broadcast**——ISA 应提供专用原子单元。

## 锁实现

| 锁 | Cache line 争抢 | 公平 | 规模 |
|----|----------------|------|------|
| TAS Spinlock | 极严重 | 否 | ≤4 核 |
| Ticket Lock | 严重（poll `now_serving`） | 是 | ≤16 核 |
| **MCS Lock** | **无**（自旋本地变量） | 是 | 100+ 核 |

MCS (1991)：32 核实测吞吐 ~**12×** Ticket Lock，invalidate **~1000×** 降低。

## WSE / NPU

**WSE 单时钟域**：无 Store Buffer 跨 PE 延迟 → 近似 **SC** 语义；代价是 ~1 GHz、良率/物理约束（[Deterministic Execution](/concepts/deterministic-execution.md)）。

| 同步方式 | ~900K PE barrier 粗估 |
|----------|----------------------|
| 硬件 fabric barrier | ~670 ns（对角 ~670 hop） |
| 软件 MCS Lock | ~**1.8 ms**（排队 + mesh 消息） |

**>~10K 核**：硬件 barrier 为唯一可行路径（[WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)）。

NPU dataflow 主路径无需 coherence/consistency；**reduction / control-plane / 统计** 需 mesh-aware barrier、tree reduce、fetch-and-add。

## 相关页面

- [Cache Coherence](/concepts/cache-coherence.md) — Day 18 单地址层
- [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) — fence 硬件路径
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — ROB/SBUF 与 Barrier bit
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 无 MFENCE 链
- [Cerebras WSE](/entities/cerebras-wse.md) — PE barrier / 无共享内存
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — async/await 显式顺序

# Citations

[1] [raw/articles/arch-study-30d-day-19.md](raw/articles/arch-study-30d-day-19.md) — H&P Ch.5.4–5.6（Day 19）
