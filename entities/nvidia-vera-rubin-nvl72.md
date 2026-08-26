---
type: Entity
title: NVIDIA Vera Rubin NVL72
description: NVIDIA Vera Rubin GPU 系统；HC2026 第一手：NVLink 6 3.6 TB/s、七芯片五机柜、Vera C2C 1.8 TB/s
tags:
- nvidia
- gpu
- accelerator
- training
- inference
- scale-up
timestamp: '2026-08-26T00:00:00Z'
created: 2026-04-16
updated: 2026-08-26
sources:
- raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
- raw/papers/hc2026-nvidia-rubin.md
- raw/papers/hc2026-nvidia-vera.md
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

## Hot Chips 2026（第一手幻灯片）

[NVIDIA RISC-V / Fusion](/papers/hc2026-nvidia-riscv-nvlink-fusion.md) 教程：单 72 GPU 全铜 L1；18 compute tray × 4 Rubin + 2 Vera；9 switch tray × 4 NVLink 6；**3.6 TB/s per GPU**、**900 GB/s** C2C、**28.8 TB/s**/switch tray。Fusion 允许 custom CPU/XPU（CHI）。

[Rubin GPU](/papers/hc2026-nvidia-rubin.md) Day1：七芯片五机柜（NVL72 / LPX / Vera CPU / BF4 STX / Spectrum-6）。NVLink 6 **3.6 TB/s per GPU all-to-all**；相对 Ethernet **3×** 更低延迟、**130 TFLOPS** in-network、**10×** packet rate。**Counted Write** 替换 MEMBAR+atomic。**2:4 sparsity**。**100 MW factory**（不是单卡）：NVFP4 **2 ZFLOPS** 推理 / **1.4 ZFLOPS** 训练；HBM4 **11 PB / 800 PB/s**。单卡 HBM4/TDP **未知**。AgentX **30×** 标 Unofficial。

[Vera CPU](/papers/hc2026-nvidia-vera.md)：NVL72 **72 GPU / 36 CPU**；**NVLink-C2C 1,800 GB/s**；SCF **3.4 TB/s**；**1.5 TB SOCAMM LPDDR5X @ 1.2 TB/s**；**CXL 3.1**。独立液冷架 **256 Veras / 22,528 Olympus**（对照 [Vera ETL256](/entities/vera-etl256.md)）。

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
- [Hot Chips 2026 NVIDIA Fusion](/papers/hc2026-nvidia-riscv-nvlink-fusion.md) — NVL72 / C2C / CHI 数字
- [Hot Chips 2026 Rubin GPU](/papers/hc2026-nvidia-rubin.md) — NVLink 6 / Counted Write / factory 表
- [Hot Chips 2026 Vera CPU](/papers/hc2026-nvidia-vera.md) — C2C 1.8 TB/s / 36 CPU
- [Hot Chips 2026 Groq 3 LPX](/papers/hc2026-nvidia-groq-3-lpx.md) — decode sidecar 第一手

# Citations

[1] [raw/articles/nvidia-groq3-lpx-blog-2026-04.md](raw/articles/nvidia-groq3-lpx-blog-2026-04.md)
[2] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
[3] [raw/papers/hc2026-nvidia-rubin.md](raw/papers/hc2026-nvidia-rubin.md) — Rubin GPU, Hot Chips 2026
[4] [raw/papers/hc2026-nvidia-vera.md](raw/papers/hc2026-nvidia-vera.md) — Vera CPU, Hot Chips 2026
