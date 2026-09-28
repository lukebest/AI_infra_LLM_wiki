---
type: Raw Source
title: "HeteroReason: Heterogeneous FPGA-GPU Acceleration for Disaggregated Speculative Reasoning"
description: "Imperial/清华/Bristol — MICRO’26；LRM draft@FPGA + PRM/target@GPU；延迟 1.01–1.42×、能效 1.25–1.57×；回退最高 +4.2% 精度。"
timestamp: '2026-09-28T00:00:00Z'
source_url: https://arxiv.org/abs/2609.28717
arxiv: '2609.28717'
ingested: 2026-09-28
sha256: 4a66c9b1c22fc2599440d693da5696643ec224b00c4b7367e41a8d7538ef0792
---

# HeteroReason: FPGA–GPU Speculative Reasoning

**Authors:** Zehuan Zhang, Quan Deng, Zhibo Ren, Hao Mark Chen, Guoyu Li, Xuchun Hu, Jose G. F. Coutinho, Ce Guo, Wayne Luk, Zhiqiang Que, Hongxiang Fan  
**Affiliation:** Imperial College London; Tsinghua University; University of Bristol  
**Venue:** MICRO 2026  
**PDF:** [HeteroReason_FPGA_GPU_Speculative_Reasoning_2026.pdf](HeteroReason_FPGA_GPU_Speculative_Reasoning_2026.pdf)  
**arXiv:** [2609.28717](https://arxiv.org/abs/2609.28717)（2026-09-23，cs.AR）

## 问题

LRM 的 speculative reasoning（draft → PRM → target）在同构 GPU 上既脆弱（纯前向轨迹易误差传播），又资源错配（小 draft 偏 memory、PRM/target 偏 compute）。

## 方法要点

- 算法：backtracking-enhanced workflow，从低质中间步回退并探索替代轨迹。
- 系统：draft 卸荷到 FPGA，PRM/target 在 GPU；本地 FPGA 上 prefill–decode 解耦 + shadow sync；step-ahead speculation/refinement 管线化。
- 平台：AMD U280 / V80 + NVIDIA RTX 3090。

## 摘录数字（仅论文给出）

- 回退：多样 reasoning 基准平均精度最高 **+4.2%**（摘要；文中亦报 +1.7%/+4.2% 配置差）。
- 相对同构 GPU：延迟 **1.01×–1.42×**（U280 约 **1.01–1.12×**，V80 约 **1.26–1.42×**）；能效 **1.25×–1.57×**。

**Working page:** [HeteroReason](/papers/heteroreason-fpga-gpu-speculative-reasoning.md)
