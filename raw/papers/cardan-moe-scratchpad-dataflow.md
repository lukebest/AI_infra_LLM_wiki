---
type: Raw Source
title: "A Multi-Engine Dataflow for MoE Decoding on Scratchpad-Based Tensor Accelerators"
description: "CARDAN 原始论文来源：Scratchpad 张量加速器 MoE 共享/私有权重表示与多引擎解码数据流。"
timestamp: '2026-09-22T00:00:00Z'
source_url: https://arxiv.org/abs/2609.21137
arxiv: '2609.21137'
ingested: 2026-09-22
sha256: 3058a9092fc8a9141cefd2baa5eaa3491a4974861f514c45e0e22bf5d29925ad
---

# CARDAN: Multi-Engine MoE Decoding on Scratchpad Tensor Accelerators

**Authors:** Bin Ma, Wenjie Fan, Dong Li  
**Affiliation:** University of California, Merced; Yotta Labs  
**PDF:** [CARDAN_Multi_Engine_MoE_Scratchpad_Dataflow_2026.pdf](CARDAN_Multi_Engine_MoE_Scratchpad_Dataflow_2026.pdf)  
**arXiv:** [2609.21137](https://arxiv.org/abs/2609.21137)（2026-09-17，cs.AR）

## 问题

Scratchpad tensor accelerator 的 MoE decode 被路由后才知道的 expert 权重搬运卡住；Qwen3-30B-A3B 上 expert 权重加载占端到端延迟 **56%**，其中 **36.8%** 暴露在关键路径。

## 方法要点

- CARDAN 用 **共享 low-rank basis + 共享 VQ codebook + expert-private coefficient/index** 表示 gate/up 权重；down projection 保持 BF16。
- 把 routing-independent 的共享传输/投影与 routing-dependent 的私有传输/计算拆开，映射到 DMA、tensor engine、GpSimd、vector/scalar engine 并发执行。
- 评测平台为 AWS Trainium3，五个 MoE 模型，TP=4。

## 摘录数字（仅论文给出）

- Batch-1 decode vs AWS BF16 dense megakernel：**1.15–1.31×**；OLMoE batch 16：**1.70×**。
- MoE projection HBM read **−26–50%**，DMA-active time **−10–31%**。
- Gate/up 权重压缩 **3.92–4.92×**；蒸馏后五模型 PPL 均达到或优于各自 BF16 teacher。

**Working page:** [CARDAN](/papers/cardan-moe-scratchpad-dataflow.md)  
**Related:** [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md)
