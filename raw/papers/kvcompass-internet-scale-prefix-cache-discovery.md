---
type: Raw Source
title: "KVCompass: A Discovery Plane for Internet-Scale Prefix Cache Sharing in LLM Serving"
source_url: https://arxiv.org/abs/2610.24179
pdf: KVCompass_Internet_Scale_Prefix_Cache_Discovery_POMACS_2026.pdf
retrieved: 2026-10-21
org: University of California, Santa Cruz
venue: POMACS (accepted), arXiv cs.NI/cs.DC 2026-10
---

# Abstract (verbatim, arXiv:2610.24179)

KV cache reuse is one of the most effective ways to reduce LLM inference cost, but today its benefits are largely confined to a single cluster. When a provider serves the same model across geographically distributed regions, each region may repeatedly prefill the same popular prefixes, wasting GPU time and increasing time-to-first-token (TTFT). Exploiting reuse across regions involves discovering which worker currently holds a reusable KV cache for each request's prefix. We show that this KV cache discovery problem is structurally harder than conventional object lookup. Unlike hash-placement mechanisms such as DHTs, where an object's location is a deterministic function of its key, KV caches are created on the workers that serve requests, and their holder sets change with subsequent requests and KV cache evictions. KV cache discovery therefore calls for decoupling KV cache identity from placement. We present KVCompass, a discovery plane for Internet-scale KV cache sharing. The discovery index supports variable-length prefix lookup with constant-time local table reads at the edge, allowing each request to be forwarded to the worker that best balances KV cache reuse against load and network distance. Evaluation includes a 64-worker geo-distributed simulation and a 14-worker three-continent real-machine testbed. Evaluation shows that KVCompass achieves 1.3-14x lower P99 TTFT than the baselines, up to 3.7x lower P99 end-to-end latency, up to 4.7x the throughput, and a peak load factor within 2% of the Oracle floor.

# Excerpts / key facts (from arXiv HTML v1)

- Simulation: 64 workers across regions; each modeled as A100-80GB running Llama-3.1-8B-Instruct BF16, 32 GB VRAM + 128 GB host DRAM reloadable over PCIe 4.0 at 25 GB/s; WAN latency from CloudPing AWS measurements.
- Testbed: 14 RTX 5090 GPUs (8 US, 4 Asia, 2 Europe), one SGLang worker per GPU; cross-region traffic over public Internet.
- Sharded maintenance units own all index writes, so the read path needs no locks; forwarding score combines network distance, queuing delay, cache tier, residual prefill.
- Code: https://github.com/011shiyiLing/KVCompass
