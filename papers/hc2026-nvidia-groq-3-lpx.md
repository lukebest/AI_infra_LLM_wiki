---
type: Paper
title: "Hot Chips 2026: NVIDIA Groq 3 LPX"
description: NVIDIA — 256 LPU / 128 GB SRAM / 315 PFLOPs FP8 / 40 PB/s；C2C 350 ns；Gemma 4 31B 10,996 TPS/user
tags:
- nvidia
- groq
- lpu
- inference
- deterministic
- sram
- scale-up
- rack
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

Vera Rubin「Extend Interactivity」机柜。更新 [NVIDIA Groq 3 LPX](/entities/nvidia-groq-3-lpx.md)。绝对 TPS/MW 曲线点 **未知**。

## 头条 / 芯片

Gemma 4 **31B**、**16K ISL**（max context **264K**）上 **10,996 TPS/user**。SPEED-bench coding：**4,767** median output tok/s。Artificial Analysis **100K** context：相对未具名第三方 **4×** 更快长上下文 decode。

LPU：VLIW，**flat SRAM** 层级；所有单元锁一颗全局时钟；SW 按 **CLK-period** 调度。单元：MEM / VXM / MXM / SXM。「No kernel boundaries / no MEMBARs / all operations fused。」

**1000+ chips** 在软件调度的虚拟全局时钟上当一颗 LPU core。每芯片既是 processor 也是 router；**no adaptive routing / congestion sensing**。包就是 tensor：header/body/tail flit 各 **8 B**，Eth Layer-1，无 HW 流控 / 无 VC。

## LPX 机柜

**256 LPU**，**128 GB** SRAM，**315 PFLOPs FP8** 由 **40 PB/s** 合计 SRAM BW 喂，芯片到芯片 SRAM→SRAM **350 ns**。延迟 vs 可达 SRAM：**0.35 µs @ 8 GB**，**0.75 @ 64**，**1.15 @ 128**，**1.60 @ 384**，**2.05 @ 640**，**2.50 @ 896**，**2.95 µs @ 1152 GB**。可扩到 **1000+** LPU。模块/基板 **8+8** LPU；**no tray cables, no re-timers, full-copper**。

确定性换电源/热：**PEP** 板级 **>60%** 少 droop、**>70%** 少 overshoot。热：非确定性会顶到例 **128 °C**；确定性 per-block 钉在 **105 °C**。

与 **72 Rubin** 异构（各 rack 自留 KV，链路上只走 token/中间量）：

1. **external drafter** — LPX 起草、NVL72 验证
2. **ATTN-FFN disagg** — GPU ATTN + KV in DRAM，LPU FFN 权重在 SRAM
3. **prefill/decode disagg** — GPU 做 KV prefill，LPX decode

GPT-OSS-2T，cached ISL **400K** / new **4K** / OSL **400**：相对 NVL72-only，verifier+draft **~3×**，ATTN+FFN **~3×**，prefill+LP30 decode **~5×**（TPS/MW 曲线）。

## 与 wiki 的关系

- [NVIDIA Groq 3 LPX](/entities/nvidia-groq-3-lpx.md) — 实体页；本页是 HC2026 第一手 TPS / 350 ns
- [NVIDIA Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) — 三种 GPU–LPU 拆分
- [Deterministic Execution](/concepts/deterministic-execution.md) — 全局时钟 + 无自适应路由
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — ATTN-FFN / prefill-decode

# Citations

[1] [raw/papers/HC2026_NVIDIA_Groq_3_LPX.pdf](raw/papers/HC2026_NVIDIA_Groq_3_LPX.pdf) — Arsovski / Raghavan, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-groq-3-lpx.md](raw/papers/hc2026-nvidia-groq-3-lpx.md) — 结构化摘录
