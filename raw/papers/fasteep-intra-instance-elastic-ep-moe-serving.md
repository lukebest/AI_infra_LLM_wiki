---
type: Raw Source
title: "FastEEP: Fast Intra-Instance Elastic Scaling for Expert-Parallel MoE Serving"
source_url: https://arxiv.org/abs/2610.18451
pdf: FastEEP_Intra_Instance_Elastic_EP_MoE_Serving_2026.pdf
retrieved: 2026-10-16
org: IPADS, Shanghai Jiao Tong University
venue: arXiv cs.DC
---

# Abstract (verbatim, arXiv:2610.18451)

Large-scale expert parallelism (EP) has become the standard deployment configuration for Mixture-of-Experts (MoE) models in production. Meanwhile, the highly dynamic nature of LLM workloads requires providers to continuously adjust serving capacity to match fluctuating demand. Scaling MoE serving cannot be efficiently achieved by simply adding or removing serving instances; instead, it often requires resizing the EP group within an existing instance, which we refer to as intra-instance scaling. Existing inference engines primarily rely on instance-level scaling, which destroys and reconstructs entire serving instances, incurring substantial scaling overhead.

We present FastEEP (Fast Elastic Expert Parallel), a fast intra-instance scaling system for MoE serving based on the principle of Partial Reuse. FastEEP reuses existing runtime state across worker execution, GPU memory, and communication by separating reusable execution structures from the resources activated by the current EP configuration. This separation enables coordinated resource reclamation and reconfiguration while preserving costly-to-reconstruct state, allowing fast EP scaling without full instance teardown and reconstruction. Our evaluation shows that FastEEP achieves 4.5×–11.7× faster scaling than the existing vLLM-based approach across different models, enabling efficient, fine-grained scaling of MoE serving.

# Excerpts (from arXiv HTML/PDF)

- Abstract / §5.2: vs vLLM Elastic EP geometric-mean 7.0× (range 4.5–11.7×); vs restart geomean 22.0×. Scaling latency 4.2–13.4 s (FullAsync 3.2–9.8 s) vs Elastic EP 36.4–92.0 s, restart 126–293 s.
- §2: bringing one DeepSeek-V2-Lite rank online (DP=8, EP=8) takes 126 s; runtime state 10.90 GiB > model weights 9.62 GiB on that rank.
- §5.3 closed-loop 8→4→8: zero-output windows FastEEP 4.2 s / 7.3 s vs Elastic EP 31 s / 44 s vs restart 141 s / 149 s.
- Phase breakdown Qwen3-30B: FastEEP scale-down 4.21 s (resize 2.81 s); scale-up 7.15 s (NIXL restore 2.50 s, resize 2.55 s). Elastic EP 47 s / 75 s.
- Design: parent NCCL + subgroup split; NIXL mask; CUDA VMM address-stable offload; shadow workers; CUMem graph pool for replay without recapture.
- Testbed: 2 nodes × 8× H20-3e, NVLink 900 GB/s, BF-3 CX-7 400 Gb/s; EP ∈ {2,4,8,12,16}.
