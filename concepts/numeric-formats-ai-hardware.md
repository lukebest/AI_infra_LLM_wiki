---
type: Concept
title: Numeric Formats for AI Hardware
description: IEEE 754 浮点与 AI 数据格式（FP32/FP16/BF16/FP8/INT8）的精度、动态范围与硬件面积权衡
tags:
- architecture
- quantization
- gpu
- accelerator
- training
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-05.md
---

# Numeric Formats for AI Hardware（AI 硬件数值格式）

加速器性能/精度/能效取决于**用什么格式表示数字**。格式选择是精度、动态范围、硬件面积之间的量化权衡。

## IEEE 754 通用形式

```
Value = (-1)^sign × 1.mantissa × 2^(exponent - bias)
```

| 格式 | 指数 | 尾数 | 特点 |
|------|------|------|------|
| FP64 | 11 | 52 | 双精度训练/科学计算 |
| FP32 | 8 | 23 | 通用 GPU 基准 |
| FP16 | 5 | 10 | 高精度低范围；最大精确整数 **2048** |
| **BF16** | 8 | 7 | FP32 截断尾数；**与 FP32 同动态范围** |
| FP8 E4M3 / E5M2 | 4/5 | 3/2 | H100/Blackwell Tensor Core |

- **尾数位** → 精度（有效数字）
- **指数位** → 动态范围

## AI 训练为何偏好 BF16

训练需要 **FP32 级动态范围**（梯度量级变化大），但不需要 FP32 精度 → BF16 是甜点。推理可进一步降至 FP8/INT8/INT4（见 [FP4 Quantization-Aware Training](/concepts/fp4-qat.md)）。

## 量化基础

对称量化：`x_quant = round(x / scale)`，`x ≈ x_quant × scale`

- INT8/INT4 减存储与带宽，引入量化误差
- **Stochastic rounding** 等新兴方向降低训练 bias

## 与 AI 基础设施的关联

| 系统 | 格式策略 |
|------|----------|
| NVIDIA Tensor Core | FP8/FP16/BF16 混合 |
| TPU | 历史上 INT8 为主 |
| WSE | 多精度灵活，编译器/数据流选择 |
| Groq LP35 | NVFP4 引入（GTC 2026 路线） |

## 相关页面

- [FP4 Quantization-Aware Training](/concepts/fp4-qat.md) — FP4 QAT 与 NVFP4
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 精度与带宽协同
- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — 面积/功耗量化思维

# Citations

[1] [raw/articles/arch-study-30d-day-05.md](raw/articles/arch-study-30d-day-05.md) — H&P Appendix J + AI 格式（Day 5）
