---
type: Concept
title: FlashAttention-3
description: Hopper H100 IO-aware attention 第三代：TMA/WGMMA 异步 producer-consumer、GEMM-softmax 流水线、FP8 block quant+incoherent processing；FP16 740 TFLOPs/s、相对 FA2 1.5–2×
tags:
- attention
- gpu
- llm
- training
- inference
- kernel
- prefill
- hopper
- fp8
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf
---

# FlashAttention-3

**FlashAttention-3**（Shah et al. / Tri Dao, arXiv 2024）将 [FlashAttention-2](/concepts/flashattention-2.md) 扩展到 **NVIDIA Hopper（H100）**：利用 **TMA + WGMMA 异步**、**GEMM 与 softmax 流水线重叠**、**FP8 Tensor Core**，在保持 **精确 attention**（FP16 与 FA2 同误差）的同时，FP16 达 **740 TFLOPs/s（75% H100 峰值）**，相对 FA2 **1.5–2.0×**。

**Authors:** Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, Tri Dao | **arXiv:** [2407.08608](https://arxiv.org/abs/2407.08608) | **Code:** https://github.com/Dao-AILab/flash-attention

## 为何需要 FA3

| 版本 | H100 利用率 | 局限 |
|------|-------------|------|
| [FlashAttention-2](/concepts/flashattention-2.md) | **~35%** | 同步模型；Ampere 指令；未用 TMA/FP8 |
| 优化 GEMM | **80–90%** | — |
| **FlashAttention-3** | **75%** (FP16) | Hopper 原生 async + FP8 |

FA2 算法正确但 **未显式利用 Hopper 异步与低精度**——专用单元（Tensor Core matmul vs TMA 搬运）可并行，FP8 同功耗下约 **2×** 吞吐。

## 三大技术

### 1. Producer–Consumer 异步（warp-specialization）

```
Producer warps: TMA 异步加载 Q, K, V tiles → SMEM
Consumer warpgroups: WGMMA 执行 QK^T、PV
Pingpong scheduling + setmaxnreg 动态寄存器分配
```

隐藏 memory 与 instruction issue 延迟；CUTLASS WGMMA/TMA 抽象。

### 2. GEMM–softmax 流水线（2-stage / 3-stage）

FA2 中 softmax 与 WGMMA **顺序依赖** → Tensor Core 空泡。

**2-stage**：对 scores 矩阵一块做 softmax 时，WGMMA 在 async proxy 中计算 **下一块 QK^T**。

| 配置 | TFLOPs/s（ablation, hdim 128） |
|------|-------------------------------|
| 基线 | **570** |
| +pipelining + warp-spec | **661** |

3-stage 进一步重叠第二段 WGMMA 与 softmax，寄存器压力更大（Appendix B.3）。

### 3. FP8：吞吐与精度

**吞吐**
- FP8 WGMMA → 峰值约 **1.2 PFLOPs/s**
- V 需 **k-major**：kernel 内 LDSM/STSM transpose；accumulator→operand layout 用 byte permute

**精度**
- **Block quantization**：每 tile 独立 scale（与 FA3 分块天然对齐）
- **Incoherent processing**：量化前 `Q' = QM`, `K' = KM`（M 正交 Hadamard×±1）；`(QM)(KM)^T = QK^T`
- vs per-tensor FP8：**2.6×** 更低数值误差（outlier feature 场景）

## 实测（H100 80GB SXM5）

| 指标 | 值 |
|------|-----|
| vs FA2 forward | **1.5–2.0×** |
| vs FA2 backward | **1.5–1.75×** |
| vs FA2 Triton | **~1.5×** |
| vs PyTorch | **3–16×** |
| FP16 peak | **740 TFLOPs/s**（75%）；hdim 256 图最高 **~756** |
| FP8 peak | **~1.2 PFLOPs/s** |
| vs cuDNN 9（seq ≥1K） | FP16 **更快**；FP8 相当（causal+大 head dim 略逊） |

## Attention 谱系（wiki）

```
FlashAttention (2022, IO tiling)
    → FlashAttention-2 (2023, 并行/warp split-Q)
        → FlashAttention-3 (2024, Hopper async + FP8)
            → FlashDecoding / FlashDecoding++ (decode 特化)
```

- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — FA 族主服务 **prefill/训练** 长序列
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — decode partial softmax 同步、flat GEMM（与 FA3 正交阶段）

## 相关页面

- [FlashAttention](/concepts/flashattention.md) — IO-aware tiling 起源
- [FlashAttention-2](/concepts/flashattention-2.md) — 直接前代
- [FP4 Quantization-Aware Training](/concepts/fp4-qat.md) — 更低精度训练（不同栈层）
- [papers/flashattention-3-asynchrony-low-precision.md](/papers/flashattention-3-asynchrony-low-precision.md) — 论文摘要

# Citations

[1] [raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf](raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf) — Shah et al., arXiv:2407.08608 (2024)
[2] [raw/papers/FlashAttention2_Faster_Attention_2023.pdf](raw/papers/FlashAttention2_Faster_Attention_2023.pdf) — FlashAttention-2
[3] [raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf](raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf) — FlashAttention
