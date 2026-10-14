---
type: Raw Source
title: "Adaptive DHiSparse: Speculative Decoding over a Load-Adaptive KV Hierarchy"
source_url: https://arxiv.org/abs/2610.13708
pdf: Adaptive_DHiSparse_Speculative_Hierarchical_KV_2026.pdf
retrieved: 2026-10-14
org: Umans AI
venue: arXiv preprint (cs.AI / cs.CL / cs.DC / cs.LG)
---

# Abstract (verbatim, arXiv:2610.13708)

Long-context serving runs out of KV memory before the hardware reaches its useful throughput. HiSparse stores history in host memory and fetches only the selected entries, but it uses one cache budget at every load and does not handle draft-model speculative decoding such as DSpark and DFlash2. We present Adaptive DHiSparse, which supports speculative decoding over hierarchical sparse KV and adapts residency to load. It protects the required working set, retains additional history while GPU memory is spare, and recovers the rest through exact fused retrieval. DSpark and DFlash2 keep their proposal and acceptance rules: queries share missing-row retrieval, draft KV uses a window-bounded ring, and verification staging is reused across layer groups. At 100K context and concurrency 128, GLM-5.3 with DFlash2 delivers 793 output tokens/s per decode GPU, 1.45$\times$ HiSparse and 1.27$\times$ non-speculative adaptive serving. Held to the same latency bounds as HiSparse, it sustains up to 4$\times$ the concurrency and 2.3 to 3.7$\times$ the output, depending on the per-token bound. On DeepSeek-V4.1-Flash at 500K context and concurrency 512, Adaptive DHiSparse with DSpark delivers 1.85$\times$ the output of resident serving with DSpark. In a load step, optional residency reduces host fetches from 14.2% to 1.4% of selected rows at low load and releases memory under pressure.

# Excerpts (from arXiv HTML v1)

- §4.1 Hardware: 8x B300 nodes (269 GiB HBM per GPU, 4.3 TB host memory over PCIe). GLM-5.3: 4 prefill + 4 decode GPUs at 100K context; DeepSeek-V4.1-Flash: 2 per role at 500K. Closed-loop concurrency benchmark from HiSparse; 2,048-token output cap. Implemented in SGLang; GLM uses FP8 KV, k=2,048, B=4,096.
- §4.2.1 "Where the 1.45x comes from": HiSparse -> non-speculative adaptive is 1.14x (copy grid scales 4–32 thread blocks vs fixed 4; resident-first admission cuts prefill/KV handoff 10.4 s -> 4.0 s; 126 vs 121 active requests). Speculation adds 1.27x: a round verifies four queries and emits 2.88 tokens in 2.2x the time of a non-speculative step. Mean TTFT 2.1x lower than HiSparse, mean TPOT 29% lower.
- Contributions: windowed draft ring + reusable verification staging add 0.060 GiB required GPU state per GLM session.
- §5 capacity: a session needs 0.432 GiB at 100K (0.492 GiB with DFlash2); speculation adds 6.6 GiB fixed per GPU; configurations admit 208 and 140 sessions; 208 sessions back up 0.93 TB of a 4.3 TB host. At C256 allocation wait is 85–97% of TTFT.
- §5 model design: vs GLM-5.3, DeepSeek-V4.1-Flash has 4x smaller k, 2.6x fewer selecting layers, rows about half as wide, one source row per selection vs 3.7 layer rows -> about 80x fewer host bytes per token at a comparable miss rate.
