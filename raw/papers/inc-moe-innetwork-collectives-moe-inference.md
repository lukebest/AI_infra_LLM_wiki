---
type: Raw Source
title: "INC-MoE: Overlapping In-Network Collectives and Expert Computation for Expert-Parallel Mixture-of-Experts Inference"
source_url: https://arxiv.org/abs/2610.36339
pdf: INC_MoE_InNetwork_Collectives_MoE_Inference_2026.pdf
retrieved: 2026-10-29
ingested: 2026-10-29
org: (authors unaffiliated on arXiv abs)
venue: arXiv cs.DC (2026-10)
---

# Abstract (verbatim, arXiv:2610.36339)

In expert-parallel mixture-of-experts (MoE) serving, dispatch moves tokens to the accelerators hosting their selected experts, and combine returns expert outputs to each token's owner. Both operations lie on the critical path and can dominate MoE layer latency in multi-node deployments. We present INC-MoE, an expert-parallel MoE layer that offloads dispatch and combine to the network switch and overlaps both collectives with each other and with expert computation. Dispatch uses in-network AllGather through switch-side multicast, while combine uses in-network ReduceScatter through switch-side reduction. Both collectives use message semantics between the end hosts and the switch. Because the in-network collectives load opposite directions of each link, executing them concurrently reduces bandwidth-bound communication time by $(N-2)/(2(N-1))$ relative to concurrent ring-based collectives: 33% for four ranks and 43% for eight. INC-MoE partitions tokens into bands and processes them through a three-stage AllGather-feed-forward network (FFN)-ReduceScatter pipeline inside a single persistent kernel. At steady state, role-specialized thread blocks gather the next band, compute the current band, and reduce the previous band concurrently, overlapping both collectives with each other and with computation using device-side synchronization. INC-MoE integrates as a drop-in replacement for the MoE layer of vLLM. We evaluate it in an emulated four-node scale-out deployment with a dedicated accelerator emulating an in-network computing (INC) switch. On OLMoE prefill with four-way expert parallelism, INC-MoE reduces time to first token (TTFT) by up to 33% and increases throughput by up to 50% relative to vLLM's default collective path, while matching its outputs.

# Excerpts / key facts (from PDF)

- Authors: John Stephan, Razvan Puscasu, Xu Yong, Ding Jiutao, Guan Zixuan.
- Setting: EP MoE dispatch=AllGather, combine=ReduceScatter; multi-node critical path.
- In-network: switch multicast AG + switch reduction RS; message semantics host↔switch.
- Theory: overlapping in-network AG+RS shortens bandwidth-bound time by (N−2)/(2(N−1)) vs concurrent ring → **33.3%** (N=4), **42.9%** (N=8); up to **1.5×** equivalent bandwidth (N=4).
- Kernel: band pipeline AG–FFN–RS in one persistent kernel; role-specialized blocks; device-side sync; tail assistance.
- Eval: emulated 4-node scale-out; 5th accelerator emulates INC switch; OLMoE prefill, EP=4; drop-in vLLM MoE layer.
- Standalone concurrent AG+RS: INC equivalent bandwidth **163–172 Gbps**, **+25.6–31.8%** vs concurrent ring (**82–86%** of INC bound; ring ~97.5% of its bound).
- End-to-end: TTFT **−20.2–33.1%** (24K→largest); prefill throughput **+25.3–49.5%** (abstract rounds to up to 33% / 50%); baseline throughput nearly flat **22.5K–23.8K** tok/s/accelerator; INC rises with prompt size (e.g. ~**32K** tok/s at large prompts).
- Correctness: matches vLLM default path outputs.
