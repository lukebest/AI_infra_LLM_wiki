---
type: Concept
title: FlashAttention-2
description: IO-aware 精确 attention 第二代：减 non-matmul FLOP、序列维并行、warp 级 split-Q；相对 FlashAttention ~2×，A100 最高 73% 峰值 TFLOPs/s、训练 225 TFLOPs/s
tags:
- inference
- training
- llm
- gpu
- attention
- kernel
- prefill
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashAttention2_Faster_Attention_2023.pdf
---

# FlashAttention-2

**FlashAttention-2**（Tri Dao, arXiv 2023）在 [FlashAttention](/concepts/flashattention.md) 的 **IO-aware tiling + online softmax** 基础上，通过更好的 **GPU 并行划分与工作分配**，将 attention 吞吐从 A100 峰值利用率的 **25–40%** 提升到 **50–73%**，接近 GEMM 效率；**精确无近似**，额外内存 **O(N)**（非 O(N²)）。

**Author:** Tri Dao (Princeton / Stanford) | **arXiv:** [2307.08691](https://arxiv.org/abs/2307.08691) | **Code:** https://github.com/Dao-AILab/flash-attention

## 背景：标准 Attention 的 IO 瓶颈

```
S = QK^T  →  P = softmax(S)  →  O = PV
```

标准实现将 **S, P ∈ R^{N×N}** 物化到 HBM → **O(N²)** 内存 + 带宽 bound。FlashAttention 分 block 在 SRAM 内 online softmax，不重写中间矩阵。

| 版本 | 相对 baseline | A100 峰值利用率 | 主场景 |
|------|---------------|-------------------|--------|
| [FlashAttention](/concepts/flashattention.md) | 2–4× vs 标准 | ~30–50% FWD | 训练 + prefill |
| **FlashAttention-2** | ~**2×** vs FA1 | **73%** FWD (A100) | 训练 + prefill |
| [FlashAttention-3](/concepts/flashattention-3.md) | **1.5–2×** vs FA2 | **75%** FWD (H100 FP16) | Hopper prefill/训练 + FP8 |
| FlashDecoding / ++ | decode 优化 | — | [Decode](/concepts/prefill-decode-divergence.md) |

## 三大改进

### 1. 减少 non-matmul FLOP

Tensor Core matmul 吞吐远高于 exp/max 等标量 op（A100 上约 **16×** 差距）。

| 改动 | 效果 |
|------|------|
| 维护 **未缩放 Õ**，循环结束再 `diag(ℓ)^{-1}` | 少一次 block 间 rescale |
| 反向只存 **logsumexp L = m + log(ℓ)** | 少存 m 与 ℓ |

### 2. 序列长度维并行

FA1 仅 **batch × heads** 并行（每 head 一个 thread block）→ 长序列 + 小 batch 时 SM 空闲。

FA2 **额外沿 seq 维**划分 row/column block：
- **Forward**：每 block 负责 attention 矩阵一行块（embarrassingly parallel）
- **Backward**：每 block 负责一列块；**dQ** 用 atomic add 汇总

长上下文（32k–100k）训练/prefill 的关键优化。

### 3. Warp 级 split-Q（非 split-K）

```
FA1:  K/V 切分到 warps，Q 共享 → warp 间 shared memory 归约
FA2:  Q 切分到 warps，K/V 共享 → forward 无 warp 间通信
```

减少 shared memory 读写，是 ~2× 的重要来源之一。

## Online Softmax 与 Causal Mask

分 tile 计算局部 max/sum，跨 tile rescale 得精确 global softmax（见 Algorithm 1）。

**Causal（自回归）**：
- 列索引全大于行索引的 block **直接跳过**（约一半）→ **1.7–1.8×**
- 每行仅 **1 个 block** 需显式 mask

## MQA / GQA

Multi-query / grouped-query：多 Q head 共享 KV → 反向对 **dK/dV** 跨 head 求和。

## 实测（A100 80GB）

| 指标 | 值 |
|------|-----|
| vs FlashAttention | **~2×**（1.7–3.0× bench） |
| vs PyTorch attention | **3–10×** |
| Attention 峰值 | **230 TFLOPs/s**（73% theoretical） |
| GPT 1.3B/2.7B 端到端训练 | **1.3×** vs FA1；**225 TFLOPs/s**（72% MFU） |
| 内存 | O(N) 额外（存 L），无 N×N 物化 |

## 在 LLM 栈中的位置

```
Prefill / 训练          Decode
FlashAttention-2   →   FlashDecoding → FlashDecoding++
     ↑                        ↑
  长 seq GEMM-like          KV cache 增长；partial softmax 同步
  [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md)
```

- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) 的 baseline 含 **FlashAttention2**；其在 decode 上进一步做 **异步 unified-max softmax**（~19% attention 开销）与 flat GEMM
- 与 [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) 正交：FA-2 优化 attention kernel；DSpark 减 decode 步数

## 相关页面

- [FlashAttention](/concepts/flashattention.md) — IO-aware tiling 与 online softmax 基线
- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper 异步 + FP8 第三代
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — prefill compute-bound，FA-2 主战场
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — decode 侧 attention/GEMM 延续优化
- [DRAM and Memory System](/concepts/dram-memory-system.md) — HBM vs SRAM 带宽层次
- [papers/flashattention-2-faster-attention.md](/papers/flashattention-2-faster-attention.md) — 论文摘要

# Citations

[1] [raw/papers/FlashAttention2_Faster_Attention_2023.pdf](raw/papers/FlashAttention2_Faster_Attention_2023.pdf) — Dao, arXiv:2307.08691 (2023)
[2] [raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf](raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf) — FlashAttention (NeurIPS 2022)
[3] [raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf](raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf) — FlashDecoding++ decode 延续
