---
type: Paper
title: "Hot Chips 2026: NVIDIA Spectrum-X Multiplane"
description: NVIDIA — 8k→512k Rubin @ 1.6T；8 plane × 4 rail；一 plane 挂仍 90% RDMA；检测 2.68 ms
tags:
- nvidia
- scale-out
- fabric
- switch
- congestion-control
- cpo
- photonic
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_NVIDIA_Spectrum_X_Multiplane.pdf
- raw/papers/hc2026-nvidia-spectrum-x-multiplane.md
---

# NVIDIA Spectrum-X Ethernet Multiplane Network Architecture

**Speaker:** Gilad Shainer（NVIDIA）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_NVIDIA_Spectrum_X_Multiplane.pdf](raw/papers/HC2026_NVIDIA_Spectrum_X_Multiplane.pdf)

五张专用网，不是一张布。ConnectX-9 同时出现 **800 Gb/s** 与 **1.6T SuperNIC** 两种写法。对照 [BlueField-4](/papers/hc2026-nvidia-bluefield-4.md)。

## 五张网

Scale-up **NVLink**；scale-out **Spectrum-X**；scale-across **Spectrum-XGS**；scale-in **BlueField**；context-scale Vera BF4 storage。Spectrum-X：自适应路由、拥塞控制、「jitter-free」；**102.4T** switch + **1.6T** SuperNIC。

相对 OTS Ethernet：**1.6×** RDMA BW；**2.2×** multi-tenant BW；**1.3×** 更低 jitter。NCCL（Nemotron Ultra pretrain）：Gradient AllReduce **2×**；Token Dispatch **2×**；ReduceScatter **3.5×**；Parallel MatMul **14×**。

光学 = 计算功耗的 **10%**。CPO 微环「in production」；**3D-stacked** SiPh on **TSMC Coupe**；少 **4×** 激光、**5×** 功耗、**10×** MTBI。

## Multiplane

Multi-rail 基线：**8k** Rubin @ **1.6T**/GPU；100T switch = **64 ports of 1.6T**，**4 rails**。

**Multiplane**：**512k** Rubin @ 1.6T；100T = **512 ports of 200G**；**8 planes × 4 rails**。相对 8k 图 **64×** GPU；相对传统多层单轨少 **1.7×** SO switch。一 plane 挂：仍 **90%** RDMA BW vs 传统多层 **0%**。检测 **2.68 ms (400× vs OTS 1080 ms)**；恢复 **100 ms (11×)**。

记分板：Scale-In **18×** services BW / **2×** storage；Scale-Up **10×** packet rate / **3×** 更低延迟；Scale-Out **1.6×** RDMA；Scale-Across **1.9×**。NVLink Fusion 旁注：**3.6 TB/s** per-XPU all-to-all。

## 与 wiki 的关系

- [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — SU 仍是 NVLink
- [Multi-plane Clos](/concepts/multi-plane-clos-topology.md) — 8-plane Ethernet 工业落地
- [BlueField-4](/papers/hc2026-nvidia-bluefield-4.md) — scale-in
- [Thor Ultra](/papers/hc2026-broadcom-thor-ultra.md) — 商用 NIC 也喷 8 plane

# Citations

[1] [raw/papers/HC2026_NVIDIA_Spectrum_X_Multiplane.pdf](raw/papers/HC2026_NVIDIA_Spectrum_X_Multiplane.pdf) — Shainer, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-spectrum-x-multiplane.md](raw/papers/hc2026-nvidia-spectrum-x-multiplane.md) — 结构化摘录
