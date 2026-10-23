---
type: Raw Source
title: "NanoCP: Taming Load Imbalance in Data-Expert Parallel Decoding under Variable-Length Workloads"
source_url: https://arxiv.org/abs/2605.21100
pdf: NanoCP_Dynamic_Context_Parallelism_MoE_ASPLOS27.pdf
retrieved: 2026-10-23
org: Fudan; SJTU; Shanghai AI Lab; CUHK; PKU; HIT; SenseTime
venue: ASPLOS'27 (replacement)
---

# Abstract (verbatim, arXiv:2605.21100)

Modern serving systems for Mixture-of-Experts (MoE) models adopt hybrid data-expert parallelism: expert parallelism (EP) shards experts across GPUs to scale capacity, while data parallelism (DP) replicates attention layers across instances to process independent requests. Existing systems bind each request's attention, MoE communication, and KV cache to a single instance. Because attention latency scales with KV cache size while MoE communication latency scales with batch size, this binding cannot balance both simultaneously, producing EP stragglers; it also fragments KV memory across instances, inflating tail latency under long contexts. While existing context parallelism (CP) mitigates these constraints, existing group-level and uniform CP designs incur prohibitive communication and attention-side overheads.

We present NanoCP, which decouples MoE communication from KV cache placement and achieves dual balance through dynamic context parallelism (DCP). DCP assigns each request a context-parallel degree sized to its KV footprint: long requests distribute attention across multiple instances; short requests remain local.

This dynamic parallelism effectively liquefies the KV cache across DP instances within each node, balancing both the per-instance KV cache occupancy and batch sizes without unnecessary load-balancing costs. To bridge DCP with static execution, NanoCP introduces an ahead-of-time (AOT) graph engine paired with a custom routing-based communication backend. Experimental results show that, under 99% TPOT-SLO attainment, NanoCP achieves 3.27× and 2.11× the maximum sustainable request rate of the best-performing vLLM baseline on the DeepSeek-V3 Issue 1% and Issue 5% workloads, respectively, while reducing P99 TPOT by 1.94× and 2.01× on the same two workloads, respectively.

# Excerpts / key facts (from arXiv HTML)

- H200 cluster; DeepSeek-V3 / Kimi-K2; FlashMLA + DeepEP; TPOT SLO 50 ms; ≥99% SLO attainment.
- Issue 1% / 5%: max sustainable request rate 3.27× / 2.11× vs best vLLM; P99 TPOT −1.94× / −2.01× at baseline's 100 ms P99 point.
- Kimi-K2: 1.88× / 2.20× request rate; mean TPOT 1.87–2.07×; P99 1.79–2.12×.
- Micro: CP comm avg 60.4 µs vs uniform CP8 629.8 µs (−90.41%); attention max-to-median gap −84%+ vs LeastBatch.
- AOT: 48 CUDA Graphs, 5.32 GiB/GPU (+4.30 GiB ≈3.0% H200 HBM vs vLLM 32DP); scheduler+RDMA 1.42–2.61% iter time; routing backend Q A2A 1.05–2.03× vs NCCL.
- Peak only 1.1% requests use cross-instance CP; DCP A2A peaks 35.5 µs.
