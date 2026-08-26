---
type: Paper
title: "Hot Chips 2026: Pistil 20-Chiplet SLM SiP"
description: Harvard/Google/Lockheed — 16 nm 2.5D，4 compute + 16 RPC-DRAM；512 MB / 51.2 GB/s；flower 拓扑；vs Jetson Nano 最高 7.6× 吞吐、5.0–7.8× 更低能量/token
tags:
- chiplet
- memory
- memory-bandwidth
- inference
- decode
- architecture
- google
- packaging
- llm
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Pistil_20_Chiplet_SLM.pdf
- raw/papers/hc2026-pistil-20-chiplet-slm.md
---

# Pistil: A 16-nm Accelerator Co-Designed with a 20-Chiplet 2.5D System-in-Package

**Orgs:** Harvard University + Google LLC + Lockheed Martin  
**Equal contrib.:** Nestor Cuevas & Matthew Adiletta；David Brooks, Gu-Yeon Wei  
**Venue:** Hot Chips 2026 Poster  
**PDF:** [raw/papers/HC2026_Pistil_20_Chiplet_SLM.pdf](raw/papers/HC2026_Pistil_20_Chiplet_SLM.pdf)

20-chiplet 2.5D、「花」形拓扑用满 compute–memory shoreline。数字全在正文。**不是** datacenter HBM，是边缘 SLM。板级速率 **未知**。

## 命题与硅

dense SLM **decode 是内存带宽问题**——逐 token 反复流权重，延迟/能量看 sustained BW 而不是峰值算力。

- **16 nm**；2.5D SiP。
- **4** Pistil compute chiplets + **16** RPC-DRAM memory chiplets = **20** chiplet。
- 总 DRAM **512 MB**，modeled 总 DRAM BW **51.2 GB/s**。
- 模型上限 **1B** 参数。

## 拓扑与执行

**flower** —— 每颗 compute 被 **4** 颗 RPC-DRAM 包围，容量和带宽随 flower 数涨。另有 Pistil-to-Pistil package link 和板级 scale-up link（板级速率 **未知**）。

执行：三独立流水线——Memory（RPC-DRAM → scratchpad）、Compute（VMM / vector / accumulate）、Network（自定义 C2C）。**无共享地址空间**。每 chiplet 自有 instruction queue + decode frontend。scratchpad 硬件同步，使流权重、计算、chiplet 通信细粒度重叠。

控制：轻量 **Arm Cortex-M55** 发 coarse command，内部 FSM 并发跑 mem/compute/comm，无需手写 micro-kernel 交错。

## 实测

dense SLM，**4-bit**，llama.cpp vs **Jetson Nano 8GB**：

- **80–250 tokens/s**
- 吞吐最高 **7.6×**
- decode 期间 **>98%** 峰值内存带宽
- 能量/token **5.0–7.8×** 更低

收益来源：持续流权重、on-the-fly dequant、mem/compute/inter-chiplet 重叠。主 takeaway：边缘 SLM decode 靠维持带宽，不靠堆容量。

## 与 wiki 的关系

- [DRAM and Memory System](/concepts/dram-memory-system.md) — 边缘 RPC-DRAM 海滩线，不是 HBM
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 这是 **2.5D SiP**，不是 TSV/HB 垂直栈
- [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) — 同属封装内 chiplet；HYDRA 是 datacenter hybrid serving DSE，Pistil 是边缘实测
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 不是晶圆级；flower 是包内 shoreline
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 带宽 bound 在 1B SLM 上也成立

# Citations

[1] [raw/papers/HC2026_Pistil_20_Chiplet_SLM.pdf](raw/papers/HC2026_Pistil_20_Chiplet_SLM.pdf) — Cuevas, Adiletta, Brooks, Wei et al., Hot Chips 2026 Poster
[2] [raw/papers/hc2026-pistil-20-chiplet-slm.md](raw/papers/hc2026-pistil-20-chiplet-slm.md) — 结构化摘录
