---
type: Raw Source
title: 'CosMoS: Architectural Support for Cost-Effective Data Movement in a Disaggregated Memory Systems'
source_path: /home/luke/wiki/raw/papers/CosMoS_Disaggregated_Memory_Data_Movement_2025.pdf
doi: '10.1145/3725218'
zotero: IY9N6IMG
ingested: 2026-07-17
sha256: df8336aa6a90cbd3a0331d9009bfa66cccdbe8ab42ecc6122dc54647021128fb
---

# CosMoS: Architectural Support for Cost-Effective Data Movement in a Disaggregated Memory Systems

Authors: Amit Puri, John Jose, Venkatesh Tamarapalli (IIT Guwahati)
Venue: ACM JETCAS 2025 | DOI: 10.1145/3725218

Structured notes / key excerpts:

- **DMS context**: Compute nodes with small local DRAM + CXL/RDMA remote memory pools; remote latency ~3–4× local (**170–250 ns** CXL vs local).
- **Page migration cost**: 4KB page move **1.2–1.5 µs**; can help if truly hot but blocks critical-path cache misses if poorly scheduled.
- **Problems with OS/software migration**: Inaccurate hot-page prediction → ping-pong; no scheduling for multi-node DMS; page fetch obstructs other remote cache misses.
- **CosMoS**: Hardware hot-page prediction + scheduled migration + early response; protects regular cache-line remote accesses on critical path.
- **DMS model**: Distributed (not shared) remote memory reservation; per-compute-node remote memory controller.
- **Results**: **+20%** vs state-of-the-art; **+86%** vs no-migration baseline (large-scale DMS simulator, data-centric workloads).
- **Characterization**: Pages vary widely in access frequency; rolling average re-access frequency stable over page lifetime (except hpcg).
