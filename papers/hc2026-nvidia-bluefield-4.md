---
type: Paper
title: "Hot Chips 2026: NVIDIA BlueField-4"
description: NVIDIA — AI DPU 7200 Gb/s；Astra 把多 CX-9 接到一颗 Grace；KV G1–G4 + G3.5 CMX
tags:
- nvidia
- storage
- interconnect
- fabric
- kv-cache
- rdma
- rack
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_NVIDIA_BlueField_4.pdf
- raw/papers/hc2026-nvidia-bluefield-4.md
---

# NVIDIA BlueField-4 Processor Powers the AI Factory

**Speaker:** Idan Burstein（NVIDIA）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_NVIDIA_BlueField_4.pdf](raw/papers/HC2026_NVIDIA_BlueField_4.pdf)

七芯片五机柜里的 **scale-in / storage / security** 处理器。小包图表逐点 **未知**。对齐 [Spectrum-X](/papers/hc2026-nvidia-spectrum-x-multiplane.md) 与 [Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md)。

## 硅

「Cloud DPU」**200 Gb/s** vs 「AI DPU」**7200 Gb/s**。BlueField-4 = **Grace** + **ConnectX-9** + **Astra**。

- Grace：SPECINT **220 (6× BF3)**；LPDDR5 **275 GB/s**；**64** Arm Neoverse V2 @ **1.7 GHz**
- ConnectX-9：**800G** Ethernet（2× BF3）；200G PAM4；PCIe Gen6 x16；Spectrum-X RDMA / MRC / RoCE / PRDMA；inline PSP/TLS/IPsec/AES-XTS；**200 MPPS**；**25 MIOPs**

Vera Rubin compute tray：4× **1.6 Tb/s** GPU scale-out + **800 Gb/s** GPU scale-in = **7200 Gb/s**。传统「每 GPU 一颗 CX-9 + 一颗 BF4」要么不隔离 scale-out，要么 **4×** 功耗。**Astra** 把多 CX-9 接到一颗 Grace。

实测平均 BW 随 NIC 线性到 **7.0 Tb/s @ 8 NIC**。NVMe-oF：**8 cores / 1.6 Tb/s**；**16 cores / 20 M IOPS**。Spectrum-X vs OTS Ethernet 存储：5/10/50 GB 文件 **1.3× / 1.4× / 1.5×**。

**Storage-Scale**（Vera CPU + CX-9）：**3.2 Tb/s**；×10 IOPS；×5 efficiency。KV 分层：G1 GPU HBM；G2 系统内存；G3 本地存储；**G3.5 CMX** on scale-in；G4 冷/共享 KV。

## 与 wiki 的关系

- [NVIDIA Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) — 同工厂 scale-in
- [Spectrum-X Multiplane](/papers/hc2026-nvidia-spectrum-x-multiplane.md) — 五张网记分板
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — KV 分层是另一条容量出路

# Citations

[1] [raw/papers/HC2026_NVIDIA_BlueField_4.pdf](raw/papers/HC2026_NVIDIA_BlueField_4.pdf) — Burstein, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-bluefield-4.md](raw/papers/hc2026-nvidia-bluefield-4.md) — 结构化摘录
