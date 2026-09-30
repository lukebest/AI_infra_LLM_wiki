---
type: Paper
title: "SpecStream: Resource-Efficient Speculative Decoding with Streamed KV"
description: "西交大 — SGLang；A800；vs 卸荷基线吞吐 Qwen3 均值 1.41×、InternLM2.5 1.32×；同 GPU 相对分卡投机每 GPU 吞吐均值 +55.4%"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- speculative-decoding
- kv-cache
- decode
- gpu
- memory
- scheduling
- throughput
- latency
created: 2026-09-30
updated: 2026-09-30
timestamp: '2026-09-30T00:00:00Z'
paper_author: [Fei Li, Song Liu, Shiqiang Nie, Jinyu Wang, Weiguo Wu]
year: 2026
arxiv: '2609.33184'
sources:
  - raw/papers/SpecStream_Resource_Efficient_Speculative_Decoding_2026.pdf
  - raw/papers/specstream-resource-efficient-speculative-decoding.md
---

# SpecStream: 长上下文投机解码的流式 KV 卸荷

## 一句话结论

在 **KV 卸荷到 CPU** 的投机解码路径上，只迁移 Target **已提交**历史、分块 H2D + 跨 verification query 共享 + online softmax，并在同 GPU 用 TPC mask 做 Target-priority Draft 共执行；相对卸荷基线吞吐均值 **1.41×（Qwen3）/ 1.32×（InternLM2.5）**，相对分卡并行投机每 GPU 吞吐均值 **+55.4%**。

## 动机

- 投机解码缩短 Target 串行步，但 Draft/Target 权重与候选 KV 一并吃满 GPU；长上下文仍逼出 **KV 卸荷**。
- 既有卸荷往往整段历史到齐才算 attention，且未摊薄 verification 轮内多 query 对同一 committed 历史的共享；H2D 等待留下 **compute bubble**。
- 并行投机（分卡 Draft/Target）掩盖草拟延迟，却未用 Target GPU 上的空泡推进 Draft。

对照 [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md)、[SPECTRA](/papers/spectra-speculative-decoding-tiled.md)、[HeteroReason](/papers/heteroreason-fpga-gpu-speculative-reasoning.md)、[Fathom](/papers/fathom-sparse-decoding-offloaded-kv.md)。

## 方案

1. **Commit-aligned 卸荷**：仅异步卸荷 Target 已提交历史；候选 rollback 留在 GPU。
2. **Streamed verification**：历史分块到达即参与 attention；轮内多 query 共享同一历史块；online softmax 保完整因果注意力。
3. **Target-priority 同 GPU 共执行**：TPC mask 限制 Draft 可用集群，运行时按 Target 延迟估计控制 Draft 准入，压低干扰。
4. **评测**：实现于 SGLang；**A800 80GB** PCIe Gen4 + 240GB host；模型对 Qwen3-32B/0.6B、InternLM2.5-20B-*；LongBench v2 / MRCR 等；基线含卸荷投机与分卡并行投机（SPECTRE+Offload 等）。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 吞吐 vs 卸荷基线（跨数据集均值） | Qwen3 **1.41×**；InternLM2.5 **1.32×** |
| 同 GPU vs 分卡并行投机（每 GPU 输出吞吐） | 均值 **+55.4%** |
| 硬件 | A800 80GB；PCIe Gen4×16 ≈**31.5 GB/s** vs HBM **1935 GB/s**（文中对比） |
| 质量 | 任务质量接近 SGLang 投机解码基线（摘要） |

## 与 wiki 的关系

- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 系统侧 **卸荷×投机** 调度轴
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — H2D 流式 KV 与 commit 边界
- [HeteroReason](/papers/heteroreason-fpga-gpu-speculative-reasoning.md) / [SPECTRA](/papers/spectra-speculative-decoding-tiled.md) — 异构/瓦片投机；本文是 **同 GPU + CPU 卸荷**

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.33184) — Li et al., arXiv:2609.33184
[2] [raw stub](raw/papers/specstream-resource-efficient-speculative-decoding.md)
