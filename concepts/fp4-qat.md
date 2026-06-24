---
type: Concept
title: FP4 Quantization-Aware Training
description: FP4 量化感知训练，无损 FP4→FP8 反量化
tags:
- quantization
- training
- inference
timestamp: '2026-04-28T00:00:00Z'
created: 2026-04-28
sources:
- DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
---

# FP4 Quantization-Aware Training

DeepSeek-V4 在后训练阶段引入 FP4 (MXFP4) 量化感知训练，应用于两个组件。

## 应用范围

1. **MoE Expert Weights**（内存大户）
2. **CSA Indexer QK Path**（长上下文下 attention score 计算瓶颈）

额外：Index scores 从 FP32 → BF16（top-k selector 2× 加速，99.7% recall）

## 核心发现：FP4→FP8 无损反量化

**关键洞察**：FP4 (E2M1) 比 FP8 (E4M3) 少 2 个指数位，动态范围更小。但只要 FP4 子块（1×32 tiles）的 scale factor 在 FP8 量化块（128×128 tiles）内的最大/最小比不超过阈值，**FP4→FP8 反量化是数学无损的**。

实际验证：当前权重满足此条件。

## Pipeline

```
FP32 master weights → quantize to FP4 → dequantize to FP8 (lossless) → compute
                    ↑                                                        |
                    └────────── gradient (STE) ──────────────────────────────┘
```

- 前向：FP4 → FP8（无损），用 FP8 计算
- 反向：梯度直接传播回 FP32 master weights（等价于 STE）
- 推理/Rollout：直接用 FP4 权重（不需要模拟量化），减少内存加载

## 实际收益
- 减少 MoE expert 权重内存占用 ~50%（vs FP8）
- 加速长上下文 attention score 计算
- 现有 FP8 训练框架零修改即可复用

## Relations
- Used in: [Deepseek V4](#DeepSeek-V4), [Csa Hca](#CSA-HCA)

# Citations

[1] [DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf](DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf)
