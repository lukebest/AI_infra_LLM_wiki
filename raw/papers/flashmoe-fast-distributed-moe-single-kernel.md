---
source_url: https://arxiv.org/abs/2506.04667
ingested: 2026-06-24
sha256: 5936a399197ff141bcb5c428e04d8a8032125c6e438247a1d0e4094cbb9b7bfc
---

# FlashMoE: Fast Distributed MoE in a Single Kernel (2025)

**Authors:** Osayamen Jonathan Aimuyo, Byungsoo Oh, Rachee Singh — Cornell University

**Venue:** NeurIPS 2025 | **arXiv:** 2506.04667v3 (Nov 2025) | **Code:** https://github.com/osayamenja/FlashMoE

## Motivation

Distributed MoE (expert parallelism) suffers from:
- **AlltoAll collectives** on critical path — up to **68%** runtime; straggler-sensitive
- **CPU-managed scheduling** + **hundreds of kernel launches** per layer (DeepSpeedMoE **550**, Megatron-TE **261**, Megatron+DeepEP **432** vs FlashMoE **1**)
- **Zero-padded token payloads** in symmetric collective APIs → wasted bandwidth
- CUDA graphs incompatible with dynamic expert routing

## FlashMoE design

**Single persistent GPU kernel** fusing gate → dispatch → expert FFN → combine.

### Actor model (reactive programming)

| Actor | Role |
|-------|------|
| **Processor** (N−1 blocks) | CUTLASS GEMM + element-wise; tile send/receive |
| **Scheduler** (1 warp in OS block) | Work-conserving task dispatch to processors |
| **Subscriber** (3 warps in OS block) | Decode remote tile packets → task descriptors |

Tile dimensions: **(128, 64)**; 128 threads/block.

### Communication

- **NVSHMEM** device-initiated one-sided **RDMA** over UVA — replaces bulk-synchronous AlltoAll
- **Symmetric tensor layout** L ∈ R^{P×R×B×E×C×H} — write-write conflict-free (Theorem 3.1); ~**4×** token buffer, ≤**2%** model memory
- **In-place padding** at compute time — payload-efficient (no null tokens on wire)

### Unified task abstraction

FFN and expert-combine as fused `__device__` tasks: t = (M, ⋆, ϕ) with matrix mul or Hadamard.

## Evaluation setup

8× H100 80G NVLink; PyTorch 2.6, CUDA 12.8; single MoE layer forward; top-2 routing, capacity 1.0; 16 heads, H=2048, FFN=2048; DDP + EP.

**Baselines:** Comet, FasterMoE, Megatron-CUTLASS, Megatron-TE (FP16); FlashMoE **FP32** (disadvantage: 2× comm/compute vs baselines).

## Key results

| Metric | FlashMoE vs SOTA |
|--------|------------------|
| Forward latency | up to **6.4×** (8 GPU, 16K tokens vs Megatron-TE) |
| SM utilization | **93.17%** vs FasterMoE **9.67%**, DeepEP **13.55%**, Comet **42.31%** |
| Throughput | **17.7 MTokens/s** @ 8 GPU — **5.7×** FasterMoE |
| Overlap efficiency | **4×** |
| Expert scaling | sublinear latency 8→128 experts |

## Lineage / contrast

- Overlap lineage: Comet (partial), FasterMoE, DeepEP — still multi-kernel + NCCL collectives
- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — DeepSeek wave-based EP overlap (different stack; pull-based, production inference)
- [M2N Communication](/concepts/m2n-communication.md) — disaggregated attention→expert traffic patterns
