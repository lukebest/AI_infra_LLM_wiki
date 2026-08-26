---
type: Paper
title: "Hot Chips 2026: Intel Crescent Island"
description: Intel — Xe3p inference GPU；Intel 卡 160 GB LPDDR5x（ODM 上限 480 GB）；350 W 风冷 PCIe；片上是 Memory Fabric + 32 MB L2，不是 packet NoC
tags:
- intel
- gpu
- accelerator
- inference
- memory
- speculative-decoding
- moe
- architecture
- decode
- cache
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Intel_Crescent_Island.pdf
- raw/papers/hc2026-intel-crescent-island.md
---

# Intel Crescent Island — GPU Designed for Agentic AI Inference

**Speakers:** Sumit Mohan, Dr. Hong Jiang（Intel）  
**Venue:** Hot Chips 2026 Conference  
**PDF:** [raw/papers/HC2026_Intel_Crescent_Island.pdf](raw/papers/HC2026_Intel_Crescent_Island.pdf)

Decode 第三条路：大容量低功耗 LPDDR5x + 空气 350 W PCIe + PCIe 交换 scale-up。**不是**训练 GPU，也**没有** NVLink/UALoE。对照 [Rubin](/papers/hc2026-nvidia-rubin.md)、[Groq 3 LPX](/papers/hc2026-nvidia-groq-3-lpx.md)、[DRAM](/concepts/dram-memory-system.md)。片上标签是 **Memory Fabric / 32 MB L2**，**不是 packet NoC**。

## 卡与 Xe3p

定位：Intel **performance-forward / next-gen PC-to-datacenter** 推理 GPU（Xe **3p**）。组合图还点名 Arc Pro、datacenter GPUs、**SN50 RDUs**。

「tokens/watt」；Intel 品牌 PCIe 卡 **160 GB LPDDR5x**；「design enables partners to build ODM branded cards with flexible options **up to 480 GB**」。**350 W**，**air-cooled PCIe**。数据类型 **FP4/MXFP4 through FP64**。**480 GB 是 ODM 上限；Intel 卡是 160 GB**。

Xe core（3rd gen / Xe3p）：每核 **8 Vector Engines (XVE)** + **8 XMX**；**3-way co-issue**；XMX **16-deep systolic**（Xe2/Xe3 是 **4-deep**）。芯片：**32 Xe-cores**，**256 XMX** engines。

SoC 四块：32 Xe cores「High-FLOP Compute Behind Every Reasoning Step」；**32 MB unified L2**「Bandwidth Filter that Keeps the Matrix Engines Fed」；LPDDR5x「KV-cache capacity」；media **4 decoder + 4 encoder**；**PCIe Gen5 x16**「Scale-Up on an Open Standard **PCIe switch fabric**」。片上互连标签是 Memory Fabric / Fabric；**没有** “packet NoC”。切片/floorplan 细分数 **未知**。

Xe-arch 表（Crescent Island / Xe3p vs Xe2 Battlemage / Xe3 Panther Lake）：**32** XeCores（Xe2: 20；Xe3: up to 12）；XMX **16-deep**；**FP8 + FP4**；**MX** microscaling；full-rate FP64 **64 FMA/XeCore**（先前 **8 FMA/XeCore**）；GRF **1 MB**/XeCore（先前 **512 KB**）；L1$/SLM **512 KB**/XeCore（Xe2: **256 KB**）；L2 **32 MB** unified；memory **up to 480 GB LPDDR5x**（Xe2: **24 GB GDDR6**，**18 MB** L2）。

RAS：ECC/parity；Xe-core + memory isolation；E2E poison；LPDDR ECC-over-DMI「without bandwidth/capacity impact」。本 deck **无** UALink / NVLink / CXL GPU fabric。

## Speculative decode 与容量

LMSYS SpecBundle / EAGLE-3 / SGLang，batch 8；**throughput metrics deliberately excluded**。frontier MoE **2.9–4.9** tokens retired per verification pass（8-token draft tree）。例：Qwen3-Next-80B-A3B **4.04**；Kimi K2 1T **4.29**；Qwen3-Coder-480B-A35B **4.94**；Qwen3-235B-A22B **2.90**。「Doubling the tree doubles compute, buys **1.39×** token」。论点：MoE 每 token 读字节塌缩后，decode 变成 **compute** 问题。

只算 weights、不含 KV：Llama 2 70B → Kimi K2 1T，「bytes held **7.5×** more, bytes read per token **4.4×** less」。Y 轴「per-user decode bandwidth (GB/s) at **30 tok/s**」。稀疏模型标「**3 to 78 GB/token**」。DeepSeek-V4-Pro / Kimi K3 2.8T 画成 **announced, config not published**。

软件：Triton、SYCL-TLA、oneCCL、oneDNN、NIXL w/ UCX、Level Zero、OpenCL。峰值 TOPS、LPDDR5x GB/s、工艺节点：**未知**。

# Citations

[1] [raw/papers/HC2026_Intel_Crescent_Island.pdf](raw/papers/HC2026_Intel_Crescent_Island.pdf) — Mohan / Jiang, Hot Chips 2026
[2] [raw/papers/hc2026-intel-crescent-island.md](raw/papers/hc2026-intel-crescent-island.md) — 结构化摘录
