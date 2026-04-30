---
title: Heterogeneous Inference
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [inference, gpu, lpu, architecture, serving, agentic-ai]
sources: [raw/articles/nvidia-groq3-lpx-blog-2026-04.md]
---

# Heterogeneous Inference（异构推理）

使用不同类型的加速器分别处理推理流水线的不同阶段，以同时优化吞吐和延迟。

## 动机
推理不是单一负载——prefill 和 decode 对硬件要求完全不同：
- **Prefill**：compute 密集，适合大 batch GPU 吞吐优化
- **Decode**：memory-bandwidth 密集，小 batch，延迟敏感，适合 LPU

单一架构无法同时最优化两者。

## Vera Rubin + LPX 异构方案
- [[nvidia-vera-rubin-nvl72]]：处理 prefill + decode attention
- [[nvidia-groq-3-lpx]]：处理 FFN / MoE expert（延迟敏感部分）
- 结果：扩展 Pareto 前沿，不牺牲 AI factory 吞吐

## Agentic AI 的推动
- Agent 推理循环中延迟跨步骤累积
- 稳定的 per-token 性能和强 tail-latency 表现至关重要
- 需要 ~1000+ tokens/sec/user

## 相关页面
- [[nvidia-groq-3-lpx]] — LPX 异构推理实例
- [[nvidia-vera-rubin-nvl72]] — GPU 侧
- [[interactive-inference]] — 交互式推理需求
