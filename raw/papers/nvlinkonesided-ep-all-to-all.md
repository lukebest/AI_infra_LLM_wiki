---
type: Raw Source
title: "One-Sided Expert-Parallel All-to-All for Mixture-of-Experts Inference over NVLink"
source_url: https://arxiv.org/abs/2611.13188
pdf: NVLinkOneSided_EP_AllToAll_2026.pdf
retrieved: 2026-11-13
ingested: 2026-11-13
org: NVIDIA
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.13188)

Expert parallelism (EP) shards the experts of a Mixture-of-Experts (MoE) layer across GPUs, so every MoE layer requires two all-to-all communications, namely dispatch and combine. Compared with training, inference processes relatively few tokens per GPU at a time, and at small batch sizes fixed costs that do not grow with the number of tokens, rather than data movement, dominate the latency. We present NVLinkOneSided, a one-sided EP all-to-all for GPUs within a single NVLink domain. Each source rank pushes its tokens, without first exchanging metadata, into rank-major buffers on the target GPUs, and the grouped GEMMs read them in place instead of from a per-expert copy. We provide two protocols for the synchronization that the communication requires, namely Fence and Sentinel, for high-throughput and low-latency scenarios respectively. On Blackwell GPUs, NVLinkOneSided completes dispatch and combine 1.2–3.0× faster than DeepEP, with the largest speedups at small batch sizes. The resulting MoE layer is up to 2.4× faster than DeepEP with DeepGEMM. It even outperforms the fused DeepGEMM MegaMoE at up to 128 tokens per GPU, making it still competitive for decoding. We expose NVLinkOneSided through a modular interface, so that it is agnostic to the activation quantization format, decoupled from the MoE compute backend and easy to integrate into inference frameworks.

# Excerpts / key facts

- Authors: Bo Li, Chulian Zhang, Or Biri, Anthony Chang, Anton Korzh, Noam Duvdevani, XingFei Xi, Daniel Stokes, Zhenhuan Chen, Ludwig Schneider, Artem Y. Polyakov, Julien Demouth, Chandler Zhou (NVIDIA). Correspondence: lbo@nvidia.com, chulianz@nvidia.com. arXiv:2611.13188, submitted 9 Nov 2026, cs.DC. Marked Preprint. PDF and abstract do not name a conference.
- Platform (§5.1): 8× NVLink-connected B300 for §5.2–5.3; one GB200 NVL72 rack for large EP (§5.4). DeepSeek-V4.1-Flash (384 experts, top-k=6, hidden 5120, MXFP8 dispatch 5328 B / BF16 combine 10240 B) and Kimi-K3 (896 experts, top-k=16, hidden 3584, latent MoE with original hidden 7168) (Table 3). Perfect routing unless Zipf. Tokens per rank 1–4096. Ours: NVLinkOneSided + Prims-TS grouped GEMMs, MXFP4 weights, MXFP8 activations. Baselines: DeepEP V2.5; DeepGEMM MegaMoE (one persistent fused kernel); DeepEP + DeepGEMM (DE+DG).
- Mechanism: one-sided push into rank-major peer buffers with only local routing; no prior metadata exchange. Fence (serial flags, high-throughput) vs Sentinel (arrival detected from data, low-latency). CUDA graph + PDL. Rank-major layout lets grouped GEMMs read in place.
- All-to-all (§5.2 / Fig 5): faster than DeepEP at every batch; **1.75–3.00×** up to 128 tokens/rank, **1.17–1.63×** from 256. Abstract states **1.2–3.0×**. At 1 token, DeepSeek-V4.1-Flash round trip: Sentinel **17.4 µs**, Fence **27.6 µs**, DeepEP **47.9 µs**. Crossover Sentinel/Fence at 256 tokens/rank. At 4096 tokens Fence reaches **68–71%** of 900 GB/s unidirectional NVLink. NVFP4 dispatch at 4096 tokens **3.0×** vs BF16 (byte ratio 3.5×); MXFP8 **1.8×** (byte ratio 1.9×) (Fig 7).
- MoE layer (Table 4, 8×B300): vs DE+DG faster at every batch, up to **2.4×** (Kimi-K3 T=1: Sentinel **42.1 µs** vs DE+DG **99.7 µs**, 2.37×). vs MegaMoE faster up to 128 tokens/rank, “by up to 30%” (latency reduction; Kimi T=1 MegaMoE **60.4 µs**). From 256 tokens MegaMoE leads, by up to **35%** at 4096 (DeepSeek 766.1 vs Fence 1185.2 µs).
- Zipf (Table 5): at T=1024, α=1.25, busiest-rank dispatch+combine DeepSeek **160 and 135 µs** vs DE+DG **267 and 400 µs** (body text).
- NVL72 (Fig 8 / Table 6): Sentinel DeepSeek T=1 stays **16.6–17.8 µs** from 8 to 64 GPUs; Fence 43.0→47.6 µs. Layer at T=128 on 64 GPUs: Ours **102.6 µs** vs 8 GPU **181.7 µs** (body: 103 vs 182).
- Integration (Conclusion): available in FlashInfer3; integrated into vLLM, SGLang, TensorRT-LLM. Limitation (§6): EP group must fit one NVLink domain (direct loads/stores and whole 32-bit words).
