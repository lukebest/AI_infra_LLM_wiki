---
type: Raw Source
title: Thermal Tuning Overhead in Wafer-Scale Optical Interconnects for LLM MoE
source_url: https://arxiv.org/abs/2608.24637
arxiv: '2608.24637'
ingested: 2026-08-27
sha256: 35b2cf90bf584f435c28fe3c772e53fff77b96542d4673931229f4e3fd9d0cb2
---

# Thermal Tuning Overhead in Wafer-Scale Optical Interconnects for LLM MoE Training

**Authors:** Seongwon Yoon, Pin-Jun Chen, Shimeng Yu  
**Affiliation:** Georgia Institute of Technology  
**PDF:** [Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf](Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf)  
**arXiv:** [2608.24637](https://arxiv.org/abs/2608.24637)  
**Submitted:** 2026-08-25 14:48 UTC

## 问题

晶圆级 DWDM 光互连用 MRR，热光调谐跟不上 MoE 训练引起的瞬态温漂，通信阶段反复 stall。

## 方法要点

- 300 mm 光 interposer：GPU 居中、HBM 外围；多层 SiN X–Y 网格；O-E-O 中继，不做片上全光交换。
- 每 reticle：W2W hybrid bonding 把 GPU/HBM + EIC + PIC 叠起来，再 D2W 接到光 interposer。
- 每波长 **32 Gb/s** × **32** λ/波导 = **1.024 Tb/s/波导**；目标 die-to-die **1.5 TB/s** → **12** 波导、**375** λ、端点 **750** MRR。
- 热：Ansys 瞬态 + Coenen OIO3D 参数；ht-sim 包级网；铁电 HZO/LN 替代热光。

## 摘录数字（仅 PDF/HTML）

- 四层 proxy 去掉热光 stall 相对热光：Mixtral 8×7B **2.7×**、Qwen-MoE 14.3B **3.8×**、LLaMA-MoE 6.7B **3.3×**。
- 稳态 stall 均值：Mixtral **48.7 ms**、Qwen-MoE **46.8 ms**、LLaMA-MoE **47.4 ms**。
- PIC 冷却斜率最大约 **0.18–0.21 K/ms** vs 热光跟踪 **0.0625 K/ms**。
- 铁电开关 **5.4 ns** / 饱和约 **10 ns**。
- 每 wafer **4×4** GPU + **16** 内存 reticle；Mixtral **256** GPU / **16** wafer。
- XPU 峰值按 **700 W**；tile **25×25 mm²**。
- **仿真，不是硅。** 四层 proxy；全文层数的包级仿真未跑完。
