---
type: Raw Source
title: "TripleKV: Predict, Prefetch, Protect – KV Cache Management for AI Agents"
source_url: https://arxiv.org/abs/2611.25112
pdf: TripleKV_Predict_Prefetch_Protect_2026.pdf
retrieved: 2026-11-24
ingested: 2026-11-24
org: University of Illinois Urbana-Champaign; IBM Research; National Technical University of Athens
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.25112)

LLM agents alternate between inference and tool execution, repeatedly reusing their growing context across calls. Under high concurrency, their combined key-value (KV) cache working set can reach hundreds of GiB, far exceeding GPU memory capacity. As idle KV cache blocks are evicted to slower storage tiers, returning agents incur expensive retrievals that stall inference.

To address this problem, we present TripleKV, a three-tier KV cache management system that hides the delays of these retrievals. In agentic workloads, the KV blocks needed by the next inference request are known in advance; only the time of their reuse is uncertain. TripleKV uses a tool-aware latency predictor to estimate when each tool call will complete and prefetches the required KV blocks from SSD into host DRAM ahead of time. Unlike GPU prefetching, this avoids reserving scarce GPU memory and interfering with concurrent inference requests. To further improve DRAM utilization, TripleKV eliminates duplication of GPU-resident blocks in DRAM, and introduces a victim-cache mechanism that refills blocks from SSD upon their eviction from GPU memory.

Across data, web, and coding agents, TripleKV reduces the fraction of requests requiring critical-path SSD reads from 45–76% to under 10%. It also reduces P95 time to first token (TTFT) by up to 49% compared with vLLM extended with DRAM and SSD KV-cache tiers, and achieves 1.5-7× lower P95 TTFT than recent agent-aware systems.

# Excerpts / key facts

- Authors: Shashwat Jaiswal, Fan Lai, Tianyin Xu, Josep Torrellas（University of Illinois Urbana-Champaign）；Chloe Alverti（National Technical University of Athens）；Mengmei Ye, Chen Wang, Hubertus Franke（IBM Research）。arXiv:2611.25112，cs.DC，提交标注 18 Nov 2026。
- 平台：单卡 H100 NVL（94 GB HBM），Qwen3-30B-A3B（BF16 约 60 GiB），L1 32 GiB / L2 64 GiB / L3 1 TiB RAID + O_DIRECT；vLLM v0.24。负载 DRB / GAIA / TB4 / BC+，现场 50 条任务轨迹回放，并发 12 / 16 / 20。
- P95 TTFT 相对带 L3 的 vLLM：DRB / GAIA / TB4 / BC+ 上分别最高降 35% / 49% / 23% / 33%。覆盖在 GAIA 20 / BC+ 20 降到 87% / 60%，因受保护需求碰到 64 GiB L2 上限。
- 相对 Oracle（轨迹真实工具时延）时延与吞吐落在 5% 以内。
