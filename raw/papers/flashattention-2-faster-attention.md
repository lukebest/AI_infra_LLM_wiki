---
source_url: https://arxiv.org/abs/2307.08691
ingested: 2026-06-24
sha256: 4aa8935dfacaf6ae8c68f772ca92f730154a0dd0e1bceeb59c7bc56c512d5868
---

# FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning (2023)

**Author:** Tri Dao — Princeton / Stanford

**Venue:** arXiv:2307.08691, Jul 2023 | **Code:** https://github.com/Dao-AILab/flash-attention

## Problem

FlashAttention [5]: IO-aware exact attention via tiling + online softmax → 2-4× vs baseline, O(N) memory. But only **25-40%** of A100 peak TFLOPs/s (vs GEMM 80-90%) due to suboptimal thread block / warp work partitioning.

## Three improvements

### 3.1 Algorithm tweaks (reduce non-matmul FLOPs)

- A100: matmul 312 TFLOPs/s vs non-matmul FP32 **19.5 TFLOPs/s** → 1 non-matmul FLOP ≈ **16×** matmul cost
- Forward: maintain **unscaled** Õ; scale once at end by diag(ℓ)^−1
- Backward: store **logsumexp L = m + log(ℓ)** only (not separate m and ℓ)

### 3.2 Parallelism

- FA1: parallelize batch × heads only (1 block per head)
- FA2: also parallelize **sequence length** (outer loop over row blocks) — long seq / small batch → better SM occupancy
- Backward: 1 block per **column** block; atomic add for dQ
- Loop order swap + seq parallel first in Triton (Phil Tillet)

### 3.3 Warp work partitioning

- FA1 **split-K**: K/V split across warps, Q shared → inter-warp shared mem reduce
- FA2: **split Q** across warps, K/V shared → no inter-warp comm on forward
- Block sizes tuned {64,128}×{64,128} per head dim d

## Causal mask

- Skip blocks where all col > row (~half blocks) → **1.7-1.8×** vs unmasked compute
- Only 1 block per row needs explicit causal mask (square blocks)

## MQA / GQA

Implicit head indexing; backward sum dK/dV across duplicated KV heads.

## Results (A100 80GB)

| vs | Speedup |
|----|---------|
| FlashAttention | **1.7-3.0×** (bench); ~**2×** typical |
| FlashAttention Triton | 1.3-2.5× |
| PyTorch standard attention | **3-10×** |
| Peak forward throughput | **230 TFLOPs/s** (**73%** of theoretical) |
| End-to-end GPT 1.3B/2.7B train | **1.3×** vs FA1, **2.8×** vs no FA |
| Training throughput | **225 TFLOPs/s** (**72% MFU**) |

## Stack position

- **Prefill / training**: FlashAttention-2 (this paper)
- **Decode attention**: FlashDecoding → FlashDecoding++ (partial softmax sync, flat GEMM)

Exact attention, no approximation. Memory O(N) extra beyond Q,K,V,O.
