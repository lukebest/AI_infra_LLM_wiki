---
type: Paper
title: "Scaling Inference Prefill with High-Radix Photonic Interconnects"
description: 3D 光子 scale-up（4× BW、1152 radix）量化 MoE prefill；高 batch 2.1–3.2×、跨 pod 边界生产平台 2.2–4.5×（分析模型）
tags:
- photonic
- optical
- cpo
- lightmatter
- interconnect
- scale-up
- fabric
- moe
- llm
- inference
- prefill
- disaggregated-inference
- serving
- architecture
- 3d
- packaging
- latency
- throughput
- batching
timestamp: '2026-09-04T00:00:00Z'
created: 2026-09-04
updated: 2026-09-04
sources:
- raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf
- raw/papers/scaling-inference-prefill-photonic.md
---

# Scaling Inference Prefill with High-Radix Photonic Interconnects

**Authors:** Arulselvan Madhavan, Peter Carson, Taylor Groves, Thomas Graham
**Affiliation:** 文内未另标；以 [Lightmatter Passage](https://lightmatter.co/products/passage/) 作 3D 光子带宽/radix/能耗参考点（不直接仿真厂商产品）
**arXiv:** [2609.01821](https://arxiv.org/abs/2609.01821)（2026-09-01，cs.DC / cs.AR）
**Venue:** 预印本
**PDF:** [raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf](raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf)

与 [晶圆级光互连热调谐](/papers/wafer-scale-optical-interconnect-moe-thermal.md) 同属光子 MoE 互连线：那篇盯 **训练 EP All-to-All 的 MRR 热 stall**；本文盯 **推理 prefill 的 scale-up pod 边界与集体带宽**。对照 [NVIDIA CPO Roadmap](/concepts/nvidia-cpo-roadmap.md) 的 NVL576/1152 与 [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) 的机柜铜域。

## 动机

- 推理已占算力周期 **80–90%**；agentic coding 中位初始上下文 ~**96K** tokens，近半请求 >128K。
- Prefill 大批次抬高 TP all-reduce、EP all-to-all、SP all-gather 流量；通信可占 prefill **>50%**（带宽受限 GPU 上 TP **>65%**）。
- 铜：224G 被动 reach ~**1 m**，448G 数十 cm → 高带宽 scale-up 困在单机柜（~**72–144** GPU）；跨机柜被迫走慢 scale-out。

## 方案

1. **成本模型**：XLA/MLIR 走生产级 TP/EP/CP 划分，捕获集体与 compute–通信重叠延迟。
2. **模型**：Mini **21B** / R1 变体 **42B** / Next **201B** active（MLA）；R1 为 mesh 整除略放大 (~+14% 参数)。FP4/FP8。
3. **电学基线**（Table III）：B200 / B300 / Rubin / R4†（R4 为路线图外推）；SU 带宽 900–1800 GB/s uni.，SU 最大 72 或 576。
4. **光学配对**：同算力/HBM；SU 带宽 **4×**（保守下界，文称 Passage >64 Tb/s bi-dir vs Blackwell 14.4 Tb/s）；最大光学 pod **1152** GPU；链路 ~**4.3 pJ/bit**。
5. **扫描**：device sweep（固定总 token ~8M）与 batch sweep；上下文 1K / 8K / 128K / 1M。
6. **DES 校验**：72 GPU 解耦 serving——6×8-GPU prefill worker + 1×24-GPU decode；Poisson λ=250；ISL 8192 / OSL 1024。

## 效果（仅论文数字）

**摘要归纳：** 高 batch 应力 **2.1–3.2×** 延迟改善；通信受限配置 **2.8–5.8×**；电学跨 pod 边界时生产平台 **2.2–4.5×**。

**B300 FP4 × R1（正文叙述）：**

| 上下文 | 代表倍数 | 备注 |
|--------|----------|------|
| 1K | ~**2.58×**（device sweep 最佳） | 大批次通信主导 |
| 8K | ~**2.21×** | batch 2048：电学通信 40.6 s vs 算力 16.8 s；光学通信 10.2 s |
| 128K | ~**2.93×** @288 GPU | 电学通信 35.5 s → 光学 2.3 s；B200/Rubin ~4.3–5.8× |
| 1M | ~**2.27×** @1152 | 电学通信 39.2 s → 光学 1.6 s；重叠 27.5 s |

**Table IV 结构（FP4 热图）：** 算力越快、越易通信受限 → 光学倍数越大；跨电学 SU pod 边界时跳变最大。Rubin@128K/288 可达 ~**5.5–5.8×**；R4@1M/1152 可达 ~**8.0–8.5×**（投机配置）。

**DES（交互小 batch）：** p99 TTFT **−12–20%**（concurrency 2048：29.4→25.8 s；6144：81.8→65.5 s）。故意单 decode worker → p99 TPOT **+77–110%**；E2E 近中性（−1 至 −5%）。光学是 **TTFT/输入吞吐杠杆**，E2E 取决于 decode 共设计。

**局限（作者自述）：** 分析扩展 XLA 成本模型 + 投影光学层；未建模额外链路延迟/热/TCO；非已部署光子硬件实测。

## 与 wiki 的关系

- [Wafer-scale optical MoE thermal](/papers/wafer-scale-optical-interconnect-moe-thermal.md) — 训练侧热 stall；本文推理 prefill + 多机柜 radix
- [NVIDIA CPO Roadmap](/concepts/nvidia-cpo-roadmap.md) — NVL576/1152 CPO 与文中 1152 光学 pod 同量级叙事
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 电学 72-GPU 铜域即本文基线边界
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — 同谈 scale-up 域放大的通信税；本文加带宽/radix 维
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — §V-E DES 用 PD 解耦布局量化光学→TTFT 传导
- [Mozart](/papers/mozart-35d-wafer-scale-moe-training.md) / [Network-on-Wafer](/concepts/network-on-wafer.md) — 晶圆/3.5D 训练；本文是机柜外光学 scale-up

## 开放问题

1. 真实 3D 光子原型上的 TTFT/功耗/热是否贴近 4× 理想带宽假设？
2. Prefill 光学加速如何与 decode 侧 HBM 带宽共设计，避免 TPOT 反噬？
3. 与 wafer-scale 光 NoW（热调谐篇）叠加时，哪一层该先上光学？

# Citations

[1] [raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf](raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf) — Madhavan et al., arXiv:2609.01821
[2] [raw/papers/scaling-inference-prefill-photonic.md](raw/papers/scaling-inference-prefill-photonic.md) — 结构化摘录
