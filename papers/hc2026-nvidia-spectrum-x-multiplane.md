---
type: Paper
title: "Hot Chips 2026: NVIDIA Spectrum-X Multiplane"
description: NVIDIA — Ethernet multiplane 把 8k→512k GPU 不必再加第三层；8 planes × 4 rails；故障检测 2.68 ms
tags:
- nvidia
- scale-out
- fabric
- switch
- topology
- congestion-control
- cpo
- optical
- interconnect
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

五张专用网，不是一张织物。对照 [Multi-plane Clos](/concepts/multi-plane-clos-topology.md)。SuperNIC 一处写 **1.6T**、XGS 页 ConnectX-9 又写 **800 Gb/s**——两处都在幻灯上。

## 五网 / 增益

**scale-up NVLink**、**scale-out Spectrum-X**、**scale-across Spectrum-XGS**、**scale-in BlueField**、**context-scale** Vera BF4 storage。Spectrum-X：adaptive routing、拥塞控制、「jitter-free」；**102.4T** 交换机 + **1.6T** SuperNIC。

相对 OTS Ethernet：**1.6×** RDMA BW、**2.2×** multi-tenancy BW、**1.3×** lower jitter。DeepSeek V3 多作业训练 **1.9×**（另有单作业 **1.2×**）。Nemotron Ultra pretrain NCCL：Gradient AllReduce **2×**，Token Dispatch **2×**，Gradient ReduceScatter **3.5×**，Parallel MatMul **14×**。

Optics = 计算功耗的 **10%**。CPO + micro-ring modulator「in production」；**3D-stacked** SiPh on **TSMC Coupe**；**4×** fewer lasers、**5×** lower power、**10×** lower MTBI。

## Multiplane

Multi-rail 基线：**8k Rubin GPUs @ 1.6T** 每 GPU scale-out；**100T** 交换机当 **64 ports of 1.6T**，**4 rails**。

**Multiplane**：**512k Rubin GPUs @ 1.6T**；**100T** 交换机当 **512 ports of 200G**；**8 planes × 4 rails**。相对 8k multi-rail 图 **64×** 更多 GPU；相对传统多层 single-rail **1.7×** 更少 scale-out 交换机。

一 plane 宕，Multiplane 仍 **90%** RDMA BW，传统多层 **0%**。检测 **2.68 ms**（**400×** vs OTS **1080 ms**）；恢复 **100 ms**（**11×** vs **1080 ms**）；相对 OTS Ethernet multiplane **1.6×** AI-factory goodput。

Spectrum-XGS：**1.9×** 多站点性能；同页写交换机 **800 Gb/s per port | 102.4 Tb/s**。NVLink Fusion 旁注：每 XPU all-to-all **3.6 TB/s**，延迟 **3×** 更低，一域 **72** XPU。

五网记分牌：Scale-In **18×** services BW / **2×** storage accel；Scale-Up **10×** packet rate / **3×** lower latency；Scale-Out **1.6×** RDMA / **3×** lower jitter（与前面 **1.3×** jitter 并存）；Scale-Across **1.9×**；Context-Scale **5×** token throughput / **5×** power efficiency。

## 与 wiki 的关系

- [Multi-plane Clos Topology](/concepts/multi-plane-clos-topology.md) — 8 planes × 4 rails 工业点
- [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 五网里的 scale-up
- [NVIDIA BlueField-4](/papers/hc2026-nvidia-bluefield-4.md) — scale-in
- [NVIDIA CPO Roadmap](/concepts/nvidia-cpo-roadmap.md) — Coupe + micro-ring「in production」

# Citations

[1] [raw/papers/HC2026_NVIDIA_Spectrum_X_Multiplane.pdf](raw/papers/HC2026_NVIDIA_Spectrum_X_Multiplane.pdf) — Gilad Shainer, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-spectrum-x-multiplane.md](raw/papers/hc2026-nvidia-spectrum-x-multiplane.md) — 结构化摘录
