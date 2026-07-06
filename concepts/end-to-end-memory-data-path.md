---
type: Concept
title: End-to-End Memory Data Path
description: 存储篇综合（Day 17-22）：load 全路径 AMAT 层级展开、内存墙时间线、一致性决策树、同步成本量级、WSE 消除 off-chip 的简化路径
tags:
- architecture
- memory
- cache
- dram
- ssd
- noc
- wse
- amat
timestamp: '2026-07-06T00:00:00Z'
created: 2026-07-06
sources:
- raw/articles/arch-study-30d-day-22.md
- raw/articles/arch-study-30d-day-17.md
- raw/articles/arch-study-30d-day-18.md
- raw/articles/arch-study-30d-day-19.md
- raw/articles/arch-study-30d-day-20.md
- raw/articles/arch-study-30d-day-21.md
---

# End-to-End Memory Data Path（端到端存储数据路径）

arch-study **第三阶段（Day 17–22）** 收官：把 DRAM、一致性、同步、SSD、NoC 从「分章知识点」拼成**一条 load 指令的真实路径**，并用 AMAT 量化各级贡献。

**Source:** [raw/articles/arch-study-30d-day-22.md](raw/articles/arch-study-30d-day-22.md)（Day 22 阶段总结）

## 传统 CPU 全路径

```
Core → L1 → L2 → LLC → NoC → Memory Controller → DRAM
  ↑                              ↓ (写回/DMA)
  └──────── coherence / atomic ← NoC ← 远端 Core/LLC
  ↓ (冷数据)
SSD / NVMe
```

| 层级 | 典型延迟 |
|------|----------|
| L1 | ~1 cycle |
| L2 | ~10 cycles |
| LLC | ~40 cycles |
| NoC（跨 die） | ~10–50 ns |
| DRAM | ~100 ns（tRCD+tCAS+burst） |
| SSD/NVMe | **50 μs–10 ms**（GC 尖峰） |

详见 [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md)、[DRAM and Memory System](/concepts/dram-memory-system.md)、[SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md)、[NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md)。

## AMAT 层级展开

```
AMAT = HT_L1 + MR_L1 × (HT_L2 + MR_L2 × (HT_LLC + MR_LLC × Penalty_DRAM))
```

**必须用条件概率逐层嵌套**——不能用 AMAT 算 AMAT。

**教科书例题**（L1: 1c/5% miss；L2: 10c/3%|L1 miss；LLC: 40c/30%|L2 miss；DRAM: 200c）：

```
AMAT = 1 + 0.05 × (10 + 0.03 × (40 + 0.30 × 200))
     = 1.65 cycles  →  @3 GHz ≈ 0.55 ns
```

**贡献分解**：

| 来源 | cycles | 占比 |
|------|--------|------|
| L1 hit（必付） | 1.0 | **60.6%** |
| L1 miss → L2 hit | 0.5 | 30.3% |
| → LLC hit | 0.06 | 3.6% |
| → DRAM | 0.09 | **5.5%** |

**敏感性结论**（Day 22 练习）：
- **降 L1 hit time 1→0.5 cycle**：AMAT −30%（最大）——每次访问都付 hit time
- **LLC miss rate 30→15% 或 DRAM 200→100 cycle**：各仅 −2.7%——因 MR 小，深层优化乘积有限
- 启示：HBM「延迟减半」对 AMAT 收益小，除非 LLC miss 已很高

## 内存墙（Memory Wall）时间线

Wulf & McKee：内存访问时间改善远慢于 CPU 频率 → `Memory_Wall_Gap = CPU_Clock / Memory_Access` 单调增。

| 世代解药 | 机制 |
|----------|------|
| Cache 层次 | L1/L2/L3 |
| Huge Pages | 减 TLB miss |
| Prefetch | 隐藏延迟 |
| HBM / 3D DRAM | **带宽**解药，非延迟 |
| PIM | 重构数据移动方向 |
| **WSE 式** | 消除 off-chip，全 on-chip SRAM |

见 [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md)、[DRAM and Memory System](/concepts/dram-memory-system.md)。

## 一致性协议决策树

```
需要 MESI/目录？
├── 共享地址空间？ → 否 → 不需要（WSE 走此分支）
│   ├── 多核共享数据 + 同时读写？ → 是 → 需要
```

**WSE**：每 PE 私有 SRAM + NoC 消息传递 → **无 MESI/Directory**。见 [Cache Coherence](/concepts/cache-coherence.md)、[Memory Consistency Model](/concepts/memory-consistency-model.md)。

## 同步原语成本（量级）

| 原语 | 典型延迟 |
|------|----------|
| Memory Fence (x86 MFENCE) | ~50–200 ns |
| Atomic CAS（L1 命中） | ~20–100 ns |
| Lock acquire | ~50–500 ns |
| Barrier（多核） | ~1–10 μs |
| **WSE 硬件 barrier** | **~1–10 ns**（单时钟域 + 短链路） |

见 [Memory Fence and Barrier](/concepts/memory-fence-barrier.md)。

## WSE 简化路径

```
传统: Core → L1 → L2 → LLC → NoC → MC → DRAM   (~100+ ns 到 DRAM)
WSE:  Core → on-chip SRAM（NoC 搬运，~10 ns 量级）
```

```
              冷数据                    热数据
                │                         │
                ▼                         ▼
         SSD/NVMe ── DMA ── DRAM ── Cache ── Core
         (10-100μs)  (1μs)  (100ns) (1-40c)  (1c)
                              │
                              │ NoC → 远端 LLC (50-100ns)

WSE 简化（无 off-chip）:

    on-chip SRAM (distributed, ~43 GB)
              │
              │ 2D Mesh (~632 hop avg, 21 PB/s)
              ▼
         ~900K SLA PE
```

- **无 L1/L2/L3/DRAM miss 概念**——SRAM 即存储
- **无 coherence 协议**——显式消息 + placement（[SpaDA](/concepts/spada-programming-language.md)）
- **容量瓶颈**：~43 GB SRAM vs 大模型权重 → streaming / 模型并行 / [memoryX NVMe tier](/concepts/ssd-nvme-storage-system.md)

**LLM 100 GB×10 次访问量级**（Day 22 练习）：
- H100 + HBM3：1 TB / 3 TB/s ≈ **333 ms**（纯传输）
- WSE SRAM：1 TB / 21 PB/s ≈ **48 μs** → 传输加速 ~7000×（未计 overlap/布局）

## 第三阶段知识地图（Day 17–22）

| Day | 主题 | 概念页 |
|-----|------|--------|
| 17 | DRAM / 内存墙 | [DRAM and Memory System](/concepts/dram-memory-system.md) |
| 18 | Cache 一致性 | [Cache Coherence](/concepts/cache-coherence.md) |
| 19 | 同步 / Memory Ordering | [Memory Consistency Model](/concepts/memory-consistency-model.md) |
| 20 | SSD / NVMe / RAID | [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) |
| 21 | NoC / 互连 | [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md) |
| 22 | **本页** | 端到端综合 |

## 相关页面

- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — AMAT 与层次
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — LLM 内存 bound
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — HBM→NVMe KV
- [Cerebras WSE](/entities/cerebras-wse.md) — 消除存储墙实例
- [Multicore SMT and NUCA](/concepts/multicore-smt-nuca.md) — 第四阶段入口（Day 23）

# Citations

[1] [raw/articles/arch-study-30d-day-22.md](raw/articles/arch-study-30d-day-22.md) — 存储篇阶段总结（Day 22）
[2] [raw/articles/arch-study-30d-day-17.md](raw/articles/arch-study-30d-day-17.md) — DRAM（Day 17）
[3] [raw/articles/arch-study-30d-day-20.md](raw/articles/arch-study-30d-day-20.md) — SSD/NVMe（Day 20）
[4] [raw/articles/arch-study-30d-day-21.md](raw/articles/arch-study-30d-day-21.md) — NoC（Day 21）
