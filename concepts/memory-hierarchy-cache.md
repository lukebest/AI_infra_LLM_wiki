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
updated: 2026-10-02
sources:
- raw/articles/arch-study-30d-day-13.md
- raw/articles/arch-study-30d-day-14.md
- raw/articles/arch-study-30d-day-15.md
- raw/articles/arch-study-30d-day-17.md
- raw/articles/arch-study-30d-day-20.md
- raw/papers/Fancy_Eviction_LLM_Prefix_Cache_2026.pdf
- raw/papers/HBFSim_Extensible_HBF_Simulator_GPU_2026.pdf
- raw/papers/KV_Cache_New_Memory_Wall_SoK_2026.pdf
- raw/papers/RREvict_Prefix_Cache_Eviction_Agentic_2026.pdf
- raw/papers/SpecStream_Resource_Efficient_Speculative_Decoding_2026.pdf
- raw/papers/SPIMOE_Hybrid_Sparsity_Reasoning_MoE_PIM_2026.pdf
---

# Memory Hierarchy and Cache（存储层次与 Cache）

**内存墙 (Memory Wall)**：CPU 算力增速 >> DRAM 延迟改善（~7%/年）→ Cache 层次是过去 30 年 CPU 设计的核心。DRAM 物理层时序、HBM 带宽与 Roofline 见 [DRAM and Memory System](/concepts/dram-memory-system.md)。

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
| [SSD / NVMe](/concepts/ssd-nvme-storage-system.md) | **50 μs–10 ms**（GC） | TB 级 |

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
| 代价 | [Cache Coherence](/concepts/cache-coherence.md)、AMAT 调优复杂 | SRAM 容量上限、编程模型约束 |

理解 CPU Cache 优化「工具箱」，才能评估 **SRAM-first**（[LPU](/concepts/lpu-architecture.md)、WSE）放弃 Cache 的权衡。

## 相关页面

- [Cache Coherence](/concepts/cache-coherence.md) — MESI、Snooping/Directory、False Sharing
- [DRAM and Memory System](/concepts/dram-memory-system.md) — Row Buffer、HBM、内存墙
- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) — 地址转换层
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — CPU vs WSE 能力矩阵
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — DRAM 带宽与 NoC
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — memory-bound decode
- [Reasoning Cliff](/concepts/reasoning-cliff.md) — KV/HBM 饱和
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — 片外 SSD/NVMe tier
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — load 全路径与 AMAT 层级（Day 22）

## LLM Prefix Cache 与 HBF 仿真（2026-09-28）

生产 LLM prefix cache 的访问节拍与 Web/块存储不同：[Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md) 显示 14 种「花哨」策略在命中率上难超 LRU，而 compute-aware（保护深前缀）才能把 TTFT/prefill 拉开（vLLM 实测平均 TTFT **−19.9%**）。共封装 HBF 则需要页/通道级模型：[HBF-Sim](/papers/hbfsim-extensible-hbf-simulator.md) 把 GPU cache-line 与 NAND page 闭合仿真（媒体吞吐最高 **15.94×**）。


## KV Cache Memory Wall SoK（2026-09-29）

[The KV Cache Is the New Memory Wall](/papers/kv-cache-new-memory-wall-sok.md) 给出上下文相关算术强度与 H100/B200/MI300X 拓扑下的 traffic **crossover**（Llama-3-70B BF16：b=1 → 427.2k；b=32 → 13.4k tokens），并统一量化/淘汰/分页/前缀/分层五域；与 [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md) 的前缀生产实证互补。

[RR-Evict](/papers/rrevict-prefix-cache-eviction-agentic.md) 指出 agentic 前缀匹配造成 **recency synchronization**，节点级 LRU 会整轨迹清空；round-robin 尾块淘汰相对 LRU 把 P99 TTFT / P99 uncached tokens 最高压到 **−75.4% / −65.7%**（vs completion-aware LRU 最高 **−46.9% / −30.6%**），与 [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md) 的「花哨难超 LRU」形成 **agentic 工况反例**。[SpecStream](/papers/specstream-resource-efficient-speculative-decoding.md) 在投机路径上只卸荷已提交历史并以流式块服务 verification；[SPIMOE](/papers/spimoe-hybrid-sparsity-reasoning-moe-pim.md) 在异构 PIM 上做物理 KV block 淘汰服务长推理。


## Janus SSD 稀疏 KV 与 SPLASH 布局（2026-10-01）

[Janus](/papers/janus-agentic-ssd-sparse-kv.md) 把 agentic 稀疏注意力的 KV 中心放到 **SSD**：用模型 indexer 提前预测选择，使关键路径 SSD I/O **<6.5%** append-prefill，TTFT 最高 **1.57–3.69×**（均值 **1.22–1.85×**）——与 RR-Evict/Fancy 的 DRAM 前缀策略互补，主攻 **介质带宽×选择时机**。[SPLASH-layouts](/papers/splash-switching-parallel-layouts-attention.md)（异文于 HBF-SPLASH）不改介质，而用 **DOP** 释放 KV 容量（相对 DP-attn **+27–60%**）并热切换并行布局。


## HBF 扩容与写寿命（2026-10-02）

[Characterizing HBF](/papers/characterizing-hbf-llm-serving.md) 在 agentic 高吞吐设定下量化：HBF 不是被动溢出层——**准入缓冲**把设备命中与写放大绑在一起（10% 余量 → 写 **−69%**，寿命 **4.77→14.82 年**）；与 [Hot–Cold](/papers/hotcold-hbm-hbf-agentic-llm.md)/[HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md) 的放置策略互补。

# Citations

[1] [raw/articles/arch-study-30d-day-13.md](raw/articles/arch-study-30d-day-13.md) — H&P Ch.2 存储层次（Day 13）
[2] [raw/articles/arch-study-30d-day-14.md](raw/articles/arch-study-30d-day-14.md) — AMAT 与 Cache 优化（Day 14）
[3] [raw/articles/arch-study-30d-day-15.md](raw/articles/arch-study-30d-day-15.md) — TLB 与访存路径（Day 15）
[4] [raw/articles/arch-study-30d-day-17.md](raw/articles/arch-study-30d-day-17.md) — DRAM/HBM（Day 17）
[5] [raw/articles/arch-study-30d-day-20.md](raw/articles/arch-study-30d-day-20.md) — SSD/NVMe（Day 20）
[6] [arXiv:2609.28870](https://arxiv.org/pdf/2609.28870) — Fancy Eviction
[7] [arXiv:2609.29246](https://arxiv.org/pdf/2609.29246) — HBF-Sim
[8] [arXiv:2609.30854](https://arxiv.org/pdf/2609.30854) — KV Cache Memory Wall SoK
[7] [arXiv:2609.32278](https://arxiv.org/pdf/2609.32278) — RR-Evict
[8] [arXiv:2609.33184](https://arxiv.org/pdf/2609.33184) — SpecStream
[9] [arXiv:2609.34612](https://arxiv.org/pdf/2609.34612) — SPIMOE
[10] [arXiv:2609.36938](https://arxiv.org/pdf/2609.36938) — Janus
[11] [arXiv:2609.37626](https://arxiv.org/pdf/2609.37626) — SPLASH-layouts
[12] [arXiv:2609.39131](https://arxiv.org/pdf/2609.39131) — Characterizing HBF
