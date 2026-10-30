---
type: Raw Source
title: "uGDS: A User-Space Development Kit for High-Performance GPU Direct Storage"
source_url: https://arxiv.org/abs/2610.30868
pdf: uGDS_UserSpace_GPU_Direct_Storage_2026.pdf
retrieved: 2026-10-30
ingested: 2026-10-30
org: ScaleX-IO / HKUST (Guangzhou)
venue: arXiv cs.DC (2026-10)
---

# Abstract (verbatim, arXiv:2610.30868)

Data-intensive GPU applications, including LLM KV-cache offloading, vector search, and large-scale analytics, increasingly rely on NVMe SSDs to extend limited GPU memory capacity and support on-demand data movement. As models and datasets continue to grow beyond GPU memory capacity, efficiently transferring data between SSDs and GPUs has become critical to application performance. NVIDIA GPU Direct Storage (GDS) enables direct data transfers between NVMe SSDs and GPU memory through PCIe peer-to-peer DMA, eliminating intermediate copies through host memory. However, removing host staging alone does not eliminate software overheads or provide the flexibility required by diverse GPU workloads. Three key limitations remain: (1) the control path still traverses the kernel for every I/O request, introducing unnecessary software overhead; (2) stream-ordered I/O path incurs significant overhead and enforces a total order even when applications require ordering only at batch granularity; and (3) closed-source user-space I/O engine limits performance diagnosis and prevents applications from adapting I/O scheduling to their access patterns.

We present uGDS, an open-source user-space GPU Direct Storage library built on four principles: user-space control, a unified abstraction across GPU vendors, flexible workload-aware scheduling, and performance and debuggability that both follow from keeping I/O in user space. The host CPU constructs NVMe commands, manages hardware queues, and handles completions entirely in user space, while payloads move directly between SSDs and GPU memory through PCIe peer-to-peer DMA. A lightweight kernel helper (ugds_drv.ko) is used only for one-time privileged setup. Keeping I/O initiation on the CPU matches how GPU applications already manage data movement and consumes no GPU compute. uGDS partitions hardware queues between synchronous and batch traffic, tracks in-flight DMA so that no buffer is released while the SSD may still access it, and exposes cuFile-style synchronous, batched, and stream-ordered asynchronous APIs with polling or interrupt-driven completion on both NVIDIA CUDA and AMD HIP. On an A100 with a Samsung 990 PRO, uGDS achieves up to 12.12× GDS’s batch-read bandwidth and 30.69× its batch-write bandwidth (8- and 4-KiB requests, batch size 128), and reduces 4-KiB synchronous write latency by 84.1% with two issuing threads. Its stream-ordered path sustains device bandwidth on a single stream (5.49 GiB/s), where GDS retains only 40.8% of its synchronous bandwidth. In LMCache, uGDS reduces median time-to-first-token by up to 62.7% and raises serving goodput by 2.63×. On AMD, uGDS achieves up to 1.19× hipFile’s synchronous-write bandwidth.

# Excerpts / key facts (from PDF)

- Authors: Jing Wei, Guanyi Chen, Qi Chen, Chuyu Zhang, Zheng Zhou, Chutian Wang, Jian Zhang (ScaleX-IO / HKUST Guangzhou).
- Path: CPU user-space builds NVMe cmds / queues / completions; payload SSD↔GPU via PCIe P2P DMA; ugds_drv.ko only for one-time privileged setup.
- Microbench (A100-SXM4-40GB + Samsung 990 PRO PCIe Gen4×4): batch R/W vs GDS up to **12.12× / 30.69×** (8-/4-KiB, batch 128); 4-KiB sync write latency **−84.1%** (2 threads); stream-ordered single stream **5.49 GiB/s** vs GDS **40.8%** of sync BW (**2.33×**).
- LMCache: median TTFT **−62.7%** (32K tokens: 1915→715 ms); goodput **2.63×**; AMD vs hipFile sync-write up to **1.19×**.
- APIs: cuFile-like sync / batched / stream-ordered async; CUDA + HIP.
