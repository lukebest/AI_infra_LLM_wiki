---
type: Raw Source
title: "Weave: Fine-Grained Dynamic SM Scheduling in an MoE Megakernel for Compute-Communication Overlap"
description: "Weave 原始论文来源：MoE persistent megakernel 内的动态通信/计算 SM 调度。"
timestamp: '2026-09-22T00:00:00Z'
source_url: https://arxiv.org/abs/2609.21483
arxiv: '2609.21483'
ingested: 2026-09-22
sha256: 3b2e432b69acf5d372856866e5312a63c370983262006585e0a4e98badd7bd20
---

# Weave: Dynamic SM Scheduling for MoE Overlap

**Authors:** Ziyu Huang, Yangjie Zhou, Chenhao Zhu, et al.  
**Affiliation:** Shanghai Jiao Tong University; National University of Singapore; Alibaba Group  
**PDF:** [Weave_Dynamic_SM_MoE_Overlap_2026.pdf](Weave_Dynamic_SM_MoE_Overlap_2026.pdf)  
**arXiv:** [2609.21483](https://arxiv.org/abs/2609.21483)（2026-09-18，cs.DC）

## 问题

MoE expert-parallel inference 的 dispatch/combine 与 GEMM 共用 SM。固定或每 iteration 才调整一次的 SM 切分无法跟随每层、每 GPU 的 routing skew，并留下中段 idle bubble。

## 方法要点

- 单个 persistent megakernel 融合 dispatch、GEMM0、activation、GEMM1、combine。
- 层内 cost model 联合搜索 communication SM 数量与 chunk 数；chunk pipeline 把 combine 插入 GEMM，bubble stealing 让空闲通信 SM 接 GEMM tile。
- 评测为 4×H100 SXM、EP=4、六个 MoE 模型。

## 摘录数字（仅论文给出）

- 相对五个基线，MoE 层几何平均 **1.95–4.76×**；摘要汇总 **2.89×**。
- 端到端几何平均 **1.12–1.70×**；摘要汇总 **1.33×**。
- DSv2-Lite 上通信-计算同时活跃比例 **47.1%**；在线 cost model **0.54 μs**，配置选择与穷举最优平均差 **8.2%**。

**Working page:** [Weave](/papers/weave-dynamic-sm-moe-overlap.md)  
**Related:** [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)
