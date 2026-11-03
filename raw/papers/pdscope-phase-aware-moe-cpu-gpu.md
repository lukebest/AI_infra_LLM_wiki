---
type: Raw Source
title: "PDScope: Breaking the Prefill-Decode Seesaw for Memory-Bound MoE Inference"
source_url: https://arxiv.org/abs/2610.39216
pdf: PDScope_Phase_Aware_MoE_CPU_GPU_2026.pdf
retrieved: 2026-11-03
ingested: 2026-11-03
org: NUDT / Qiyuan Laboratory
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2610.39216)

Local deployment of MoE-based LLMs on CPU-GPU nodes is attractive for cost and privacy reasons, yet limited GPU memory forces most experts into CPU memory. Prefill is then compute-bound and benefits from aggressive GPU loading, while decode is I/O-bound and requires conservative PCIe transfers. These demands cannot be amortized under low batching—forcing phase-agnostic schedulers into a seesaw. We observe that expert routing is predictable in phase-specific ways. PDScope predicts expert activations to guide placement and prefetching, adapts these policies to each phase's bottleneck via cross-layer cost modeling, and compiles decisions into overhead-free pipelines using a static computation graph, cache prefetching, and zero-copy asynchronous I/O. On mainstream MoE models, PDScope achieves 2.5–10.3× higher prefill throughput and 2.1–6.1× higher decode throughput than existing systems.

# Excerpts / key facts (from PDF)

- Authors: Enda Yu, Dezun Dong, Zhaoning Zhang, Xiaojian Yang, Weiling Yang, Shaonan Ma, Dongsheng Li, Yongwei Wu, Xiangke Liao (NUDT / Qiyuan Lab).
- Components: PhasePer (phase-aware prediction; ~94% Top-6 on DS-V2-Lite / Qwen3-30B-A3B), AdaptSched (cross-layer cost model), static graph + zero-copy async I/O.
- Baselines include Fate, KTransformers, Fiddler, HybriMoE, MoE-APEX; A100 + Intel 6230R.
- Prefill throughput **2.5–10.3×**, decode **2.1–6.1×** vs existing systems.
