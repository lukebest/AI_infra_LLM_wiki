---
type: Raw Source
title: "M3D-FLOW: A Monolithic 3-D-Stackable Processing-Near-DRAM Architecture for Generative Normalizing Flow Applications"
source_url: https://arxiv.org/abs/2610.27371
pdf: M3D_FLOW_Monolithic_3D_PNM_Normalizing_Flow_2026.pdf
retrieved: 2026-10-22
org: Univ. of Kentucky; Colorado State University
venue: CASES 2026 (ESWEEK) / IEEE TCAD
---

# Abstract (verbatim, arXiv:2610.27371)

Normalizing Flows (NFs) have shown strong results in generative modeling, recently reaching state-of-the-art image generation performance. However, their repetitive, sequential operations limit the computational and memory efficiency achievable with GPUs and TPUs. We propose M3D-FLOW, a novel monolithic 3D-stackable (M3D) DRAM-based processing-near-memory (PNM) architecture that eliminates memory bottlenecks using a Cu-Cu hybrid-bonded logic die integrated with an M3D DRAM die. The M3D DRAM provides dense bank integration and a tiered organization with variable access latencies that M3D-FLOW exploits for the efficient processing of different NF workloads. To maximize compute density while minimizing area, energy, and thermal overhead, M3D-FLOW employs hybrid binary--stochastic floating-point multipliers, performing mantissa multiplication in the stochastic domain and exponent operations in the binary domain. A pipelined execution strategy maps sequential NF stages across dynamically partitioned PE groups, and together with the stochastic hardware, enables M3D-FLOW to achieve at least 6.6x higher performance and 3x better energy efficiency than prior PNM accelerators, with only a 2.2% bits-per-dimension (BPD) increase over bfloat16 and 4.1% over FP32. An analysis of stochastic hardware variants further shows that shorter stochastic bitstreams reduce execution time by up to 3.3x at the cost of higher approximation error, providing a concrete design guide for latency-accuracy trade-offs.

# Excerpts / key facts (from arXiv PDF v1)

- Stochastic mantissa multipliers: 13x less area, 46x less power than binary; stochastic adders 2.97x larger and 1.46x more power -> additions stay binary (VAE).
- M3D DRAM: 1024 layers partitioned into 8 latency tiers; critical data mapped to low-latency tiers. Hybrid-bond pitch ~1 um (cited background: up to 110,000 vias/mm2; 19-30 TB/s internal BW vs ~800 GB/s per HBM3 stack).
- PE = Multiplier Engine + Vector Adder Engine + Non-Linear Engine. NLE implements exp, GeLU, ln, reciprocal as single-cycle LUTs; ReLU via sign-bit mux; max via reduction tree; softmax = exp LUT -> reduction -> reciprocal LUT -> scale, all inside NLE. ME 61% / VAE 30% of PE power; inter-PE 128 GB/s.
- Baselines: AMD EPYC CPU, NVIDIA A100, TPUv7, 2DRAM-PNM, PNM-DDR, Stratum, NeuPIMs. Thermal: stays within safe DRAM temperature under full load (45 C ambient model).
- Bitstream 256 -> 2,048: 3.3x longer execution; 512 / 1,024-bit variants 1.2x / 1.7x; temperature largely unaffected.
