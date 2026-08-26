---
type: Raw Source
title: Hot Chips 2026 Pistil 20-Chiplet SLM SiP
ingested: 2026-08-26
sha256: 963a5ca3b46d6829b0c0e544331ae5aade20ecdf8214da34b9898d872570bc8a
venue: Hot Chips 2026 Poster
---

# Pistil: A 16-nm Accelerator Co-Designed with a 20-Chiplet 2.5D System-in-Package Architecture for Distributed Small Language Model Inference at the Edge

**Orgs:** Harvard University + Google LLC + Lockheed Martin  
**Equal contrib.:** Nestor Cuevas & Matthew Adiletta；David Brooks, Gu-Yeon Wei  
**PDF:** [HC2026_Pistil_20_Chiplet_SLM.pdf](HC2026_Pistil_20_Chiplet_SLM.pdf)  
**Venue:** Hot Chips 2026 Poster

边缘 SLM，不是 datacenter HBM。板级速率未知。

## 摘录数字（仅海报正文）

- **16 nm**；**4** Pistil compute + **16** RPC-DRAM = **20** chiplet。
- 总 DRAM **512 MB**；modeled 总 DRAM BW **51.2 GB/s**。模型上限 **1B** 参数。
- flower：每颗 compute 被 **4** 颗 RPC-DRAM 包围。
- 实测（dense SLM，**4-bit**，vs Jetson Nano 8GB）：**80–250 tokens/s**；吞吐最高 **7.6×**；decode **>98%** 峰值内存带宽；能量/token **5.0–7.8×** 更低。
- 轻量 Arm Cortex-M55；无共享地址空间。
