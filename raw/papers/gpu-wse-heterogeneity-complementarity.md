---
type: Raw Source
title: "When Does Heterogeneity Pay Off? Understanding GPU–WSE System Complementarity"
source_url: https://arxiv.org/abs/2610.39222
pdf: GPU_WSE_Heterogeneity_Complementarity_2026.pdf
retrieved: 2026-11-02
ingested: 2026-11-02
org: Stevens Institute of Technology / Argonne National Laboratory
venue: arXiv
---

# Abstract (verbatim, arXiv:2610.39222)

As AI accelerator architectures become increasingly diverse, integrating different architectures into a unified system is emerging as a new heterogeneous computing paradigm. GPUs and WSEs differ substantially in compute, memory, and communication organization, creating both architectural complementarity and additional overheads, yet how to translate this heterogeneity into practical performance gains remains unclear. To address this gap, we propose a hierarchical benchmarking methodology to characterize GPU–WSE heterogeneous execution and the conditions for exploiting complementarity, together with an analytical performance model that identifies when heterogeneity becomes a bottleneck and when it yields system-level performance gains.

# Excerpts / key facts (from PDF)

- Authors: Ziyu Hu, Zhijing Ye, Jiamin Wang, Zhiqing Zhong, Zhendong Mi, Shaoyi Huang (Stevens); Weijian Zheng, Rajkumar Kettimuthu (Argonne); Xiaodong Yu (Stevens).
- Platform: Cerebras WSE-3 + NVIDIA A100 via SimAI hierarchical bench of DP / PP / PD disaggregation; industrial context notes AWS–Cerebras plans to integrate Trainium and WSE.
- DP: three regimes with two workload thresholds; under enough batch, hybrid DP approaches the aggregate upper bound.
- Standard (unified micro-batch) PP: none of the heterogeneous PP configs outperform single-platform setups.
- Architecture-aware PP (different micro-batch sizes across GPU/WSE): 7B/13B/35B can beat WSE-only at global batch 1024, but still below theoretical upper bound; 70B does not show the same gain in the reported comparison.
- PD: GPU better at prefill; WSE decode completes a step in tens of microseconds with relatively stable µs-level latency, while GPU decode grows from tens to hundreds of milliseconds as context length increases.
- Analytical model median prediction error: DP **6.8%** (P90 13.4%); PD **8.2%** (P90 16.4%).
