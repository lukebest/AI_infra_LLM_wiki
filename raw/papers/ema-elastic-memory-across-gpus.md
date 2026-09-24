---
type: Raw Source
title: "EMA: Elastic and Performance Transparent Memory Across GPUs"
description: "伯克利 — 机内 GPU 互借 HBM；吞吐最高 +52%，达 2× 容量静态配置的 96%；借方预取 / 贷方可回收。"
timestamp: '2026-09-24T00:00:00Z'
source_url: https://arxiv.org/abs/2609.27040
arxiv: '2609.27040'
ingested: 2026-09-24
sha256: 3225a70fa1c920578e56b76f0e5b28d73d7ca2be5dd5d82956708d093127e42b
---

# EMA: Elastic and Performance Transparent Memory Across GPUs

**Authors:** Yi Xu, Tian Xia, Ion Stoica  
**Affiliation:** UC Berkeley  
**PDF:** [EMA_Elastic_Memory_Across_GPUs_2026.pdf](EMA_Elastic_Memory_Across_GPUs_2026.pdf)  
**arXiv:** [2609.27040](https://arxiv.org/abs/2609.27040)（2026-09-22，cs.DC）

## 问题

LLM 推理等负载内存需求动态：一张 GPU HBM 打满时，同机其他 GPU 仍可能空闲；静态实例绑定导致容量搁浅。

## 方法要点

- **Elastic Address Space (EAS)**：GPU 间借/还内存池；借方用预取掩盖远端访问；贷方可按需回收，性能不低于静态分区。
- 实现：memory-slice 进程 + slab/layer-group 预取；走 NVLink（评测 A100 双向最高约 600 GB/s）。
- 评测：A100 等多卡；LLaMA/OPT + Alpaca/ShareGPT 等。

## 摘录数字（仅论文给出）

- 相对静态分区，单用户吞吐最高 **+52%**。
- 达 **2×** 物理容量静态供给吞吐的 **96%**。
- 延迟与静态本地基线相近；EAS 可把可用地址空间扩到约 **2×** 本地 HBM（文中 doubling 叙述）。

**Working page:** [EMA](/papers/ema-elastic-memory-across-gpus.md)
