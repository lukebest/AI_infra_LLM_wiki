---
type: Raw Source
title: Hot Chips 2026 Intel Crescent Island
ingested: 2026-08-26
sha256: ecbdfdc88d3821e9441e3b99495ef0383c229fa8a7e1d7b1d50f93d9296976fb
venue: Hot Chips 2026 Conference
---

# Intel Crescent Island — GPU Designed for Agentic AI Inference

**Speakers:** Sumit Mohan, Dr. Hong Jiang（Intel）  
**PDF:** [HC2026_Intel_Crescent_Island.pdf](HC2026_Intel_Crescent_Island.pdf)  
**Venue:** Hot Chips 2026 Conference

片上标签是 Memory Fabric / 32 MB L2，不是 packet NoC。

## 摘录数字（仅幻灯片正文）

- Intel 卡 **160 GB LPDDR5x**；ODM 上限 **480 GB**。**350 W** 风冷 PCIe。Xe **3p**。
- **32** Xe-cores / **256 XMX**；每核 **8 XVE + 8 XMX**；XMX **16-deep**；**32 MB** unified L2；**PCIe Gen5 x16** switch fabric。
- vs Xe2：GRF **1 MB**（原 512 KB）；L1$/SLM **512 KB**（原 256 KB）；FP64 **64 FMA/XeCore**（原 8）。
- SpecBundle τ：Qwen3-Next-80B-A3B **4.04**；Kimi K2 1T **4.29**；Qwen3-Coder-480B **4.94**；Qwen3-235B **2.90**。树加倍买 **1.39×** token。
- Llama 2 70B → Kimi K2 1T：bytes held **7.5×**，bytes read/token **4.4×** less。峰值 TOPS / LPDDR GB/s / 工艺未知。
