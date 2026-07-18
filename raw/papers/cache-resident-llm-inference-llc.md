---
type: Raw Source
title: 'Cache-resident LLM inference in GB-scale last-level caches'
source_path: /home/luke/wiki/raw/papers/Cache_Resident_LLM_Inference_GB_LLC_2026.pdf
arxiv: '2606.25353'
doi: '10.48550/arXiv.2606.25353'
zotero: N6X2E6WF
ingested: 2026-07-17
sha256: 810de0ad8aae570d5425ae7e7a6783194554d656bc998ac08a26d1baea522dac
---

# Cache-resident LLM inference in GB-scale last-level caches

Authors: Wanning Zhang, Tongzhou Gu, Marco Canini, Ceyu Xu, Jian Weng (KAUST, HKUST)
Year: 2026

Structured notes / key excerpts:

- **Opportunity**: 3D-stacked caches enable **GB-scale LLC** on server CPUs; weights can stay cache-resident exploiting cache bandwidth/latency vs DRAM.
- **PP scalability trap**: Layer-wise pipeline parallelism deepens pipeline → more in-flight tokens → KV footprint grows with depth, competing with weight residency in same cache.
- **Insight**: Weights (static, reusable) vs KV (per-request runtime state) have different access patterns — should occupy **separate resource domains**.
- **Execution model**: Decouple weight-centric ops from attention/KV management; relax sync from operator boundaries to **sub-operator dependencies** (e.g., independent attention heads).
- **vs operator-centric TP**: Global barriers at each operator costly when data already in LLC; fine-grain scheduling amortizes sync.
- **Prototype**: Multi-socket CPU cluster with weight–attention decoupled architecture + locality-aware placement + static runtime.
- **Measured (Llama-3.2-3B, Llama-2-7B vs llama.cpp)**: **2.04×–11.51×** TPOT speedup.
- **Analytical model extrapolation**: Up to **13.9×** TPOT; up to **12.5×** throughput across model sizes, context lengths, batch sizes.
- **Bottleneck shift**: Once cache-resident, operator-boundary synchronization becomes dominant overhead.
