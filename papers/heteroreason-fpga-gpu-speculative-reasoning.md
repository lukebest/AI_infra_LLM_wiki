---
type: Paper
title: "HeteroReason: FPGA–GPU 解耦投机推理加速"
description: "MICRO’26；draft@FPGA + PRM/target@GPU；延迟 1.01–1.42×、能效 1.25–1.57×；回退最高 +4.2% 精度。"
tags:
- architecture
- accelerator
- gpu
- inference
- decode
- latency
- throughput
- speculative-decoding
- disaggregated-inference
- llm
- serving
- power
created: 2026-09-28
updated: 2026-09-28
timestamp: '2026-09-28T00:00:00Z'
paper_author: [Zehuan Zhang, Quan Deng, Zhibo Ren, Hao Mark Chen, Guoyu Li, Xuchun Hu, Jose G. F. Coutinho, Ce Guo, Wayne Luk, Zhiqiang Que, Hongxiang Fan]
year: 2026
arxiv: '2609.28717'
sources:
  - raw/papers/HeteroReason_FPGA_GPU_Speculative_Reasoning_2026.pdf
  - raw/papers/heteroreason-fpga-gpu-speculative-reasoning.md
---

# HeteroReason：FPGA–GPU 解耦投机推理

## 一句话结论

HeteroReason（MICRO 2026）把 LRM 的 **draft / PRM / target** 投机推理做成算法–硬件协同：算法侧加 **backtracking** 逃离低质中间步；系统侧把 draft 卸到 FPGA、PRM 与 target 留在 GPU，并用 shadow sync + step-ahead 管线隐藏同步。相对同构 GPU，延迟 **1.01×–1.42×**、能效 **1.25×–1.57×**；回退平均精度最高 **+4.2%**。

## 动机：前向轨迹脆弱 + 同构 GPU 错配

投机推理用小 draft 生成候选推理步，PRM 验证、强 target 精炼，以降低 target 调用频率。但标准流程严格前向：早期劣质子步被接受会误差传播。硬件上 draft 多为 memory-bound 自回归，PRM/target 偏并行 compute；同构 GPU 频繁小核切换既耗能又难吃满。剖析显示 draft 与 target 合计可占逐步延迟的大部分（文中区间约 **34.6–55.4%** 与 **22.4–47.5%**），PRM 约 **16.1–22.2%**。

## 方案

### 1. Backtracking-enhanced workflow

低 PRM 分数时回退到更早边界，探索替代轨迹，提高鲁棒性。

### 2. FPGA–GPU 异构 + 本地 PD 解耦

Draft @ AMD U280/V80；PRM/target @ RTX 3090。FPGA 侧做 prefill–decode 解耦；shadow synchronization 让 GPU 精炼与 FPGA token 更新重叠。

### 3. Step-ahead speculation & refinement

在 PRM 验证当前步时，draft 抢跑后续步，把串行 draft→verify→refine 变成并行管线。

## 量化结果

- **精度**：回退机制在多样 reasoning 基准上平均最高 **+4.2%**（摘要；实验亦区分约 **+1.7% / +4.2%** 配置）。
- **延迟 vs 同构 GPU**：整体 **1.01×–1.42×**；文中细分 U280 约 **1.01–1.12×**，V80 约 **1.26–1.42×**。
- **能效（J/token）**：**1.25×–1.57×**。
- **Goodput**：文中报 U280 **1.01×–1.12×**、V80 侧更高区间（与延迟/能效图一致）。

## 局限与解读

- V80 结果部分为投影；主机–FPGA 经 PCIe，同步隐藏依赖工作流设计。
- 对标同构 GPU 与 RSD 类算法基线，非大规模集群 serving。
- 相对 [SPECTRA](../papers/spectra-speculative-decoding-tiled.md)（瓦片内验证期算术强度）与 [DSpark Speculative Decoding](../concepts/dspark-speculative-decoding.md)（算法层 τ/verify），HeteroReason 把旋钮放到 **异构器件分工 + 步级管线**；亦落在 [Disaggregated Inference](../concepts/disaggregated-inference.md) 与 [Heterogeneous Inference](../concepts/heterogeneous-inference.md)。

# Citations

1. Zhang, Z., Deng, Q., Ren, Z., Chen, H. M., Li, G., Hu, X., Coutinho, J. G. F., Guo, C., Luk, W., Que, Z., Fan, H. “HeteroReason: Heterogeneous FPGA-GPU Acceleration for Disaggregated Speculative Reasoning.” MICRO 2026 / arXiv:2609.28717. [arXiv](https://arxiv.org/abs/2609.28717)
2. [本地原文 PDF](../raw/papers/HeteroReason_FPGA_GPU_Speculative_Reasoning_2026.pdf)；[原始来源记录](../raw/papers/heteroreason-fpga-gpu-speculative-reasoning.md)
