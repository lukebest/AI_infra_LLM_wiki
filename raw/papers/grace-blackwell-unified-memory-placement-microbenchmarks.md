---
type: Raw Source
title: "Understanding NVIDIA Grace–Blackwell Unified Memory Through Placement-Controlled Microbenchmarks"
source_url: https://arxiv.org/abs/2610.20354
pdf: Grace_Blackwell_Unified_Memory_Placement_Microbenchmarks_2026.pdf
retrieved: 2026-10-16
org: University of Delaware
venue: arXiv cs.DC / cs.AR
---

# Abstract (verbatim, arXiv:2610.20354)

NVIDIA Grace–Blackwell systems make CPU–GPU memory increasingly unified at the programming level, but unified addressability does not make the memory system uniform. A CUDA managed allocation on GB200 may be served from GPU-local HBM, accessed through host/system memory, demand-migrated, prefetched, reused after GPU access, or evicted and reloaded under capacity pressure. The problem is that these states share a programming interface while exercising different hardware paths and runtime mechanisms, making a single "Unified Memory bandwidth" number misleading.

This paper presents a placement-controlled microbenchmark study of CUDA Unified Memory on NVIDIA GB200, using GH200 as a Grace–Hopper baseline and GB10/DGX Spark as a validation platform. Our methodology separates local HBM access, host/system-memory access, explicit movement, managed first touch, prefetch, reuse, access-pattern sensitivity, oversubscription, and CPU–GPU handoff, then summarizes the observations with a measurement-calibrated model of compute, access, migration, eviction, synchronization, and handoff costs. On GB200, a 1 GB STREAM-style triad reaches 3963 GB/s from local HBM but 304 GB/s through host-mapped CPU/system memory; for a 256 MB streaming kernel, cold CPU-initialized managed memory reaches 14.1 GB/s, while managed prefetch and reuse reach 4606 GB/s and 4504 GB/s. Below the capacity boundary, prefetched and reused managed memory remain above 4.6 TB/s, but at 125% of CUDA-visible memory they fall to 968 GB/s and 1214 GB/s, showing that Grace–Blackwell unified memory must be understood through placement, access history, locality, reuse, and capacity pressure.

# Excerpts (from arXiv HTML/PDF)

- §V-A: 1 GiB triad GB200 HBM 3963 GB/s vs GH200 3165 GB/s (~1.25×); host-mapped 304 GB/s GB200 vs 345 GB/s GH200.
- Explicit H2D/D2H 1 GiB: GB200 211 / 193 GB/s; GH200 130 / 67 GB/s. Managed prefetch CPU→GPU 115 GB/s (GH200 42).
- §V-C 256 MiB stream: explicit HBM 4582 GB/s; cold managed 14.1 GB/s (0.3%); prefetch 4606; reuse 4504 (98.3%).
- Oversubscription: prefetch/reuse 4683–4736 / 4674–4701 GB/s at 25–90% capacity; at 105% → 2385 / 2722; at 125% → 968 / 1214 GB/s.
- Handoff 1 GiB R=1: managed 272.1 ms vs CPU+GPU baseline 54.2 ms; prefetch 79.9 ms; explicit copy 60.5 ms. At R=32: explicit 73.3, prefetch 92.6, host-mapped 218.7, managed 284.4 ms.
- Model validation median APE ~0.40% over larger working sets; host vs explicit crossover R*≈1.06.
