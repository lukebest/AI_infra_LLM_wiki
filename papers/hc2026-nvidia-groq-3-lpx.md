---
type: Paper
title: "Hot Chips 2026: NVIDIA Groq 3 LPX / LP30"
description: NVIDIA 第一手幻灯片 — 10,996 TPS/user；256 LPU / 128 GB SRAM / 40 PB/s / 350 ns C2C；三种 GPU–LPU 拆分
tags:
- nvidia
- groq
- lpu
- inference
- decode
- deterministic
- sram
- disaggregated-inference
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_NVIDIA_Groq_3_LPX.pdf
- raw/papers/hc2026-nvidia-groq-3-lpx.md
---

# Think Fast: LPU Accelerator for Heterogeneous Compute

**Speakers:** Igor Arsovski, Santosh Raghavan（NVIDIA）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_NVIDIA_Groq_3_LPX.pdf](raw/papers/HC2026_NVIDIA_Groq_3_LPX.pdf)

Vera Rubin「extend interactivity」架。第一手幻灯片，更新 [NVIDIA Groq 3 LPX](/entities/nvidia-groq-3-lpx.md)。TPS/MW 曲线绝对值 **未知**。

## 头条

角色：Vera CPU（单线程/工具）、Rubin GPU（吞吐/prefill）、**LPU（TPS/user / decode）**。Gemma 4 **31B**：**10,996 TPS/user**，16K ISL / max **264K** context。SPEED-bench coding：**4,767** median output tok/s。Artificial Analysis **100K** context：**4×** 更快长上下文 decode（对照未标名）。

LPU：VLIW，**flat SRAM**，全单元同一全局时钟；SW 按 **CLK-period** 调度。无 kernel 边界 / 无 MEMBAR。**1000+** 芯片在软件调度的虚拟全局时钟上当一颗 LPU；无自适应路由 / 拥塞感知。包是张量：8 B header/body/tail flit，Eth L1，无 HW 流控 / 无 VC。

## LPX 机柜

**256 LPU**；**128 GB** SRAM；**315 PFLOPs FP8** 由 **40 PB/s** 聚合 SRAM 喂；C2C **350 ns** SRAM→SRAM。可达 SRAM 延迟：0.35 µs @ 8 GB … **2.95 µs @ 1152 GB**。扩展到 **1000+** LPU。封装：8+8 LPU / 模块；**32 RU** cable cartridge；无 tray 线、无 retimer、全铜。

确定性→电源/热：**PEP >60%** 更少 droop、**>70%** 更少 overshoot。热：非确定例 **128 °C**；确定每块顶在 **105 °C**。

与 **72 Rubin** 三种拆分（各 rack 自持 KV，只过 token/中间量）：(1) LPX draft / NVL72 verify；(2) GPU ATTN+KV / LPU FFN；(3) GPU prefill / LPX decode。GPT-OSS-2T 相对 NVL72-only：**~3× / ~3× / ~5×** 交互。

## 与 wiki 的关系

- [NVIDIA Groq 3 LPX](/entities/nvidia-groq-3-lpx.md) — 实体页补第一手数字
- [NVIDIA Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) — 同工厂
- [Deterministic Execution](/concepts/deterministic-execution.md) — 虚拟全局时钟
- [Cerebras WSE](/entities/cerebras-wse.md) — 另一条确定性路径

# Citations

[1] [raw/papers/HC2026_NVIDIA_Groq_3_LPX.pdf](raw/papers/HC2026_NVIDIA_Groq_3_LPX.pdf) — Arsovski / Raghavan, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-groq-3-lpx.md](raw/papers/hc2026-nvidia-groq-3-lpx.md) — 结构化摘录
