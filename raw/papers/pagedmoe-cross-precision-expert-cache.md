---
type: Raw Source
title: "PagedMoE: Cross-Precision Expert Caching for Token-Level Dynamic Precision in SSD-Resident MoE Inference"
source_url: https://arxiv.org/abs/2611.03173
pdf: PagedMoE_Cross_Precision_Expert_Cache_2026.pdf
retrieved: 2026-11-04
ingested: 2026-11-04
org: Tsinghua University
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2611.03173)

Large Mixture-of-Experts (MoE) models are promising for local inference because sparse routing allows the routed-expert pool to reside on SSD while DRAM caches recently used experts. However, under practical DRAM cache capacities, substantial SSD I/O remains on the critical path despite I/O–computation overlap. Token-level dynamic expert precision offers a natural way to reduce this data demand by allocating bits according to expert importance and quantization sensitivity. Nevertheless, treating each bit-width of the same expert as an independent object prevents cross-precision cache reuse, causing overlapping data to be fetched repeatedly. The key insight is that precision should instead denote the refinement depth of one shared expert state. Based on this insight, we present PagedMoE, which stores each expert once using a prefix-compatible tree codebook and bitplane layout. Lower-precision representations are valid prefixes of higher-precision ones, allowing cached data to be reused or extended by fetching only missing bitplanes. PagedMoE selects the required prefix length before I/O using current routing weights and offline expert-specific error profiles, and directly executes cached 1–8-bit prefixes without materializing full-precision experts. At an average routed-expert precision of 2.5 bits, PagedMoE achieves quality close to GPTQ-INT4 on Qwen3.5-397B-A17B and to MXFP4 on most evaluated GLM5.2 tasks. With a 24 GiB expert cache, it reaches 8.89 tokens/s on Qwen3.5, 1.33× the throughput of the same dynamic requests using independent precision objects and 1.56× that of uniform 4-bit execution.

# Excerpts / key facts (from HTML/PDF)

- Authors: Yutong Lin, Yingdi Shan, Shaoyuan Chen, Yuanyong Chen, Yongwei Wu, Mingxing Zhang (Tsinghua).
- Tree codebook + bitplane layout; prefix-compatible cross-precision reuse; pre-I/O allocator; direct CPU GEMV of prefixes.
- Avg **2.5-bit** routed experts: quality close to GPTQ-INT4 (Qwen3.5-397B-A17B) / MXFP4 (most GLM5.2 tasks).
- 24 GiB expert cache: **8.89 tok/s** on Qwen3.5; **1.33×** vs independent precision objects; **1.56×** vs uniform 4-bit.
