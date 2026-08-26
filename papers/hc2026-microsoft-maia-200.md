---
type: Paper
title: "Hot Chips 2026: Microsoft Maia 200"
description: Microsoft — SDLA 推理芯；FP4 10,145 TOPS；HBM 216 GB @ 7 TB/s；Ethernet-ATL <1 µs；自称影响 UET / MRC
tags:
- microsoft
- accelerator
- inference
- dataflow
- noc
- hbm
- scale-up
- fabric
- rdma
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Microsoft_Maia_200.pdf
- raw/papers/hc2026-microsoft-maia-200.md
---

# Maia 200 — Data Center Scale AI Accelerator (Software Defined Dataflow)

**Speakers:** Prashant Ranjan, Jackson Peng, Torsten Hoefler（Microsoft）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_Microsoft_Maia_200.pdf](raw/papers/HC2026_Microsoft_Maia_200.pdf)

Azure 推理压 $/token 与 W/token。架构类 **SDLA**（Software Defined Local Access Dataflow）：显式 SW 编排、控制/数据流分离。Kernel roofline 逐点 **未知**（图、无表）。

## SoC

Dense tensor TOPS：**FP4 10,145** / **FP8 5,072** / **BF16 1,268**。HBM **7 TB/s**，**6** stacks，**216 GB**。SRAM **272 MB @ 80 TB/s**。Host **PCIe Gen6 x8**，**64 GB/s**。Backend 网：**1,400 GB/s** 单向，**28×400**。Die **~820 mm²**，package **75×75**，TDP（provision）**750 W**，TSMC **3 nm**，CoWoS-S。

存储：tile L1 TSRAM、cluster L2 CSRAM、chip HBM。层级 **GNOC** 做片内 multicast/broadcast。Tile：**TTU**（矩阵/卷积，FP8/FP6/FP4 block-scaled）、**TVP**（可编程 SIMD）、**TCP**（控制 + semaphore）。HW 队列最多 **3** pre- 和 **3** post-semaphore。

## ATL / 机柜

自定义嵌入式 AI NIC **ANC** + Ethernet scale-up 传输 **ATL**：端点控 multipath（packet spray、负载均衡、OOO receiver）、HW 快速故障检测/恢复、E2E 加密。**<8 pJ/b**，**<1 µs** P2P 单向 mem2mem。幻灯写 ATL 影响 **UET** 与 **MRC** 标准化。

Tray **FCQ**：**4** 加速器固定 Ethernet 全连接（无交换机）做 TP AllGather/AllReduce。之上一条 Ethernet/ATL，两层 unified Clos，口号 **chip → 6k accelerator cluster**。软件 **MCCL**（non-blocking MPI）。

集体按尺寸自适应：broadcast（小）/ hierarchical（中）/ ring（大）。Attention：FlashAttention 风格 QK block；交错 **2** tensor + **2** SIMD。Kernel 结果「as of June 2026」：FP8×FP8 与 FP4×FP4 GEMM TP=1；fused SDPA FA2；AllReduce BF16 TP8 与 AllToAll TP8。

## 与 wiki 的关系

- [MRC](/entities/mrc.md) — 幻灯自称 ATL 影响 MRC / UET
- [AMD Helios UALoE](/papers/hc2026-amd-helios-ualoe.md) — 另一条以太网 load-store scale-up
- [Layout-Aware NoC](/concepts/layout-aware-noc-flexible-dataflow.md) — GNOC 广播 vs flexible interconnect
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — MCCL 尺寸自适应集体

# Citations

[1] [raw/papers/HC2026_Microsoft_Maia_200.pdf](raw/papers/HC2026_Microsoft_Maia_200.pdf) — Ranjan / Peng / Hoefler, Hot Chips 2026
[2] [raw/papers/hc2026-microsoft-maia-200.md](raw/papers/hc2026-microsoft-maia-200.md) — 结构化摘录
