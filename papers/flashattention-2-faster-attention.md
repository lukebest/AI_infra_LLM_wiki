---
type: Summary
title: 'FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning'
description: IO-aware 精确 attention 第二代：减 non-matmul、seq 维并行、warp split-Q；相对 FlashAttention ~2×，A100 73% 峰值 TFLOPs/s、GPT 训练 225 TFLOPs/s
tags:
- attention
- gpu
- llm
- training
- inference
- kernel
- prefill
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashAttention2_Faster_Attention_2023.pdf
---

# FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning

**Author:** Tri Dao (Princeton / Stanford) | **Venue:** arXiv:2307.08691, Jul 2023 | **PDF:** [raw/papers/FlashAttention2_Faster_Attention_2023.pdf](raw/papers/FlashAttention2_Faster_Attention_2023.pdf)

## 一句话总结

FlashAttention-2 在 IO-aware tiling + online softmax 之上，通过 **减少 non-matmul FLOP**、**沿序列长度并行 thread block**、**warp 级 split-Q（替代 split-K）** 三项工作划分优化，相对 FlashAttention 约 **2×** 加速，A100 上 attention 达 **230 TFLOPs/s（73% 峰值）**，GPT 训练 **225 TFLOPs/s（72% MFU）**——精确 attention、O(N) 内存。

## 核心贡献

1. **算法微调**：未缩放 Õ + 末次 rescale；反向仅存 logsumexp **L** — 降低 16× 贵的 non-matmul 占比
2. **序列维并行**：长 seq / 小 batch 时沿 row/column block 调度，提高 SM occupancy
3. **Warp 划分**：Q 分 warp、K/V 共享 — 消除 forward 的 inter-warp shared memory 归约
4. **Causal 优化**：跳过无效 block + 每行单 block mask → **1.7–1.8×**
5. **MQA/GQA** 与 Triton 实现生态（Dao-AILab flash-attention）

## 关键数字

| 指标 | 值 |
|------|-----|
| vs FlashAttention | **~2×**（bench 1.7–3.0×） |
| vs PyTorch attention | **3–10×** |
| FA1 → FA2 峰值利用率 | 25–40% → **50–73%** FWD |
| Attention 峰值（A100） | **230 TFLOPs/s** |
| 端到端 GPT 训练 | **225 TFLOPs/s**，**72% MFU** |
| 额外内存 | **O(N)**（非 O(N²)） |

## 与 wiki 交叉引用

- [FlashAttention-2](/concepts/flashattention-2.md) — 机制与 LLM 栈位置
- [FlashAttention](/concepts/flashattention.md) — IO-aware 基线（NeurIPS 2022）
- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper 后继（async + FP8）
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — prefill attention 主优化目标
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — decode 侧 FA/FlashDecoding 延续（partial softmax 同步等）
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 算法层 decode 加速（正交）

# Citations

[1] [raw/papers/FlashAttention2_Faster_Attention_2023.pdf](raw/papers/FlashAttention2_Faster_Attention_2023.pdf) — Dao (2023)
