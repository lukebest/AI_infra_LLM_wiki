---
type: Concept
title: FlashDecoding++
description: GPU LLM 推理引擎：统一 max 值的异步 partial softmax、M 维 pad-8 flat GEMM+双缓冲、FastGEMV/CUTLASS 启发式 dataflow；相对 FlashDecoding 平均 1.37×、HF 最高 4.86×
tags:
- inference
- llm
- gpu
- decode
- attention
- kernel
- serving
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf
---

# FlashDecoding++

**FlashDecoding++**（Infinigence-AI / 清华 / 上交 / 北大, arXiv 2024）是面向 **GPU LLM 推理**的 kernel 级加速引擎，在 FlashDecoding 之上解决 decode 阶段三类瓶颈：**partial softmax 同步**、**flat GEMM 算力浪费**、**单一静态 GEMM dataflow**。支持 Llama2、OPT、ChatGLM2 等主流模型及 NVIDIA/AMD 后端。

**Authors:** Ke Hong, Guohao Dai†, Jiaming Xu, Yu Wang 等 | **arXiv:** [2311.01282](https://arxiv.org/abs/2311.01282) | **Affiliation:** Infinigence-AI, Tsinghua, SJTU

## 问题背景：Prefill vs Decode

与 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) 一致：

| 阶段 | 主算子形状 | 瓶颈 |
|------|------------|------|
| **Prefill** | 大 GEMM（M = seq×batch） | Compute |
| **Decode** | **GEMV / flat GEMM**（M = batch ≪ 64） | Memory BW + kernel 效率 |

Transformer 层 = 线性投影（①⑤⑥ GEMM）+ Attention（②③④ softmax）。[FlashAttention](/concepts/flashattention.md) → [FlashAttention-2](/concepts/flashattention-2.md) → [FlashAttention-3](/concepts/flashattention-3.md) / FlashDecoding 将 attention 分 tile 并行（online softmax，O(N) 内存）；FlashDecoding++ 针对 decode 中 **跨 tile 同步更新 partial softmax max** 占 Llama2-7B attention **~18.8%**（A100, input 1024）。

## 三大优化

### 1. Asynchronized softmax + unified max value

FlashDecoding 的 partial softmax 需式 (2) 跨 tile 同步 `m(x)` 并重标定先前 partial 结果。

**洞察：** softmax 分母分子可共用任意缩放因子 ϕ（不限于 max），只要 `e^{x_i - ϕ}` 不溢出/下溢。

```
softmax(x) = [e^{x_1-ϕ}, …, e^{x_d-ϕ}] / Σ e^{x_i-ϕ}   ∀ϕ ∈ R
```

- 对 Llama2 等模型，**>99.99%** 的 attention logits 落在窄区间 → 离线选统一 **ϕ**
- 各 partial tile **独立**累加分子 `Σ e^{x-ϕ}·v` 与分母，最后再归一化 — **无 tile 间同步**
- `x_i - ϕ` 越界 → 回退 FlashDecoding 同步 partial softmax（极少触发）
- OPT-6.7B logits 分布过宽，不适用此技巧

### 2. Flat GEMM：M pad 到 8 + double buffering

Decode 线性层 M 常为 1–8；cuBLAS/CUTLASS 将 M **pad 到 64** → **>50%** 无效计算。

| 改进 | 机制 |
|------|------|
| **M=8 tile** | 对齐现代 Tensor Core 最小 M |
| **BN 选择** | 小 N：parallelism-bound（~108 SM → BN 使 block 数 ~128–256）；大 N：memory-bound |
| **Double buffering** | shared memory 双缓冲重叠 load 与 GEMM |

### 3. Heuristic dataflow（Tensor Core vs CUDA Core）

同一 LLM 仅 **4 种 [N,K]**（K/Q/V proj、O proj、FFN1、FFN2）；M 由 batch 或 seq×batch 决定。

| 实现 | 适用 | 硬件 |
|------|------|------|
| **ImplA** FastGEMV | 小 M（GEMV） | **CUDA Core** |
| **ImplB** flat GEMM | 中 M | **Tensor Core** |
| **ImplC** CUTLASS | 大 M（prefill GEMM） | **Tensor Core** |

离线对每个 [N,K] profile 找拐点 **M1**（A↔B）、**M2**（B↔C），运行时查表。例：Llama2-7B decode batch=1 时 K/Q/V 用 FastGEMV，FFN1 在 M=8 时用 flat GEMM。

静态单一 dataflow 可导致 **50.25%** 性能损失（A100 上 Tensor Core GEMV 仅为 CUDA Core FastGEMV 的 82%，反之 batch=4 时 CUDA Core 仅为 Tensor Core 的 50%）。

## 评估摘要

**平台：** A100 / RTX 3090；MI210 / RX 7900 XTX  
**模型：** Llama2-7B/13B, OPT-6.7B, ChatGLM2-6B  
**对比：** HF, vLLM, DeepSpeed, TensorRT-LLM, OpenPPL, [FlashAttention-2](/concepts/flashattention-2.md)/FlashDecoding

| 指标 | 结果 |
|------|------|
| Decode vs HF（NVIDIA） | 最高 **4.86×** |
| Decode vs HF（AMD MI210） | 最高 **3.93×** |
| Decode vs FlashDecoding（A100 平均） | **1.37×** |
| Decode 平均 vs vLLM/DeepSpeed/TRT-LLM/OpenPPL/FlashDecoding | 1.24× / 1.44× / 1.13× / 1.24× / 1.21× |
| Prefill vs HF | 最高 **1.40×** |

Figure 1（batch=1, input 1K, Llama2-7B）：相对 HF 首 token / 每 token 延迟大幅缩短（A100 上 SOTA 对比含 TensorRT-LLM）。

## 在推理栈中的位置

```
Serving（vLLM paging / disagg） ── 调度与 KV 管理
         ↓
Kernel ── [FlashAttention](/concepts/flashattention.md) → [FlashAttention-2](/concepts/flashattention-2.md) → [FlashAttention-3](/concepts/flashattention-3.md)（prefill/训练；Hopper FP8）
       └─ [FlashDecoding++](/concepts/flashdecoding-plus-plus.md)（decode：async softmax + flat GEMM）
         ↓
Algorithm（DSpark speculative decode 等） ── 减少 decode 步数
```

- 与 [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) **正交**：FlashDecoding++ 降 **每步** latency；DSpark 降 **步数**
- 与 [Disaggregated Inference](/concepts/disaggregated-inference.md) / [Heterogeneous Inference](/concepts/heterogeneous-inference.md) 互补：后者分 hardware tier，前者优化单 GPU decode kernel
- [Reasoning Cliff](/concepts/reasoning-cliff.md) / [Inference Capacity Trap](/concepts/inference-capacity-trap.md) 的主战场在 decode — kernel 效率直接改善 TPOT

## 相关页面

- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode flat GEMM/GEMV 与 BW-bound
- [FlashAttention](/concepts/flashattention.md) — IO-aware 精确 attention 基线（NeurIPS 2022）
- [FlashAttention-2](/concepts/flashattention-2.md) — prefill/训练 IO-aware attention 第二代
- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper H100 异步 + FP8 第三代
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — decode 算法层加速
- [DRAM and Memory System](/concepts/dram-memory-system.md) — decode memory-bound 与 HBM 利用率
- [papers/flashdecoding-plus-plus-llm-gpu-inference.md](/papers/flashdecoding-plus-plus-llm-gpu-inference.md) — 论文摘要

# Citations

[1] [raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf](raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf) — Hong et al., arXiv:2311.01282 (2024)
