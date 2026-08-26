---
type: Paper
title: "Hot Chips 2026: NVIDIA BlueField-4"
description: NVIDIA — AI DPU 7200 Gb/s；Astra 把多颗 CX-9 挂一颗 Grace；NVMe-oF 8 cores / 1.6 Tb/s；Storage-Scale 3.2 Tb/s
tags:
- nvidia
- scale-out
- interconnect
- fabric
- rack
- rdma
- storage
- protocol
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

Vera Rubin 七芯片五机柜里的 **scale-in** / 存储 / 安全处理器。本甲板没有 Spectrum-X 那张五网 **18× / 2×** 记分牌。线性扩展图各 NIC 计数精确 Tb/s **未知**。

## 硅

「Cloud DPU」**200 Gb/s** vs「AI DPU」**7200 Gb/s**。可插拔 PCIe 卡 vs 系统级共设计。

**Grace**：SPECINT **220**（**6× BF3**），LPDDR5 **275 GB/s**，**64** Arm Neoverse V2 **@ 1.7 GHz**，PCIe + **Astra**。**ConnectX-9**：**800G** Ethernet（**2× BF3**），**200G PAM4** SerDes，**PCIe Gen6 x16**，Spectrum-X RDMA / **MRC** / RoCE / PRDMA，inline PSP/TLS/IPsec/AES-XTS，**200 MPPS**，**25 MIOPs**。

Vera Rubin compute tray：**4× 1.6 Tb/s** GPU scale-out + **800 Gb/s** GPU scale-in = **7200 Gb/s** 每 tray（另一页写「Every compute tray needs **7Tb/s**」）。传统「每 GPU 一颗 CX-9 + 一颗 BF4」要么 scale-out 不隔离，要么「每 NIC 一颗 DPU」功耗 **4×**。**Astra** 把多颗 CX-9 挂到一颗 Grace。

## 存储 / KV

BF4 Grace 上 NVMe-oF：**8 cores for 1.6 Tb/s**；**16 cores for 20 M IOPS**；口号「**2x** faster data access for Rubin GPUs」。Spectrum-X vs OTS Ethernet 存储访问：**5 / 10 / 50 GB** 文件分别 **1.3× / 1.4× / 1.5×**。

**Storage-Scale**（Vera CPU + CX-9）：**3.2 Tb/s** storage access，**×10** IOPS，**×5** efficiency。KV 分层：G1 GPU HBM（active）、G2 system memory（staging/spill）、G3 local storage（warm reuse）、**G3.5 CMX** 走 scale-in、G4 cold/shared KV。

## 与 wiki 的关系

- [NVIDIA Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) — 七芯片五机柜里的 STX / scale-in
- [NVIDIA Spectrum-X Multiplane](/papers/hc2026-nvidia-spectrum-x-multiplane.md) — 五张专用网；本页只扛 scale-in
- [MRC](/entities/mrc.md) — CX-9 列 Spectrum-X RDMA / MRC / RoCE
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — NVMe-oF 与 KV spill

# Citations

[1] [raw/papers/HC2026_NVIDIA_BlueField_4.pdf](raw/papers/HC2026_NVIDIA_BlueField_4.pdf) — Idan Burstein, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-bluefield-4.md](raw/papers/hc2026-nvidia-bluefield-4.md) — 结构化摘录
