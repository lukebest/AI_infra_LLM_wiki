---
type: Raw Source
title: Hot Chips 2026 NVIDIA RISC-V CPUs and NVLink Fusion
ingested: 2026-08-26
sha256: 19f5ef4adf0ee02d91dcee964f481321a5c163c0d79b1c16c0a49136438898b0
venue: Hot Chips 2026 Tutorial
---

# RISC-V CPUs in NVIDIA Servers（Hot Chips Tutorial Part III）

**Speaker:** Frans Sijstermans（NVIDIA）  
**PDF:** [HC2026_NVIDIA_RISC-V_NVLink_Fusion.pdf](HC2026_NVIDIA_RISC-V_NVLink_Fusion.pdf)  
**Venue:** Hot Chips 2026 Tutorial Part III

后半是 NVL72 + NVLink Fusion + CHI。无新的 HBM/封装数字。前半 CUDA 软件可少写。

## 摘录数字（仅幻灯片正文）

- ACPI **6.6**（**2025-05** 批准）+ RISC-V BRS（**2025-08** RVI 批准）。
- Vera Rubin：**七颗芯片、五机柜**。NVL72：单 **72 GPU** L1 domain，全铜。**9** switch tray × **4** NVLink 6 switch/tray = **36** switch；**28.8 TB/s per switch tray**。**18** compute tray × **4 Rubin GPU** + **2 Vera CPU**/tray。**3.6 TB/s per GPU**；**900 GB/s CPU–GPU**（NVLink-C2C）。
- Custom CPU：C2C + **~88 PCIe lanes**；CHI ports；SPECrate 2026 integer **400**；Memory **1 TB/s, 1 GB capacity**（1 GB 按幻灯片照抄，是否笔误未知）；L1 **64+64 kB**、L2 **1 MB**、L3 **100 MB**。
- PCIe P2P：**128-byte** 包全速。
