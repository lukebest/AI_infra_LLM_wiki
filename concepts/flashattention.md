---
type: Concept
title: FlashAttention
description: IO-aware 精确 attention：SRAM tiling + online softmax + 反向重算；O(N) 内存、HBM 访问 IO-optimal；GPT-2 attention 7.6×、训练最高 3×
tags:
- attention
- gpu
- llm
- training
- inference
- kernel
- prefill
- memory-hierarchy
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf
---

# FlashAttention

**FlashAttention**（Dao et al., NeurIPS 2022）提出 **IO-aware** 精确 self-attention：在 GPU **HBM ↔ SRAM** 层次上减少读写，通过 **tiling + online softmax + 反向重算** 避免物化 **N×N** attention 矩阵，实现 **O(N)** 额外内存与 **2–4×**（最高 **7.6×** kernel）wall-clock 加速，**无近似**。

**Authors:** Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré | **Venue:** NeurIPS 2022 | **arXiv:** [2205.14135](https://arxiv.org/abs/2205.14135) | **Code:** https://github.com/Dao-AILab/flash-attention

## 问题：FLOP ≠ 墙钟时间

近似 attention（sparse / low-rank）常降 FLOP 但**无墙钟收益**——Transformer 在 GPU 上多为 **memory-bound**（HBM ~1.5 TB/s vs SRAM ~19 TB/s on A100）。标准 attention 将 **S = QK^T**、**P = softmax(S)** 写入 HBM → **O(N²)** 内存与带宽。

```
标准:  HBM ←→ S(N×N) ←→ P(N×N) ←→ O
FA:    HBM ←→ Q,K,V blocks → SRAM 内 online softmax + PV → O
```

## 算法要点

### Online softmax（分 block 精确合并）

对 row block 维护 **m**（running max）与 **ℓ**（exp sum），跨 K/V column block  rescale 输出 O — 与全局 softmax **数学等价**（algebraic aggregation）。

### 反向：重算而非存储

不保存 S,P；仅存 **O** 与 **(m, ℓ)**，backward 在 SRAM 内从 Q,K,V block **重算** attention — FLOP 增加但 HBM 访问大减，**整体更快**。

### Kernel fusion

单 CUDA kernel 融合：QK^T → softmax（+ mask/dropout）→ PV，避免中间结果往返 HBM。

## IO 复杂度

| 实现 | HBM 访问 |
|------|----------|
| 标准 attention | **Θ(Nd + N²)** |
| FlashAttention | **Θ(N²d²M⁻¹)**（M = SRAM 容量） |

对典型 d、M，HBM 访问可达标准实现的 **~9×** 更少；并证明在 streaming 意义下 **IO-optimal**（无法对所有 M 渐近更优）。

## Block-Sparse FlashAttention

固定 block 稀疏 mask → 跳过零 block；IO 随稀疏度 s 线性下降。LRA 上 **2.8×** 于 dense FA，精度与标准 attention 相当。Path-256（seq **64K**）首次 > random（**63.1%**）。

## 实测摘要

| 场景 | 结果 |
|------|------|
| GPT-2 attention（seq 1K） | **7.6×** vs PyTorch |
| BERT-large 8×A100 | **15%** 快于 MLPerf 1.1 纪录 |
| GPT-2 small 训练 | **3.5×** vs HuggingFace |
| LRA | **2.4×**；精度持平 |
| GPT-2 context 4K | 比 Megatron 1K **快 30%** 且 ppl **−0.7** |
| Path-X（16K） | **61.4%**（首个 Transformer > chance） |
| 内存 vs seq length | **线性**至 64K |

## 谱系

| 版本 | 相对 FA | 主要增量 |
|------|---------|----------|
| **FlashAttention** (2022) | — | IO-aware tiling、online softmax、重算 |
| [FlashAttention-2](/concepts/flashattention-2.md) (2023) | ~**2×** | 减 non-matmul、seq 并行、warp split-Q |
| [FlashAttention-3](/concepts/flashattention-3.md) (2024) | **1.5–2×** vs FA2 | Hopper TMA/WGMMA 异步、GEMM-softmax 流水线、FP8 |
| FlashDecoding → [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) | decode | partial softmax 同步、flat GEMM |

[Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md)：FA 族主要优化 **prefill / 训练** 长序列 attention；decode 见 FlashDecoding 系列。

## 相关页面

- [FlashAttention-2](/concepts/flashattention-2.md) — 第二代并行与工作划分
- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper 第三代（async + FP8）
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — decode 侧延续
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — HBM/SRAM 层次类比
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 带宽 bound
- [papers/flashattention-io-aware-exact-attention.md](/papers/flashattention-io-aware-exact-attention.md) — 论文摘要

# Citations

[1] [raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf](raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf) — Dao et al., NeurIPS 2022
[2] [raw/papers/FlashAttention2_Faster_Attention_2023.pdf](raw/papers/FlashAttention2_Faster_Attention_2023.pdf) — FlashAttention-2
