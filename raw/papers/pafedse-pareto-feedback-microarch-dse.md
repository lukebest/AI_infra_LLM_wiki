---
type: Raw Source
title: "PaFeDSE: Pareto-Feedback-Guided Microarchitecture Design Space Exploration for Efficient Pareto Search"
source_url: https://arxiv.org/abs/2610.34838
pdf: PaFeDSE_Pareto_Feedback_Microarch_DSE_ASPDAC2027.pdf
retrieved: 2026-10-28
ingested: 2026-10-28
org: KAIST
venue: ASP-DAC 2027 (Tokyo)
---

# Abstract (verbatim, arXiv:2610.34838)

Efficient microarchitecture design space exploration (DSE) is critical for optimizing performance, power, and area trade-offs in modern out-of-order processors. While machine-learning-based DSE significantly reduces the cost of exhaustively evaluating large design spaces, existing methods still waste expensive simulations on Pareto-miss candidates that do not improve the Pareto frontier and repeatedly process redundant candidates during iterative exploration. In this paper, we propose PaFeDSE, a Pareto-feedback-guided microarchitecture DSE framework for efficient Pareto search. PaFeDSE leverages Pareto-hit feedback to prioritize candidates likely to improve the frontier and Pareto-miss feedback to suppress exploration of unpromising local regions, while filtering redundant candidates that remain low priority across iterations. Evaluated on SPEC CPU 2017 workloads, PaFeDSE requires up to 49.0% fewer simulations than the strongest prior baseline to reach target hypervolume levels, while achieving a 7.1× reduction in exploration overhead through adaptive candidate filtering.

# Excerpts / key facts (from PDF)

- Authors: Joonyong Park, Hyojeong Lee, Sejeong Yang, Joo-Young Kim (KAIST); ASP-DAC '27, Jan 25–28 2027, Tokyo.
- Components: HitFormer (Pareto-Hit-Aware Transformer Surrogate: PPA + hit score); MissGraph (Locality-Aware Pareto-Miss Penalty Graph); TCFilter (Temporal-Consistency-Guided Filtering).
- Setup: gem5 + McPAT @ 22 nm; SPEC CPU 2017; design space **3,359,232** points.
- vs MoDSE: up to **49.0%** fewer simulations to target HV; avg sims to 90/95/99% HV: **32.9 / 43.3 / 118.8**.
- TCFilter: exploration time/iter 374.19 s → 52.94 s = **7.1×** overhead reduction; no final HV degradation.
- PPA MAPE: **0.731%**, −**30.2%** vs MoDSE.
- Baselines: ActBoost, BOOM-explorer, MoDSE.
