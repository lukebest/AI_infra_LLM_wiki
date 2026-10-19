---
type: Raw Source
title: "Top-Down Microarchitecture Analysis Without Causal Modelling Is Dangerous!"
source_url: https://arxiv.org/abs/2610.21387
pdf: Causal_Top_Down_Microarchitecture_Analysis_2026.pdf
retrieved: 2026-10-19
org: ICT CAS; BenchCouncil (Technical Report BENCHCOUNCIL-CTMA-2026)
venue: arXiv cs.PF (submitted 2026-10-15)
---

# Abstract (verbatim, arXiv:2610.21387)

Top-Down Microarchitecture Analysis (TMA) is the standard for identifying CPU bottlenecks. However, TMA implicitly models performance via a single causal path: Workload(dataset, algorithm) => CPU(CPI) => System(Performance) (microarchitectural efficiency path). It overlooks two hidden causal paths: Workload(dataset, algorithm) => Instructions(Retired) => System(Performance) (algorithmic efficiency path) and Workload(dataset, algorithm) => Instructions(Retired) => CPU(CPI) => System(Performance) (microarchitecture-algorithm efficiency path). This causal blindness often misleads architects into futile hardware optimizations. To address this, we propose Causal Top-Down Microarchitecture Analysis (CTMA). Utilizing the object causal model, CTMA explicitly models these three causal paths among the workload, instructions, CPU, and system. We validate CTMA across Intel, AMD, and ARM platforms. Our experiments reveal counterintuitive insights: (1) CPI Profiling Blindness: Algorithmic instruction bloat can double elapsed time while the CPI profile remains frozen. (2) Over-Speculation Congestion: Throttling the Frontend paradoxically improves performance in pointer-chasing algorithms. (3) ILP Window Collapse: Extreme data topologies shift bottlenecks from Backend ROB capacity to Frontend fill-rate starvation. (4) Op-Cache SMT Overlap: Ultra-small footprints yield SMT speedups on Intel but cause severe thrashing on AMD. (5) "Ghost State" Artifact: Stale pipeline mitigations on Intel Xeon Gold 5120T artificially boost performance by 22.75% on SPEC CPU2017 and 42.2% on SPEC CPU2026. Based on this, we propose a dynamic speculation throttling mechanism.

# Excerpts (from arXiv PDF v1)

- Platforms: Intel Xeon Gold 5120T (Skylake-SP), AMD EPYC 7543 (Zen 3), ARM Kunpeng 920 (Taishan 110 / ARMv8).
- CPI Profiling Blindness (leela_r): changing dataset spatial locality causes >100% elapsed-time variation while CPI profile stays frozen; cross-ISA validation shows 2.06× instruction inflation.
- Over-Speculation Congestion (mcf_r): highly regular data improves branch prediction but halves performance; aggressive speculation overflows Line Fill Buffers and congests the memory controller; injecting NOPs to throttle the pipeline slightly improves performance.
- ILP Window Collapse (cactuBSSN_r): SMT-based ROB partitioning (pause process) degrades perfect-topology datasets ~23% (Intel) / ~12% (AMD) vs distorted datasets ~9% / ~10% → bottleneck shifts from ROB capacity to frontend fill rate.
- Op-Cache SMT Overlap (xalancbmk_r): tiny recursion footprint fits Intel DSB → SMT speedup; AMD Zen3 >50% degradation (rigid op-cache sharing).
- Ghost State (Xeon Gold 5120T): kill -9 of an SMT sibling without OS-level microarchitectural flush leaves pipeline in aggressive state: average 22.75% artificial boost on SPEC CPU2017, 42.20% on SPEC CPU2026; linked to Spectre v2 mitigation toggles.
- Proposes (as recommendation) a dynamic speculation throttling mechanism for online congestion control; open-sources SPEC CPU2017 workload configuration treatment tools.
