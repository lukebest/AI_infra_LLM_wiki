---
type: Raw Source
title: 'SuperInfer: SLO-aware rotary scheduling and memory management for LLM inference on superchips'
source_path: /home/luke/wiki/raw/papers/SuperInfer_SLO_Aware_Rotary_Scheduling_Superchips_2026.pdf
arxiv: '2601.20309'
doi: '10.48550/arXiv.2601.20309'
zotero: 2X6DFSCG
ingested: 2026-07-17
sha256: b669cacc88de6b35e5b2a652c1f40a7667531b5a21ed5273c8d43b581292ed7a
---

# SuperInfer: SLO-aware rotary scheduling and memory management for LLM inference on superchips

Authors: Jiahuan Yu, Mingtao Hu, Zichao Lin, Minjia Zhang (UIUC)
Year: 2026

Structured notes / key excerpts:

- **Problem**: High request rates exhaust GPU KV budget → head-of-line blocking; PCIe offloading (~32–64 GB/s) too slow for tight TTFT/TBT SLOs; prior SLO schedulers still memory-bound.
- **Superchip opportunity**: GH200 Hopper+Grace via NVLink-C2C (~900 GB/s); direct port of PCIe offload achieves **<5%** C2C bandwidth utilization — software mismatch, not hardware limit.
- **RotaSched**: OS-inspired proactive rotary scheduler; transient rotary state rotates requests between HBM and DRAM based on SLO progress (Virtual Lag Time), not passive OOM preemption.
- **DuplexKV**: Full-duplex, data-race-free KV rotation engine — merges fragmented paged KV blocks, overlaps transfer with compute, maximizes C2C bandwidth.
- **vs PagedAttention**: Paging reduces fragmentation but scatters KV → expensive GPU–CPU transfer; SuperInfer co-designs scheduler + rotation engine for superchips.
- **Results**: Up to **74.7%** higher TTFT SLO attainment under high load; comparable TBT and throughput vs SOTA; at low load matches baseline (no overhead when memory sufficient).
- **Platform**: Evaluated on NVIDIA GH200 across multiple models/datasets; code at github.com/Supercomputing-System-AI-Lab/SuperInfer.
- **Contrast**: Aqua uses peer GPU NVLink offload; InfiniGen/CacheGen reduce KV volume but are lossy; FastDecode/NEO remain PCIe-bound.
