---
type: Summary
title: 'FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision'
description: Hopper H100：TMA/WGMMA producer-consumer、2-stage GEMM-softmax 流水线、FP8 block quant+incoherent processing；FP16 740 TFLOPs/s、相对 FA2 1.5–2×
tags:
- attention
- gpu
- llm
- hopper
- fp8
- kernel
- prefill
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf
---

# FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision

**Authors:** Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, Tri Dao (Colfax, Meta, NVIDIA, Georgia Tech, Princeton, Together AI) | **Venue:** arXiv:2407.08608, Jul 2024 | **PDF:** [raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf](raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf)

## 一句话总结

针对 H100 上 FlashAttention-2 仅 **~35%** 峰值利用率，FlashAttention-3 用 **warp-specialized TMA/WGMMA 异步**、**GEMM 与 softmax 2-stage 流水线**、**FP8 block 量化 + incoherent processing**，FP16 达 **740 TFLOPs/s（75%）**、相对 FA2 **1.5–2.0×**，FP8 近 **1.2 PFLOPs/s** 且比 per-tensor FP8 **2.6×** 更准。

## 核心贡献

1. **Producer–consumer asynchrony**：TMA 加载与 WGMMA 计算 warp 分工 + pingpong
2. **Overlapped GEMM–softmax**：打破 FA2 顺序依赖；ablation 570→661 TFLOPs/s
3. **FP8 path**：kernel 内 V transpose、layout permute、block quant + 正交 Hadamard 预处理
4. **H100 全面 benchmark**：中长 seq 可超 cuDNN；开源并入 Dao-AILab flash-attention

## 关键数字

| 指标 | 值 |
|------|-----|
| FA2 on H100 utilization | **~35%** |
| FA3 FP16 peak | **740 TFLOPs/s**（75%） |
| FA3 FP8 peak | **~1.2 PFLOPs/s** |
| vs FA2 FWD / BWD | **1.5–2.0×** / **1.5–1.75×** |
| FP8 vs per-tensor FP8 error | **2.6×** lower |
| Ablation (pipelining+async) | 570→**661** TFLOPs/s |

## 与 wiki 交叉引用

- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper 机制与谱系
- [FlashAttention-2](/concepts/flashattention-2.md) — 直接前代
- [FlashAttention](/concepts/flashattention.md) — IO-aware 起源
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — decode kernel 栈
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — prefill attention 优化

# Citations

[1] [raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf](raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf) — Shah et al. (2024)
