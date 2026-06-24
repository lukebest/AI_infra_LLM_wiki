---
type: Concept
title: Inference Capacity Trap
description: 推理容量陷阱：KV cache 饱和导致 preemption + recomputation，throughput 崩溃
tags:
- inference
- reasoning
- capacity-trap
- kv-cache
- serving
- parallelism
timestamp: '2026-06-15T00:00:00Z'
created: 2026-06-15
sources:
- raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf
---

# Inference Capacity Trap（推理容量陷阱）

## 定义

在 reasoning-centric LLM 推理中，增加并发请求数（concurrency）只在 KV cache 饱和前提升 throughput；一旦 KV cache 耗尽 HBM 容量，scheduler 被迫 preempt 请求，触发 recomputation，导致 throughput 崩溃。这一非线性退化现象称为 **Capacity Trap**。

## 机制

```
Concurrency ↑ → 初始 throughput ↑
                → KV cache 线性增长（OSL ≫ 10k tokens）
                → HBM 饱和
                → Scheduler preempt（防 OOM）
                → Prefix cache 失效（内存耗尽下通常 miss）
                → Full prefill recomputation
                → Tail latency 飙升 → throughput 崩溃
```

## 根因：DP 的内存不池化

Data Parallelism（DP）是最常见的推理缩放策略，但存在结构性缺陷：

1. **Weight Replication**: 每个 GPU 复制完整模型权重（如 32B = 64 GB FP16/卡），仅剩有限空间给 KV cache
2. **Request Partition**: 请求分配到各 replica，但一个请求的 KV cache 不能跨 replica 存取
3. **Stranded Capacity**: GPU 0 在 thrash 时，GPU 1 可能有空闲 KV blocks → 资源浪费
4. **Tail Latency**: 整体 tail latency 由**最先**达到 KV 饱和的 replica 决定

**H200 实测**（DP=8, BS=5000）：
- 每卡分配 ≈625 请求，独立面对同样的 capacity wall
- HBM bandwidth utilization 呈 "sawtooth"（40%-85%），因 prefill/decode 交替
- Aggregate HBM ≈1.1 TB 但无法有效利用

## TTFT-TPOT 权衡

Capacity Trap 导致服务质量呈现凸形 Pareto frontier：

| Concurrency | TTFT | TPOT | E2E |
|------------|------|------|-----|
| 低 (<2K) | 高（queue bound） | 低（资源充裕） | queue-dominated |
| **Sweet spot (≈2K)** | **中** | **中** | **最优** |
| 高 (>2K) | 低 | 高（capacity+BW 争用） | preemption-dominated |

- **TTFT**（queue-bound）：concurrency ↑ → admission 等待 ↓
- **TPOT**（bandwidth+capacity bound）：concurrency ↑ → 每请求可用内存/带宽 ↓
- **最优 operating point**：TTFT 下降不再补偿 TPOT 恶化的拐点

## 解决方案方向

### 1. KV-aware Admission Control
不盲目最大化 concurrency，而是基于 available HBM headroom + active sequence length + expected decode growth 动态设定并发上限。

### 2. Tensor Parallelism（释放 KV capacity）
- Sharding weights → 每 GPU 只存 1/N weights → 释放 HBM 给 KV cache
- 32B 是 DP→TP 的 inflection point（见 [Parallelism Transition Point](/concepts/parallelism-transition-point.md)）
- TP=8 时 32B 模型：weights 从 64 GB → 8 GB/卡，KV 空间从 77 GB → 133 GB

### 3. Memory Pooling / Tiering
- HBM → DDR → CXL → NVMe 显式 KV placement 和 migration
- Proactive eviction + compression + reuse
- 见 [Disaggregated Inference](/concepts/disaggregated-inference.md) 的 tiered memory 讨论

### 4. 架构级 KV 压缩
- **MLA (Multi-Head Latent Attention)**：DeepSeek-R1 将 KV 压缩为低秩 latent vector
- **GQA**: 减少 KV heads（3-8× 压缩 vs MHA）
- 这些缓解但不消除 capacity trap——KV 仍线性增长

## 与 Reasoning Cliff 的关系

Capacity Trap 是**机制**（为什么 throughput 崩溃），[Reasoning Cliff](/concepts/reasoning-cliff.md) 是**现象**（KV cache 何时超过 HBM 容量）。Reasoning workload 因 OSL ≫ 10k 将 cliff 提前，有时甚至在 prefill 阶段就饱和。

## 相关概念

- [Reasoning Cliff](/concepts/reasoning-cliff.md) — KV 饱和导致 scheduler 进入 convoy mode
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — DP→TP 切换的模型规模阈值
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — decode 阶段是 capacity trap 的主战场
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — prefill/decode 物理解耦作为根本性解决方案
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构硬件针对性优化 decode

# Citations

[1] [raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf](raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf)
