---
type: Raw Source
title: "Crossflow: Prefill–Decode Elasticity for Agentic LLM Serving"
description: "Meta — decode 节点可撤销租约做本地 prefill；相对静态 P/D 吞吐 geomean +16.2–17.4%，高负载最高 +43.4%。"
timestamp: '2026-09-24T00:00:00Z'
source_url: https://arxiv.org/abs/2609.27085
arxiv: '2609.27085'
ingested: 2026-09-24
sha256: 57ad56261e34e8e8a48f0d6b2f72a7d0425ff39f4195c3fc0c03f1cfe73f5268
---

# Crossflow: Prefill–Decode Elasticity for Agentic LLM Serving

**Authors:** Yi Xu, Ehsan K. Ardestani, Wenyin Fu, Martin Schatz, Krishna Malladi, Zhan Shu, Adnan Aziz, Shobhit Kanaujia, Ajit Mathews, Chunqiang Tang  
**Affiliation:** Meta Platforms  
**PDF:** [Crossflow_PD_Elasticity_Agentic_2026.pdf](Crossflow_PD_Elasticity_Agentic_2026.pdf)  
**arXiv:** [2609.27085](https://arxiv.org/abs/2609.27085)（2026-09-22，cs.DC）

## 问题

静态 P/D 分池无法跟上相位需求波动：舰队分钟级 uncached-in/out peak-to-mean 最高 **4.7×**；公开 agentic trace 日内小时比中位 **24.5×**；换 replica 需数十分钟。按 p95 定容会闲置最高约 **17%** 集群容量。

## 方法要点

- 节点角色固定，边界弹性：每个 decode 节点发布短寿命可撤销 **lease**，约束本地 prefill 算力、KV 容量、传输与投影输出。
- 评测：公开 + 内部 traces；GPT-OSS-120B 与 GLM-5.2（753B total / 40B active）于 NVIDIA GB300。

## 摘录数字（仅论文给出）

- 相对静态 P/D：token 吞吐 geomean **+16.2–17.4%**（请求/输入/输出分别为 16.6% / 17.4% / 16.2%）；高负载最高 **+43.4%**（输出）/ **+42.7%**（输入）。
- Mean TTFT：每个评测点均下降，**−10.0–34.4%**（内部 GLM-5.2 可达 **−32.2–47.7%**）。
- 动机：分钟级 peak-to-mean 最高 **4.7×**；agentic 小时比中位 **24.5×**；p95 定容闲置最高约 **17%**（文中各用例 17.5/10.8/13.8/12.0%）。

**Working page:** [Crossflow](/papers/crossflow-pd-elasticity-agentic.md)
