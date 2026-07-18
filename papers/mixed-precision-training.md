---
type: Summary
title: 'Mixed Precision Training'
description: Micikevicius et al. (ICLR 2018) — FP16 training with FP32 master weights, loss scaling, and FP32 accumulation; ~2× memory savings, no hyperparameter change
tags:
- training
- quantization
- gpu
- memory
- optimization
- model
- training-system
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Mixed_Precision_Training_2018.pdf
---

# Mixed Precision Training

**Authors:** Paulius Micikevicius, Sharan Narang, et al. | **Affiliations:** NVIDIA, Baidu Research | **PDF:** [raw/papers/Mixed_Precision_Training_2018.pdf](raw/papers/Mixed_Precision_Training_2018.pdf)

## 一句话总结

ICLR 2018 经典：**FP16** 存权重/激活/梯度，**FP32 master weights + loss scaling + FP32 accumulate** 三件套，在不改超参前提下匹配 FP32 精度，训练内存约 **减半**、GPU 算力 **2–8×**。

## 核心贡献

1. **FP32 master copy of weights**：optimizer 在 FP32 累加更新，再 round 到 FP16 做 fwd/bwd
2. **Loss scaling**：把小梯度 exponent 抬入 FP16 可表示区间，防 underflow 变零
3. **FP16×FP16→FP32 accumulate**：乘积累加后存 FP16，保数值精度
4. **无精度损失验证**：>100M 参数 CNN/RNN/LM/MT/检测/语音等大规模任务
5. **工业基线**：现代 GPU BF16/FP8 训练栈的理论与实践前身

## 关键数字

| 设置 | 结果 |
|------|------|
| Training memory | **~50%** of FP32 (activations in FP16) |
| GPU FP16 vs FP32 math | **2×–8×** throughput |
| FP16-only weight updates (speech) | **80%** relative accuracy loss |
| Grad exponents < 2⁻²⁴ | **~5%** of values |
| Loss scale example (Multibox SSD) | **×8** to match FP32 |

## 与 wiki 交叉引用

- [Mixed Precision Training](/concepts/mixed-precision-training.md) — 概念页（三件套与当代栈）
- [FlashAttention-3](/concepts/flashattention-3.md) — 低精度 attention/inference 演进
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — 精度与算子强度对 memory/compute bound 的影响
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 训练/推理精度栈与硬件映射
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — 推理侧量化与训练精度基线
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 模型 footprint 与 serving capacity

# Citations

[1] [raw/papers/Mixed_Precision_Training_2018.pdf](raw/papers/Mixed_Precision_Training_2018.pdf) — Micikevicius et al. (ICLR 2018)
[2] [raw/papers/mixed-precision-training.md](raw/papers/mixed-precision-training.md) — 结构化摘录
