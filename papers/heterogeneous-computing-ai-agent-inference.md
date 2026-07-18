---
type: Summary
title: 'Heterogeneous Computing for AI Agent Inference'
description: Zhao & Liu — OI/CF framework beyond roofline for agent inference; snowballing contexts (300K–1M tokens) expose memory capacity wall and system heterogeneity need
tags:
- agentic-ai
- ai-agent
- inference
- llm
- memory
- accelerator
- memory-bandwidth
- optimization
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Heterogeneous_Computing_AI_Agent_Inference_2026.pdf
---

# Heterogeneous Computing for AI Agent Inference

**Authors:** Aaron Zhao, Junyi Liu | **Affiliations:** Imperial College London, Microsoft Research | **PDF:** [raw/papers/Heterogeneous_Computing_AI_Agent_Inference_2026.pdf](raw/papers/Heterogeneous_Computing_AI_Agent_Inference_2026.pdf)

## 一句话总结

本文用 **Operational Intensity (OI)** 与 **Capacity Footprint (CF)** 刻画 AI agent 推理：agent 工作流（coding/WUA/CUA）上下文雪崩至 **300K–1M** tokens，暴露 roofline 未覆盖的 **memory capacity wall**，论证未来需 compute/network/memory **系统级异构**。

## 核心贡献

1. **OI + CF 双指标**：补全 roofline/MFU/MBU 对 memory capacity 限制的盲区（“双低”区域）
2. **Agent 工作负载画像**：Chatbot vs Coding vs Web-use vs Computer-use 在 LLaMA-70B 上 CF/OI 差异巨大
3. **Snowballing context**：Agent 多轮交互（~20–30 次/任务）使 CF 快速超过单卡 B200 HBM
4. **架构/优化映射**：MHA/GQA/MLA、MoE、量化、prefill-decode 分离各改变 OI/CF 象限
5. **异构 scaling 论点**：加卡解 CF 但不提 OI — 需跨 compute、互联、memory 的 cohesive datacenter 设计

## 关键数字

| 设置 | 结果 |
|------|------|
| Coding agent context | **300K–1M** tokens (typical snowball) |
| Env interactions / task | **20–30** (reported) |
| CF vs B200 | Most agent CF exceeds single-card capacity at modest batch |
| Decode OI | Extremely low — DRAM load dominates over compute |

## 与 wiki 交叉引用

- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构推理部署框架
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — capacity/OI 双低下的 serving 困境
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — prefill vs decode OI/CF 差异
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — prefill-decode 分离作为 CF/OI 优化
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — KV capacity 管理基线

# Citations

[1] [raw/papers/Heterogeneous_Computing_AI_Agent_Inference_2026.pdf](raw/papers/Heterogeneous_Computing_AI_Agent_Inference_2026.pdf) — Zhao & Liu (2026)
[2] [raw/papers/heterogeneous-computing-ai-agent-inference.md](raw/papers/heterogeneous-computing-ai-agent-inference.md) — 结构化摘录
