---
type: Raw Source
title: 'PRESERVE: prefetching model weights and KV-cache in distributed LLM serving'
source_path: /home/luke/wiki/raw/papers/PRESERVE_Prefetch_Weights_KV_Cache_LLM_Serving_2025.pdf
arxiv: '2501.08192'
doi: '10.48550/arXiv.2501.08192'
zotero: VSLU435D
ingested: 2026-07-17
sha256: 2b43b8506d8f039f450bce52b6a9879f6d7489219e5f6b844db39629d529d97f
---

# PRESERVE: prefetching model weights and KV-cache in distributed LLM serving

Authors: Ahmet Caner Yüzügüler, Jiawei Zhuang, Lukas Cavigelli (Huawei Zurich Research Center)
Year: 2025

Structured notes / key excerpts:

- **Problem**: Multi-device LLM serving — collective comm (allreduce) leaves accelerators idle; prior GEMM+allreduce fusion only overlaps two consecutive ops and cannot cover KV (ops between attention and allreduce).
- **Decode bottleneck**: Autoregressive decode is **memory-bandwidth limited** — weights + KV fetched from HBM each step; OI ~16 Op/word vs accelerator roofline >100 Op/word.
- **PRESERVE**: Prefetch model weights **and KV-cache** from HBM to on-chip L2 **during** collective communication — hides comm latency with memory reads.
- **Graph optimization**: Compiler inserts prefetch ops in parallel streams; tracks prefetched data and caps L2 usage at compile time to avoid cache pollution.
- **Data dependency barrier**: Comm and subsequent matmul dependencies prevent trivial HW/compiler prefetch — PRESERVE explicit graph pass required.
- **Results**: Up to **1.6×** end-to-end speedup on commercial AI accelerators with SOTA open LLMs.
- **DSE**: Optimal L2 for prefetching grows **8 MB → 104 MB**; **1.25×** performance-per-cost vs baseline accelerator (GB200 **126 MB** L2, MI300X **256 MB** L3, Ascend 910B **196 MB** L2 cited).
- **Context**: Tensor parallelism partitions weights + KV; long context KV can exceed weight size; multi-device needed for ~100 ms/token SLO on 100B+ models.
