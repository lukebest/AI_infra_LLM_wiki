---
type: Summary
title: 'FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness'
description: IO-aware tiling + online softmax + 反向重算；O(N) 内存、IO-optimal HBM 访问；GPT-2 attention 7.6×、BERT 15% 快于 MLPerf 纪录、Path-X 16K 61.4%
tags:
- attention
- gpu
- llm
- training
- kernel
- prefill
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf
---

# FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

**Authors:** Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré (Stanford / SUNY Buffalo) | **Venue:** NeurIPS 2022 | **arXiv:** [2205.14135](https://doi.org/10.48550/arXiv.2205.14135) | **PDF:** [raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf](raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf)

## 一句话总结

将 attention 算法设计为 **IO-aware**：在 SRAM 内对 Q/K/V **分块**、用 **online softmax** 精确合并、**反向重算** S/P 以避免 O(N²) HBM 读写——**精确无近似**、额外内存 **O(N)**，GPT-2 attention **7.6×** 加速，并首次让 Transformer 在 Path-X（16K）与 Path-256（64K block-sparse）上超过随机基线。

## 核心贡献

1. **IO-aware 精确 attention**：tiling + kernel fusion，HBM 访问 **Θ(N²d²M⁻¹)** vs 标准 **Θ(Nd+N²)**
2. **Online softmax + 反向重算**：存 (m,ℓ) 与 O，backward 在片上重算 — 少 HBM 访问胜过额外 FLOP
3. **IO 下界**：证明 exact attention 无法渐近优于该 HBM 访问阶
4. **Block-sparse FlashAttention**：稀疏 block 跳过，2–4× 于 dense FA
5. **长上下文能力**：4K GPT-2 训练、ppl 提升、Path-X/Path-256 突破

## 关键数字

| 指标 | 值 |
|------|-----|
| vs PyTorch attention (GPT-2) | **7.6×** |
| BERT-large vs MLPerf 1.1 | **15%** faster |
| GPT-2 small training vs HF | **3.5×** |
| LRA speedup | **2.4×** |
| Path-X (16K) accuracy | **61.4%** |
| 额外内存 | **O(N)** |
| HBM access reduction | up to **9×** |

## 与 wiki 交叉引用

- [FlashAttention](/concepts/flashattention.md) — 机制与 IO 分析
- [FlashAttention-2](/concepts/flashattention-2.md) — 第二代 ~2× 加速
- [FlashAttention-3](/concepts/flashattention-3.md) — Hopper 第三代（async + FP8）
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — decode 侧 kernel 栈
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — prefill attention 主战场
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 存储层次

# Citations

[1] [raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf](raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf) — Dao et al. (2022)
