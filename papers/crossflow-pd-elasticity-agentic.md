---
type: Paper
title: "Crossflow: Prefill–Decode Elasticity for Agentic Serving"
description: "Meta — decode 租约弹性本地 prefill；相对静态 P/D 吞吐 geomean +16.2–17.4%，高负载最高 +43.4%"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- disaggregated-inference
- prefill
- decode
- kv-cache
- agentic-ai
- throughput
- latency
created: 2026-09-24
updated: 2026-09-24
timestamp: '2026-09-24T00:00:00Z'
paper_author: [Yi Xu, Ehsan K. Ardestani, Wenyin Fu, Martin Schatz, Krishna Malladi, Zhan Shu, Adnan Aziz, Shobhit Kanaujia, Ajit Mathews, Chunqiang Tang]
year: 2026
arxiv: '2609.27085'
sources:
  - raw/papers/Crossflow_PD_Elasticity_Agentic_2026.pdf
  - raw/papers/crossflow-pd-elasticity-agentic.md
---

# Crossflow: Prefill–Decode Elasticity for Agentic LLM Serving

## 一句话结论

在**不改节点角色**的前提下，让 decode 节点用短寿命可撤销租约借出本地 prefill 能力，使 P/D 边界弹性化：相对静态分池，token 吞吐 geomean **+16.2–17.4%**，高负载最高 **+43.4%**，且每个评测点 mean TTFT 都下降。

## 动机

- 静态 P/D 换 replica 需数十分钟，而相位比波动更快：舰队分钟级 uncached-in/out peak-to-mean 最高 **4.7×**；公开 agentic 日内小时比中位 **24.5×**。
- 按 p95 定容闲置最高约 **17%** 集群容量；定低则一侧排队、一侧空转。
- Agentic 流量（成簇到达、tool 释放、前缀复用、输出长度发散）放大错配。对照 [PDD](/papers/pdd-cross-datacenter-prefill-decode-disaggregation.md) 的跨 DC 静态异构、[PipeSwift](/papers/pipeswift-pipeline-parallel-agentic-serving.md) 的 PP 代理服务。

## 方案

1. Decode 节点保持 decode-first，但发布 **lease**：上限约束本地 prefill 算力、KV 容量、传输工作量与投影输出。
2. 租约短寿命、可撤销，避免长期侵占 decode 余量。
3. 评测：公开 TraceLab + 内部 traces；GPT-OSS-120B、GLM-5.2（753B/40B active）于 **GB300**。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| Token 吞吐 vs Static P/D | geomean **+16.2–17.4%**（req/in/out：16.6/17.4/16.2%） |
| 高负载峰值 | 输出 **+43.4%**、输入 **+42.7%** |
| Mean TTFT | 每点下降 **−10.0–34.4%**（内部 GLM 可达 −32.2–47.7%） |
| 动机波动 | 分钟 peak-to-mean **4.7×**；agentic 小时比中位 **24.5×**；p95 闲置最高 ≈**17%** |

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) / [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — 弹性边界补丁
- [PDD](/papers/pdd-cross-datacenter-prefill-decode-disaggregation.md) — 跨 DC 异构 PD；本文是 **同集群边界弹性**
- [PipeSwift](/papers/pipeswift-pipeline-parallel-agentic-serving.md) — agentic JCT；本文聚焦 **P/D 容量错配**

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.27085) — Xu et al., Meta, arXiv:2609.27085
[2] [raw stub](raw/papers/crossflow-pd-elasticity-agentic.md)
