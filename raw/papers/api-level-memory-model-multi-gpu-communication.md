---
type: Raw Source
title: "A New Lens on Multi-GPU Communication: API-Level Memory Models for Portable Optimization"
source_url: https://arxiv.org/abs/2610.16190
pdf: API_Level_Memory_Models_Multi_GPU_Communication_2026.pdf
retrieved: 2026-10-15
org: AMD
venue: arXiv preprint (cs.DC)
---

# Abstract (verbatim, arXiv:2610.16190)

As network communication increasingly becomes a performance bottleneck for ML and HPC workloads, it is more important than ever to optimize multi-GPU data transfers. Recently, low-level device APIs have emerged that allow programmers to perform fine-grain optimizations via one-sided put/get operations triggered directly from the device. However, the communication libraries providing these device APIs (e.g., rocSHMEM, MSCCL++, and NCCL/RCCL GIN) currently lack a rigorous memory model defining how their primitives interact with the underlying memory systems. Without this, emerging HPC and ML workloads aggressively optimizing network communication via device APIs can be brittle, error-prone, and face compatibility and inter-operability challenges. This paper proposes the use of API-level memory models for these emerging device communication APIs. An API-level memory model defines the memory semantics of communication API calls in a way that abstracts lower-level details from the API user and simplifies development. This work defines one such model for device-side communication (implemented in AMD's recently open sourced rocSHMEM library) and demonstrates how formal relaxations to such a model can enable low-level LLM performance optimizations while retaining a well-defined standardized interface. Specifically, we describe how updating the SHMEM API implemented by rocSHMEM can properly support cache bypassing for network data, improving performance of a collective communication workload by up to 2.48x, a fused compute+communication workload by up to 1.77x, and a state-of-the-art expert-parallel communication workload by up to 1.18x.

# Excerpts (from arXiv PDF v1)

- Authors: Alsop, Beckmann, Potter, Yan, Bouteiller, Mor, Tye, Sahasrabuddhe (AMD).
- §III–V: formal API-level memory model for SHMEM device API on top of PL-level (scoped HRF-style) GPU model; relations ilv, lco, rdo, rco, aso, hb_api; ambiguities identified in SHMEM spec and NCCL/RCCL GIN; validated with litmus tests (MP, SB, LB, IRIW, WRC, CoWW, ISA2).
- §IV: GPU SHMEM implementation needs acquire/release (system scope) in fence/wait_until, which lower to cache flush/invalidate.
- §VI targeted ordering: new com_id property per operation/access/allocation; relations defined per com_id; if all data of a com_id uses cache-bypassing loads/stores, acquire/release need no flush/invalidate (only waitcnt).
- §VII: implemented in rocSHMEM IPC backend (intra-node xGMI) and GDA backend (GPUDirect Async, inter-node InfiniBand); nodes with eight AMD Instinct MI300X GPUs; workloads RS, fused GEMM+RS, DeepEP (DeepSeek 7K embedding, 64–256 tokens/GPU).
- §VIII: RS up to 2.48× (IPC), both saturate ~220 GB/s per GPU (~50% of theoretical peak) at large sizes; GEMMRS up to 1.77×; DeepEP 10–20% for most token counts, max 1.18× (IPC and GDA) at low token counts.
