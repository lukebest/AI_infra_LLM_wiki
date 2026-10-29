---
type: Raw Source
title: "Speeding up Log-Sum-Exp: Kernel Fusion at the Memory Wall, Integer Arithmetic at the Compute Wall"
source_url: https://arxiv.org/abs/2610.33647
pdf: FuseLSE_IntLSE_LogSumExp_NeurIPS2026.pdf
retrieved: 2026-10-29
ingested: 2026-10-29
org: Aalto; (coauthors across affiliations on paper)
venue: NeurIPS 2026 (arXiv cs.DC replacement)
---

# Abstract (verbatim, arXiv:2610.33647)

While the Log-Sum-Exp (LSE) function is a foundational numerical primitive for stable log-domain computation in modern machine learning, its fast and efficient computation on generic platforms (i.e., CPUs and GPUs) has been underexplored, potentially creating execution bottlenecks for large workloads. On GPU, the de facto implementation torch.logsumexp dispatches a chain of nine sub-kernels per call, incurring redundant High Bandwidth Memory (HBM) traffic and launch overhead. On CPU, exp and log operations are hardware-hungry, limiting the computing efficiency. To address these bottlenecks, we propose two drop-in kernels to significantly accelerate LSE computation on both GPUs and CPUs: FuseLSE, a single-pass fused kernel that evaluates LSE's exp and log functions on the GPU's Special Function Unit (SFU); and IntLSE, which further replaces the LSE computation with approximated integer arithmetic for CPU computation. Our experiments, validated by benchmarks across workload sizes and hardware platforms, show that both kernels are ~10−11× faster than PyTorch at small workloads and ~6× faster on larger ones on GPUs, where the speed-up is attributed to reduced launch overhead and HBM traffic. On CPU, where no SFU is available, LSE computation dominates the cost, allowing IntLSE to gain ~3−6× execution speed over FuseLSE.

# Excerpts / key facts (from PDF)

- Authors: Lingyun Yao, Martin Andraud, Niki Loppi, Andrea Pilzer, Anji Liu, Guy Van den Broeck, Martin Trapp. Accepted NeurIPS 2026. Code: https://github.com/lingyunyao/fuselse
- Motivation: torch.logsumexp ~**6×** slower than torch.sum on same tensor (example **1.95 ms vs 0.31 ms**); nine sub-kernels; ~**6×** input-size HBM round-trips (amax/sub/exp/sum).
- FuseLSE: pairwise associative LSE, single HBM pass (~**1×** traffic), SFU `__expf`/`__logf`, B blocks × warps covering 128 float32/step.
- IntLSE: Mitchell-style integer approx of log2(1+2^z) with adds/shifts (+ optional LUT); same reduction skeleton.
- GPU results: both kernels **~10–11×** vs torch.logsumexp at small workloads, **~6×** at large; FuseLSE/IntLSE nearly identical on GPU (memory-bound); example profile FuseLSE **312 µs** / IntLSE **315 µs** ≈ torch.sum **311 µs**.
- CPU: IntLSE **3–6×** over FuseLSE; particle-filter app **2.8–5.2×** over torch.logsumexp.
- Conclusion claim: **~6–12×** across microbenchmarks and three ML apps; fusion dominates on GPU; integer wins without SFU.
- Limits: IntLSE cumulative approx error; FuseLSE16 / IntLSE-Q10.6 not yet in app benchmarks.
