---
type: Summary
title: 'DynaX: Dynamic X:M Sparse Attention Acceleration'
description: ASPLOS '25 DynaX — dynamic X:M structured attention pruning + block scheduling; 89–92% sparsity at <1% accuracy loss; 1.99× speedup vs Sanger on BERT
tags:
- attention
- sparse
- accelerator
- optimization
- transformer
- llm
- kernel
- hardware
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/DynaX_Sparse_Attention_Dynamic_XM_Pruning_2025.pdf
---

# DynaX: Dynamic X:M Sparse Attention Acceleration

**Authors:** Xiao Xiong, Zhaorui Chen, et al. | **Affiliation:** Chongqing University | **PDF:** [raw/papers/DynaX_Sparse_Attention_Dynamic_XM_Pruning_2025.pdf](raw/papers/DynaX_Sparse_Attention_Dynamic_XM_Pruning_2025.pdf)

## 一句话总结

DynaX 用 **dynamic X:M** 两步结构化剪枝 + block scheduling 匹配 PEA，在长序列 attention 上达 **89–92%** 稀疏度且精度损失 **<1%**，BERT-base 相对 Sanger **1.99×** 加速、**5.16×** 能效。

## 核心贡献

1. **Dynamic X:M pruning**：每组动态选 X 个重要 score（非固定 N:M），降低 prediction 内存开销
2. **2-step 剪枝流程**：低比特 Q/K 预计算 → N:M → X:N，兼顾稀疏度与规则性
3. **Block scheduling**：score block 重组对齐 SDDMM/SpMM 的 PEA 粒度
4. **Algorithm-hardware co-design**：专用模块流水线实现各优化步骤
5. **长序列瓶颈定位**：attention 占 BERT/ViT 总算力 **47–93%**

## 关键数字

| 设置 | 结果 |
|------|------|
| Sparsity (short / long seq) | **89.54%** / **91.77%** |
| Accuracy loss | **<1%** |
| Speedup vs Sanger / SALO2 (BERT) | **1.99×** / **1.50×** |
| Energy vs Sanger / SALO2 | **5.16×** / **4.20×** |
| vs GPU (accelerator) | **35.14×** speedup; **299.23×** energy efficiency |
| Accelerator efficiency | **25.55 TOPS/W** avg |

## 与 wiki 交叉引用

- [FlashAttention](/concepts/flashattention.md) — IO-aware dense attention 基线
- [FlashAttention-2](/concepts/flashattention-2.md) — 长序列 attention kernel 优化
- [FlashAttention-3](/concepts/flashattention-3.md) — 低精度/async attention 演进
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — 长上下文 prefill attention 成本
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — attention SDDMM/SpMM 算子强度

# Citations

[1] [raw/papers/DynaX_Sparse_Attention_Dynamic_XM_Pruning_2025.pdf](raw/papers/DynaX_Sparse_Attention_Dynamic_XM_Pruning_2025.pdf) — Xiong et al. (ASPLOS '25)
[2] [raw/papers/dynax-sparse-attention-acceleration.md](raw/papers/dynax-sparse-attention-acceleration.md) — 结构化摘录
