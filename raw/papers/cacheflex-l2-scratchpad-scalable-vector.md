---
type: Raw Source
title: "CacheFlex: Direct Software-Managed Access to Higher-Level Cache for Scalable Vector Support"
source_url: https://arxiv.org/abs/2610.12940
pdf: CacheFlex_L2_Scratchpad_Scalable_Vector_2026.pdf
retrieved: 2026-10-13
org: University of Washington / Rutgers University
venue: MICRO 2026 (to appear)
---

# Abstract (verbatim, arXiv:2610.12940)

Wider vector/SIMD lanes multiply compute throughput, but cache improvements remain challenging. We identify L1 data cache capacity as the most impactful parameter for performance and efficiency. L1 capacity is constrained by pipeline coupling and latency requirements; private L2 offers an order of magnitude more capacity but is inaccessible from software. This work proposes CacheFlex, an ISA and microarchitecture co-design that enables software-managed, direct access to private L2 SRAM by allowing runtime conversion of parts of L2 into a scratchpad memory (SPM). Through a lightweight ISA extension, software explicitly controls data placement and lifetime within the L2. CacheFlex integrates into an out-of-order pipeline with cross-domain memory consistency and OS context-switch support, with merely 2.02% area overhead relative to the L2 in a post-layout 12 nm implementation. We prototype CacheFlex based on the Armv8-A SVE ISA, model it in gem5, and evaluate it using optimized general matrix multiplication (GEMM) kernels with diverse model-derived shapes, FlashAttention-based fused attention, and full-layer workloads from LLaMA-3.2-1B and BERT-Base in the prefill phase. As the vector length (VL) scales from VL = 4 (512-bit) to VL = 16 (2048-bit), CacheFlex's kernel-level geometric-mean speedup and memory-subsystem energy reduction grow from 1.12x and 26% to 1.44x and 40%, respectively, bridging the widening gap between per-instruction data demand and memory performance. On full transformer layers combining CacheFlex with FlashAttention, the design delivers up to 1.78x speedup and 45% memory-subsystem energy savings (BERT-Base, sequence length T=4096, VL = 16; LLaMA-3.2-1B: 1.64x and 38%). CacheFlex is complementary to hardware prefetching, and its benefit grows as vector width and peak compute throughput increase for compute-intensive AI kernels.
