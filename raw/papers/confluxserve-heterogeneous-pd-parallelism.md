---
type: Raw Source
title: "ConfluxServe: Reconciling Resource Utilization and Parallelism Efficiency across Prefill and Decode in LLM Serving"
source_url: https://arxiv.org/abs/2610.37810
pdf: ConfluxServe_Heterogeneous_PD_Parallelism_2026.pdf
retrieved: 2026-11-03
ingested: 2026-11-03
org: University of Waterloo
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2610.37810)

Prefill and decode are complementary in resource usage, but often divergent in parallelism preferences. Executing the two phases separately preserves their preferred parallelism but leaves complementary resources underutilized, while co-batching improves utilization but often requires a uniform parallel configuration that hurts execution efficiency. To resolve this utilization–efficiency dilemma, we propose Conflux Parallelism (XP), a parallel execution abstraction that co-executes prefill and decode with different parallelism within the same batch. Conflux Parallelism exploits operator-level Transformer structure to construct a heterogeneous execution path with different batching and parallelism strategies across operators, combining the best of co-batching and phase-specific execution. Building on Conflux Parallelism, we design ConfluxServe, an SLO-aware serving system that maximizes cluster goodput under TTFT and TBT constraints. Evaluation on production workloads shows that ConfluxServe improves serving goodput by 1.26–1.62× over the strongest baselines.

# Excerpts / key facts (from PDF)

- Authors: Wenhao Chen, Hong Zhang (University of Waterloo).
- XP: co-batch dense linear ops across different SP; separate attention paths (decode local, prefill SP across ranks); spatial multiplexing of attention.
- ConfluxServe: CUDA Graph for shared linear ops, SM partitioning, latency model, waterfill prefill dispatch, decode-residency rank selection.
- Serving goodput **1.26–1.62×** over strongest baselines on production workloads.
