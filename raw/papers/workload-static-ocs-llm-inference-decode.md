---
type: Raw Source
title: "Workload-Static Optical Circuit Switching for Scalable LLM Inference Decode"
source_url: https://arxiv.org/abs/2611.05104
pdf: Workload_Static_OCS_LLM_Inference_Decode_2026.pdf
retrieved: 2026-11-06
ingested: 2026-11-06
org: Salience Labs / NVIDIA / Heidelberg University
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.05104)

LLM inference decode executes fine-grained collectives whose latency directly limits per-user interactivity, yet scale-up fabrics are still built from electronic packet switches designed for training. We observe that, for a given model deployment and parallelization, the communication structure of decode is fixed, and propose workload-static optical circuit switching (OCS): circuits are configured once per deployment, co-designed with model parallelism and with topology-aware collective schedules that turn spare accelerator ports into fewer communication phases or higher bandwidth. We evaluate this design with GXNET, a graph-based workload emulator coupled to analytical and flit-level network models grounded in hardware measurements. In a 576-accelerator scale-up domain serving 5T-parameter MoE models with up to 5M tokens of context, all-OCS fabrics improve interactivity by up to 65% and energy efficiency by up to 119% over 4:1 oversubscribed packet-switched fabrics.

# Excerpts / key facts

- Authors: Maximilian Thürmer, Nicolas Scotto di Perto, Eloise Stein, Natanijel Vasic, Mikaeil Bagherli, Zhenguo Wu, Benjamin Klenk, Holger Fröning, Johannes Feldmann.
- Circuits once per deployment; co-designed with model parallelism + topology-aware collectives.
- GXNET graph emulator + analytical/flit-level nets grounded in HW measurements.
- 576-accelerator；5T MoE；至 5M tokens context。
- all-OCS vs 4:1 EPS：交互性最高 **65%**，能效最高 **119%**。
- Megatron 5T：**52%** interactivity / **102%** energy；GPT-OSS-5.3-like：至 **65%/119%**。
