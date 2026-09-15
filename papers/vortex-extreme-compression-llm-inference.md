---
type: Paper
title: "Vortex: Bridging Extreme Compression and Efficient LLM Inference"
description: Duke — 脉动兼容 bi-flow 加速 VQ+上下文稀疏；相对 SOTA 8.03×–23.7× 加速、5.68×–12.5× 能耗（仿真）
tags:
- accelerator
- dataflow
- quantization
- compression
- sparse
- llm
- inference
- kv-cache
- prefill
- decode
- throughput
- latency
- architecture
- memory
- pipeline
timestamp: '2026-09-15T00:00:00Z'
created: 2026-09-15
updated: 2026-09-15
sources:
- raw/papers/Vortex_Extreme_Compression_LLM_Inference_2026.pdf
- raw/papers/vortex-extreme-compression-llm-inference.md
---

# Vortex: Bridging Extreme Compression and Efficient LLM Inference

**Authors:** Haoxuan Shan*, Cong Guo*†, Bowen Duan, Chiyue Wei, Feng Cheng, Yuzhe Fu, Yintao He, Hai "Helen" Li, Yiran Chen（*共同一作；†通讯）
**Affiliation:** Duke University
**arXiv:** [2609.12208](https://arxiv.org/abs/2609.12208)（2026-09-10，cs.AR）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.12208)

相对 [FlexPosit](/papers/flexposit-tunable-fractional-precision-llm.md) 的 bit-serial 分数精度脉动，本文做 **向量量化（VQ）+ 输入依赖稀疏** 与脉动阵列的 **bi-flow 协同**；相对常规 LUT/整数加速器（FIGLUT/FIGNA），强调码本查找冲突与 decode 小-M 场景。

## 动机

极端压缩（VQ codebook、输入依赖稀疏）能压内存足迹，但在常规脉动阵列上难变成实测吞吐：VQ 需要片上 dequant/查找，多 PE 并发查码本冲突；稀疏模式不规则，且与 batched VQ 的向量粒度错位。decode 小 batch 时问题更尖锐——带宽密、稀疏仍有效，但 LUF 式「先还原权重再乘」启动开销大。

## 方案

**Bi-flow vGEMM。** Lookup-First（**LUF**）：先经 LUU 还原码本权重再走脉动 MXU，贴近标准脉动、适合 **prefill（M≥16）**。Multiply-First（**MUF**）：输入子向量先与码本相乘再按索引累加，避免显式权重还原，适合 **decode（M<16）**。同一硬件按输入规模切换。

**三块增量单元（相对基线脉动）。** **LUU** 多 bank 并行码本查找（文内 128KB、256×16-bit entries/bank 量级）；**QAU** 对运行时 KV 做 CQ 风格向量量化（流式 matcher）；**SPU** 做 **codebook-wise** 上下文稀疏，使稀疏掩码对齐 VQ 块、在小 batch（<16）decode 仍有效。

**算法配置。** 评测主配置 AQLM 风格 **n=2, v=8, b=8**；模型 Llama2-7B/13B、Mistral-7B。硬件为周期精确仿真 + SRAM Cacti 面积/能量；**非硅**。

## 效果（仅论文数字）

摘要/结论口径：相对 state-of-the-art 加速器，端到端 **8.03×–23.7×** 加速、**5.68×–12.5×** 能耗降低。

相对常规脉动阵列（SA）：跨工作负载平均 **22.4×** 加速、**9.75×** 能耗降低；相对 FIGLUT **8.03×**（FIGLUT 本身相对 SA **2.79×**）。消融：权重量化（LUU+加宽 VPU）**11.33×** → 叠加注意力量化（QAU）至 **18.8×** → 叠加激活稀疏（SPU）至 **22.4×**。几何均值相对 SA **17.6×** 加速 / **7.39×** 能耗。

面积：Vortex 芯片 **2.10 mm²**（表内 SA/ANT/FIGNA/FIGLUT/Vortex 面积 1.47 / 1.21 / 1.58 / … / 2.10）；文称面积效率相对 SA/ANT/FIGNA 为 **11.9× / 10.1× / 4.42×**。Wgt-Q 单独可达 **31.1×** 加速 / **14.3×** 能耗（相对 SA，FC 层口径，端到端被 Amdahl 稀释）。

**口径提醒：** 周期级仿真 + Cacti，非实测硅；基线为其他加速器架构，不可与 H100+vLLM tok/s 直接横比。

## 与 wiki 的关系

- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 脉动 dataflow；本文 = VQ/稀疏友好的 LUF/MUF 双流扩展
- [FlexPosit](/papers/flexposit-tunable-fractional-precision-llm.md) — 同窗脉动路线；分数精度 bit-serial vs 本文 codebook VQ
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — decode 小-M ↔ MUF；prefill 大-M ↔ LUF
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 权重量化 + KV 量化同时砍静态与动态流量
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 本文是 **单加速器内** prefill/decode 数据流切换，不是机柜 PD 池

## 开放问题

1. 全仿真；无硅、无与商用 GPU serving 同口径对照。
2. 主配置固定 n/v/b；更大模型与 MoE 路由未展开。
3. codebook-wise 稀疏与生产 batching/调度如何共存，文内以小 batch decode 为主。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.12208) — Shan/Guo et al., arXiv:2609.12208
[2] [raw/papers/vortex-extreme-compression-llm-inference.md](raw/papers/vortex-extreme-compression-llm-inference.md) — 结构化摘录
