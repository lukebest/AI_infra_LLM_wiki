---
type: Raw Source
title: "Ofan: Optimal Load Balancing for AI Training"
source_url: https://arxiv.org/abs/2610.07230
pdf: Ofan_Destination_Aware_Load_Balancing_AI_Training_2026.pdf
retrieved: 2026-10-12
org: UC Berkeley / Technion / NVIDIA / ICSI
---

# Abstract excerpt (verbatim, arXiv:2610.07230)

The extreme collective completion time (CCT) demands of AI workloads challenge existing packet spraying algorithms... on a fat tree, once a packet picks its upward path, the downward path to its destination is unique, so destination-oblivious schemes cannot undo the imbalance it creates. We prove that such schemes can suffer from Θ(√m) queueing for messages of size m... Ofan, a switch-based destination-aware LB scheme that can reach O(1) queueing. We also present its pOfan variant that fits the pipe-based architecture of current switches. Our P4 implementation shows that it consumes modest resources. An end-to-end FSDP2 evaluation with Llama-3 405B-parameter models shows that Ofan cuts CCT inflation by 16–39× when compared to existing algorithms.
