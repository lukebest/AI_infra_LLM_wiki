---
type: Raw Source
title: "To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems"
source_url: https://arxiv.org/abs/2610.28637
pdf: KVLearn_Disagg_KV_Retention_2026.pdf
retrieved: 2026-11-03
ingested: 2026-11-03
org: UCLA / Columbia
venue: SYSTOR '26
---

# Abstract (verbatim gist, arXiv:2610.28637)

Disaggregated LLM serving separates prefill and decode into distinct node pools, interposing a network fabric between the moment a KV cache is computed and the moment it is consumed. This architectural shift invalidates a core assumption of classical cache policies: that the cost of a miss is simply recomputation on the same device. In disaggregated systems, a miss triggers both recomputation on a prefill node and a network transfer of the resulting KV block to the decode node. We present KVLearn, a learning-based retention framework with (i) Prefix Reuse Predictor (PRP), (ii) Cost-Aware Retention Score (CARS), and (iii) Adaptive Threshold Controller (ATC). KVLearn reduces end-to-end TTFT by up to 56% vs. No-Cache, up to 38% vs. LRU-Pool, and up to 33% vs. Mooncake-style disaggregated baselines. Inter-node KV transfer volume is cut by up to 53% vs. LRU-Pool. On MM-Session, throughput stays within ∼5% of oracle.

# Excerpts / key facts (from PDF)

- Authors: Dong Liu*, Yanxuan Yu*, Eric Jiang, Shu Wang, Ying Nian Wu† (UCLA / Columbia; SYSTOR '26).
- Code: https://github.com/FastLM/KVLearn
- PRP: structural + temporal prefix features, no model weights; CARS: recompute/transfer/storage costs; ATC: closed-loop hit-rate / memory pressure.
- Text + multimodal (image/video-derived tokens) workloads.
- TTFT up to **−56%** vs No-Cache, **−38%** vs LRU-Pool, **−33%** vs Mooncake-style; inter-node KV transfer up to **−53%** vs LRU-Pool; MM-Session throughput within **~5%** of oracle.
