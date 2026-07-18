---
type: Raw Source
title: 'Fast state restoration in LLM serving with HCache'
source_path: /home/luke/wiki/raw/papers/HCache_Fast_State_Restoration_LLM_Serving_2025.pdf
arxiv: ''
doi: '10.1145/3689031.3696072'
zotero: VNS762WY
ingested: 2026-07-17
sha256: 0492cc094dfc401bec3a0727b56f70e144ccd3c8f19601498a565edd03107529
---

# Fast state restoration in LLM serving with HCache

Authors: Shiwei Gao, Youmin Chen, Jiwu Shu (Tsinghua University)
Year: 2025 (EuroSys '25)

Structured notes / key excerpts:

- **Stateful LLM serving**: Multi-turn chat and RAG reuse historical context/KV across requests; stateless serving recomputes or offloads everything.
- **GPU cache limit**: Single A100-40GB holds only **7–20** multi-round conversations or **1–3** long contexts (ShareGPT4, L-Eval traces).
- **Existing restoration extremes**: (1) **Recomputation** — prefill history tokens, high compute; (2) **KV offload** — host storage fetch, high I/O.
- **HCache core idea**: Restore from **intermediate hidden states** (half KV size) → recompute KV via GEMM; uses **both** compute and I/O concurrently.
- **Resource savings vs extremes**: **6×** less compute than full recomputation; **2×** less I/O than KV offload (Figure 1).
- **Bubble-free restoration scheduler**: Combines resource-complementary methods when recompute vs I/O completion times mismatch across hardware.
- **Chunk-based storage manager**: Fixes layer-before-token save vs token-before-layer restore layout mismatch.
- **Results vs KV offload**: TTFT up to **1.93×** faster; **1.92–2.40×** less storage.
- **Results vs recomputation**: TTFT up to **5.73×** faster; **<4%** TBT overhead.
- **Hardware range**: **1.33–2.66×** vs KV offload across varying compute/IO speeds.
