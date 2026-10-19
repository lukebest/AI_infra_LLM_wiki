---
type: Raw Source
title: "Architecting for Hardware Diversity: Meta's End-to-End Co-Design for High-Performance AI Training on AMD GPUs"
source_url: https://arxiv.org/abs/2610.22230
pdf: Meta_AMD_MI350X_Training_CoDesign_MICRO26.pdf
retrieved: 2026-10-19
org: Meta; AMD
venue: MICRO 2026 (arXiv cs.DC, submitted 2026-10-15)
---

# Abstract (verbatim, arXiv:2610.22230)

Meta deploys a heterogeneous fleet comprising NVIDIA GPUs, AMD GPUs, and proprietary MTIA accelerators to reduce costs and mitigate vendor lock-in. However, the extensive history of NVIDIA-specific optimizations hinders performance portability to other hardware. This paper presents our methods for optimizing alternative accelerators, using AMD Instinct MI350X versus NVIDIA B200 for recommendation model training as a case study. We propose three reusable principles. First, hardware-model co-design is essential: rather than directly porting models from NVIDIA GPUs, revising model structures and software recipes allows full exploitation of accelerator-specific strengths (e.g., MI350X's 1.6x HBM capacity relative to B200). Second, our analytical performance model enables zero-warmup optimal kernel selection across diverse datatypes and matrix shapes in production models, drastically simplifying tuning. Third, increasingly mature agentic workflows have lowered the barrier to porting from the CUDA ecosystem; we extend these workflows for microarchitecture-aware kernel optimizations and custom shim generation. Compared to the directly ported baseline, these methods deliver up to 1.5x improvement in end-to-end training throughput. To our knowledge, this is the first hyperscaler report on productionizing AMD GPUs for large-scale training. Our contributions have been upstreamed to the open-source PyTorch, Triton, and ROCm ecosystems.

# Excerpts (from arXiv PDF v1)

- Table I: MI350X CDNA 4, 256 CU (8 XCD × 32), 2300 BF16 dense TFLOPS, HBM3e 288 GB, up to 8 TB/s, LDS 160 KB/CU, scale-up 538 GB/s uni-dir, air-cooled 1000 W (Meta on-prem). B200: 148 SM (2 chiplets), 2250 TFLOPS, HBM3e 180 GB, 8 TB/s, 256 KB/SM, 900 GB/s, Meta deploys at 750 W air-cooled.
- §I: hardware-model co-design (bigger batch, less activation checkpointing, longer sequences / larger hidden dims / larger embedding tables) delivers 20% training speedup and >0.1% NE improvement. Origami analytical GEMM model achieves 93% accuracy relative to exhaustively autotuned kernels. Agentic kernel workflows: 1.6×–2× speedups; tree reduction in shared memory up to 4× in custom kernels. Production training on tens of thousands of MI350X; geomean throughput 101% of B200 across representative production models; LLM training on >2,000 MI350X (analysis deferred).
- Origami: per-tile compute latency = N_MI · L_MI; cache hit rate H = 1 − (M_C·M_T + N_C·N_T)/(M_C·N_C·(M_T+N_T)) applied at L2 and LLC; XCD-aware workgroup-ID swizzle maps adjacent output tiles to the same XCD.
- Power: OAM excursion design power permits 1.1× TBP over 20 ms up to 2.0× TBP over 20 µs; tuning the control loop gives up to 1.33× in a synthetic GEMM-duty microbenchmark.
- RCCL: gap narrowed from 2× slower than NCCL to within 10–15% of NCCL. LL128 replaced with LL64 (56 B payload + 8 B flags in one cache-line-atomic 64 B packet): 2× AllGather/ReduceScatter, 1.2–1.4× AllReduce. Direct AllGather 1.4× for small messages; P2P batching cuts AllToAll latency 40% at 128 GPUs; 46% VGPR reduction doubles occupancy → ReduceScatter +63%, AllReduce +48%.
- GDPA kernel: GeLU fast math (direct sigmoid-based GeLU via fast_expf / fast_dividef instead of tanh = 2σ(2x)−1), occupancy hints, MFMA config, PID swizzle: forward 1.47 ms (58.4 TFLOP/s) → 0.59 ms (145.9 TFLOP/s), −60.0% latency, 2.5× throughput; backward 3.67 → 2.17 ms (−40.9%); optimized GDPA kernels on MI350X beat B200. HSTU kernel: forward block-size tuning + occupancy hints + PID swizzle 3.22× (45.0 → 144.8 TFLOP/s); backward MFMA tuning 1.21× (60.2 → 72.6 TFLOP/s); averaged over sequence lengths optimized MI350X HSTU kernels are 1.22× faster than B200 forward and 1.80× backward (combined 1.69×).
- Atomics: multi-chiplet MI350X atomics may need cross-XCD coherence; MI350X can be >10× slower than B200 on atomic-heavy kernels at high contention. Tree reduction: at 10% violations 4.26× (2.1 vs 9.0 ms); at 20% 4.34× and 1.75× faster than B200.
- Larger HBM: friend recommendation model 26% speedup at 2× batch, 46% at 4×, 51% at 6×; GPT model on B200 needs aggressive activation checkpointing (budget ≤0.35), 1.35× throughput disadvantage attributable to memory.
- Where B200 leads: GEMM 1.3–1.7× higher latency on MI350X; TF32 emulated with three BF16 GEMMs. End-to-end geomean 101.2% across ten production models (Table III).
