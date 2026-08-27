---
type: Paper
title: "Maia 200: A Software Defined Dataflow System for Large-scale AI Acceleration"
description: Microsoft 归档全文 — SDLA 数据流；ATLv2 接收端驱动；Hamming Mesh 20+8 / 4 plane 到 6144；8 芯 Allgather 78%/94% SoL；GNoC multicast
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
- llm
- moe
- protocol
- transport
- mesh
timestamp: '2026-08-27T00:00:00Z'
created: 2026-08-27
updated: 2026-08-27
sources:
- raw/papers/Maia_200_Software_Defined_Dataflow_2026.pdf
- raw/papers/maia-200-sdla.md
- papers/hc2026-microsoft-maia-200.md
---

# Maia 200: A Software Defined Dataflow System for Large-scale AI Acceleration

**Authors:** Sherry Xu, Marco Heddes, Jackson Peng, Tom Savell, Monica Tang, Prashant Ranjan, Jesse Benson, Ofer Dekel, Saurabh Dighe, Anupama Kurpad, Artour Levin, Matthew Mattina, George Petre, Cheng Tang, Yuan Yu, Li Zhang, Torsten Hoefler  
**Affiliation:** Microsoft  
**arXiv:** [2608.24664](https://arxiv.org/abs/2608.24664)（2026-08-25 15:05 UTC）  
**Venue:** 预印本。文内未另报会议。Hot Chips 2026 幻灯是另一来源，见 [HC Maia 200](/papers/hc2026-microsoft-maia-200.md)。  
**PDF:** [raw/papers/Maia_200_Software_Defined_Dataflow_2026.pdf](raw/papers/Maia_200_Software_Defined_Dataflow_2026.pdf)

本页只写**全文相对幻灯多出来的架构事实**。峰值 TOPS、HBM 7 TB/s、28×400、750 W、TSMC 3 nm、CoWoS-S、FCQ/6k 口号等已在幻灯页，不重复。

## 中文摘要

Maia 200 把控制流和数据流拆开（SDLA）：程序员/编译器显式编排 DMA、信号量和专用 SRAM，而不是 SIMT warp。片上 4 cluster × 9/10 tile，GNoC 做组播；片外 **28×400G** ANC 跑 **ATLv2**（接收端驱动 RDMA）。拓扑是 Hamming Mesh 特例：**20** 条盘内固定链路 + **8** 条接到 **4** plane 交换网，设计点 **6144** SoC。8 芯 Allgather 到延迟界 **78%** / 带宽界 **94%** SoL。

## Motivation

LLM 推理（含 MoE）是数据搬运问题：decode 吃 KV 带宽，MoE 要运行时 All-to-All，SLA 约 **300–4000 ms** TTFT、**20–30 ms**/token。SIMT 把 DMA 藏在 firmware；SDLA 把数据路径当成可编程 ISA。

## Approach（全文增量）

1. **SDLA / DISA**：宏指令带最多 **2** 个前置 + **2** 个后置 semaphore；控制用 C/C++（NEPAL），数据路径异步跑在前。
2. **存储**：不用 cache 当主路径。论文引用 cache tag/映射约 **30–35%** 面积能量、延迟 **+10–15%**。Maia SRAM 占 die **<20%**。每 tile **3 MiB** 操作数 SRAM；TTU **65,536** FP4 MAC/cycle，2 GHz 时每操作数输入约 **2024 GiB/s**。
3. **层次 NoC**：Tile 1D mesh + Cluster NoC + **GNoC**（数据/控制逻辑拆分、QoS、组播到全体 cluster）。
4. **ATLv2**：PFC 以太 L2；L3 IP；端到端 AES-GCM-256；ECMP + UDP 源端口熵；REPS 式回收好路径；selective retransmit。接收端先把收地址控制消息发给发送端，再 RDMA Write；ANC 不缓存 payload。优化 **>4 KiB** 消息。ANC 可远程 semaphore++、远程 GNoC broadcast。
5. **拓扑**：2×2 1D Hamming Mesh + 盘上交叉全连接。28 ANC 里 20 固定、8 交换（4 plane × 2×400G）。T0 **51.2T** / 128×400G：48 SoC（12 tray）×2 链路，余 32 口上 T1，过订阅 **1:3** → **48×128 = 6144**。南北固定 **300 GB/s**、东西/对角 **350 GB/s**，可用交换侧 **50 GB/s** 补齐到四向 **350 GB/s**、合计 **1.4 TB/s** 平衡带宽。
6. **集体**：先实现 direct-connect（深度 1）和 ring；库按尺寸选。小消息交换路径约 **4 µs**。

## Results（仅全文）

| 项 | 数字 |
|----|------|
| 6144-chip 系统 | **62** exaflop/s FP4；**43 PiB/s** 内存；**8.6 PiB/s** Ethernet |
| 内部相对机队其他加速器 | TCO **−30%**；能量 **−15%** |
| 晶体管 / die | **>140B**；**26×33 mm** |
| 9 tile/cluster @ 2 GHz | BF16 **1180** Tflop/s；FP8 **4785** Tflop/s |
| BF16 GEMM（6143 尺寸） | 计算界最高 **99.69%** 峰值；>**90%** 当计算量 >58 Tflop；存储界最高 **51.4%** 峰值带宽 |
| FP8 GEMM | 计算界 **96%**；存储界 **56%** |
| 8 芯 Allgather | 延迟界 **78%** SoL；带宽界 **94%** SoL |
| Qwen 2.5 7B decode | 权重 **14.14 GiB**；KV @16,384 token = **939.52 MiB**；未融合 PyTorch **2434** token/s（>**70%** 估计上限） |
| 成本结构 | 网络 **<20%** 系统成本 |

**生产硅 + Azure 机队。** 集体只报 8 芯；没有与外部 GPU 的官方对照表。幻灯 **<1 µs** P2P mem2mem 与全文 **~4 µs** 小消息交换路径不是同一指标。

## 和 wiki 的关系

- [HC Maia 200](/papers/hc2026-microsoft-maia-200.md) — 幻灯来源；峰值 TOPS/HBM/FCQ 在那边
- [MRC](/entities/mrc.md) — 全文写 ATLv2 影响 Ultra Ethernet / AI Base profile
- [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md) — 另一家的包内 NIC 集体；Maia 是 Ethernet ANC + MCCL
- [AMD Helios UALoE](/papers/hc2026-amd-helios-ualoe.md) — 以太网 load-store scale-up 对照
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — Allgather SoL
- [Layout-Aware NoC](/concepts/layout-aware-noc-flexible-dataflow.md) — GNoC 组播
- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — ATLv2 在传输层
- [Cerebras WSE](/entities/cerebras-wse.md) — 文内把 WSE 标成 LSLA，不是 SDLA

## 开放问题

1. 6144 规模没有 All-to-All / MoE dispatch 实测，只有 8 芯 Allgather。
2. 幻灯 SRAM **272 MB @ 80 TB/s** 未在全文复述；tile **3 MiB** 与幻灯总量对不上，不要混用。
3. NEPAL / 软件栈细节本文刻意不写。

# Citations

[1] [raw/papers/Maia_200_Software_Defined_Dataflow_2026.pdf](raw/papers/Maia_200_Software_Defined_Dataflow_2026.pdf) — Xu et al., arXiv:2608.24664
[2] [raw/papers/maia-200-sdla.md](raw/papers/maia-200-sdla.md) — 结构化摘录
[3] [papers/hc2026-microsoft-maia-200.md](papers/hc2026-microsoft-maia-200.md) — Hot Chips 2026 幻灯页
