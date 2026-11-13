---
type: Raw Source
title: "Placing LLM Lookup Tables by Per-Layer Prefetch Deadlines"
source_url: https://arxiv.org/abs/2611.13413
pdf: SlackTier_Engram_Prefetch_Deadlines_2026.pdf
retrieved: 2026-11-13
ingested: 2026-11-13
org: Microsoft
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.13413)

DeepSeek-V4.1’s 203 GB of Engram n-gram tables sit in host DRAM today, taking 190 of the 223 GiB a 4-GPU serving process uses. Row indices depend only on input tokens, so reads can start with each step and overlap earlier layers. V4.1’s two Engram layers have windows that differ by 30× (0.3 vs. 9.3 ms). We show that this deadline, together with session reuse and contention on a shared device, decides which tier each table can use and which layers need cache, and we give a model that predicts the resulting slowdown from measured read times. Agent and chat traffic reuse rows within sessions, and static hot sets transfer poorly. We build SlackTier, a table tier for SGLang that issues all lookups at step start. It reads the short-window layer first and splits a small GPU row cache across layers. The path runs inside the decode CUDA graph and is bit-exact with the original gather. Layer 14’s table can go to NVMe uncached with no measurable decode cost. With both tables on four NVMe disks, mean time per output token on agent and chat replays rises at most 1.4% over unmodified SGLang, and host memory falls from 212 to 34 GiB. Both tables need no cache when read over RDMA from another node’s memory; one copy serves two instances. On a KV-constrained agent workload, using the freed memory as host KV cache at the same memory budget raises median throughput by 36% and cuts median p90 time to first token from 38 to 24 s.

# Excerpts / key facts

- Authors: Wen Huang (Microsoft), Jack Liu (Independent Researcher). Correspondence: wenhuang@microsoft.com. arXiv:2611.13413, submitted 10 Nov 2026, cs.DC. Marked Preprint.
- Setup (§6): DeepSeek-V4.1-Flash, SGLang 0.5.22, TP4/EP4 on 4×H200, FP8 KV, decode CUDA graphs, bounded SWA replay. Tables on local 3.5 TB NVMe raw devices. Workloads: OpenHands agent trajectories (held-out repos) and WildChat. B = concurrent sessions. Unmodified SGLang processes held **212 GiB** host memory; their host-table gather path uses **223 GiB** (190 GiB tables). Bit-identical: in-server checker, no mismatch over **790K** lookups (V4.1) and **1.1M** (Qwen PLE), including evictions.
- Windows (§6.3 / Table 3): measured W1=**0.27 ms**, W14=**9.35 ms** (~30×). Joint-delay prediction within **0.12 ms RMSE**. Gemma 4 E4B: window ≈ **0.85–0.92 k/L** of a step across H200 / MI300X / GB10 (Fig 4); H200 slope ~0.12–0.14 ms/layer; GB10 step 47 ms at B=32, 0.94 ms/layer.
- Naive NVMe (intro / Table 2): both tables on 1 disk +6.4% (agent) / +7.2% (chat) at B=128. Caching only layer 14 (1M rows) leaves +4.9% / higher chat overhead. Layer 14 alone on NVMe uncached: **−0.0% / −0.1%**, p99 unchanged.
- Best NVMe (Table 2): both on 4 disks, 1M-row cache split evenly: agent **+0.7%**, chat **+1.7%**; RSS **34 GiB**. Client-side vs unmodified SGLang (Table 6, B=128): 4 disks split, mean TPOT agent **−0.5%** [−2.2, 0.5], chat **+1.4%** [1.0, 1.9]; “at most 1.4%”; process **34 vs 212 GiB**.
- Cache allocation (§6.2): giving everything to layer 14 (f=0) costs +4.9% agents; f=0.25–1 yields +1.3–1.9%. Quarter budget (0.25M rows/rank) even split +1.8% agents.
- RDMA (§6.8): second H200 node, 195 GiB tables, 400 Gb/s IB NIC per rank. Uncached step B=128 reads 600–740 pages/rank/layer in **0.21–0.25 ms**. At B=128 and 256, every remote placement within **−0.7% to +0.0%** of host-DRAM table. Two instances share one copy; TPOT within **2.2%** of a single instance with local DRAM tables. Device-side check: no mismatch over 3.9M decode and 18.8M prefill lookups per rank and layer.
- Freed memory as host KV (Table 5): 256 agent sessions, GPU KV pool fixed 1.5M tokens. 4 disks + 185 GiB host KV: prefix hit **76%** (vs DRAM-tables 63%), TTFT p90 **24.1 s** (vs 38.1 s), tokens/s **956** (vs 702) = **36%**. Same host KV with tables still in DRAM needs **408 GiB** RSS. With a 3M-token GPU pool the host KV adds no hit-rate or throughput gain.
- Qwen3.8-Flash-Next PLE (§6.7): one 320M×320 B table at layer 1, window 0.27 ms; process 201 GiB with pinned host table. 4 disks + 1M-row cache: decode **+3.4%** agent / **+2.4%** chat (Table 7); cache serves 93% / 57% of lookups. DGX Spark (GB10, 128 GB): Qwen3.8 NVFP4 (124 GiB incl. 48 GiB PLE) fails to load with table in host memory; mmap from NVMe loads in 74 GiB and keeps 17 GiB (0.58M tokens) KV (§7).
