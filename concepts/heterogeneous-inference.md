---
type: Concept
title: Heterogeneous Inference
description: GPU + LPU 异构推理，分别优化 prefill/decode
tags:
- inference
- gpu
- lpu
- architecture
- serving
- agentic-ai
timestamp: '2026-05-08T00:00:00Z'
created: 2026-04-16
sources:
- raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
---

# Heterogeneous Inference（异构推理）

使用不同类型的加速器分别处理推理流水线的不同阶段，以同时优化吞吐和延迟。

## 动机
推理不是单一负载——prefill 和 decode 对硬件要求完全不同：
- **Prefill**：compute 密集，适合大 batch GPU 吞吐优化
- **Decode**：memory-bandwidth 密集，小 batch，延迟敏感

即使同为 decode 阶段，不同操作的特性也不同：
- **Attention**：stateful（动态 KV cache），memory-bound，GPU 利用率不随 batch 提升
- **FFN / MoE Expert**：stateless，compute-bound（dense）或 sparse（MoE），利用率随 batch 提升

单一架构无法同时最优化所有操作。

## Vera Rubin + LPX 异构方案

### 两种使用模式

#### 1. Attention FFN Disaggregation（AFD）
- **GPU 负责**：Attention（decode 阶段，stateful，需要大量 HBM 存 KV cache）
- **LPU 负责**：FFN / MoE expert（stateless，确定性架构适配静态工作负载）
- Ping-pong pipeline 掩盖 GPU↔LPU 通信延迟
- 源自 [Megascale Infer 2504.02263](/papers/megascale-infer-2504.02263.md) 和 Step-3

#### 2. Speculative Decoding
- **LPU 运行**：Draft model 或 MTP layer（利用低延迟）
- **GPU 验证**：Main model warm prefill k 个 draft tokens
- 通常 1.5-2× output tokens per decode step
- Draft model 需要 KV cache → 使用 FPGA 附加 DDR5（256 GB/FPGA）
- GPU 侧负载感知调度见 [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md)（confidence + batch 容量动态截断 verify）

### AFD 为什么 work
MoE 稀疏性 → 每个 expert effective batch 小 → 解耦后 GPU HBM 全给 KV cache → 更多 token → expert batch 增大 → FFN 回到 compute-intensive

## Agentic AI 的推动
- Agent 推理循环中延迟跨步骤累积
- 稳定的 per-token 性能和强 tail-latency 表现至关重要
- 需要 ~1000+ tokens/sec/user

## 实证基础

[Understanding Inference Scaling For Llms](/papers/understanding-inference-scaling-for-llms.md) 系统量化了 prefill/decode 的正交资源需求，为异构推理提供了实证基础：
- Prefill: compute-bound, 适合高 TFLOP GPU
- Decode: bandwidth-bound, 适合 memory-centric 架构（如 LPU SRAM）
- 见 [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) 的详细分析

## 相关页面
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPX 实体
- [Nvidia Vera Rubin Nvl72](/entities/nvidia-vera-rubin-nvl72.md) — GPU 侧
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 解耦推理概念
- [Lpu Architecture](/concepts/lpu-architecture.md) — LPU 架构
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — Prefill vs Decode 资源分歧
- [Understanding Inference Scaling For Llms](/papers/understanding-inference-scaling-for-llms.md) — 推理 scaling 系统分析

# Citations

[1] [raw/articles/nvidia-groq3-lpx-blog-2026-04.md](raw/articles/nvidia-groq3-lpx-blog-2026-04.md)
[2] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
