---
type: Raw Source
title: "KVStream: Adaptive Parallel Storage Management for KV Caching in Large-Scale LLM Serving"
source_url: https://arxiv.org/abs/2610.31827
pdf: KVStream_Parallel_Storage_KV_Cache_2026.pdf
retrieved: 2026-10-27
org: Argonne National Laboratory; Rochester Institute of Technology; Illinois Institute of Technology
venue: arXiv cs.DC (2026-10)
---

# Abstract (verbatim, arXiv:2610.31827)

Long-context LLM serving for agentic, coding, and document workloads reuses prefixes whose key-value (KV) cache outgrows GPU and host memory, putting storage I/O on the critical path of the inference step for retrieving prefixes. A single node-local NVMe absorbs all retrievals, while the parallel file system or cloud file store that nodes already mount carries almost no inference traffic. We cast prefix retrieval as aggregate-bandwidth scheduling across these tiers and present KVStream, a KV cache engine that batches a step's reads, defers writes behind the forward pass, replicates each chunk on every tier, and lets each tier adaptively claim the next unread chunks once it is free. Our performance model shows this routing attains the aggregate-bandwidth bound without prediction or tuning, whereas any static split misses it by a margin that grows as per-tier bandwidths drift or fluctuate. It also predicts that the time-to-first-token (TTFT) gain grows with load, as faster retrieval drains the queue, and disappears when host memory or arrival order keeps reuse in cache. Plugged into LMCache and evaluated on four models, six datasets, and up to 128 GPUs, KVStream retrieves within 5% of the bound, delivers up to 1.49x higher offline throughput than LMCache, and lowers mean TTFT by up to 6.1x under bursty arrivals.

# Excerpts / key facts (from PDF)

- Testbeds: 4×H100-80GB and 4×A100-40GB nodes; 2×1.6 TB NVMe RAID-0 node-local; PFS 4 PB VAST (Testbed-1) and 100 PB Lustre (HPE ClusterStor E1000, Testbed-2). vLLM v0.15.0, LMCache v0.3.14.
- Characterization: LMCache offload up to 2.2× faster than recomputing on H100 despite disk reads 6.2–13 GB/s; serving a dataset reads 5–32 TB (read amplification) for 32B/70B; retrieval is 80–88% of LMCache time.
- Node-local NVMe reads only 2.2× (Testbed-1) / 3.2× (Testbed-2) faster than PFS in isolation, yet PFS carries no inference traffic; concurrent R+W on one device 6% / 27% slower than isolated.
- Results: up to 1.49× offline throughput vs LMCache (3.22× vs recompute); mean TTFT up to 6.1× lower under bursty arrivals; retrieval within 5% of aggregate-bandwidth bound.
- Where it loses: 0.98–1.05× when host memory / arrival order keeps reuse in cache; 0.81× when reuse is sparse. Datasets have 81–96% prompt tokens hitting cached prefixes. Multi-path replication doubles storage footprint (per scope section).
- Releases kvsim, a trace-driven simulator.
