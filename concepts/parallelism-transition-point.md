---
type: Concept
title: Parallelism Transition Point
description: 并行度切换点：32B 是 DP→TP inflection，MoE 需 hybrid PP+TP
tags:
- inference
- parallelism
- serving
- kv-cache
- gpu
timestamp: '2026-06-15T00:00:00Z'
created: 2026-06-15
sources:
- raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf
---

# Parallelism Transition Point（并行度切换点）

## 定义

在 LLM 推理中，随着模型规模增大，最优并行策略从 Data Parallelism（DP）切换到 Tensor Parallelism（TP）或 hybrid DP+TP 的模型规模阈值。论文通过 8B-671B 的系统实验确定了这一 inflection point。

## 三个规模区间

### 1. Small (8B-14B): DP Dominant

- Weights fit comfortably in per-GPU HBM（8B ≈16 GB, 14B ≈28 GB）
- TP 的 all-reduce 通信开销**不值得**——通信 > 内存释放收益
- DP=8 optimal（near-linear throughput scaling）
- Hybrid（如 PP=2+TP=4）比纯 DP 慢 3.5×

### 2. Medium (32B): The Inflection Point

**关键阈值**: 32B 是 DP→TP 的切换点

| Strategy | Speedup (8 GPU) | Why |
|----------|----------------|-----|
| DP=8 | 4.9× | Weight replication (64 GB) leaves only 77 GB KV |
| TP=8 | 6.15× | Weights shard to 8 GB/GPU, releases 133 GB KV |
| **DP=4+TP=2** | **Optimal** | Min TP degree (reduce comm) + DP concurrency |

**核心洞察**: TP 的收益来自**释放 KV capacity**（缓解 [Inference Capacity Trap](/concepts/inference-capacity-trap.md)），而非加速 kernel 执行。性能 inflection 与 DP replicas 达到 KV-capacity-bound 的点对齐。

### 3. Frontier (405B-671B): Architecture-Dependent

**Dense (Llama-405B)**:
- KV: 1.05 MB/token → 需要所有 GPU 内存
- DP=1 forced, TP=8 or PP=8
- TP=8: 986s ✓ | PP=8: 7537s ✗（dense activation 太大 → pipeline bubbles 无法填满）

**MoE (DeepSeek-R1-671B)**:
- 37B active params → 低 compute-to-communication ratio
- TP=8 的 all-reduce 成瓶颈（GPU 间计算时间不足以掩盖同步）
- MLA 压缩 KV → 支持 higher micro-batch depth → 填满 PP bubbles
- **PP=4+TP=2: 1663s ✓** (beats TP=8: 2047s)

## 切换判据

论文给出经验判据：

```
if model_weights_per_gpu < HBM_capacity × 0.4:
    → DP (weights comfortably fit, KV space sufficient)
elif model_weights_per_gpu < HBM_capacity × 0.6:
    → Hybrid DP+TP (minimal TP to release KV space)
else:
    → TP or PP (all memory needed)
    
if MoE and active_params/token is low:
    → prefer PP+TP over pure TP (sync latency dominates)
```

## Bandwidth-Compute Inversion

论文发现一个反直觉现象：

| Model Size | HBM Utilization | Bottleneck |
|-----------|----------------|------------|
| 8B | ≈85% | Memory bandwidth |
| 70B | ≈70% | Mixed |
| 671B (MoE) | ≈50-60% | **Sync + routing latency** |

→ 超大 MoE 模型**不是** bandwidth-bound，而是 synchronization-bound。这解释了为何 high-degree TP 对 MoE 不利。

## MLA 的关键角色

DeepSeek-R1 的 [MLA](/concepts/csa-hca.md)（Multi-Head Latent Attention）在推理优化中起到双重作用：
1. **压缩 KV cache** → 延缓 [Reasoning Cliff](/concepts/reasoning-cliff.md) 到来
2. **使 PP 可行** → reduced KV 允许更高 micro-batch depth → 填满 pipeline bubbles

这是 MoE + MLA 天然适配 PP 架构的根本原因。

## 决策矩阵

| Model | Type | Optimal | E2E (2K BS) | Key Factor |
|-------|------|---------|-------------|------------|
| 8B | Dense | DP=8 | — | Weight fits, comm not justified |
| 14B | Dense | DP=8 | 332s | Same |
| 32B | Dense | DP=4+TP=2 | 484s | Weight replication exceeds HBM |
| 70B | Dense | Hybrid TP | — | Mixed regime |
| 405B | Dense | TP=8 | 986s | KV footprint demands all memory |
| 671B | MoE | PP=4+TP=2 | 1663s | Sync latency, MLA advantage |

## 相关概念

- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — TP 通过释放 KV capacity 解决 capacity trap
- [Reasoning Cliff](/concepts/reasoning-cliff.md) — 并行度选择影响 cliff 到来时机
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 超越单一并行策略的解耦方案
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构硬件下的并行度选择
- [Deepseek V4](/summaries/deepseek-v4.md) — MLA 架构使 PP 在 MoE 场景下可行

# Citations

[1] [raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf](raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf)
