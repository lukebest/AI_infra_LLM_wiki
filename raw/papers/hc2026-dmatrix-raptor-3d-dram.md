---
type: Raw Source
title: Hot Chips 2026 d-Matrix Raptor 3D DRAM
ingested: 2026-08-26
sha256: 3d01855bb13cbf4cc29e39b63655514628fd2e2a5b55c12870aeca4b8a01f3f0
venue: Hot Chips 2026 Tutorial
---

# Raptor: The First 3D-DRAM Accelerator for Generative Inference

**Speakers:** Sudeep Bhoja（d-Matrix, Co-founder & CTO）；Aayush Ankit（Meta；标注 work done while at d-Matrix）  
**PDF:** [HC2026_dMatrix_Raptor_3D_DRAM.pdf](HC2026_dMatrix_Raptor_3D_DRAM.pdf)  
**Venue:** Hot Chips 2026 Tutorial  
**Paper pointer:** Raptor paper: ISCA 2026

Model Details 表是图，容量分解未知。不写招聘。

## 摘录数字（仅幻灯片正文）

- **64 users × 1M context ≈ 935 GB KV**。
- SRAM 对照：BW **300 TB/s**，容量 **4 GB**，延迟 **~1 ns**，I/O **~0.5 pJ/bit**；bitcell **~0.021 μm²**；成本 **100× DRAM**。
- HBM4 实用上限 **~20 TB/s**（Vera Rubin、MI 455）。**2.4 pJ/bit × 100 TB/s = 1.92 kW**。
- 1-Hi、logic-on-top、功率密度 **≤0.5 W/mm²** → 液冷 DRAM **<100 °C**。
- 3D vertical IO **0.3–0.4 pJ**；HBM4 system **2.5 pJ + 3 pJ (on chip)**；约 **~10×** 低于 HBM。
- **1-Hi 32 GB/card** × **72 cards** 声称装下 Kimi K3 @ 1M context；协调 **8K virtual devices** vs 典型 GPU **~72**。
- 封装：top TSMC **N4**（热页 **N4P**），**36 μm F2F**；路线图 hybrid bonding **<2 μm pitch、8-high**。
- **840 banks/chiplet**（72 spare → 768）对 **256 ch**；I/O **100 TB/s × 0.37 pJ/bit = 296 W**；stream flipping 省 **20%** I/O，开销 **0.8%**。
- Tj **105 °C**；retention **32 ms@85 °C → 4 ms**（**8×** refresh）；**~700 TSV/mm²**。
- 硅面积归一：Raptor Capacity **11.4 MB/mm²**、BW **32.6 GB/s/mm²**、Power **2.96 mW/GB/s** vs HBM4 24 Gb **21.9 / 1.67 / 40.0**。自称 **≈20×** BW/mm²、**13.5×** 更好 mW/GB/s。
- 服务口号：**~1000 TPS/User**，3T 级、**1M context**。
