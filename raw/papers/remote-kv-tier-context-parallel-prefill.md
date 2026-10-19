---
type: Raw Source
title: "When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill"
source_url: https://arxiv.org/abs/2610.21500
pdf: Remote_KV_Tier_Context_Parallel_Prefill_2026.pdf
retrieved: 2026-10-19
org: Multiverse Computing (author Muhammad Ibrahim)
venue: arXiv cs.DC (submitted 2026-10-15)
---

# Abstract (verbatim, arXiv:2610.21500)

Reusing the attention KV cache across requests is a standard way to cut prefill cost in long-context LLM serving, and production systems increasingly back the per-engine cache with a remote tier shared by every engine. We study such a tier in a disaggregated deployment of GLM-5.3, an FP8 mixture-of-experts model with multi-head latent attention (MLA), on 8xB300 nodes running prefill context parallelism (PCP8). Enabling the remote tier (LMCache with a Valkey store) left median time-to-first-token unchanged but raised the 16k-token p99 from 3.96 s to 17.3 s. Replaying a production request stream on an isolated engine, we find that a remote hit took 0.88 s against 0.31 s to recompute the prompt, and that synchronous loading turned a hit-heavy stream into an unstable queue: p99 83.32 s with the GPUs 7% busy. A two-term cost model explains both: a hit pays off only if the tier delivers more than B* = sR (2.53 GB/s for this model and GPU), and a fixed per-hit engine cost (T0 ~ 0.33 s) means that hits on prompts shorter than about 17k tokens cannot beat recompute at any bandwidth. Guided by the model, we (i) shard the MLA KV store across PCP ranks, with a proof that the existing minimum-over-ranks lookup returns the longest cached prefix and a load protocol that can never desynchronize collectives; (ii) partition the remote tier by rank, one server instance per rank with no coordination, which raises GET bandwidth 6.3x to 10.76 GB/s; (iii) add asynchronous loading to the sharded store; and (iv) fix three client bugs that caused unbounded stalls. On the hit-heavy stream, with 98.5% of prompt tokens served from the remote tier, p99 falls from 83.32 s to 0.67 s. The sharded store raises prefill throughput by 14%, and by 34% together with an upstream kernel fix. All changes are submitted upstream to LMCache.

# Excerpts (from arXiv PDF v1)

- Setting: GLM-5.3 FP8 MoE with DeepSeek-style MLA on 8× B300 nodes; prefill/decode disaggregated; one vLLM engine per prefill node with PCP8; remote L2 tier = LMCache + Valkey.
- Cost model: ignoring T0, a hit pays off iff B > B* = sR (prompt length cancels). GLM-5.3 FP8 on one B300 node: s = 48.4 KB/token, R = 52.2k tokens/s → B* ≈ 2.53 GB/s. With T0 > 0 a hit pays off only if n/R > T0 + ns/B, requiring n > R·T0. T0 fit = 0.40 − 0.79/10.76 ≈ 0.33 s → R·T0 ≈ 17k tokens; model predicts 0.79 s for a 16k hit on one instance vs measured 0.83–0.88 s.
- Synchronous loading under PCP stalls all ranks; engine behaves like a single-server queue; λ = 1.21 req/s, median prompt 0.79 GB, single instance sustained 0.78–0.89 GB/s → ρ ≈ 1.13 (unstable); eight instances ρ ≈ 0.09. Single Valkey instance serving 8 PCP ranks delivered 1.71 GB/s at best (< B*).
- Eight instances: median 0.41 s, p99 0.80 s; with all fixes (H5b) p99 0.67 s, 124× below H1b; Valkey shards averaged 8.9 ms server time per 12.4 MB GET.
- Prefill throughput (8 concurrent ~200k-token prompts): sharded store +14%, +34% with upstream kernel fix. Five-node disaggregated deployment passes the workload SLA.
- Lesson: "on current GPUs recompute is a demanding baseline. A cache tier has to be judged against the prefill rate of the hardware it serves, not against the latency of the network." "Lockstep amplifies everything": under PCP any per-rank stall stalls all ranks.
- Limitations: single runs per condition (differences <~10% not established); prefill only, one engine as sole Valkey client, KV handoff to decode omitted.
- Upstream: LMCache PRs (e.g., #5545 shard MLA KV store across PCP ranks).
