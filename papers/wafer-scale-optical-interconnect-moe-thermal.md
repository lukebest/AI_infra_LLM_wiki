---
type: Paper
title: "Thermal Tuning Overhead in Wafer-Scale Optical Interconnects for LLM MoE Training"
description: Georgia Tech — 晶圆级 DWDM MRR 的热光 stall；铁电调谐在四层 proxy 上 Mixtral/Qwen-MoE/LLaMA-MoE 相对热光 2.7×/3.8×/3.3×
tags:
- now
- network-on-wafer
- wse
- photonic
- optical
- cpo
- wdm
- interconnect
- hybrid-bonding
- 3d
- packaging
- moe
- training
- llm
- architecture
- fabric
- scale-up
timestamp: '2026-08-27T00:00:00Z'
created: 2026-08-27
updated: 2026-08-27
sources:
- raw/papers/Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf
- raw/papers/wafer-scale-optical-interconnect-moe-thermal.md
---

# Thermal Tuning Overhead in Wafer-Scale Optical Interconnects for LLM MoE Training

**Authors:** Seongwon Yoon, Pin-Jun Chen, Shimeng Yu  
**Affiliation:** Georgia Institute of Technology  
**arXiv:** [2608.24637](https://arxiv.org/abs/2608.24637)（2026-08-25）  
**Venue:** 预印本。文内未另报会议。  
**PDF:** [raw/papers/Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf](raw/papers/Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf)

## 中文摘要

MoE 训练的 EP All-to-All 把 scale-up 带宽推到电学 I/O 边长墙之外。作者给 300 mm **光 interposer**（多层 SiN X–Y、O-E-O 中继）建了一个跨层模型：FlexFlow 任务图 → 功率轨迹 → Ansys 瞬态热（OIO3D 参数）→ MRR 失谐 stall → ht-sim。热光环跟踪只有 **0.0625 K/ms**，PIC 冷却斜率到 **0.18–0.21 K/ms**，每个 All-to-All 突发平均 stall **~47–49 ms**。铁电 HZO/LN 开关约 **10 ns**。四层 proxy 上去掉 stall：Mixtral 8×7B **2.7×**、Qwen-MoE 14.3B **3.8×**、LLaMA-MoE 6.7B **3.3×**。这不是新拓扑论文，是证明 **调谐延迟比名义带宽更先卡住** 晶圆级光 NoW。

这不是 [Iff WoW](/papers/network-design-wafer-scale-wow-hybrid-bonding.md) 的电学重叠网，也不是 [Mozart](/papers/mozart-35d-wafer-scale-moe-training.md) 的 NoP-Tree。物理是 **chiplet-on-photonic-interposer**。

## Motivation

- EP dispatch/combine 可占迭代 **1/3–1/2**。
- 电学带宽跟芯片周长走，算力跟面积走。
- MRR+DWDM 密度高，但共振对温度 **<1 K** 量级敏感；热光环是 µs–ms。

## Approach

1. **封装**：GPU/HBM die + EIC + PIC 先 **W2W hybrid bonding**，再 **D2W** 接到 300 mm 无源 SiN interposer。垂直 evanescent coupler。
2. **NoW**：多层 SiN，正交方向分层，减少交叉；reticle 拼接波导。中继是 **O-E-O**，不用片上 MZI 交换/光 crossbar。
3. **带宽账**：32 Gb/s × 32 λ = **1.024 Tb/s/波导**。目标 **1.5 TB/s**（12 Tb/s，对标 Dojo 级电学）→ **N_λ = 375**、**N_WG = 12**（12.288 Tb/s）、端点 **750** MRR（或按满槽 **768**）。
4. **规模**：每 wafer **4×4** GPU + **16** 内存 reticle。DP=2 时 Mixtral **256** GPU / **16** wafer，Qwen-MoE **512** / **32**，LLaMA-MoE **128** / **8**。功率按 H100 80 GB 剖面映射到 **700 W** XPU。
5. **Stall 链**：T(t) → Δλ_th = 80 pm/K · ΔT → 跟踪环 0.0625 K/ms → 残差超 FWHM 的 10%（19.4 pm）即通信 stall。注入是**每个 All-to-All 一次**，不是每包传播延迟。
6. **铁电**：HZO 栅 + LN 波导 Pockels；开关 **5.4 ns**、饱和 **~10 ns**；90 °C 仍保留 >85% 极化。

## Results（仅 PDF）

| 项 | Mixtral 8×7B | Qwen-MoE 14.3B | LLaMA-MoE 6.7B |
|----|--------------|----------------|----------------|
| EP / 专家数 | 8 / 8 | 64 / 64 | 16 / 16 |
| 稳态 stall 均值 | **48.7 ms**（14–79） | **46.8 ms**（6.0–55.2） | **47.4 ms**（14.5–79） |
| 四层 proxy 相对热光 | **2.7×** | **3.8×** | **3.3×** |
| 最大冷却斜率 | −0.177 K/ms | −0.177 K/ms | −0.209 K/ms |
| 无 stall makespan（四层，400 Gbps 对照里自家设计） | 1089.5 ms | 710.0 ms | 422.5 ms |

无 stall 时自家晶圆光网并不无条件赢：LLaMA-MoE 相对电学 fat-tree **1.7×**；Mixtral/Qwen-MoE 慢于 flat all-to-all。大倍数来自**去掉 stall**，不是拓扑本身。全文层数（24/32）热 stall 更长（Mixtral **173.9 ms**），但包级仿真 50 min–4.7 h 没跑完。铁电循环：10^6 iteration 约 **3–6×10^6** 次，低于文献 125 °C 下 **10^7** 次。

**仿真。** 功率分数是 roofline 假设，不是实测功耗轨迹。四层 proxy 数字不要当成全文训练。

## 和 wiki 已有概念的关系

- [Network-on-Wafer](/concepts/network-on-wafer.md) — 第四条物理近亲：光 interposer + 拼接 SiN，不是 field stitch / 电学 WoW。
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — W2W HB（GPU–EIC–PIC）+ D2W 到光 interposer。
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP All-to-All 被 MRR 热 stall 卡住。
- [Mozart](/papers/mozart-35d-wafer-scale-moe-training.md) — 电学 3.5D 树压 All-to-All；本文是光层调谐。
- [Iff WoW](/papers/network-design-wafer-scale-wow-hybrid-bonding.md) — 电学放置即拓扑。
- [Fovea](/papers/fovea-physical-implication-aware-wafer-scale-dse.md) — 电学 D2D 可行域。
- SCHEMA 已有 `lightmatter` / `celestial-ai` / `cpo`：文内当工业动机引用，不是评测对象。

## 开放问题

1. 全文层数没有端到端倍数。
2. 铁电 MRR 阵列、串扰、写入电压未做系统集成。
3. DyPNet-MSC 类可重构光子 NoW 仍未对照。
4. O-E-O 中继的延迟/能量未单独拆。

# Citations

[1] [raw/papers/Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf](raw/papers/Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf) — Yoon, Chen, Yu, arXiv:2608.24637
[2] [raw/papers/wafer-scale-optical-interconnect-moe-thermal.md](raw/papers/wafer-scale-optical-interconnect-moe-thermal.md) — 结构化摘录
