---
type: Paper
title: "BOOST: Concurrent Host+HBM Access for LLM Inference"
description: GT/NVIDIA/Stanford — wave-aware 并发吃满 host+HBM；Grace Hopper 上 iso-batch TPOT +4.3%、高吞吐 +31%（vs prefetch +15%）
tags:
- gpu
- hbm
- memory
- memory-bandwidth
- llm
- inference
- kv-cache
- serving
- serving-system
- throughput
- latency
- architecture
- nvidia
- cpu
timestamp: '2026-09-16T00:00:00Z'
created: 2026-09-16
updated: 2026-09-16
sources:
- raw/papers/BOOST_Concurrent_Host_HBM_LLM_Inference_2026.pdf
- raw/papers/boost-concurrent-host-hbm-llm-inference.md
---

# BOOST: Concurrent Access to Host Memory and HBM to Accelerate LLM Inference

**Authors:** Anish Saxena†, Jae Hyung Ju†, Hritvik Taneja, Po-An Tsai, Aamer Jaleel, Christos Kozyrakis, Moinuddin Qureshi（†共同一作）
**Affiliation:** Georgia Tech / Nvidia Research / Stanford
**arXiv:** [2609.13592](https://arxiv.org/abs/2609.13592)（2026-09-11，cs.DC/cs.AR）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.13592)

相对 [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) 的远端层与 prefetch/页迁移叙事，BOOST 把 **同节点 host DRAM 与 HBM 当对等带宽源**，要求每个 GPU wave **并发且按带宽比**访问，而不是先搬进 HBM 再算。

## 动机

Decode 吃内存带宽与容量。现有 serving：装得下就只读 HBM；溢出则 prefetch——prefetch 写 HBM 会挤掉读带宽，host 层闲置。Grace Hopper 上 host 约为 HBM 带宽的 **9–11%**，合并理论上约 **1.1×**；容量侧若 KV 仅占 HBM 20%，再加 10% host 容量可把 KV 空间抬约 **50%**。既有带宽比例放置因 **wave 感知缺失** 与 **2MB 大页**，无法在短时间尺度上保证并发。

## 方案

**CAP（Concurrent and Proportional）** 访问。运行时（集成 **vLLM**，不改 kernel）：

1. **MPP（Modulo-Based Page Placement）**：静态权重按 modulo 落两层，压低 wave 内访问比方差。
2. **Wave-aware KV 池**：动态 KV 空闲页按 CTA/wave 组织，使并发波次同时触达两层。

评测平台：Grace Hopper。

## 效果（仅论文数字）

- **iso-batch**：相对 HBM-only **TPOT 改善 4.3%**；prefetch 使 TPOT **恶化 6%**。
- **高吞吐 serving**：平均吞吐 **+31%**；相对 prefetch **高出 15%**；其中并发访问相对「只扩容」再贡献约 **4%**。

**口径提醒：** 单机 GH 实测 + vLLM；增益含容量扩批与带宽并发两部分，勿与跨节点 CXL/HBF 吞吐直接横比。

## 与 wiki 的关系

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 两层对等并发 vs 层级 prefetch
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 远端层迁移；本文是 **C2G host↔HBM** 同节点对等
- [DRAM Memory System](/concepts/dram-memory-system.md) — host DRAM 作为第二带宽腿
- [Hopper Utilization](/papers/dissecting-gpu-utilization-llm-inference-hopper.md) — 同代 GPU 利用率；本文补内存层级并发

## 开放问题

1. 非 Grace 相干 C2G（PCIe-only）上 CAP 是否仍划算。
2. 与 HBF/CXL 第三层如何三层 CAP。
3. 闭源 kernel 场景下仅靠运行时放置的上限。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.13592) — Saxena/Ju et al., arXiv:2609.13592
[2] [raw/papers/boost-concurrent-host-hbm-llm-inference.md](raw/papers/boost-concurrent-host-hbm-llm-inference.md) — 结构化摘录
