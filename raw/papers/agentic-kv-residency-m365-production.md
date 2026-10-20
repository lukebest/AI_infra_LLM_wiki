---
type: Raw Source
title: "Understanding KV Residency in Production-Scale Agentic LLM Workloads"
source_url: https://arxiv.org/abs/2610.22863
pdf: Agentic_KV_Residency_M365_Production_2026.pdf
retrieved: 2026-10-20
org: Microsoft M365 Research / IISc
venue: arXiv cs.DC (v1 2026-10-16)
---

# Abstract (verbatim, arXiv:2610.22863)

Agentic large language model (LLM) applications turn one user request into a sequence of model and tool calls over a growing context. Retaining this context's key-value (KV) state in GPU memory lets later calls reuse it instead of recomputing it, but at fleet scale this needs substantial memory. We characterize four production Microsoft M365 workload traces (Deep Research, Enterprise Assistant, Coding Agent and Enterprise Chat) spanning more than 121 million model calls. In Deep Research, the application issues 89% of model calls and the median context grows from about 10K to 68K tokens by the 30th call. About 80% of context tokens are served from the prefix cache. With the public Llama-2-70B KV layout standing in for confidential models, one 99th-percentile Deep Research session exceeds the 80 GB HBM of an NVIDIA H100, and holding all live sessions at their peak needs an estimated 501.8 TB of HBM, although inference occupies only 5.6% of that retention time. Trace-driven replay shows that a one-hour idle cap cuts this ceiling by 3.6x while raising the share of calls that recompute context only from 4.07% to 4.53%. Under tighter budgets, eviction alone is insufficient: at one tenth of the busiest hour's demand, LRU eviction makes 63% of Deep Research calls recompute and clairvoyant furthest-next-use 31%, whereas multi-resolution retention (MRR), which demotes the LRU session's KV state to int4, lowers this to 13.6%. Placement imposes a separate limit: when the next call reaches a different deployment, cached-context reuse drops from 89% to 29%, and treating KV state as deployment-local raises the recompute floor under unlimited memory from 5.4% to 20.2%. These findings motivate retention that changes the representation of KV state, together with deployment-aware routing or migration. We plan to release AgenticTraceSim, a parametric trace generator, and a residency replay framework.

# Excerpts (from arXiv PDF v1)

- "Under the reference KV representation, a single P99 Research session requires 81.6 GiB, exceeding the 80 GB high-bandwidth memory (HBM) of an NVIDIA H100 GPU, and holding every live Research session at its peak lifetime working set requires an estimated 501.8 TB at the exact peak."
- "In Research, mean same-model reuse is also associated with deployment continuity: 88.9% when consecutive calls remain on one deployment versus 29.0% after a same-model deployment change within the region (Section 4)."
- "the heavyweight Spine class, which carries the long-running context, holds 67% of call-context KV bytes but only 32% of uncached-context tokens and has a self-transition probability of 0.97 (Section 3)."
- "Counting per-group quantization metadata enlarges each int4 copy beyond a quarter of fp16 and raises the in-HBM MRR rate to between 14.99% and 19.25%."
- "The replay does not measure how int4 KV changes responses"
