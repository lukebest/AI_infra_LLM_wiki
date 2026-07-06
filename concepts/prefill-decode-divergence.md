---
type: Concept
title: Prefill-Decode Resource Divergence
description: Prefill（compute-bound）vs Decode（bandwidth-bound）资源需求正交，>99% 时间在 decode
tags:
- inference
- prefill
- decode
- kv-cache
- latency
- throughput
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-15
sources:
- raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf
- raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf
---

# Prefill-Decode Resource Divergence（Prefill vs Decode 资源分歧）

## 定义

LLM 推理的两个阶段——Prefill 和 Decode——对硬件资源的需求**正交**：Prefill 是 compute-bound，Decode 是 memory-bandwidth-bound。Reasoning-centric 工作负载（OSL ≫ 10k）将 >99% wall-clock time 花在 decode，使系统长期处于低 arithmetic intensity 的低效状态。

## 两阶段特性对比

| Dimension | Prefill | Decode |
|-----------|---------|--------|
| **Compute Type** | Matrix-Matrix (GEMM) + tiled attention | Matrix-Vector (GEMV) |
| **Attention Kernel** | [FlashAttention](/concepts/flashattention.md) / [FlashAttention-2](/concepts/flashattention-2.md) / [FlashAttention-3](/concepts/flashattention-3.md)（IO-aware prefill；H100 FP8） | FlashDecoding / [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) |
| **Arithmetic Intensity** | High（reuse weights across all tokens） | 极低（每 token 读全部 weights + KV） |
| **Bottleneck** | Compute (FLOPS) | Memory Bandwidth + Capacity |
| **SM Occupancy** | High | Low / Variable |
| **HBM BW Utilization** | Low (≈20-30%) | High (≈85% for 8B) |
| **Latency Proxy** | TTFT | TPOT |
| **Reasoning Share** | <1% | **>99%** |

## 核心矛盾

同一加速器（如 H200）无法同时最优化两个阶段：
- Prefill 需要高 TFLOP tensor cores，HBM 带宽不是瓶颈
- Decode 需要高 HBM 带宽和容量，tensor cores 大量闲置

推理模型的出现使这一矛盾尖锐化：
- Standard chat（OSL ≈ 500）：prefill 占比尚可
- Reasoning（OSL ≫ 10k）：>99% 时间在 decode 的低效 regime

## 实测数据（H200）

### Small Model (8B)
- Prefill: HBM BW util ≈30%, high SM occupancy
- Decode: HBM BW util ≈85%, variable SM occupancy
- 两者呈"两台不同机器"的行为

### Frontier Model
- 405B Decode: HBM BW util ≈65% (weights reads dominate)
- 671B Decode: HBM BW util ≈50-60% (sync/routing latency, 非 bandwidth bound)
- 大模型 decode 的 low BW util 说明瓶颈已从纯带宽转向 sync 开销

## Reasoning 的乘数效应

### KV Cache 增长
- KV cache 线性增长 with OSL
- Decode KV 是 **persistent**（prefill KV 是 transient）
- 8B: 20M token aggregate output → 2 TB KV demand
- 405B: 1.05 MB/token → batch=1K with long context = 100% saturation

### Agentic AI 进一步放大
Agent 工作负载将推理从单条长链变为**多步有状态执行**：
- Planner / executor / verifier / retrieval / tool calls 各维护 KV state
- Fan-out × branching depth × tool interaction → **multiplicative** memory demand
- CPU-GPU tight coupling：CPU 维持 agent environments, tool execution, per-agent state
- 瓶颈从 isolated GPU → system-wide（HBM + host DRAM 同时受压）

## 硬件解耦方向

论文提出将 prefill 和 decode **物理解耦**到不同硬件：

### Prefill Tier
- 高 TFLOP accelerators（compute-optimized）
- Moderate HBM bandwidth 即可
- 可以接受 cost-optimized memory subsystem

### Decode Tier  
- Memory-centric hierarchy
- HBM → DDR/LP → CXL → NVMe tiered KV placement
- 3D-stacked memory（如 D-Matrix SRAM-based）缓解 KV read bandwidth
- HBF (High-Bandwidth Flash)：增容但有 read/write asymmetry + power 挑战

### 3D-stacked AI chip 视角（Voxel 论文）

[Voxel](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) 在 [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) 上量化了两阶段对设计旋钮的不同响应：

| 设计旋钮 | Prefill（compute/NoC-bound） | Decode（memory-bound） |
|----------|------------------------------|------------------------|
| DRAM 带宽 | 扩 BW 收益有限 | 显著降 latency，~10 TBps 后平台 |
| NoC 带宽 | 低于 32 B/cycle 显著拖慢 | 不敏感 |
| Per-core SRAM | 大 SRAM 收益有限（FLOPS 已饱和） | 大 SRAM 利于 prefetch，BW 饱和后递减 |
| Compute paradigm | compute-shift 相对 SPMD **46.73%** 提升 | paradigm 差异仍存在但 NoC 非主瓶颈 |
| Core 数量 | 过多 core 加剧 bank 冲突 | 同上，能效可能下降 |

### 绑定互连
- NVLink + optical interconnects 跨 tier 低延迟
- Explicit KV placement, migration, proactive eviction

## 与现有概念的关联

这一发现为以下已有 wiki 概念提供了**实证基础**：

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — Prefill/Decode 解耦是该概念的阶段层变体
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 不同阶段用不同硬件是异构推理的核心动机
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — Decode 阶段是 capacity trap 的主战场
- [Reasoning Cliff](/concepts/reasoning-cliff.md) — Decode 的 KV 线性增长导致 cliff
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — 不同阶段的 optimal parallelism 不同（prefill: DP; decode: TP）
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — decode 步 speculative 提高有效 τ（DeepSeek-V4 生产 +57–85% tok/s/user）
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — GPU kernel 层：异步 partial softmax + flat GEMM + 启发式 GEMV/GEMM dataflow（相对 FlashDecoding ~1.37×）
- [FlashAttention](/concepts/flashattention.md) — IO-aware 精确 attention 起源（NeurIPS 2022）
- [FlashAttention-2](/concepts/flashattention-2.md) — prefill/训练 IO-aware attention（相对 FA ~2×，73% A100 峰值）
- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper 异步 + FP8（740 TFLOPs/s，相对 FA2 1.5–2×）
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 3D 堆叠缓解 BW wall，prefill/decode 对 DRAM/NoC/SRAM 响应不同
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — KV spill 至 NVMe tier 的延迟与带宽

## 相关概念

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 模块层和阶段层的解耦推理
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构硬件针对不同推理阶段
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — Decode 阶段的 KV 饱和问题
- [Reasoning Cliff](/concepts/reasoning-cliff.md) — KV 增长的时序行为
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — decode kernel 层（attention/flat GEMM）
- [FlashAttention](/concepts/flashattention.md) — IO-aware 精确 attention 起源
- [FlashAttention-2](/concepts/flashattention-2.md) — prefill/训练 attention kernel
- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper prefill/训练 + FP8
- [Kv Cache](#kv-cache) — KV cache 是 decode 阶段的核心资源

# Citations

[1] [raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf](raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf)
