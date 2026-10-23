---
type: Raw Source
title: "MCCL: Measurement-based Collective Communication Library"
source_url: https://arxiv.org/abs/2610.17091
pdf: MCCL_Measurement_Based_Collective_Communication_2026.pdf
retrieved: 2026-10-23
org: EURECOM; Independent; Université de Lorraine
venue: PACMNET / CoNEXT'26 (replacement)
---

# Abstract (verbatim, arXiv:2610.17091)

Collective communication is a critical performance bottleneck in large-scale distributed training. Existing libraries and synthesis frameworks compute open-loop schedules once, assuming a static topology and peak link capacities. In production, however, persistent gray failures can silently degrade link throughput and latency for hours, causing pre-computed schedules to lose much of their efficiency during execution. In this paper, we present Measurement-based Collective Communication Library (MCCL), a collective communication library that closes the loop between runtime network measurement and dynamic schedule synthesis. MCCL passively measures GPU-to-GPU throughput, detects persistent degradation, re-synthesizes the affected communication-intensive schedules with warm-started synthesizers, and hot-swaps them without interrupting training. We validate the complete loop on a multi-node hardware prototype and use simulations to evaluate cluster-scale scenarios. In our experiments, MCCL incurs negligible overhead (<2%) while maintaining high measurement accuracy (<1.2% error) and low schedule hot-swap time (≈12 ms). Notably, under gray failures, MCCL reduces training time by up to 4.99× over static schedules on simulated training workloads for state-of-the-art LLMs such as Llama and DeepSeek.

# Excerpts / key facts (from arXiv HTML)

- Targets AllGather / AllToAll (communication-intensive); AllReduce via ReduceScatter (static/in-network) + AllGather (dynamic).
- Warm-start ForestColl for AllGather (up to 3.79× / 4.40× faster re-opt Fail1/Fail2); CG AllToAll warm-start up to 18.3× / 17.8× vs cold; rounding gap ≤2.13%.
- Prototype: 2 hosts × 4 H200, ConnectX-7 200 Gbps; measurement overhead <2% at saturation, error <1.2%; hot-swap ≈12 ms (OOB AllGather 5.74 ms + load 4.48 ms); failure detection 53.1 ms (α=0.012); total reaction 78.2 ms; AllGather algo BW 74.02→44.76→59.72 GB/s after swap.
- Offline SimAI: AllGather up to 7.33×, AllToAll up to 7.12× vs static under gray failures.
- E2E SimAI Llama 405B / DeepSeek 671B (one PP stage, 128–2048 GPUs): training time reduction up to 2.85× (Llama Fail2) and 4.99× (DeepSeek Fail2) vs NCCL static.
