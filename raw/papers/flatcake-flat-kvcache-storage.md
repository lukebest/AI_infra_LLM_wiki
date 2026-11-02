---
type: Raw Source
title: "FlatCake: A Flat KVCache Storage Architecture for LLM Serving"
source_url: https://arxiv.org/abs/2610.38355
pdf: FlatCake_Flat_KVCache_Storage_2026.pdf
retrieved: 2026-11-02
ingested: 2026-11-02
org: Fudan / PKU / MetaX / ICT
venue: arXiv cs.DC
---

# Abstract (verbatim, arXiv:2610.38355)

KV cache reuse accelerates LLM serving, but existing systems manage host DRAM and NVMe SSD as a tiered hierarchy where DRAM acts as an intermediate cache. Production LLM workloads break both premises of this hierarchy. First, bimodal reuse defeats DRAM temporal filtering, since workloads are dominated either by one-shot blocks with long reuse distances or by multi-gigabyte agentic sessions that exceed DRAM capacity, putting SSD on the critical read path. Second, DRAM staging and eviction-ordered layout bottleneck SSD restoration. Holding host staging buffers for in-flight prefixes causes contention under load that aborts prefetches, while incremental eviction scatters a session's blocks across the SSD and prevents large sequential reads.

We present FlatCake, a flat KV storage architecture that exposes host DRAM and NVMe SSD as peer media in a unified 64-bit address space. Exploiting the fact that KV blocks are write-once, immutable, and reused at session scope, FlatCake places each block directly onto its target medium in session-contiguous, layer-major order at creation time and never migrates it. FlatCake streams coalesced SSD reads directly into a bounded GPU window via GPUDirect Storage and decouples DRAM and SSD request queues to prevent head-of-line blocking. On a production Claude Code trace with DeepSeek-V4-Flash, FlatCake sustains a 94% cache hit rate as load increases (versus 64% for Mooncake), eliminates Mooncake's 6.5×–6.7× SSD read amplification, and reduces peak-load mean TTFT by 1.6× while improving total token throughput by 1.6×. Across 8K–128K contexts on Llama-3.1-70B, FlatCake further reduces mean TTFT by up to 2.4× over Mooncake and 1.8× over Mooncake-GDS.

# Excerpts / key facts (from PDF)

- Authors: Xin Huang, Teng Ma, Zhuoran Li, Yibo Zhao, Zhaoshi Li, Qianchao Zhu, Wei Yang, Chenxi Wang, Tao Xie, Youwei Zhuo* (Fudan Institute of Systems for Advanced Computing; Independent; PKU School of Integrated Circuits; MetaX; ICT/CAS).
- Mechanisms: FC-GVA (64-bit global virtual address, write-once peer DRAM+SSD placement); FC-MAS (medium-aware dual queues); FC-CIO (coalescing GDS I/O into bounded GPU window); SGLang HiCacheStorage; session-contiguous layer-major layout; never migrates blocks.
- Claude Code prod trace + DeepSeek-V4-Flash on 8×B200: delivered hit rate **94.2–94.6%** under load (Mooncake **87.9%→64.3%**); peak-load mean TTFT **7.57 s** vs Mooncake **12.24 s** (**1.6×**); P50 **6.26 s** (**1.8×** vs Mooncake); throughput **98.3K** vs **61.6K** tok/s (**1.6×**).
- SSD: eliminates Mooncake read amp **6.5×–6.7×** (6.51×–6.72×); SSD BW **1.9×** (≈5.03 vs 2.69 GB/s at 1.0 QPS); prefetch latency **5.8×** lower at peak (Mooncake 9.50 s vs FlatCake ≈1.64 s).
- Llama-3.1-70B 8K–128K mean TTFT up to **2.4×** vs Mooncake, **1.8×** vs Mooncake-GDS.
