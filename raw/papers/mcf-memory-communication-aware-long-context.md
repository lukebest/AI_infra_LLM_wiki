---
type: Raw Source
title: "MCF: A Memory- and Communication-Aware Co-Designed Framework for Long-Context LLM Inference"
source_url: https://arxiv.org/abs/2610.34731
pdf: MCF_Memory_Communication_Aware_Long_Context_2026.pdf
retrieved: 2026-10-30
ingested: 2026-10-30
org: University of Essex
venue: arXiv cs.AR (2026-10); EuroSys'27 (per PDF header)
---

# Abstract (verbatim, arXiv:2610.34731)

This paper presents Memory- and Communication-Aware Framework for Long-Context LLM Inference (MCF) that optimizes long-context inference through communication-aware and stage-adaptive KV-cache layout transitions. At the core of MCF is Memory-Aware Replication and Scheduling (MARS), a dynamic orchestration mechanism for chunked prefill. MARS exploits early-stage memory headroom by selectively replicating highly reused KV blocks, improving locality and hiding KV propagation latency behind attention computation. As prefill progresses and memory pressure increases, MARS progressively drains redundant replicas and converges the KV cache into a sharded decode-ready layout, avoiding expensive layout conversion at the prefill–decode boundary. For decoding, MCF adopts a query-centric execution model in which KV shards remain stationary while lightweight query tensors are routed across workers. This changes communication from KV-cache-dependent transfer to query-dependent transfer, reducing communication growth with context length. MCF further integrates a hardware-software co-designed execution layer based on an FPGA compute-NIC datapath, enabling metadata-driven KV routing and collective operations directly in the network path. Experiments show that MCF improves TTFT, throughput, and scalability over state-of-the-art distributed inference systems, with larger benefits as context length and system scale grow.

# Excerpts / key facts (from PDF)

- Authors: Huaizhi Zhang, Jiacheng Zhu, Xuqi Zhu, Junkyu Lee, Klaus McDonald-Maier, Xiaojun Zhai (University of Essex).
- MARS: early prefill temporary replicate high-reuse KV; mid prefill drain replicas; end prefill converge to owner-only shards (decode-ready) without bulk migration.
- Decode: KV-stationary; exchange lightweight query / online-softmax partial states; NIC reduction merges max/sum.
- Hardware: AMD-Xilinx KR260 FPGA cluster; compute core + packetization + metadata-driven NIC (multicast / all-to-all / reduce); ARM only for init + MARS control.
- Model: Qwen2.5-1.5B benchmark.
- 16K prefill Table 1: MARS TTFT N=2 **1.68 s** → N=16 **0.62 s**; at N=16 Ring **1.91 s** / Zigzag **1.81 s** → ~**3.1× / 2.9×**; MCF comm volume N=16 **5.12 GiB** (slightly higher than streaming baselines).
- Prefill TTFT up to 8K: MCF lowest vs Ring / Zigzag / PD disaggregation (flatter curve).
- Decode throughput: 4×KR260 cluster **17.3 token/s** on Qwen2.5-1.5B.
