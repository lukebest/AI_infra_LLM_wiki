---
type: Raw Source
title: Hot Chips 2026 OpenAI Jalapeño
ingested: 2026-08-26
sha256: 1ae0e3aa6d80781e08609926b8161c171edc30ec36b88547a6bfed6b7ee5bcf8
venue: Hot Chips 2026
---

# OpenAI Jalapeño

**Speakers:** Richard Ho, Ravi Narayanaswami, Chris Leary（OpenAI）  
**PDF:** [HC2026_OpenAI_Jalapeno.pdf](HC2026_OpenAI_Jalapeno.pdf)  
**Venue:** Hot Chips 2026 Day 2

伙伴 Broadcom & Celestica。RTL→tapeout **9 months**。

## 摘录数字（仅幻灯片正文）

- Package TDP **700 W**。InferenceX 8k/1k、weight f4、按包 TDP 归一。
- GPT-OSS-120B vs GB200 STP：peak mixed TPS/kW **85,448 vs 44,960 (≈1.9×)**；e2e **1.03 vs 1.80 s**；min TBT **0.69 vs 1.87 ms**。
- DeepSeek R1 MXFP4 vs GB300 STP：**19,641 vs 11,781**；e2e **1.65 vs 5.99 s**；TBT **1.43 vs 5.90 ms**。
- Kimi K2.5 1T vs GB300 STP：**18,195 vs 11,862**；e2e **1.56 vs 5.31 s**；TBT **1.44 vs 5.48 ms**。
- 算力：mxfp8×mxfp8 **3.4 PF**；mxfp8×mxfp4 **6.7**；mxfp4×mxfp4 **13.4**。Memory **15.4 TB/s, 216 GiB**。
- SU：local **128 @ 600 GB/s**；global **2048 @ 200 GB/s**；半扁平两层 Clos，Broadcom TH6，8 rails。
- 2048-ASIC：**27 EF** mxfp4，**32 PB/s**，**432 TiB**。
