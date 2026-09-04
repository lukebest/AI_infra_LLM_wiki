---
type: Concept
title: NVIDIA CPO Roadmap
description: NVIDIA CPO 用于 scale-up 的路线图：Rubin NVL576 测试 → Feynman NVL1152 volume
  ramp
tags:
- nvidia
- cpo
- optical
- photonic
- scale-up
- fabric
timestamp: '2026-05-08T00:00:00Z'
created: 2026-05-08
updated: 2026-09-04
sources:
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
- raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf
---

# NVIDIA CPO Roadmap（Co-Packaged Optics）

NVIDIA 在 GTC 2026 公布了 CPO 用于 scale-up 网络的路线图。核心原则：**copper where possible, optics where necessary**。

## Rubin 世代

| 系统 | 规模 | Scale-up 方式 |
|------|------|---------------|
| NVL72 | Oberon × 1 | All copper |

## Rubin Ultra 世代

| 系统 | 规模 | Scale-up 方式 |
|------|------|---------------|
| NVL72 | Oberon × 1 | All copper |
| NVL144 | Kyber × 1 | All copper |
| NVL288 | Kyber × 2 | Copper（含 rack-to-rack copper backplane） |
| NVL576 | Oberon × 8 | Copper rack 内 + **CPO rack 间**（两层 all-to-all） |

- NVL576 为低产量测试用途
- Blackwell NVL576 原型 "Polyphe" 使用 pluggable optics → BOM 成本过高，TCO 不合理
- Rubin Ultra NVL576 转向 CPO

## Feynman 世代

| 系统 | 规模 | Scale-up 方式 |
|------|------|---------------|
| NVL72 | Oberon × 1 | All copper |
| NVL144 | Kyber × 1 | All copper |
| NVL1152 | Kyber × 8 | Copper rack 内 + **CPO rack 间** |

- NVL1152 为首个大规模 CPO volume ramp
- 独立量化：[Photonic Prefill](/papers/scaling-inference-prefill-photonic.md) 用 **1152** GPU 全光 scale-up 扫 MoE prefill（1K–1M），相对电学跨 pod 边界给出 **2.2–4.5×** TTFT 向延迟改善（分析；Passage 作参考点）
- GPU-to-NVSwitch 仍为 copper POR（448G SerDes 挑战 + 制造/成本/可靠性考量）
- 路线图距量产仍多年，可能继续变化

## 技术约束

- **448G uni-di SerDes**：shoreline、reach、power 均有挑战，vs die-to-die optical engine 更优
- **但制造、成本、可靠性**使得 copper-to-switch 仍为必要
- CPO 首先用于 switch-to-switch（rack 间），非 GPU-to-switch

## 相关页面
- [Kyber Rack](/entities/kyber-rack.md) — Kyber rack 架构（CPO 的主要载体）
- [Nvidia Vera Rubin Nvl72](/entities/nvidia-vera-rubin-nvl72.md) — Oberon rack
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPX rack

# Citations

[1] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
[2] [raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf](raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf) — arXiv:2609.01821；1152 光学 pod prefill
