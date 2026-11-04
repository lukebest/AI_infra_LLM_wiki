---
type: Raw Source
title: "NORmal: Architecting 3D Ferroelectric NOR Flash as Main Memory — From Co-Fabricated BEOL Arrays to 200B-Class Multi-Agent LLMs in a Smartphone"
source_url: https://arxiv.org/abs/2610.40000
pdf: NORmal_3D_FeNOR_LPDDR6_Main_Memory_2026.pdf
retrieved: 2026-11-04
ingested: 2026-11-04
org: Peking University / IME CAS / HKUST-GZ
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2610.40000)

Smartphone agents increasingly work as teams, in which a large planner directs parallel workers across long sessions. Running such a team on the device requires 200B-class models and contexts that exceed phone DRAM many times over, yet existing tiers treat flash as storage: UFS starves per-token weight streaming, and mobile High-Bandwidth Flash (HBF) needs a redesigned SoC and cannot absorb continuous KV writes. We show that a non-volatile memory can join an unmodified LPDDR6 bus as a plain rank only if its access latency fits the DRAM timing window, a condition no NAND tier meets. We present NORmal, to our knowledge the first main-memory architecture for 3D ferroelectric NOR flash. We have fabricated and experimentally characterized back-end-of-line (BEOL) 3D FeNOR arrays that co-integrate dense 3-bit MLC and fast, high-endurance in-place-writable SLC with sub-7.5 ns sensing. NORmal turns these co-fabricated arrays into a byte-addressable, deterministic-timing load/store rank on an unmodified LPDDR6 interface through an under-array DRAM-emulation bridge, staggered bank reads with zero-cycle weight swizzling, and posted SLC writes. Across this rank and DRAM, NORmal places agent state by mutability and lifetime rather than by hotness, serving 200B-class models and persistent planner contexts in place while dynamically partitioning subchannels across agent phases. In serving-level simulation on production agent traces, NORmal is 8.9×–28.0× faster than UFS offloading, within 0.4% of an unlimited-DRAM ideal, and 2.8×–6.3× faster than HBF on sessions beyond 256K tokens, with 8.1×–17.8× less memory energy per token.

# Excerpts / key facts (from HTML/PDF)

- Authors: Zhuoran Li, Chen Gu, Zhuohang Bian, Haochen Yu, Yibo Zhao, Xuxiao Yang, Youwei Zhuo (PKU / IME CAS / HKUST-GZ).
- Fabricated BEOL 3D FeNOR: sub-7.5 ns sensing; co-fab 3-bit MLC + in-place SLC; unmodified LPDDR6 rank (153.6 GB/s shared).
- Capacity on shared bus: MLC 49–197 GB; SLC 4–24 GB.
- Lifecycle placement: MLC weights; SLC planner KV; DRAM worker KV; adaptive subchannel allocation.
- vs UFS offloading: **8.9×–28.0×** faster (agent team **21.4×**); within **0.4%** of unlimited-DRAM ideal (>99.6% throughput).
- vs HBF on sessions >256K tokens: **2.8×–6.3×** faster; memory energy/token vs HBF: **8.1×–17.8×** less.
