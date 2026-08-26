---
type: Concept
title: DRAM and Memory System
description: DRAM 访问时序与 Row Buffer、Channel/Bank 并行、DDR/HBM 带宽公式、内存墙与 Roofline Ridge Point、WSE 分布式 SRAM 对 HBM 的绕过
tags:
- architecture
- memory
- memory-bandwidth
- dram
- hbm
- wse
timestamp: '2026-08-26T00:00:00Z'
updated: 2026-08-26
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-17.md
- raw/articles/arch-study-30d-day-20.md
---

# DRAM and Memory System（DRAM 与内存系统）

CPU Cache 之上是 [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md)；**DRAM/HBM** 是层次最底、容量最大、也是 AI 时代**带宽瓶颈**所在。Hennessy & Patterson **内存墙**：DRAM 延迟 ~1.05×/年 vs 算力 ~1.5×/年（历史）→ 绝大多数 AI workload **带宽受限**。

## DRAM 物理与层次

```
Channel → DIMM/Rank → Chip → Bank → Row → Cell (1T1C)
```

访问时序（DDR5-6400 量级）：

| 参数 | 典型 | 含义 |
|------|------|------|
| t_RCD | ~14 ns | 行选通 → 列选通 |
| t_RP | ~14 ns | 行预充电 |
| t_CAS (tCL) | ~16 ns | 列选通 → 数据 |
| t_BURST | ~5 ns | 突发传输 |

| 场景 | 延迟 |
|------|------|
| 冷启动 / 跨行 | t_RP + t_RCD + t_CAS + Burst ≈ **49 ns** |
| **Row Buffer 命中** | t_CAS + Burst ≈ **21 ns**（~4× 差距） |

Row Buffer 命中率由**访问顺序**决定（硬件被动）；不同于 Cache 可通过替换策略优化——推理 KV 访问模式差时命中率仅 ~30–50%。

## 带宽与并行

```
带宽 = 数据速率 (MT/s 或 GT/s) × 总线宽度 (bit) ÷ 8
```

| 类型 | 峰值带宽（示例） |
|------|------------------|
| DDR5-6400 单通道 | 51.2 GB/s |
| DDR5-6400 双通道 | 102.4 GB/s |
| HBM3 单 stack (1024b @ 6.4 GT/s) | 819.2 GB/s |
| H100（5× HBM3 stack） | **3350 GB/s** |

三层并行：**Channel**（粗）→ **Rank**（中，交错隐藏 precharge）→ **Bank**（细，16–32 bank/rank）。单 bank 等效 ~2.1 GB/s；需多 bank 并行才能打满通道。

**HBM**：TSV 垂直堆叠 8-Hi/12-Hi，1024-bit 宽接口——在 die  perimeter 受限下突破带宽；见 [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md)。

## 内存墙与 Roofline

H100 FP16：**1979 TFLOPS** / **3350 GB/s** → Ridge Point ≈ **590 FLOPS/byte**。

| 工作负载 | 算力强度 | 瓶颈 |
|----------|----------|------|
| GPT-3 175B 训练 forward | ~30 | 带宽 |
| LLM 推理 / Diffusion | ~50 | 带宽 |
| GPT-3 单 token 推理 | ~590 | 临界 |

算力强度 < Ridge Point → **memory-bound**（与 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) decode 阶段一致）。100 TFLOPS @ 50 FLOPS/byte 需 **2 TB/s**——DDR5 双通道远不够，必须 HBM 或片上 SRAM。

## WSE：用 SRAM 绕过 DRAM

| | H100 HBM3 | WSE-3 片上 SRAM |
|--|-----------|-----------------|
| 容量 | ~80 GB | ~40 GB |
| 带宽 | ~3.35 TB/s | ~21 PB/s |
| 带宽/容量 | ~42 GB/s per GB | ~525,000 GB/s per GB |

无 DRAM、900K PE × 48 KB SRAM；**带宽密度比 GPU 高约 12,500×**，单 GB SRAM 成本远高于 HBM 但 AI 瓶颈在带宽而非容量——[Cerebras WSE](/entities/cerebras-wse.md) / [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) 的核心经济逻辑。

代价：整晶圆面积、良率、显式数据布局（[Deterministic Execution](/concepts/deterministic-execution.md)）。

## 相关页面

- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — Cache 层与 AMAT
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — TSV + 堆叠 DRAM
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 带宽 bound
- [Reasoning Cliff](/concepts/reasoning-cliff.md) — KV/HBM 容量饱和
- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — 局部性与量化权衡
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — DRAM 以下片外存储 tier
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — Day 17–22 存储篇综合
- [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md) — NoC 五问（Day 21）
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — H100 HBM Roofline 与 WSE 带宽密度对比（Day 24）
- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) — HBF 与 HBM 并列近 GPU；专家权重走 Direct∥Relay，不经 HBM 阵列
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — 用 ReRAM 读带宽密度（0.128 B/FLOP）绕开 HBM 权重复用膝点
- [Handy HBM 开场](/papers/hc2026-handy-hbm-tutorial.md) — Hot Chips 2026：HBM 吃 **3×** DDR 晶圆面积；DRAM 产能十年未涨
- [SK hynix packaging](/papers/hc2026-skhynix-hbm-advanced-packaging.md) — HBM4 2048 IO / 2048 GB/s；12Hi 量产、16Hi Qual
- [OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md) — HBF 是低 α/低 β 容量点；同机柜 ~14× 容量 / ~0.6× 带宽
- [Pistil](/papers/hc2026-pistil-20-chiplet-slm.md) — 边缘 2.5D RPC-DRAM flower，512 MB / 51.2 GB/s

# Citations

[1] [raw/articles/arch-study-30d-day-17.md](raw/articles/arch-study-30d-day-17.md) — H&P Ch.2 内存技术（Day 17）
