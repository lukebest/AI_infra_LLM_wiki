---
type: Paper
title: "SPECTRA: 运行时可重构瓦片上的 Speculative Decoding"
description: "Columbia — tile 内 systolic/vector 切换 + 跨 tile 并行映射；20-tile FPGA；相对固定 datapath 最高 2.09×，系统级再最高 1.25×。"
tags:
- architecture
- accelerator
- inference
- llm
- speculative-decoding
- dataflow
- pipeline
- noc
- throughput
- latency
created: 2026-09-23
updated: 2026-09-23
timestamp: '2026-09-23T00:00:00Z'
paper_author: [Gabriele Tombesi, William Baisi, Je Yang, Elisavet Lydia Alvanaki, Kevin Lee, Michael Lippe, Biruk Seyoum, Luca P. Carloni]
year: 2026
arxiv: '2609.24847'
sources:
  - raw/papers/SPECTRA_Speculative_Decoding_Reconfigurable_Tiled_2026.pdf
  - raw/papers/spectra-speculative-decoding-tiled.md
---

# SPECTRA：运行时可重构瓦片上的 Speculative Decoding

## 一句话结论

SPECTRA 针对边缘 speculative decoding 的 **中间算术强度区**：verification 既不是纯 GEMV 也不是纯 GEMM。瓦片内在 systolic / vector-lane 间切换，瓦片间按 kernel 调并行度与通信；20-tile FPGA 上相对最佳固定 datapath 最高 **2.09×**，系统级自适应再最高 **1.25×**。

## 动机

边缘设备上自回归 decode 受带宽与片上容量限制。Speculative decoding 用小 draft 提 token、大 target 批量验证，但验证阶段的算术强度随 speculation 长度与接受率变化，固定架构难以全程高利用率。

## 方案

1. **Tile 级**：同一 compute engine 在 systolic（GEMM / 高 AI）与 vector-lane（GEMV / 低 AI）间切换。
2. **系统级**：每 kernel 选择 tile 数、切分轴与通信模式；由 FPGA-profiled 成本模型驱动。
3. **原型**：proFPGA UltraScale+ XCVU19P，20 accelerator tile + NoC + CVA6 控制核；评测 Pythia / SmolLM2 / GPT-2 三组 draft→target。

## 量化结果

- 相对 **systolic-only**：Pythia / SmolLM2 / GPT-2 为 **1.42× / 2.09× / 1.16×**；相对 **vector-only**：**3.80× / 5.97× / 8.02×**。
- 系统级 mixed 映射相对最佳静态映射：**1.14× / 1.25× / 1.05×**（摘要取峰值再 **+1.25×**）。
- 相对匹配的 target-only baseline，可重构架构 speculative 加速可达 **1.36× / 2.04× / 3.82×**。

## 局限与解读

模型规模偏小（百兆–七亿级），结论外推到大模型需谨慎；收益来自 datapath 切换与映射，而非 draft 算法本身。与 [DSpark Speculative Decoding](../concepts/dspark-speculative-decoding.md) 互补：DSpark 优化 draft/verify 策略，SPECTRA 优化验证期落在 [GEMM vs GEMV](../concepts/gemm-vs-gemv.md) 中间区时的硬件利用率；脉动侧对照 [DNN Accelerator Systolic Dataflow](../concepts/dnn-accelerator-systolic-dataflow.md)。

# Citations

1. Tombesi et al. “SPECTRA: Adaptive Execution of Speculative Decoding on a Runtime-Reconfigurable Tiled Architecture.” arXiv:2609.24847, 2026. [arXiv](https://arxiv.org/abs/2609.24847)
2. [本地原文 PDF](../raw/papers/SPECTRA_Speculative_Decoding_Reconfigurable_Tiled_2026.pdf)；[原始来源记录](../raw/papers/spectra-speculative-decoding-tiled.md)
