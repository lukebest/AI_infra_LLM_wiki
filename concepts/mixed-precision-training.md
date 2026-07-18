---
type: Concept
title: Mixed Precision Training
description: FP16/BF16 混合精度训练经典配方 — FP32 master weights、loss scaling、FP32 accumulate；现代 LLM 训练默认基线
tags:
- training
- quantization
- llm
- optimization
- nvidia
- gpu
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
updated: 2026-07-17
sources:
- raw/papers/Mixed_Precision_Training_2018.pdf
---

# Mixed Precision Training

## 定义

**Mixed precision training**（Micikevicius et al., ICLR 2018）在几乎不损精度的前提下，用 **FP16（或后续 BF16）** 做前向/反向大部分计算与激活存储，用 **FP32** 保留关键累加与权重主副本，从而提升吞吐并降低显存。

## 经典三件套

1. **FP32 master weights**：优化器更新在 FP32 副本上进行，再 cast 到 FP16 参与下一 iter
2. **Loss scaling**：放大 loss 防止 FP16 梯度下溢；反传后再 unscale
3. **FP32 accumulate**：reduction（如归一化、Softmax、部分 GEMM accumulate）保留更高精度

## 与当代栈的关系

| 年代 | 实践 |
|------|------|
| 2018 论文 | FP16 + loss scaling |
| Ampere+ | **TF32** 默认 matmul；BF16 训练更稳（无需动态 loss scale） |
| LLM 时代 | ZeRO/FSDP + 混合精度；推理侧再接 [FlashAttention-3](/concepts/flashattention-3.md) FP8 等 |

混合精度是 **训练系统默认假设**；后续量化/稀疏（如 [DynaX](/papers/dynax-sparse-attention-acceleration.md)）是在此之上的进一步压缩。

## 相关页面

- [Mixed Precision Training (paper)](/papers/mixed-precision-training.md) — 论文摘要
- [FlashAttention-3](/concepts/flashattention-3.md) — 低精度 attention 推理/训练加速
- [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — 算子强度与精度选择
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — Tensor Core 承载混合精度

# Citations

[1] [raw/papers/Mixed_Precision_Training_2018.pdf](raw/papers/Mixed_Precision_Training_2018.pdf) — Micikevicius et al., ICLR 2018
