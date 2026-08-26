---
type: Paper
title: "Hot Chips 2026: SambaNova SN50"
description: SambaNova — SN50 RDU 3200 TFLOPS FP8；Ethernet scale-up 2 TB/s / 256+ 域；DeepSeek-R1 256-RDU 500 tok/s/user
tags:
- sambanova
- accelerator
- dataflow
- inference
- scale-up
- hbm
- sram
- fabric
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_SambaNova_SN50.pdf
- raw/papers/hc2026-sambanova-sn50.md
---

# Dataflow at Scale: the SN50 RDU

**Speaker:** Raghu Prabhakar（SambaNova，Chief Architect）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_SambaNova_SN50.pdf](raw/papers/HC2026_SambaNova_SN50.pdf)

前代见 [SN40L](/papers/sambanova-sn40l-dataflow-coe.md)。**MBU** = 权重+KV 实际用掉的 peak HBM 比例。AgentX 时间份额：DeepSeek V3 8K/1K decode **97%**。

## 芯片 / 机柜

SN50：**3200 TFLOPS FP8**（**5× SN40**）；**5 nm CoWoS-L**；片上 SRAM **432 MB**；HBM **64 GB @ 1.84 TB/s**；scale-up Ethernet **2 TB/s**；scale-up 域 **256+** SN50；scale-out **400G**；CXL DDR prompt cache **100 GB/s**。Die：**864** PCU + PMU。持久融合 decoder kernel；无全局 sync。

风冷机柜：**16 RDU / 2 nodes**。每柜：**25.6 PFLOPs BF16**、**51.2 PFLOPS FP8**；SRAM **6.9 GB**；HBM **1 TB**；RDU DDR **256 GB–2 TB**。Scale-up **6.4 TB/s**，scale-out **800 GB/s**。典型 **15–20 kW**，最大 **34 kW**。

每 RDU **10× 800G** Ethernet（**2 TB/s**）。**7** 口全连接 **8-socket** 节点；**2** 口出节点 scale-up（标 **400 GB/s** per RDU）；**1× 400G RoCEv2**（**50 GB/s**）。节点内链路 **200 GB/s** on **800G** Ethernet。64-socket scale-up：**2× 64p 800G** 交换机。Scale-out 口号「tens of thousands」。

## 并行与实测

片上 TP GEMM：8/16/32 socket **70%+** TFLOP 利用率；32-SN50「full overlap」。DeepSeek TP-32 MoE 层 **>70% MBU**。64-socket EP：**>70%** 带宽去装 expert。

DeepSeek-R1 8K/1K vs B300 FP4 InferenceX：SN50 **64 → 128 → 256** 给出 **200 → 300 → 500** tok/s/user，MBU **51% → 44% → 45%**。功率/容量（MTP3 accept 3.1）：**128 RDU / 120 kW / 43.7% / 103 TB/s / 8.2 TB**；**256 / 240 kW / 45.1% / 212 TB/s / 16.4 TB**；**512 / 480 kW / 40.0% / 377 TB/s / 32.8 TB**。对照：**4× NVL72 @ 5% MBU / 28.8 TB/s**；**32× DGX B300 @ 25% / 16 TB/s**。

MiniMax M2.7（AA serverless，10k input，07-07-26）：SN50 private **763** tok/s vs SN40 public **482** — 相对 SN40 **3.3×**。标题句「over 750 tokens/s」。

## 与 wiki 的关系

- [SambaNova SN40L](/papers/sambanova-sn40l-dataflow-coe.md) — 5× FP8、同一 dataflow 编译
- [NVIDIA Rubin](/papers/hc2026-nvidia-rubin.md) — 幻灯用 4× NVL72 @ 5% MBU 对照
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — decode 带宽墙 + MBU
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — CXL DDR prompt cache 100 GB/s

# Citations

[1] [raw/papers/HC2026_SambaNova_SN50.pdf](raw/papers/HC2026_SambaNova_SN50.pdf) — Raghu Prabhakar, Hot Chips 2026
[2] [raw/papers/hc2026-sambanova-sn50.md](raw/papers/hc2026-sambanova-sn50.md) — 结构化摘录
