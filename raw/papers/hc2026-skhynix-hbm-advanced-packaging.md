---
type: Raw Source
title: Hot Chips 2026 SK hynix HBM Advanced Packaging
ingested: 2026-08-26
sha256: 746358d7203ede9d1293ec5a157369b885f31ece8a19a1c1c78d058d074f91b6
venue: Hot Chips 2026 Tutorial
---

# Advanced Packaging for High Bandwidth Memory (HBM)

**Speaker:** Jaesik Lee（SK hynix America，VP of Package Engineering）  
**PDF:** [HC2026_SK_hynix_HBM_Advanced_Packaging.pdf](HC2026_SK_hynix_HBM_Advanced_Packaging.pdf)  
**Venue:** Hot Chips 2026 Tutorial

相对倍率（0.5× gap、0.40× 热阻）保留原文，不换算成绝对 μm。

## 摘录数字（仅幻灯片正文）

- HBM2E / HBM3 / HBM3E / HBM4：Density **16 / 16 / 24 / 24 Gb**；Capacity **16 / 24 / 36 / 36 GB**；I/O **1024 / 1024 / 1024 / 2048**；IO Speed **3.6 / 5.6 / 8 / 8 Gbps**；Max BW **460 / 717 / 1024 / 2048 GB/s**；PKG **10×11 / 11×11 / 11×11 / 12.4×11**。
- HBM4 另一页：**>2 TB/s**；**40+% lower power efficiency**（原文用词）；热阻比 HBM3E 好 **14+%**；容量最高 **48 GB**（**12Hi 量产，16Hi under Qual**）；Z **775 μm**；平面 **12.8×11 mm²**；**16148** base micro-bumps；**>20K** TSVs。
- GDDR6 ×12 = **24 GB / 768 GB/s** vs HBM3E ×4 = **144 GB / 4 TB/s**，面积 **-50%**。能效归一：DDR4 **1.0**，GDDR6 **0.82**，HBM3 **0.33**，HBM3E **0.29**。
- 12Hi→16Hi：封装高 **720 → 775 μm**；chip thickness **1.0× → 0.9×**；gap-height **1.0× → 0.5×**；bump pitch **1.0× → 0.9×**。
- HyB：室温 SiO₂–SiO₂ + **>200 °C** Cu–Cu；同限高下 core die 可厚最多 **24%**（20Hi vs 20Hi）；pitch **below <18 μm**；相对热阻约 **0.40×**。
- i-HBM 热阻 **>30%** ↓。Samsung HPB+HCB：~**30%** 温度 ↓、热阻抗 **16%** ↑（原文）。Micron 能效 **>20%** ↑（SK 引公开源）。
- Power TSVs：**75% PDN improvement**（ISSCC 2024）。
