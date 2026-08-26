---
type: Raw Source
title: Hot Chips 2026 NVIDIA Spectrum-X Multiplane
ingested: 2026-08-26
sha256: 47096d3db57c490dcea55129ad3ebad1ae95c21db2f15d38f499bd94a54f263a
venue: Hot Chips 2026
---

# NVIDIA Spectrum-X Ethernet Multiplane Network Architecture

**Speaker:** Gilad Shainer（NVIDIA）  
**PDF:** [HC2026_NVIDIA_Spectrum_X_Multiplane.pdf](HC2026_NVIDIA_Spectrum_X_Multiplane.pdf)  
**Venue:** Hot Chips 2026 Day 2

ConnectX-9 同时出现 800G 与 1.6T SuperNIC 两种写法。

## 摘录数字（仅幻灯片正文）

- 五张网：SU NVLink / SO Spectrum-X / scale-across Spectrum-XGS / scale-in BlueField / context-scale STX。
- 相对 OTS Ethernet：**1.6×** RDMA BW；**2.2×** multi-tenant BW；**1.3×** 更低 jitter。
- Multi-rail：**8k** Rubin @ 1.6T；100T switch = 64×1.6T，4 rails。
- Multiplane：**512k** Rubin @ 1.6T；100T = 512×200G；**8 planes × 4 rails**。相对 8k 图 **64×** GPU；相对传统多层单轨少 **1.7×** SO switch。
- 一 plane 挂：仍 **90%** RDMA BW vs 传统 **0%**。检测 **2.68 ms (400×)**；恢复 **100 ms (11×)**。
- CPO：微环，TSMC Coupe 3D-stacked SiPh；少 **4×** 激光、**5×** 功耗、**10×** MTBI。
