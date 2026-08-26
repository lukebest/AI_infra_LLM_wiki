---
type: Paper
title: "Hot Chips 2026: NVIDIA RISC-V CPUs and NVLink Fusion"
description: NVIDIA — Vera Rubin NVL72 全铜 72 GPU L1；3.6 TB/s per GPU、900 GB/s C2C、28.8 TB/s/switch tray；Fusion 让 custom CPU 经 CHI 进 NVLink
tags:
- nvidia
- scale-up
- interconnect
- fabric
- gpu
- cpu
- isa
- architecture
- chiplet
- switch
- protocol
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_NVIDIA_RISC-V_NVLink_Fusion.pdf
- raw/papers/hc2026-nvidia-riscv-nvlink-fusion.md
---

# RISC-V CPUs in NVIDIA Servers（Hot Chips Tutorial Part III）

**Speaker:** Frans Sijstermans（NVIDIA）  
**Venue:** Hot Chips 2026 Tutorial Part III  
**PDF:** [raw/papers/HC2026_NVIDIA_RISC-V_NVLink_Fusion.pdf](raw/papers/HC2026_NVIDIA_RISC-V_NVLink_Fusion.pdf)

不是 RISC-V ISA 课。后半是 NVL72 + NVLink Fusion + CHI 一致性，给自定义 CPU 进 NVIDIA scale-up。前半 CUDA 软件从简。无新的 HBM/封装数字。更新既有 [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) 与 [Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md)。

## 两平台

CUDA 与 **NVLink Fusion**。CUDA 侧要求 RISC-V 跟 **RVA23 / BRS / Server SOC / Server Platform**；CUDA 特有要求「mostly related to data movement between memories」，细则对 partner 开放。

RISC-V 服务器规格的价值：RVA23 二进制兼容；V/B 扩展；可发现可选特性。ACPI 6.6（**2025-05** 批准）+ RISC-V BRS（**2025-08** RVI 批准）被标成 CUDA port 的关键依赖。

CUDA 数据路径：

1. **PCIe I/O coherence** —— 免去频繁 cache flush/invalidate，降延迟、卸 CPU；称其他现代服务器 CPU 大多已有。
2. **PCIe P2P**（多 GPU 设备内存互拷）。要求：多种 RC/EP 拓扑；**128-byte** 包全速；RC 保持标准 PCIe ordering。

## Vera Rubin / NVL72

Vera Rubin 被写成 full-stack AI factory：**七颗芯片、五机柜** —— Vera Rubin NVL72、Groq 3 LPX、Vera CPU Rack、Vera BlueField-4 STX Storage、Spectrum-6 SPX Networking。角色：foundation / interactivity / tool-call sandboxes / context memory / scale-out fabric。对照 [Groq 3 LPX](/entities/nvidia-groq-3-lpx.md)。

NVL72（可读数字）：

- 单 **72 GPU** L1 domain，**全铜**。
- **9** 个 switch tray × **4** NVLink 6 switch/tray = 图示 **NVLink Switch 1…36**；**28.8 TB/s per switch tray**。
- **18** compute tray × **4 Rubin GPU** + **2 Vera CPU**/tray。
- **3.6 TB/s per GPU**；**900 GB/s CPU–GPU**（经 **NVLink-C2C**）。
- 每 GPU 旁一颗 **NVLink Fusion chiplet**。
- NIC/DPU：ConnectX + BlueField，N/S 与 E/W 两套网。

## Fusion 变体

同一 72-XPU L1，CPU 可以是 Vera **或 custom CPU**（PCIe / NVLink-C2C）；XPU 可以是 Rubin **或 custom XPU**。数字重复：3.6 TB/s per XPU、900 GB/s CPU–XPU、28.8 TB/s/switch tray。

Custom CPU 集成：软 IP + PHY；片上 **C2C HUB** 连 **NVLink-C2C PHY**；CPU 侧 **CHI ports** 进 fabric。**Unified Memory**：GPU 与 CPU 看全部内存，一致性协议 **CHI**。

Fusion 对自定义 CPU 的要求：CUDA 全套 + 高速互连 **C2C, ~88 PCIe lanes** + DOCA / NCCL + 与 NVIDIA 紧密合作。例规（原文）：SPECrate 2026 integer **400**；Memory **1 TB/s, 1 GB capacity**（1 GB 按幻灯片照抄，是否笔误 **未知**）；Cache L1 **64+64 kB**、L2 **1 MB**、L3 **100 MB**。强调系统级能效比裸 SPEC 重要。

收束：RISC-V 作为 x86/Arm 之外的服务器 CPU 选项；RVA23 硅已有；RISE 推软件。

## 与 wiki 的关系

- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — Hopper/Blackwell 固定 fat-tree；本文补 Rubin 代 NVLink 6 / Fusion chiplet / CHI
- [NVIDIA Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) — 实体页；本文给出 3.6 TB/s、900 GB/s C2C、28.8 TB/s/tray
- [NVIDIA NVLink Hopper Blackwell](/papers/nvidia-nvlink-hopper-blackwell.md) — 上一代摘要
- [Cerebras WSE](/entities/cerebras-wse.md) — 对照：单晶圆 mesh，无 NVSwitch
- [Network-on-Wafer](/concepts/network-on-wafer.md) — NVL72 是机柜级铜域，不是 WoW

# Citations

[1] [raw/papers/HC2026_NVIDIA_RISC-V_NVLink_Fusion.pdf](raw/papers/HC2026_NVIDIA_RISC-V_NVLink_Fusion.pdf) — Frans Sijstermans, Hot Chips 2026 Tutorial Part III
[2] [raw/papers/hc2026-nvidia-riscv-nvlink-fusion.md](raw/papers/hc2026-nvidia-riscv-nvlink-fusion.md) — 结构化摘录
