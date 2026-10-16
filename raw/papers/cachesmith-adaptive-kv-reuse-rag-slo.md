---
type: Raw Source
title: "CacheSmith: Accurate RAG Serving under Latency SLOs with Adaptive KV Reuse"
source_url: https://arxiv.org/abs/2610.18925
pdf: CacheSmith_Adaptive_KV_Reuse_RAG_SLO_2026.pdf
retrieved: 2026-10-16
org: POSTECH / Microsoft Research
venue: arXiv cs.AR / cs.DC
---

# Abstract (verbatim, arXiv:2610.18925)

This paper presents CacheSmith, a KV cache reuse system for RAG prefill that maximizes quality-gated SLO attainment. While context caching lowers prefill latency by reusing precomputed KV states for retrieved chunks, it misses cross-chunk attention that a full prefill would compute over concatenated inputs. Prior selective recomputation schemes tackle this problem but enforce static, one-size-fits-all configurations that fail to effectively handle request heterogeneity or dynamic latency budgets. CacheSmith decomposes selective recomputation into a three-phase workflow of WarmUp, Probe, and Patch that can be dynamically configured to exploit a wide range of cost-accuracy trade-offs. At serving time, an SLO-aware scheduler in CacheSmith forms batches to mitigate inter-request interference during layer-by-layer prefill, while a budget-aware planner configures recomputation phases across the batch to maximize the number of requests satisfying both generation quality and latency targets. Both components make fast, solver-free decisions over profiled cost-accuracy bands. On four benchmarks across varying arrival rates and burstiness levels, CacheSmith improves quality-gated SLO attainment by up to 27.5%, over four state-of-the-art baselines.

# Excerpts (from arXiv HTML/PDF)

- Intro eval: quality-gated SLO attainment up to 27.5%; P99 TTFT cut by up to 86% vs EPIC / ProphetKV / CacheBlend / FusionRAG.
- Abstraction: (S, w, p, r) = selection signal, warm-up depth, probe length, patch coverage; WarmUp / Probe / Patch phases.
- Hardware: 2× RTX PRO 6000 96 GB; Llama-3.1-8B (1 GPU) and Qwen3-32B (TP=2); vLLM 0.10.2.
- Fig.8: exceeds BestStatic in 93/96 settings; QSA improvement 2–27.5%.
- Fig.9: PR example 97% attainment at 89% accuracy combination no prior method reaches.
- Transfer-aware: at 3 GB/s SSD, baselines stall 12–72% serving time; CacheSmith 3–7% stalled; accuracy rises as link slows (PR 69%→92%).
- Ablation: Scheduler alone lifts CacheBlend QSA +10% PR / +20% VT; ProphetKV +29%.
