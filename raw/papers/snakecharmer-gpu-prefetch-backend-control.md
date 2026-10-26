---
type: Raw Source
title: "SnakeCharmer: Orchestrating Utility, Timeliness, and Placement in GPU Prefetching"
source_url: https://arxiv.org/abs/2610.30990
pdf: SnakeCharmer_GPU_Prefetch_Control_MICRO2026.pdf
retrieved: 2026-10-26
org: National University of Defense Technology; Peking University
venue: MICRO 2026 (accepted), arXiv cs.AR
---

# Abstract (verbatim, arXiv:2610.30990)

GPUs rely on massive thread-level parallelism to tolerate long memory latency, yet they still suffer severe stalls when many warps simultaneously wait for data from the memory system. Address-prediction-based GPU prefetchers can mitigate such stalls, but accurate prediction alone does not guarantee performance improvement: a predicted prefetch becomes beneficial only if it is worth issuing, arrives at the right time, and is retained without harmful interference. Because these requirements interact, optimizing any single dimension in isolation can simply move the bottleneck to another. We capture these requirements with a predicted-prefetch-to-realized-benefit perspective and propose SnakeCharmer, a unified backend prefetch-control framework for address-prediction-based GPU prefetchers. SnakeCharmer separates address prediction from prefetch realization: the frontend predictor generates prefetch candidates, while the backend control path jointly controls utility, timeliness, and placement by determining whether each candidate should be issued, when it should be issued, and where the returned data should be retained. SnakeCharmer realizes this control path with zero-value-aware filtering for utility, hierarchical feedback-driven distance tuning for timeliness, and a register-assisted prefetch buffer for placement. We design and implement SnakeCharmer primarily on top of Snake, and adapt the same backend-control principles to APOGEE to demonstrate that SnakeCharmer's benefits are not limited to a single frontend predictor. On an A100 GPU model, SnakeCharmer improves performance/energy efficiency by 12.8%/20.8% over Snake and by 1.7%/3.2% over APOGEE, with modest hardware overhead.

# Excerpts / key facts (from PDF)

- Sparse apps: 36.8% of L2 prefetch traffic is zero-valued at 4B granularity vs 31.9% of demand traffic (Fig. 3b).
- Register file 256 KB/SM: at least 8 KB idle across all evaluated apps, average 21.0 KB idle — reused as prefetch buffer.
- Zero-value confidence per pattern; counter reset after 128 cycles; complementary to zero-compressed caches (acts before issue).
- Overhead: 2.7 KB per SM (0.6% of A100 on-chip SRAM), 0.04 mm² (<0.005% of 826 mm² die); one-cycle structures at 1410 MHz (CACTI 7.0).
- SK+SC reduces L2 cache traffic by 23.6% (A100 model, Accel-Sim; Rodinia/Tango etc. workloads).
