---
type: Raw Source
title: "Zepp: Accelerating Distributed MoE Serving under Relaxed Balance Constraints"
source_url: https://arxiv.org/abs/2610.11158
pdf: Zepp_Distributed_MoE_Serving_Relaxed_Balance_2026.pdf
retrieved: 2026-10-12
org: UCSD / ETH Zürich
---

# Abstract excerpt (verbatim, arXiv:2610.11158)

Skewed expert workloads create imbalance across computation, communication, and memory... balance is not free: operations introduced to balance one dimension can themselves be expensive or imbalanced. This motivates us to rethink balance as a constraint rather than an optimization objective. We present Zepp, which directly optimizes the bottleneck communication in distributed MoE serving subject to simplified balance constraints on physical resources, i.e., GPUs and NICs... achieving up to 6.68× MoE layer speedup and a geometric mean speedup of 1.86× over the fastest competing baseline.
