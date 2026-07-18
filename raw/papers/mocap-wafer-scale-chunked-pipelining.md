---
type: Raw Source
title: 'MOCAP: wafer-scale-chip-oriented memory-orchestrated chunked pipelining framework for prefill-only LLM inference'
source_path: /home/luke/wiki/raw/papers/MOCAP_Wafer_Scale_Chunked_Pipelining_Prefill_2026.pdf
arxiv: '2606.22968'
doi: '10.48550/arXiv.2606.22968'
zotero: 3ESPDYTY
ingested: 2026-07-17
sha256: daf67009ffe97e2706385bda0e199a3c2f2a73c45670e0a73dba34cdf8adbc3e
---

# MOCAP: wafer-scale-chip-oriented memory-orchestrated chunked pipelining framework for prefill-only LLM inference

Authors: Zichuan Wang, Huizheng Wang, Yuheng Xiao, Haonan Zuo, et al. (Tsinghua University, SJTU, Shanghai AI Lab)
Year: 2026

Structured notes / key excerpts:

- **Problem**: Prefill-only LLM workloads (process long context, emit one token) are latency-dominated by prefill; communication grows with sequence length and bottlenecks GPU clusters; wafer-scale chips (WSCs) offer higher bandwidth but existing work targets general inference.
- **Chunked pipeline challenge**: Causal attention causes uneven KV accumulation across pipeline stages (memory imbalance) and later chunks incur higher attention cost (latency imbalance); naive GPipe/Terapipe-style chunking fails on long prefill.
- **MOCAP**: Memory-Orchestrated Chunked Pipelining — first systematic optimization of prefill-only inference on WSCs.
- **MBKR (Memory-Balanced KV Reallocation)**: Redistributes KV cache across pipeline stages to relieve buildup at early stages and extend feasible sequence length.
- **LBCP (Latency-Balanced Chunk Partitioning)**: Non-uniform chunk sizes balance attention growth vs KV reallocation overhead; reduces pipeline bubbles.
- **WSC vs GPU**: On GR24-equivalent configs, WSC communication advantage cuts average total latency ~46.8% vs HGX B200 at matched compute/memory.
- **Results vs GPipe**: 76.4% lower end-to-end latency; 3.24× average throughput.
- **Results vs Terapipe**: Up to 1.31× maximum supported sequence length.
- **Context**: Prefill-only contexts up to ~10⁵ tokens; KV from prefill need not persist for long decode (unlike generative serving).
- **Inspiration**: Terapipe token-wise pipeline for training; MOCAP adapts chunked pipeline to prefill-only with memory orchestration.
