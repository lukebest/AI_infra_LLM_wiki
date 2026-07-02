---
source_url: https://arxiv.org/abs/2407.08608
ingested: 2026-06-24
sha256: 3d05ca102802e6b8ebbae5181efe777b7d258cd75e2fe9cca209efd2f5e6c6cb
---

# FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision (2024)

**Authors:** Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, Tri Dao — Colfax, Meta, NVIDIA, Georgia Tech, Princeton, Together AI

**Venue:** arXiv:2407.08608, Jul 2024 | **Code:** https://github.com/Dao-AILab/flash-attention

## Motivation

FlashAttention-2 on H100: only **~35%** peak utilization vs GEMM **80–90%** — synchronous model, no Hopper async/FP8.

## Hopper hardware (H100)

- **TMA** (Tensor Memory Accelerator): async GMEM↔SMEM
- **WGMMA**: warpgroup matrix multiply on Tensor Cores; FP8 **2×** throughput vs FP16
- Warp-specialization + dynamic register limits (`setmaxnreg`)

## Three techniques

### 1. Producer-consumer asynchrony

Warp-specialized pipelining: producer warps issue **TMA** loads; consumer warpgroups run **WGMMA**. Pingpong scheduling hides latency.

### 2. GEMM–softmax pipelining (2-stage / 3-stage)

Overlap low-throughput softmax (exp, FMA) with async WGMMA:
- While softmax on block j of S, WGMMA computes next QK block
- Rework FA2 to break sequential deps between softmax and GEMMs
- Ablation: **570 → 661 TFLOPs/s** (FP16, hdim 128, batch 4, seqlen 8448)

### 3. FP8 + accuracy

- **Block quantization**: per tile (B_r×d / B_c×d) scale — fuse with rotary embedding
- **Incoherent processing**: Q,K × random orthogonal M (Hadamard × ±1 diagonal) before quantize; MM^T=I preserves QK^T
- In-kernel V transpose via LDSM/STSM for FP8 k-major WGMMA layout
- FP8 error **2.6×** lower than per-tensor FP8 attention

## Results (H100 80GB SXM5)

| vs | Speedup / peak |
|----|----------------|
| FlashAttention-2 FWD | **1.5–2.0×** |
| FlashAttention-2 BWD | **1.5–1.75×** |
| FA2 Triton (H100) | **1.5×** |
| PyTorch standard | **3–16×** |
| FP16 peak | **740 TFLOPs/s** (**75%** util) |
| FP8 peak | **~1.2 PFLOPs/s** |
| vs cuDNN (seq ≥1K) | FA3 FP16 **surpasses**; FP8 competitive |

Head dim 256 FWD peak ~**756 TFLOPs/s** (figures in paper).

## Lineage

[FlashAttention](/concepts/flashattention.md) → [FlashAttention-2](/concepts/flashattention-2.md) → **FA3** (Hopper async + FP8)

Decode: FlashDecoding → [FlashDecoding++](/concepts/flashdecoding-plus-plus.md)
