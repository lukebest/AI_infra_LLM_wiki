---
type: Concept
title: SSD and NVMe Storage System
description: 片外存储：NAND/FTL/GC/写放大、RAID 0/1/5/6 写惩罚、NVMe 多队列与 PCIe 带宽、read() 延迟分解与 io_uring；WSE memoryX 与 CMX KV tier
tags:
- architecture
- storage
- ssd
- nvme
- raid
- io
- inference
- wse
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/articles/arch-study-30d-day-20.md
---

# SSD and NVMe Storage System（SSD 与 NVMe 存储系统）

[DRAM and Memory System](/concepts/dram-memory-system.md) 之下是 **TB 级片外存储**：HDD/SSD、RAID 阵列与 **NVMe** 协议。Hennessy & Patterson **Appendix D**：AI 训练/推理的完整数据路径常在此层卡住——DataLoader、checkpoint、KV cache spill 均受 **带宽悬崖** 与 **GC 延迟尖峰** 约束。

**Source:** [raw/articles/arch-study-30d-day-20.md](raw/articles/arch-study-30d-day-20.md)（H&P 6th App.D，Day 20）

## 存储层次中的位置

| 层级 | 延迟 | 带宽（量级） | 容量 |
|------|------|-------------|------|
| [SRAM/HBM](/concepts/dram-memory-system.md) | ns–μs | TB/s–PB/s（WSE 片上） | GB |
| DRAM | ~80 ns | ~100 GB/s | GB–TB |
| **NVMe SSD** | **50–200 μs**（GC 可达 ms） | **7–14 GB/s** 顺序 | TB |
| HDD | 5–20 ms | ~200 MB/s | TB–PB |

相对 [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) 中「SSD μs 级」：随机读与 GC 可使有效延迟 **比 NAND 物理读高 2–3 个数量级**。

## SSD：NAND + FTL

```
Host (NVMe) → FTL (L2P / wear-level / GC) → Flash Controller → NAND dies
```

| 机制 | 要点 |
|------|------|
| **Block erase** | 擦除单位 = block；写 = program 到新 page → 需 **L2P 重映射** |
| **Wear-leveling** | 均衡 P/E cycle；**TBW** ≈ capacity × P/E ÷ **WA**（例：1 TB TLC, P/E=1K, WA=3 → **~333 TBW**） |
| **Garbage Collection** | 搬活页 → 擦 victim block；**写放大 WA** 理想 1，GC 不利时 **3–5** |
| **GC 停顿** | 前台 I/O 阻塞 → latency **100 μs → 10 ms** 尖峰 |

**性能量级**：4 KB 随机读 **~1M IOPS**；顺序读 **~14 GB/s**（PCIe Gen5 ×4）；随机等效带宽 **~4 GB/s**（1M×4 KB）。

## RAID 与写放大

| 级别 | 容量 | 随机写（相对单盘） | 典型用途 |
|------|------|-------------------|----------|
| **RAID 0** | N× | **N×** | 临时/中间结果 |
| **RAID 1** | 1× | **1×** | 元数据镜像 |
| **RAID 5** | (N−1)× | **~1/4×**（4 次 I/O RMW） | 读多写少 |
| **RAID 6** | (N−2)× | **~0.5×** | 大阵列双盘容错 |

**关键洞察**：RAID 5 **4 KB 随机写** = read old data + read parity + write data + write parity → 10 盘阵列随机写 IOPS ≈ 单盘 **/4**（vs RAID 0 **×10**）。数据库随机写场景常避 RAID 5。

## NVMe vs AHCI

| | AHCI (SATA) | NVMe (PCIe) |
|--|-------------|-------------|
| 队列 | 1 × depth 32 | **65535 队列 × depth 65535** |
| 提交 | I/O 寄存器 | **Doorbell + SQ/CQ in host memory** |
| 中断 | 单命令 | **MSI-X** 多核友好 |

**PCIe Gen5 ×4**：理论 **16 GB/s**，实测 **~14 GB/s**。

## I/O 路径延迟分解

典型 `read()`（page cache miss → NVMe）：

```
syscall/VFS/fs ~1 μs → blk-mq/driver ~1 μs → PCIe ~0.5 μs
→ NVMe controller ~5–10 μs → NAND read ~50–100 μs → 返回 ~2 μs
```

| 路径 | 总延迟 |
|------|--------|
| Page cache hit | **~3–5 μs** |
| NVMe 正常读 | **~50–200 μs** |
| **GC 期间** | **~1–10 ms** |
| HDD | **~5–20 ms** |

**软件路径 ~3 μs** 与 NAND **~50 μs** 同量级——**io_uring** 绕过 syscall，随机读 IOPS 可从 libaio **~200K** 提升到 **~800K**（接近 SSD 上限）。

## 现代趋势

- **io_uring**：用户态 submission ring，批处理友好
- **NVMe-oF**：RDMA/TCP 远程 NVMe，**~10–20 μs** 额外延迟
- **ZNS**：主机可见 zone 布局，可控 GC
- **Computational Storage**：SSD 内 filter/compress

## AI 工作负载关联

**训练数据路径**（GPT 量级）：

```
Dataset (PB) → NVMe pool (~28 GB/s, 4盘) → Host DRAM (~100 GB/s)
→ GPU HBM (~3 TB/s) → SRAM → ALU
```

DataLoader 需 **10 GB/s** 时单盘 **7 GB/s** 即瓶颈 → sharding、prefetch、**io_uring**、压缩。

**推理 KV tier**：HBM → DRAM → **NVMe**（[CMX & STX](/concepts/cmx-stx.md) Tier G3.5；[Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) paged attention spill）。

## WSE memoryX

[Cerebras WSE](/entities/cerebras-wse.md) 片上 **~21 PB/s SRAM** vs memoryX **4× NVMe ~28 GB/s** → 带宽差 **~750,000×**：

```
WSE wafer (900K PE, 43 GB SRAM, mesh NoC)
    │ PCIe Gen5 ×16 ~64 GB/s
    ▼
memoryX: 4× NVMe (~30 TB) + host DRAM pool
    ▼
Host CPU
```

- **无 L1/L2/L3**——SRAM 即 cache；**软件显式** tier 迁移（[SpaDA](/concepts/spada-programming-language.md) / CSL）
- **可行**：checkpoint、冷启动加载、streaming prefetch
- **不可行**：每 token 从 SSD 读 KV（相对算力 **100×+** 延迟差）

与 Day 19 [Memory Consistency Model](/concepts/memory-consistency-model.md)：PE 写 KV 到 HBM/外存时的 **atomic ref count** 为实际一致性场景。

## 相关页面

- [DRAM and Memory System](/concepts/dram-memory-system.md) — DRAM/HBM 上一层
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 完整层次与 AMAT
- [CMX & STX](/concepts/cmx-stx.md) — 推理 NVMe KV tier
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 内存 bound
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — HBM→NVMe KV placement
- [Cerebras WSE](/entities/cerebras-wse.md) — memoryX 外置 tier
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 软件管理存储 vs 硬件 cache

# Citations

[1] [raw/articles/arch-study-30d-day-20.md](raw/articles/arch-study-30d-day-20.md) — H&P App.D 存储系统（Day 20）
