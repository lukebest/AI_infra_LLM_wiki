---
type: Concept
title: Reasoning Cliff
description: 推理悬崖：KV 线性增长使 HBM 饱和，scheduler 进入 convoy mode
tags:
- inference
- reasoning
- capacity-trap
- kv-cache
- decode
- latency
timestamp: '2026-06-15T00:00:00Z'
created: 2026-06-15
sources:
- raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf
---

# Reasoning Cliff（推理悬崖）

## 定义

当推理工作负载的 KV cache 增长超过可用 HBM 容量时，inference scheduler 被迫 preempt/recompute/reject 请求的临界点。在 reasoning-centric 工作负载中（OSL ≫ 10k tokens），KV cache 线性增长使 cliff 显著提前到来。

## 机制

### KV Cache 线性增长

| Model | KV/Token (FP16) | 10K tokens × 128 requests |
|-------|-----------------|--------------------------|
| Llama-405B (Dense, GQA) | ≈1.05 MB | ≈1.3 TB |
| DeepSeek-32B (Dense, GQA) | ≈262 KB | ≈336 GB |
| DeepSeek-R1-671B (MoE, MLA) | Low (compressed) | Moderate |

- Llama-405B: 单卡 H200 (141 GB) 远不够 → 必须 TP=8 聚合
- 8B 模型 20M token output aggregate → 2 TB memory demand

### Cliff 的时序行为

**Short-output workload**: cliff 出现在 decode 晚期，影响有限
**Reasoning workload (OSL ≫ 10k)**: cliff 提前，有时在 **prefill 阶段**就饱和：
- Batch=5K + long context: KV exhaustion during prefill
- 系统无法 even initialize requests → admission blocking

### Scheduler 的反应

1. **Chunked Prefill**: 仅处理子集 prompt tokens/iteration → 防 OOM 但引入 "Start-Up Latency"
2. **Preemption**: Running → Waiting queue，或 swap 到 CPU memory
3. **Convoy Mode**: 新请求仅在旧请求完成释放 KV blocks 后才能被 admit
4. **系统 stall 在 memory capacity management 而非 productive token generation**

## 度量指标

- **KV Cache Saturation**: 接近 100% 时触发 preemption
- **Request State Tracking**: Running/Waiting 比例反映系统健康度
- **HBM Bandwidth Sawtooth**: prefill/decode 交替导致的 BW 震荡

## 容量估计的局限性

论文指出：虽然 KV cache capacity 可以从 model + batch 参数解析估计来指导 admission control，但在动态长上下文 reasoning 负载下，scheduling effects 和 KV fragmentation 创造 transient capacity spikes，使得静态估计**不足以防止 preemption**。

→ 需要**在线** KV-aware admission control，而非静态阈值。

## 与 Capacity Trap 的区分

- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) 描述 **throughput 崩溃的因果链**（preemption → recomputation → collapse）
- Reasoning Cliff 描述 **KV saturation 的时间点和行为**（何时饱和、scheduler 如何反应）

两者是同一现象的不同视角：capacity trap 是"为什么"，reasoning cliff 是"什么时候"。

## 启示

1. **Admission 时预估未来 KV growth**：不能仅基于当前内存使用 admit 请求
2. **Decode throttling**: 主动限制并发 decode 流数量
3. **Priority policies**: 平衡 TTFT, TPOT, preemption risk
4. **Scheduling = memory traffic shaping**: HBM capacity bounds throughput, bandwidth bounds per-token latency

## 相关概念

- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 容量陷阱的完整因果机制
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — decode 阶段是 reasoning cliff 的主战场
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — TP 通过释放 KV capacity 延缓 cliff 到来
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — tiered memory 超越单卡 HBM 限制

# Citations

[1] [raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf](raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf)
