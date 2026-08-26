---
type: Paper
title: "Hot Chips 2026: Meta MTIA 400"
description: Meta — 5-chiplet 2.5D；288 GB HBM3E @ 9.4 TB/s；6 PFLOPS FP8 / 12 PFLOPS MX4；2D mesh + leaky-bucket；72 ASIC scale-up
tags:
- meta
- accelerator
- chiplet
- noc
- hbm
- scale-up
- rdma
- training
- inference
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Meta_MTIA_400.pdf
- raw/papers/hc2026-meta-mtia-400.md
---

# Meta’s Custom AI Silicon: From Recommendation to Dual-Mandate with GenAI

**Speakers:** Srinagesh Loke, Xing Cindy Chen, Jatinder Singh（Meta）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_Meta_MTIA_400.pdf](raw/papers/HC2026_Meta_MTIA_400.pdf)

双职责：DLRM 推理 + GenAI 训练。400 TDP **未知**。交叉 [HCCL / MTIA 300](/papers/hccl-meta-mtia-300-collective-communication.md)。

## 三代

| | MTIA 200 | MTIA 300 | MTIA 400 |
|--|----------|----------|----------|
| 年 | 2024（ISCA’25） | 2025（ISCA’26） | 2026+ |
| 角色 | 推理 | 第一颗 DLRM 训练芯 | DLRM 推理 + GenAI 训练 |
| 工艺 | **5 nm** | **3 nm** + HBM3E | 3 nm compute/SoC + I/O |
| 峰值 | **354 TOPS** | **1.12 PFLOPS FP8** | **3 / 6 / 12 PFLOPS**（FP16 / FP8 / MX4） |

300：HBM3E **216 GB @ 6.1 TB/s**；I/O **1.2 TB/s**；**72 PE** 排 **12×6**；**16 ME**；TDP **667 W**。相对「leading GPUs」：embedding fwd/bwd **1.87× / 1.88×**；1 MB P2P **1.5×**；SU **2.2×**。卖点相对 GPU：**>2x** bytes-to-FLOPS，对 TCO 不是对峰值 FLOPS。

## MTIA 400

**5-chiplet 2.5D**：**2** compute（3 nm, **1.7 GHz**）+ **1** SoC（3 nm, **1.5 GHz**）+ **2** I/O（RoCE SU/SO）+ **8** HBM3E。HBM **288 GB**，**9200 MHz**，peak **9.4 TB/s**。D2D：compute↔compute **1.3 TB/s**；compute↔SoC/I/O **1.2 TB/s**。Host：**4×16-lane PCIe Gen6**，**512 GB/s**。

每 compute chiplet：**8×6** active PE + 一行冗余；南边 **1×6 ME**。相对 300：**1.3×** PE、**4×** GEMM MAC 密度。GEMM 整个 **256×256** work unit 进 CREG。原生 OCP MX，**16 elements / shared exponent**（OCP 是 32）。MX4 = **2× FP8** 吞吐。新增水平 reduction（LayerNorm / SoftMax / RMSNorm）。

相对 300：HBM 容量 **1.3×**、BW **1.5×**；I/O 仍 **1.2 TB/s**。相对 200：**15.4×** FP16、**46×** DRAM BW、**16×** host PCIe。

NoC：**2D mesh** + 多 VC。拥塞控制：**leaky buckets** + **Max OT**。集体：**12 ME/device**（每 compute 6），RISC-V。NMC：**128 B/cycle** DMA + streaming reduction。Scale-up RDMA **1.2 TBps**；scale-out 经 PCIe switch **100 GB/s**。

系统：**4× MTIA 400 / compute tray**；scale-up 域 **72 ASICs**。下一步无数字：450 / 500。

## 与 wiki 的关系

- [HCCL / MTIA 300](/papers/hccl-meta-mtia-300-collective-communication.md) — 300 的 ME/NMC 集体；400 仍是 1.2 TB/s SU，ME 变成 12/device
- [Meta RDMA](/papers/rdma-over-ethernet-meta-training.md) — 主机 RoCE 运维对照
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — leaky-bucket 2D mesh vs 片上 in-network 算术
- [AMD Helios UALoE](/papers/hc2026-amd-helios-ualoe.md) — 同是 72 加速器以太网 scale-up

# Citations

[1] [raw/papers/HC2026_Meta_MTIA_400.pdf](raw/papers/HC2026_Meta_MTIA_400.pdf) — Loke / Chen / Singh, Hot Chips 2026
[2] [raw/papers/hc2026-meta-mtia-400.md](raw/papers/hc2026-meta-mtia-400.md) — 结构化摘录
