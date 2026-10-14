---
type: Raw Source
title: "Ember: Making Unified Virtual Memory Practical for Discrete-Memory GPUs"
source_url: https://arxiv.org/abs/2610.13408
pdf: Ember_UVM_Oversubscription_Discrete_GPU_2026.pdf
retrieved: 2026-10-14
org: Technical University of Munich
venue: arXiv preprint (cs.OS / cs.DC)
---

# Abstract (verbatim, arXiv:2610.13408)

GPU working sets have outgrown GPU memory, so applications must oversubscribe it, keeping only hot data on the GPU. NVIDIA's Unified Virtual Memory (UVM) supports oversubscription, but its performance degrades once data exceeds the GPU's memory. This stems from its fault-driven data placement, wasting interconnect bandwidth, and underutilizing the GPU. This raises the question: can UVM oversubscription become practical on stock GPUs, exploiting GPU memory speed and minimizing wasted interconnect bandwidth, without placement hints, profiling runs, or application changes?
To this end, we present Ember, a UVM management framework for oversubscribed workloads. Ember introduces a hybrid address space; allocations start as mapped into host memory, omitting data migration. Ember's counter-driven region promotion uses GPU's hardware counters to fetch hot regions to the GPU, its decay-based eager reclamation proactively evicts cold regions in batches, while via online region re-placement, Ember tracks the hot set at runtime.
We implement Ember within NVIDIA's open-source UVM driver for unmodified applications and as a userspace variant on stock CUDA. At 1.5x oversubscription, it is 6.8-10.6x faster than UVM on six applications across three PCIe GPUs, and generates LLM tokens 4.7-16x faster at sizes where manual placement cannot run at all. Without a profiling run, it beats a profile-guided alternative by 2.1x on kernel time.

# Excerpts (from arXiv HTML v1)

- Table 2 platforms: RTX 5080 16 GiB GDDR7 / PCIe 5.0 x16 (~15x gap); A40 48 GiB GDDR6 / PCIe 4.0 x16 (~22x); H200 141 GiB HBM3e / PCIe 5.0 x8 (~150x); GH200 96 GiB HBM3 / NVLink-C2C (~9x). Gap = device-memory-to-interconnect bandwidth ratio.
- §2.3: NVIDIA GPUs expose roughly 256 hardware access counters that count accesses to host-resident memory; crossing a threshold writes a notification without stalling the GPU. The driver does not migrate on them by default and discards notifications with 4 KiB OS pages.
- §5.3 reclamation: background worker every 25 ms halves each root chunk's demand; above 90% occupancy evicts down to 85%; at most 16 chunks per pass; a block returning within 500 ms of eviction gets a migration score (+1 per 2 MiB, halves every second).
- §7.3: while data fits, Ember-static mean 1.9–3.0x over stock UVM (Prefetch 1.3–2.3x, UVM-mapped 0.3–0.5x).
- §7.4 LLM (llama-bench, 512-token prompt + 128 generated, Qwen2.5 14B and Qwen3 32B, GPUs capped at 16 GB): at 1.41x oversubscription stock UVM and prefetching fall to 0.2–0.5 tokens/s; Ember-static 4.7x (RTX 5080) and 8–13x (A40, H200); Ember-adaptive 3–10x; UVM-mapped 2.5–4.8x over UVM; no strategy exceeds 3 tokens/s.
- §7.6 GH200 (Ember-static only): geomean gain over UVM ~3.5x at both footprints (PCIe: 6.8–10.6x); LLM 128 tokens in 62 s vs 211 s for UVM-mapped; UVM-mapped wins on read-once workloads (pathfinder, radix sort).
- §7.7: Ember-adaptive beats HELM on all five benchmarks by mean 7.9x end-to-end (HELM profiling 39–1449 s, 18–95% of its runtime); kernel time alone mean 2.1x, up to 28.0x, slower on bfs and gramschm.
- §8: places only cudaMallocManaged memory; Ember-adaptive needs a kernel module (bare metal); single GPU + host only, multi-GPU peer tier left open.
