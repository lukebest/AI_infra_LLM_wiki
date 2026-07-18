---
type: Raw Source
title: 'PANDA: Adaptive Prefetching and Decentralized Scheduling for Dataflow Architectures'
source_path: /home/luke/wiki/raw/papers/PANDA_Adaptive_Prefetch_Dataflow_Architectures_2025.pdf
doi: '10.1145/3721288'
zotero: MFT988HQ
ingested: 2026-07-17
sha256: 2dbc7f906edac3a7e4c1530502f9e1b66807b072a037e82f2e77c3b6bcb13fa1
---

# PANDA: Adaptive Prefetching and Decentralized Scheduling for Dataflow Architectures

Authors: Shantian Qin, Zhihua Fan, Wenming Li, Zhen Wang, Xuejun An, Xiaochun Ye, Dongrui Fan (ICT CAS)
Venue: ACM TACO 2025 | DOI: 10.1145/3721288

Structured notes / key excerpts:

- **Problem**: Traditional dataflow uses SPM + centralized controller; prefetch-all-to-SPM fails on irregular/small data; centralized scheduling limits parallelism.
- **Insight 1**: Split **prefetchable** (stream/block-stride) vs **non-prefetchable** (irregular) data — different memory interfaces.
- **Insight 2**: PEs can **decentralized schedule** tasks (task stealing/migration) without central controller bottleneck.
- **On-chip memory**: Reconfigurable physical storage shared by SPM + cache (ISA-driven); application-adaptive partitioning.
- **PE microarchitecture**: Autonomous internal task scheduling + decentralized load balancing.
- **Evaluation** (Verilog impl): vs REVEL **2.53×**, Plasticine **1.90×**, DFU **1.38×**, MTDE **1.19×** geomean; up to **1.79×** energy efficiency.
- **Domains**: Scientific computing, AI, DSP, graph (BFS etc.).
