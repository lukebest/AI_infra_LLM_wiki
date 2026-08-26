---
type: Paper
title: "Hot Chips 2026: NVIDIA Rubin GPU"
description: NVIDIA — Rubin GPU + NVLink 6；72 GPU / 3.6 TB/s all-to-all；100 MW factory 2 ZFLOPS NVFP4、11 PB / 800 PB/s HBM4；2:4 稀疏与 Counted Write
tags:
- nvidia
- gpu
- accelerator
- training
- inference
- scale-up
- fabric
- hbm
- rack
- architecture
- sparse
- quantization
- interconnect
- switch
- agentic-ai
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_NVIDIA_Rubin.pdf
- raw/papers/hc2026-nvidia-rubin.md
---

# NVIDIA Rubin GPU: Driving the Era of Agentic AI

**Speakers:** Manas Mandal, Raj Dash, Rouslan Dimitrov（NVIDIA）  
**Venue:** Hot Chips 2026 Conference  
**PDF:** [raw/papers/HC2026_NVIDIA_Rubin.pdf](raw/papers/HC2026_NVIDIA_Rubin.pdf)

同日对照：[Helios UALoE](/papers/hc2026-amd-helios-ualoe.md)（也是 72-GPU scale-up）、[Vera CPU](/papers/hc2026-nvidia-vera.md)。更新 [Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) 与 [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md)。

## 七芯片五机架

Vera Rubin 写成 full-stack AI factory：**七芯片、五机架** — NVL72、[Groq 3 LPX](/entities/nvidia-groq-3-lpx.md)、Vera CPU rack、Vera BlueField-4 STX、Spectrum-6 SPX。角色：Foundation Platform / Extend Interactivity / Tool Calls and Sandboxes / Context Memory Storage / Scale-out Fabric。

Agentic 对标传统推理：输入从固定 1k/8k/32k 变成 **32k & 100k & 400k**；多轮 + tool calling。优化目标改成 token revenue：Δ tokens/watt、Δ TTFT、Δ MTBI、Δ useful life。

AgentX 图标 **Unofficial Results. Pending SemiAnalysis Review**：DeepSeek-v4-PRO，**140K+** context；纵轴 TPS per MW 到 **60M**，横轴 TPS/User 到 **300**。NVL72 vs GB300 NVL72 标 **2X / 10X / 30X**（高交互端 30X）。给定 TPS/User 的绝对坐标 **未知**。

## 100 MW factory（不是单 GPU）

脚注：*Specifications based on at scale AI factory using DSX with MaxLPS*。**2 ZFLOPS / 11 PB / 800 PB/s 是 100 MW factory，不是单卡**：NVFP4 inference **2 ZFLOPS**；NVFP4 training **1.4 ZFLOPS**；HBM4 **11 PB**；HBM4 BW **800 PB/s**。单卡 HBM4 GB / TB/s、GPU TDP、工艺节点：本 deck **未知**。

Die 标签：Enhanced **5th Gen Tensor Cores**；**NVLink-C2C** coherent CPU–GPU；**x16 PCIe Gen6**；HBM CTRL / distributed L2 / GPC；**NVLink v6**；Confidential Computing **TEE-I/O capable**。图上还有 NV-HBI、MIG CONTROL、GIGATHREAD ENGINE、NV-DEC。

## 2:4 稀疏与 Counted Write

稀疏路线：2023 FP8 weight sparsity → 2024/2025 NVFP4 → 2026 **Rubin Adaptive Compression Sparsity**。**2:4 sparsity** 比上代 NVFP4 sparsity 更通用；多数情况「no change to model and no finetuning」；inference runtime opt-in。注意力：BMM1 → **LDTM.Sparsify** → SoftMax → BMM2；「**2x** faster downstream SoftMax and BMM2」。精度演示是 Qwen-Image BF16 dense vs NVFP4 sparse（分数表 **未知**）。

**Counted writes** 替换 Blackwell 的 MEMBAR + atomic-flag GPU-to-GPU sync。延迟 µs **未知**。

## NVLink 6 / NVL72

**72 GPU** scale-up domain；**3.6 TB/s per GPU all-to-all BW**。相对 Ethernet：「**3x** lower latency」；**130 TFLOPS** in-network compute；**10x** higher packet rate；另有 **4X** callout，分母 **未知**。

3rd-gen MGX：all-copper；**80+** MGX partners；**350+** factory sites / **30** countries；**45°C** liquid cooling；no retimers；**800 VDC**。TCS supply **45 °C** / return **55 °C** vs 传统 **35 / 45 °C**。LLM training 上 intelligent power smoothing **13%** peak power reduction；叠加其它改进「up to **40%** more GPUs per provisioned watt」。2nd-gen RAS Engine（RIST）：seconds 级 zero-downtime GPU health checks；in-field SRAM repair；HBM bank re-mapper。

# Citations

[1] [raw/papers/HC2026_NVIDIA_Rubin.pdf](raw/papers/HC2026_NVIDIA_Rubin.pdf) — Mandal / Dash / Dimitrov, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-rubin.md](raw/papers/hc2026-nvidia-rubin.md) — 结构化摘录
