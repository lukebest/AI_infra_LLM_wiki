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
timestamp: '2026-10-19T00:00:00Z'
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

## 2026-10-19 补充：低比特让激活成为瓶颈

[Multi-Threshold 非单调激活](/papers/multi-threshold-non-monotonic-activations-finn.md)：权重/MAC 压到极低比特后，激活与浮点 scale 可精确折叠为阈值比较，SiLU 等非单调函数也可表示；LeNet 上可降到 4 级（约 2.32 bit）。总览见 [核内非线性运算加速](/concepts/in-core-nonlinear-operator-acceleration.md)。

## 2026-10-21 补充：MX/NVFP4 缩放格式的硅代价
[MX-like Tensor Core](/papers/mx-like-tensor-core-npu-codesign.md)：6 bit 以上 UE8M0 缩放即 Pareto 最优；FP4 下缩放格式决定精度，UE5M3 比 NVFP4-like 的 UE4M3 少 **25.3%** 困惑度劣化，面积 +0.06%、功耗 +0.49%。累加器占 MAC 面积 39–66%。

## 2026-10-26 补充：整数权重比特数怎么换成算力
[FIGFLEX](/papers/figflex-mixed-precision-fp-int-gemm.md)：FP16 激活 × 低比特整数权重，radix-4 移位加让部分积约减半，PE 吞吐随 INT4→INT1 上升；INT3 配对融合高位回收半车道。3-bit 混合精度下单位面积吞吐比 AxCore **1.56×**、比 FIGLUT **1.42×**，LLaMA-2-7B PPL **5.85**。

# Citations

[1] [raw/articles/arch-study-30d-day-05.md](raw/articles/arch-study-30d-day-05.md) — H&P Appendix J + AI 格式（Day 5）
[2] [arXiv:2610.21825](https://arxiv.org/abs/2610.21825) — Multi-threshold activations
- [arXiv:2610.26083](https://arxiv.org/abs/2610.26083) — MX-like Tensor Core
- [arXiv:2610.30480](https://arxiv.org/abs/2610.30480) — FIGFLEX
