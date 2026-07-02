---
source_url: https://arxiv.org/abs/2205.14135
ingested: 2026-06-24
sha256: ca7f9fda10b90fc05dd291a3accc85e9c1a4a860b99b31928dab03ed3fcb14e4
---

# FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (2022)

**Authors:** Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré — Stanford / SUNY Buffalo

**Venue:** NeurIPS 2022 | **arXiv:** 2205.14135

## Core idea

**IO-aware** exact attention: account for HBM ↔ SRAM traffic, not just FLOPs. Standard attention materializes S,P ∈ R^{N×N} to HBM → O(N²) memory + bandwidth bound.

## Algorithm (Algorithm 1)

1. **Tiling**: split Q,K,V into blocks; load to SRAM
2. **Online softmax**: track row-wise (m, ℓ) statistics; rescale across K/V blocks — exact, no approximation
3. **Recomputation**: backward recompute S,P from blocks in SRAM; store only O and (m,ℓ) — selective gradient checkpointing that **speeds up** backward via fewer HBM reads
4. **Kernel fusion**: single CUDA kernel — matmul, softmax, mask/dropout, matmul without round-trips to HBM

Block sizes: B_c = ⌈M/(4d)⌉, B_r = min(⌈M/(4d)⌉, d) for SRAM size M.

## IO complexity (Theorem 2)

| | HBM accesses |
|--|--------------|
| Standard | Θ(Nd + N²) |
| FlashAttention | Θ(N²d²M⁻¹) |

Proposition 3: no exact attention can do o(N²d²M⁻¹) for all SRAM sizes M ∈ [d, Nd] — **IO-optimal** in streaming sense.

Typical d=64–128, M~100KB → up to **9×** fewer HBM accesses.

## Block-sparse extension

Block-sparse mask → skip zero blocks; IO ∝ sparsity s. 2–4× faster than dense FA; LRA 2.8×. Butterfly sparsity pattern.

## Results

| Benchmark | Result |
|-----------|--------|
| GPT-2 attention kernel | **7.6×** vs PyTorch |
| BERT-large (8×A100) | **15%** faster than MLPerf 1.1 record (17.4 vs 20.0 min) |
| GPT-2 small training | **3.5×** vs HuggingFace; **2.0×** vs Megatron |
| GPT-2 medium training | **3.0×** vs HuggingFace |
| LRA | **2.4×** speedup; accuracy on par |
| GPT-2 4K context | 30% faster than Megatron 1K + **0.7** better ppl |
| Path-X (16K) | **61.4%** — first Transformer > random |
| Path-256 (64K, block-sparse) | **63.1%** |
| Attention runtime (128–2K) | up to **3×**; memory linear to **64K** |

## Lineage

→ [FlashAttention-2](/concepts/flashattention-2.md) (2023): parallelism + warp partitioning
→ FlashDecoding → [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) (decode)

Code: Dao-AILab flash-attention (open source)
