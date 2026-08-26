---
type: Paper
title: "Hot Chips 2026: OpenAI Jalapeño"
description: OpenAI — 推理 ASIC；700 W；128 @ 600 GB/s / 2048 @ 200 GB/s Ethernet SU；mxfp4 13.4 PF；216 GiB / 15.4 TB/s
tags:
- openai
- accelerator
- inference
- noc
- scale-up
- hbm
- llm
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_OpenAI_Jalapeno.pdf
- raw/papers/hc2026-openai-jalapeno.md
---

# OpenAI Jalapeño

**Speakers:** Richard Ho, Ravi Narayanaswami, Chris Leary（OpenAI）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_OpenAI_Jalapeno.pdf](raw/papers/HC2026_OpenAI_Jalapeno.pdf)

推理 ASIC + 系统；RTL → tapeout **9 months**（架构 Oct’24 … 第一硅 May’26）。伙伴 **Broadcom & Celestica**。Package TDP **700 W**。非目标：芯片数、单卡吞吐、TTFT。

## InferenceX（8k/1k，weight f4，按包 TDP 归一）

Jalapeño 跑 STP；部分 GPU 基线用 MTP。GPT-OSS-120B vs GB200 STP：peak mixed TPS/kW **85,448 vs 44,960 (≈1.9×)**；e2e **1.03 vs 1.80 s**；min TBT **0.69 vs 1.87 ms**（**1,459 vs 535** tok/s/user）。DeepSeek R1 MXFP4 vs GB300 STP：**19,641 vs 11,781**；e2e **1.65 vs 5.99 s**；TBT **1.43 vs 5.90 ms**。Kimi K2.5 1T vs GB300 STP：**18,195 vs 11,862**；e2e **1.56 vs 5.31 s**；TBT **1.44 vs 5.48 ms**。汇总：交互 **2.1–4.1×**，e2e **1.7–3.6×**，peak **1.5–1.9×**。

论点：**keep KV local**；dark silicon 比闲加速器便宜；一颗平衡芯片按 phase 关块。

## 硅与网络

Floorplan：compute die + I/O chiplet + **6× HBM4**。**64** core slice，各配 HBM slice（快本地路径）+ 专用集体网 + 较慢通用 **NoC** 到 SU Ethernet 桥。算力：mxfp8×mxfp8 **3.4 PF**；mxfp8×mxfp4 **6.7**；mxfp4×mxfp4 **13.4**。Memory **15.4 TB/s, 216 GiB**。

SU：local **128 ASICs @ 600 GB/s**；global **2048 @ 200 GB/s**；半扁平两层 Clos，Broadcom **TH6**，**8 rails**。「Higher BW for TP. Lower BW for EP。」2048-ASIC：**27 EF** mxfp4，**32 PB/s**，**432 TiB**。带宽天花板：128 卡 **1+ PB/s** ÷ **0.5 TB** → **2,000+** 全模型读/s；理论 **1000–2000** tok/s/user 无投机——「nowhere close」。

## 与 wiki 的关系

- [NVIDIA Groq 3 LPX](/papers/hc2026-nvidia-groq-3-lpx.md) — 不是 decode sidecar，是 KV-local 空间 ASIC
- [Microsoft Maia 200](/papers/hc2026-microsoft-maia-200.md) — Ethernet SU 对照
- [Broadcom Thor Ultra](/papers/hc2026-broadcom-thor-ultra.md) — 同场伙伴的 800G NIC
- [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 不用 NVLink

# Citations

[1] [raw/papers/HC2026_OpenAI_Jalapeno.pdf](raw/papers/HC2026_OpenAI_Jalapeno.pdf) — Ho / Narayanaswami / Leary, Hot Chips 2026
[2] [raw/papers/hc2026-openai-jalapeno.md](raw/papers/hc2026-openai-jalapeno.md) — 结构化摘录
