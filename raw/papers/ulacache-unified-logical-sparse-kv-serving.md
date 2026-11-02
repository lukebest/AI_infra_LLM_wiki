---
type: Raw Source
title: "UlaCache: Unified Logical Addressing for Sparse LLM Serving"
source_url: https://arxiv.org/abs/2610.29820
pdf: UlaCache_Unified_Logical_Sparse_KV_Serving_2026.pdf
retrieved: 2026-11-02
ingested: 2026-11-02
org: Scitix.AI
venue: arXiv (ICML-style PDF)
---

# Abstract (verbatim, arXiv:2610.29820)

Long contexts increase the memory cost of the key-value (KV) cache in large language model (LLM) inference. Sparse attention reduces attention computation and memory traffic by selecting historical tokens, but the retained KV cache must remain available for later decoding steps. We present UlaCache, a KV cache management system built around a unified logical address space spanning GPU KV pools and optional CPU memory. Stable logical references let the inference engine allocate and select KV independently of physical placement. Common allocation and sparse-access interfaces support data-parallel (DP) and tensor-parallel (TP) attention. For distributed storage, local GPU buffers retain selected KV across decoding steps, so only missing entries require transfers. When CPU storage is enabled, Parallel Bucketed LRU (PB-LRU) manages a GPU pool shared across requests. It updates recency metadata and selects eviction victims in parallel. UlaCache transfers KV and then updates the address mappings. With speculative decoding enabled under matched CPU and GPU memory budgets, UlaCache achieves peak decoding throughput speedups of 1.16 × (DP) and 1.70 × (TP) on H200, and 1.73 × (DP) and 2.51 × (TP) on B300, compared with the state-of-the-art baseline.

# Excerpts / key facts (from PDF)

- Authors: Isaac Zhu, Alan Cao, Hugh Yin, Rocky Wang, Orion Wang, Hscos Zhang, Jack Li, Jason Zhao (Scitix.AI; corresponding Jason Zhao / jason@scitix.ai).
- Problem: sparse attention still needs retained historical KV; HiSparse-style fixed per-request GPU buffers leave idle capacity unused and inflate TPOT (one 8×B300 DP + speculative config: HiSparse TPOT **23.5%** higher than GPU-resident SGLang).
- UlaCache: unified logical KV address across GPU pools + optional CPU; DP rank-local vs TP distributed history; local GPU buffers for selected KV in TP; Parallel Bucketed LRU (PB-LRU); integrated in SGLang; GLM-5.3; Multi-LexSum 64K–128K prompts, **2,048** greedy output tokens; FP8 weights/KV, BF16 activations; MTP speculative (2 draft steps) when enabled.
- Peak decode throughput vs HiSparse (speculative on, matched CPU/GPU budgets): **1.16× (DP) / 1.70× (TP)** on 8×H200; **1.73× (DP) / 2.51× (TP)** on 8×B300.
- Without speculative on B300 TP: UlaCache peak throughput **3.51×** SGLang’s peak (capacity-limited SGLang).
- PB-LRU scheduling ~**1.5–2.3×** faster than naive LRU at larger measured batches (GPU scheduling time excl. KV transfers).
