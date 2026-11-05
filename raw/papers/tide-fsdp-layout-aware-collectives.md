---
type: Raw Source
title: "TIDE: Zero-Copy Layout-Aware Collectives for FSDP2 (FSDP Endgame)"
source_url: https://arxiv.org/abs/2610.38228
pdf: TIDE_FSDP_Layout_Aware_Collectives_2026.pdf
retrieved: 2026-11-05
ingested: 2026-11-05
org: KlingAI Research / Kuaishou
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2610.38228)

Fully Sharded Data Parallelism (FSDP2) maintains parameters and gradients as per-parameter tensors, whereas its collective path operates on flat, rank-major buffers. Converting between these layouts copies all-gather outputs into parameter storage and packs gradients into full-group fp32 buffers. Layout conversion alone accounts for 6.4% of step time in Llama-3.1 70B training at 8K tokens per GPU. Communication kernels impose a second cost: a default NCCL reduce-scatter can slow a concurrent GEMM that would otherwise complete in a single wave by 69%. We present TIDE, a set of zero-copy collectives built on public NCCL 2.31+ APIs. TIDE preserves FSDP2’s per-parameter storage and compute kernels while folding layout placement into collective addressing. TIDE-AG delivers shards directly to parameter storage using NVSwitch multicast and paced recursive-doubling RDMA, with no SMs used for transport or placement. TIDE-RS consumes per-parameter bf16 gradients directly and reduces them into fp32 shards—a mixed-precision mode that NCCL does not provide—using copy engines and short-lived thread blocks (CTAs) for node-local accumulation and NVSwitch for cross-node reduction. A two-phase pipeline separates gradient reads from network progress; Slot-Reuse optionally stages gradients in vacated all-gather slots. On 64 GPUs, TIDE reduces step time by up to 27.1% relative to Stock FSDP2 and 6.0% relative to FSDP2+SymmMem across Llama-3.1 70B, Wan2.2, and Qwen3-30B-A3B. It reduces reduce-scatter SM time by factors of 12.5–14.5 and cuts interference with concurrent compute by up to an order of magnitude.

# Excerpts / key facts

- Authors: Zejian Wang et al., KlingAI Research / Kuaishou.
- Layout 转换 alone：Llama-3.1 70B @ 8K tok/GPU 占 step **6.4%**；默认 NCCL RS 可把单波 GEMM 拖慢 **69%**。
- 64 GPU：step 相对 Stock FSDP2 最高 **−27.1%**，相对 FSDP2+SymmMem **−6.0%**；RS SM 时间 **12.5–14.5×** 更少。
- 缓冲：backward 约 **3.72𝑁𝑆**（In-Place）/ **2.29𝑁𝑆**（Slot-Reuse）；可比 SymmMem 少约 **4.7 GiB**。
