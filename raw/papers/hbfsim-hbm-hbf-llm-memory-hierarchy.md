---
type: Raw Source
title: "HBFSim: A Simulator for Exploring HBF in Memory Hierarchies for LLMs"
source_url: https://arxiv.org/abs/2610.23503
pdf: HBFSim_HBM_HBF_LLM_Memory_Hierarchy_RACS26.pdf
retrieved: 2026-10-20
org: MBZUAI
venue: RACS ’26 (Fukuoka, 2026-11-17–20); arXiv cs.AR v1 2026-10-16
---

# Abstract (verbatim, arXiv:2610.23503)

High Bandwidth Flash (HBF) has recently emerged as a promising technology that provides terabyte-scale accelerator-local capacity at bandwidths approaching HBM, with a potential cost-per-bit advantage over HBM. However, its NAND foundation brings long latency, out-of-place updates, and finite write endurance directly into the accelerator memory hierarchy, making its effects on performance and lifetime difficult to predict. To study this emerging design space, we present HBFSim, an LLM-aware event-driven simulator for heterogeneous HBM+HBF memory systems that preserves application-level memory semantics while modeling flash-internal behavior. HBFSim models HBM, HBF with host-managed flash translation, and conventional capacity tiers in one simulation driven by a calibrated serving frontend. Using HBFSim, we study decoding of Llama-3.1-70B and Qwen3-235B-A22B under three workloads that differ in their input and output lengths. HBF serves data that does not fit in HBM 11.0--19.0$\times$ faster than host DRAM; HBM is better used to hold the running sequences' KV cache than as a cache for HBF; and at a published peak load of Llama-3.1-70B, HBF lasts 2.0 to 6.9 years, in proportion to the stacks that share the KV writes. The artifact is available at (artifact URL in arXiv abstract) and will track public HBF device data as it becomes available.

# Excerpts (from arXiv PDF v1)

- "HBM4 stack, 48 GiB 2.0 TB/s 42 ns read; HBF stack, 512 GiB 1.5 TB/s 4 µs read, 75 µs program; Host DRAM, PCIe 5.0 54 GB/s 9.3 µs per transfer (measured); CXL SSD 36 GB/s link 40 µs NAND read, 6.6 GB/s NAND; NVMe SSD 16 GB/s link (Table, modeled devices)"
- "Takeaway 1: HBF is most valuable under memory-capacity pressure. It offers little benefit when the working set fits in HBM, but substantially outperforms offloading to CPU memory, CXL SSDs, and NVMe SSDs once spilling occurs"
- "Takeaway 4: HBF mapping should preserve internal parallelism rather than maximize address granularity. ... An extent mapping that stripes each run across all planes matches a page-level table at a fraction of its memory, whereas a block-level mapping that keeps each block on a single plane serializes its page reads and slows decoding considerably."
- "Takeaway 5: HBF endurance is a first-order system constraint. Under baseline inference workloads, KV spill generates enough writes to make projected HBF lifetime a major challenge even when performance is acceptable."
- "Assuming 100,000 P/E cycles, as for the SLC NAND used in HBF ... HBF lasts 2.0 to 6.9 years"
