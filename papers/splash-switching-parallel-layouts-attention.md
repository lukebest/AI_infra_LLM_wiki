---
type: Paper
title: "SPLASH: Switching Parallel Layouts of Attention (Serving)"
description: "中科院计算所 — 运行中热切换 TP/DP-attn/CP/DOP；吞吐 1.3–1.73×；中位切换开销 <0.51% step；异文于 HBF-SPLASH"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- attention
- kv-cache
- parallelism
- scheduling
- agentic-ai
- throughput
- latency
- gpu
- distributed
created: 2026-10-01
updated: 2026-10-01
timestamp: '2026-10-01T00:00:00Z'
paper_author: [Chuan Liu, Shuoming Zhang, Zhicheng Li, Qianqi Sun, Ruiyuan Xu, Qiuchu Yu, Xiyu Shi, Huimin Cui, Jiacheng Zhao]
year: 2026
arxiv: '2609.37626'
sources:
  - raw/papers/SPLASH_Switching_Parallel_Layouts_Attention_2026.pdf
  - raw/papers/splash-switching-parallel-layouts-attention.md
---

# SPLASH（布局切换）：服务中热切换 Attention 并行布局

> **命名**：与既有 [SPLASH（稀疏注意力×HBF）](/papers/splash-sparse-attention-hbf.md)（arXiv:2609.23816）**同名异文**。本文为 ICT CAS 的 **并行布局切换** 服务系统（arXiv:2609.37626）。

## 一句话结论

在请求不停机的前提下切换 attention 并行布局（TP / DP-attention / CP / 新提出的 **DOP**）；B200 上 GLM-5.3 端到端吞吐相对固定布局 **1.3–1.73×**；中位切换开销 **<0.51%** 所在 step（完整切换 e2e **0.02–11.76 ms**，阻塞式可达 **667.31 ms**）。

## 动机

- Reasoning / agentic / RL-rollout：批次从「大量短请求」演变为「少数超长上下文」，最优布局随运行变化；现有引擎启动时钉死布局。
- 现代少/无 KV head 的注意力使 **权重分片** 与 **KV 归属** 可解耦——布局差异主要是谁持有权重与 cache。

对照 [Disaggregated Inference](/concepts/disaggregated-inference.md)、[Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md)、[Parallelism Transition Point](/concepts/parallelism-transition-point.md)。

## 方案

1. **复用+后台搬移+批边界交接**：多数状态已在目标布局所需位置；缺态按层在推理背景传输，step 边界 handoff。
2. **Decoupled Ownership Parallelism (DOP)**：权重按 TP 切、每请求 KV 单 owner（如 DP-attn）；相对 DP-attn **不复制**，KV 容量 **+27–60%**（GLM-5.3 FP8@T=8 每卡多出 **12.69 GiB** 给 KV）。
3. **过渡感知调度**：分析模型选当前最优布局；四布局随负载跟踪。
4. **实现**：SGLang 0.5.10 fork；GLM-5.3@B200、DeepSeek-V3.2@H200、GLM-5.3-Flash@DCU。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| e2e 吞吐 vs 固定布局（GLM-5.3@B200） | **1.3–1.73×** |
| 切换中位开销 | **<0.51%** step |
| 完整切换 e2e | **0.02–11.76 ms**（vs 阻塞最高 **667.31 ms**） |
| DOP vs DP-attn KV 容量 | **+27–60%**；示例 **+12.69 GiB/GPU** |
| 固定布局长上下文：DOP vs CP | 最长四点吞吐 **3.4–10.6%** 更高（文中测量段） |

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 运行时并行布局作为服务旋钮
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — DOP 释放的是 **KV 容量** 而非介质层级
- [SPLASH（HBF）](/papers/splash-sparse-attention-hbf.md) — 同名异文：稀疏×闪存 vs 布局热切换

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.37626) — Liu et al., arXiv:2609.37626
[2] [raw stub](raw/papers/splash-switching-parallel-layouts-attention.md)
