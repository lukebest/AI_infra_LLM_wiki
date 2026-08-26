---
type: Paper
title: "Hot Chips 2026: Broadcom Thor Ultra"
description: Broadcom — 800G NIC；eRoCE = MRC++；packet spray 最多 8 planes；RCCC；RDMA write 781 Gbps（97.6%）
tags:
- broadcom
- rdma
- scale-out
- congestion-control
- protocol
- interconnect
- switch
- fabric
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Broadcom_Thor_Ultra.pdf
- raw/papers/hc2026-broadcom-thor-ultra.md
---

# Thor Ultra Ethernet NIC for AI and HPC Markets

**Speaker:** Hemal Shah（Broadcom，Distinguished Engineer）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_Broadcom_Thor_Ultra.pdf](raw/papers/HC2026_Broadcom_Thor_Ultra.pdf)

商家 800G NIC。对照 [MRC](/entities/mrc.md) 与同日 [Helios UALoE](/papers/hc2026-amd-helios-ualoe.md) / [Maia ATL](/papers/hc2026-microsoft-maia-200.md)。

## 硅 / 端口

**800G** NIC：host **PCIe Gen6 x16**，**SR-IOV 256 VFs**；网络 **8× 100G PAM4/NRZ** SerDes。端口：OSFP112 **1×800 / 2×400 / 4×200 / 8×100**；双 QSFP112 **2×400 / 4×200 / 8×100**。DAC / LPO / AEC / optics；风冷或液冷。

芯片：**5 nm**，**2.4B+** 晶体管，封装 **27×27**，最大芯片功耗 **40–42 W**；板（不含光学）**50–55 W**。板型：PCIe CEM **HHHL** 和 OCP NIC 3.0 **TSFF**。

## eRoCE = MRC++

**64K+ QPs**；packet spray + OOO placement；可靠性（SACK/NACK、选择重传、path probe）；**receiver-credit congestion control (RCCC)** 作基线 + P4-like 可编程 CC；遥测 ECN / packet trim / CSIG。

Multipath：每 QP 或每包 header entropy；交换机 LB：ECMP / E-ECMP / DLB flowlet / DLB spray；NIC 可跨 **最多 8 planes** spray。OOO：Write & Read response 可乱序落位（Write-with-Imm 保序）；Send / Read Request / Atomic 保序。

RCCC：接收端给活跃发送端分配 credit；投机 credit 拉满起步。Peer memory：远端走 eRoCE，本机 P2P 走 Linux **dma-buf**。

## 集体 / 线速

集体（Gen5 GPU 平台：2 nodes，**8 GPU/node**，**16 ranks**，**16×400G** 上交换机），bus BW vs 天花板：all_gather **381.92 GB/s @ 8 GB**（ceil **400**）；all_reduce **383.93 @ 2 GB**（**400**）；alltoall **84.62 @ 8 GB**（**93**）；reduce_scatter **380.23 @ 2 GB**（**400**）— 「**>96%** for gather/reduce/reduce_scatter。」软件：upstream verbs + xCCL 插件（NCCL / RCCL / MPI）。

TCP（Gen6 CPU）：单向 **791 Gbps** @ 16 flows = **98.9%** of 800G；双向 **~1.51 Tbps**。RDMA write：单向 **781 Gbps**（**97.6%** of 800G）；双向 **1558 Gbps**（**97.9%** of **1.6 Tb/s**）；**32 KB** 已到线速约 **88%**，**128 KB** 距峰值约 **3%**。

## 与 wiki 的关系

- [MRC](/entities/mrc.md) — eRoCE 自称 MRC++
- [NVIDIA Spectrum-X Multiplane](/papers/hc2026-nvidia-spectrum-x-multiplane.md) — 另一条最多 8-plane Ethernet
- [AMD Helios UALoE](/papers/hc2026-amd-helios-ualoe.md) — Vulcano 也跑 MRC；Helios 交换是 Broadcom
- [Resilient AI Supercomputer Networking](/papers/resilient-ai-supercomputer-networking-mrc-srv6.md) — MRC 生产叙事

# Citations

[1] [raw/papers/HC2026_Broadcom_Thor_Ultra.pdf](raw/papers/HC2026_Broadcom_Thor_Ultra.pdf) — Hemal Shah, Hot Chips 2026
[2] [raw/papers/hc2026-broadcom-thor-ultra.md](raw/papers/hc2026-broadcom-thor-ultra.md) — 结构化摘录
