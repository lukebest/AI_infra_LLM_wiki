---
type: Paper
title: "Hot Chips 2026: OpenAI Jalapeño"
description: OpenAI — 推理 ASIC；mxfp4 13.4 PFLOP/s / 216 GiB @ 15.4 TB/s；scale-up 128@600 GB/s / 2048@200 GB/s
tags:
- openai
- accelerator
- inference
- noc
- hbm
- scale-up
- chiplet
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_OpenAI_Jalapeno.pdf
- raw/papers/hc2026-openai-jalapeno.md
---

# You Can Just Build Things … Chips (OpenAI Jalapeño)

**Speakers:** Richard Ho, Ravi Narayanaswami, Chris Leary（OpenAI）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_OpenAI_Jalapeno.pdf](raw/papers/HC2026_OpenAI_Jalapeno.pdf)

推理 ASIC + 系统。**RTL → tapeout 9 months**。伙伴点名 **Broadcom & Celestica**。Package TDP **700 W**。非目标：芯片数、单芯片吞吐、TTFT。Jalapeño 跑 **STP**；部分 GPU 基线用 **MTP**。

## InferenceX（名义 8k/1k，weight f4，按 package-TDP 归一）

相对 GB200 **1.2 kW** / GB300 **1.4 kW** / MI355X **1.4 kW**。

| 模型 | 对照 | peak mixed TPS/kW | e2e | min TBT |
|------|------|-------------------|-----|---------|
| GPT-OSS-120B | GB200 STP | **≈1.9×**（**85,448 vs 44,960**） | **≈1.7×**（**1.03 s vs 1.80 s**） | **≈2.7×**（**0.69 vs 1.87 ms**） |
| DeepSeek R1 MXFP4 | GB300 STP | **≈1.7×**（**19,641 vs 11,781**） | **≈3.6×**（**1.65 s vs 5.99 s**） | **≈4.1×**（**1.43 vs 5.90 ms**） |
| DeepSeek R1 | GB300 MTP | **≈1.5×**（**19,641 vs 12,951**） | **2.2×**（**1.65 vs 3.69 s**） | **2.1×**（**1.43 vs 3.04 ms**） |
| Kimi K2.5 1T MXFP4 | GB300 STP | **≈1.5×**（**18,195 vs 11,862**） | **≈3.4×**（**1.56 s vs 5.31 s**） | **≈3.8×**（**1.44 vs 5.48 ms**） |

汇总：交互性 **2.1–4.1×**，e2e **1.7–3.6×**，旧最佳 TBT 的 perf/W **8.6–104.3×**，峰值 **1.5–1.9×**。内部模型「advantage widens」；MTP 再给 **3–5×** latency（iso-efficiency）；frontier 模型 **<1 ms TBT**。

## 架构 / 网络

论点：keep **KV local**；「dark silicon is cheaper than idle accelerators」。平面：compute die + I/O chiplet + **6× HBM4**。**64** core slice 各配一块 HBM slice + 专用 collective 网 + 较慢通用 **NoC** 接到 scale-up Ethernet bridge。

Scale-up：local 域 **128** ASICs @ **600 GB/s**；global **2048** @ **200 GB/s**；**half-flattened two-level Clos**，Broadcom **TH6**，**8 rails**。「Higher BW for TP. Lower BW for EP。」

ASIC：mxfp8×mxfp8 **3.4 PFLOP/s**；mxfp8×mxfp4 **6.7**；mxfp4×mxfp4 **13.4**。Memory **15.4 TB/s, 216 GiB**。2048-ASIC 系统：mxfp4 **27 EFLOP/s**，**32 PB/s**，**432 TiB**。带宽天花板页：**1+ PB/s** ÷ **0.5 TB** → **2,000+** 全模型读/秒；理论无 spec **1000–2000** tok/s/user、有 spec **5000–10000** — 「nowhere close。」

空间编程 / **Gluon**。AI PPA vs 优化过的人：BF16 mul **56%**，FP4 dot **21%**，FP32 acc **10%**。Gen 2「approaching tapeout」；Gen 3 planned。

## 与 wiki 的关系

- [NVIDIA Groq 3 LPX](/papers/hc2026-nvidia-groq-3-lpx.md) — 不是 decode sidecar；Jalapeño 是 KV-local 空间 ASIC
- [Clos and Fat-Tree](/concepts/clos-fat-tree-topology.md) — half-flattened two-level Clos + 8 rails
- [Broadcom Thor Ultra](/papers/hc2026-broadcom-thor-ultra.md) — 同场 Broadcom 以太网 NIC
- [Intel Crescent Island](/papers/hc2026-intel-crescent-island.md) — 另一条「decode 是算力问题」推理卡

# Citations

[1] [raw/papers/HC2026_OpenAI_Jalapeno.pdf](raw/papers/HC2026_OpenAI_Jalapeno.pdf) — Ho / Narayanaswami / Leary, Hot Chips 2026
[2] [raw/papers/hc2026-openai-jalapeno.md](raw/papers/hc2026-openai-jalapeno.md) — 结构化摘录
