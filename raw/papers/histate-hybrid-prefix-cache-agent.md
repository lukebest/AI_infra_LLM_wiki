---
type: Raw Source
title: "HiState: Hierarchical Prefix Cache Management for Hybrid LLM Serving in Agentic Workloads"
source_url: https://arxiv.org/abs/2610.41508
pdf: HiState_Hybrid_Prefix_Cache_Agent_2026.pdf
retrieved: 2026-11-04
ingested: 2026-11-04
org: UC San Diego
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2610.41508)

Hybrid large language models combine full-attention and recurrent linear layers to reduce inference costs. Prefix caching can further reduce redundant computation across requests, but a recurrent checkpoint cannot recover an earlier state corresponding to a shorter prefix. Existing hybrid prefix caching systems retain checkpoints at selected boundaries to support common reuse patterns in conventional conversations. However, agent workloads modify and revisit earlier contexts, exposing reusable prefixes whose checkpoints were never saved or have already been evicted. A straightforward approach is to retain more checkpoints to reduce recomputation, but their cumulative footprint can displace reusable prefixes from other sessions and cause additional cache misses. To address these problems, we present HiState, a prefix cache management system for hybrid models serving agent workloads. Our key observation is that prefix reuse accesses all matching key-value (KV) entries but only one recurrent checkpoint, regardless of how many checkpoints are retained. This asymmetry allows HiState to retain historical checkpoints on SSD while prioritizing fast memory for KV entries: each hit retrieves only one checkpoint whose size is independent of context length. Within this hierarchy, we propose adaptive interval control to balance checkpoint storage against recomputation, and unified eviction to coordinate checkpoint sparsification with reclamation of stale trajectories. We implement HiState on top of vLLM and evaluate it on two public coding-agent trace datasets and controlled microbenchmarks. On real agent traces, HiState achieves up to 5.73× and 5.44× speedups in p99 TTFT over vLLM-Marconi and SGLang-HiCache, respectively.

# Excerpts / key facts (from HTML/PDF)

- Authors: Zaifeng Pan, Lucas Wang, Xinwei Qiang, Yanbo Zhou, Chang Chen, Zhengding Hu, Yue Guan, Yufei Ding (UCSD).
- Asymmetric tiering: KV in fast mem; historical recurrent checkpoints on SSD; adaptive interval; unified eviction.
- Implemented on vLLM; Qwen3.5-9B; Weka + TraceLab traces.
- On real coding-agent traces: up to **5.73×** and **5.44×** speedups in **p99 TTFT** over vLLM-Marconi and SGLang-HiCache.
- Also reports up to **7.40×** p95 TTFT over vLLM-Marconi (Fig. 8).
