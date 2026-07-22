---
type: Entity
title: NVIDIA Vera Rubin NVL72
description: NVIDIA Vera Rubin GPU 系统，含 NVL72/144/288/576/1152 系统谱系
tags:
- nvidia
- gpu
- accelerator
- training
- inference
- scale-up
timestamp: '2026-05-08T00:00:00Z'
created: 2026-04-16
sources:
- raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
---

# NVIDIA Vera Rubin NVL72

NVIDIA Vera Rubin 平台的核心 GPU 系统。72 个 Rubin GPU 通过 NVLink 互联。通用 AI 工作负载（训练 + 推理），与 [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) 组成异构推理架构。

## 角色
- AI factory 的通用工作马（training + inference）
- 处理 prefill 和 decode attention
- 高吞吐、高并发服务

## 与 LPX 的分工
- GPU：prefill + decode attention（memory-bandwidth 密集）
- LPU：FFN / MoE expert（compute 密集、延迟敏感）
- 两者共同扩展 Pareto 前沿

## NVL 系统谱系

### Rubin
- **NVL72**：Oberon × 1，all copper scale-up

### Rubin Ultra
- **NVL72**：Oberon × 1，all copper
- **NVL144**：[Kyber Rack](/entities/kyber-rack.md) × 1，all copper（144 GPU/rack，4 GPU + 2 CPU/blade，72 NVLink 7 switch）
- **NVL288**：Kyber × 2，copper（含 rack-to-rack copper backplane，供应链探索中，未官方发布）
- **NVL576**：Oberon × 8，copper rack 内 + **CPO rack 间**（低产量测试）

### Feynman
- **NVL72**：Oberon，all copper
- **NVL144**：Kyber，all copper
- **NVL1152**：Kyber × 8，copper rack 内 + **CPO rack 间**（首次大规模 CPO volume ramp）

详见 [Nvidia Cpo Roadmap](/concepts/nvidia-cpo-roadmap.md)

## Kyber Rack 更新（GTC 2026）

相比 GTC 2025 原型，主要变化：
- Compute blade 密度翻倍：4 GPU + 2 CPU（原 2+2）
- 36 blades / rack（原 4 canisters × 18）
- Switch blade 高度翻倍：6 NVLink 7 switch / blade
- 12 switch blades / rack = 72 NVLink 7 switch
- 每 GPU 14.4 Tbit/s uni-di scale-up（80DP connector, 72 DP used × 200G bi-di）
- Copper flyover cable 连接 switch 到 midplane

详见 [Kyber Rack](/entities/kyber-rack.md)

## 相关页面

- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — Hopper/Blackwell NVLink 机制（paper-deepdive Day 8）
- [TPU v4 OCS Reconfigurable Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) — Google 可重构对照
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — 异构推理搭档
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构推理概念
- [Kyber Rack](/entities/kyber-rack.md) — Kyber rack 架构
- [Nvidia Cpo Roadmap](/concepts/nvidia-cpo-roadmap.md) — CPO 路线图
- [Vera Etl256](/entities/vera-etl256.md) — Vera CPU 独立 rack

# Citations

[1] [raw/articles/nvidia-groq3-lpx-blog-2026-04.md](raw/articles/nvidia-groq3-lpx-blog-2026-04.md)
[2] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
