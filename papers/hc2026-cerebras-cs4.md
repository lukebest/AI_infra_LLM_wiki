---
type: Paper
title: "Hot Chips 2026: Cerebras CS-4"
description: Cerebras — CS-4 三片 WSE-3 Turbo；SRAM 132 GB / 129.6 PB/s；Direct Wafer Links 2 µs；CS-6 写 3D stacked DRAM
tags:
- cerebras
- wse
- now
- network-on-wafer
- inference
- rack
- sram
- 3d
- interconnect
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Cerebras_CS4.pdf
- raw/papers/hc2026-cerebras-cs4.md
---

# Rack-Scale Architecture for Wafer Scale Engine (CS-4 / Nexus)

**Speaker:** Jean-Philippe Fricker（Cerebras，Co-Founder & Chief System Architect）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_Cerebras_CS4.pdf](raw/papers/HC2026_Cerebras_CS4.pdf)

三片晶圆进一个机柜。相对倍率默认对 CS-3。CS-6 FLOPS / BW / 绝对延迟 **未知**。更新 [Cerebras WSE](/entities/cerebras-wse.md)。

## CS-3 → CS-4

| | CS-3 | CS-4 |
|--|------|------|
| Compute | **125 PFLOPS** | **750 PFLOPS** |
| Wafers | 1× WSE-3 | **3× WSE-3 Turbo** |
| SRAM | **44 GB** | **132 GB** |
| Memory BW | **21.6 PB/s** | **129.6 PB/s** |
| Fabric BW | **26.7 PB/s** | **160.5 PB/s** |
| I/O | **1.2 Tbit/s** | **7.2 Tbit/s** |
| I/O latency | **5 µs** | **2 µs** |

头条：相对 CS-3 最高 **2×** tokens、**10×** throughput/watt；相对 GPU 最高 **30×** 更快、**10×** token capacity。柱状图（Gemma 4-31B … GPT 5.6 Sol）Y 轴到 **5,000** tok/s，各柱精确高度 **未知**。来源 Artificial Analysis + 内部（August 2026）。

单片 WSE-3T：**43,200 TB/s** mem BW vs 幻灯所标 NVIDIA Rubin **22 TB/s**（标 **2,000x**）。晶圆 fabric **53.5 PB/s**，「no cables, all on-chip」；对照 Rubin NVL72 **260 TB/s NVLink**、**5,000 cables**。

## Direct Wafer Links + 机柜

新 **Direct Wafer Links** + 标准 RoCE。每片 aggregate I/O **2.4 Tb/s**（**2×** vs CS-3）。到 users / disaggregated devices **3 µs**（**1.7×**）；晶圆间 **2 µs**（**2.5×**）。更高 I/O 自称给 **10T-parameter model <0.2 ms** hop。

供电：**54.5 VDC** busbar，无 PCB 到晶圆；DC/DC **~0.5 mm** vs GPU **~50 mm**（**100X**）。输入最高 **277 VAC**；每 backpack 最多 **30** PSU 模块。相对 CS-3：**2×** power、**2×** cooling；**50%** fewer components。CS-4 绝对瓦数 **未知**。

Early access now，GA **later in Q3 2026**。Nexus 面向 CS-5 / CS-6。CS-5（2027，internal projections, August 2026）：Gemma 4 31B / gpt-oss 120B 档最高 **10,000 TPS/user**；DeepSeek / Kimi / GPT 5.6 Sol 档最高 **5,000 TPS/user**；最高 **3M TPS/MW**。CS-6：「wafer-scale SRAM, with **3D stacked DRAM**」；「order of magnitude smaller footprint」。

## 与 wiki 的关系

- [Cerebras WSE](/entities/cerebras-wse.md) — 单晶圆 44 GB / 21.6 PB/s 基线；本页是三片 + wafer-to-wafer
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 片上 53.5 PB/s vs 电缆 NVLink
- [NVIDIA Rubin](/papers/hc2026-nvidia-rubin.md) — 幻灯自己拿 22 TB/s / 260 TB/s 对照
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — CS-6 写 3D stacked DRAM，无数字

# Citations

[1] [raw/papers/HC2026_Cerebras_CS4.pdf](raw/papers/HC2026_Cerebras_CS4.pdf) — Jean-Philippe Fricker, Hot Chips 2026
[2] [raw/papers/hc2026-cerebras-cs4.md](raw/papers/hc2026-cerebras-cs4.md) — 结构化摘录
