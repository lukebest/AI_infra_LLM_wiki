---
type: Raw Source
title: Hot Chips 2026 NVIDIA Vera CPU
ingested: 2026-08-26
sha256: d9510bbefdc9f4df9d3e6548268a5327ccb1a5755f0c5912b267b2408bd1a222
venue: Hot Chips 2026 Conference
---

# NVIDIA Vera CPU

**Speakers:** Jonathon Evans, Polychronis Xekalakis（NVIDIA）  
**PDF:** [HC2026_NVIDIA_Vera.pdf](HC2026_NVIDIA_Vera.pdf)  
**Venue:** Hot Chips 2026 Conference

## 摘录数字（仅幻灯片正文）

- **88** Olympus / **176** threads。AgentX 30X unofficial。
- SCF **164 MB L3** / **3.4 TB/s** bisection。**1.5 TB SOCAMM LPDDR5X @ 1.2 TB/s**。BW/W **5X** vs 16-ch DDR5-8000。
- NVLink-C2C **1,800 GB/s**。PCIe Gen6 x16 **256 GB/s**，**CXL 3.1**。Aggregate off-die **4.3 TB/s**。
- SPECrate vs EPYC 9755：Python **1.8X**；gcc/cppcheck/llvm/gem5 **1.7X**。
- Spatial MT：loaded per-core traditional **67%** vs Vera **100%**。SPECint Rate-1 峰约 **13.0**。
- NVL72：**72** GPU + **36** Vera + **18** BF4。独立架 **256 Veras / 22,528 Olympus**。GHz / TDP 未知。
