---
type: Raw Source
title: 'FlexInfer: breaking memory constraint via flexible and efficient offloading for on-device LLM inference'
source_path: /home/luke/wiki/raw/papers/FlexInfer_On_Device_LLM_Offloading_2025.pdf
arxiv: '2503.03777'
doi: '10.48550/arXiv.2503.03777'
zotero: X3BEJQKP
ingested: 2026-07-17
sha256: eaa7fd7913660b1007b26e36b1bee94c17292089c9ace6cd6c542cce6682c829
---

# FlexInfer: breaking memory constraint via flexible and efficient offloading for on-device LLM inference

Authors: Hongchao Du, Shangyu Wu, Arina Kharlamova, Nan Guan, Chun Jason Xue (CityU HK, MBZUAI)
Year: 2025

Structured notes / key excerpts:

- **Problem**: On-device LLM inference exceeds mobile/edge memory; quantization/pruning fix memory budget inflexibly; mmap page-fault offload (llama.cpp) thrashes I/O.
- **FlexInfer**: Offloading framework with **async prefetch**, **balanced memory locking**, **flexible tensor preservation** — adapts to user-specified memory budgets without retuning quant/sparsity.
- **Motivation (Table 1)**: Llama2-70B 4-bit (~36.2 GB); full-memory **31.14 tok/s**; at 5–25 GB avail mem, throughput **0.46–0.51 tok/s** (near-zero); only at 35 GB reaches **2.06 tok/s**.
- **Async prefetch**: Overlap I/O with compute to mitigate storage bandwidth bottleneck.
- **Balanced memory locking**: Uniformly retain hot parameters in limited RAM vs naive partial mmap.
- **Flexible tensor preservation**: Select which tensors to keep/offload per budget — not one-shot compression config.
- **Results**: **10.6–12.5×** speedup vs existing offloading methods across memory-limited scenarios; abstract also cites **12.5×** peak.
- **Contrast**: Distillation/compression lack budget flexibility; storage offload without prefetch loses to I/O bound.
