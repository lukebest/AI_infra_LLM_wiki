---
type: Raw Source
title: "Elastic Precision: Software–Hardware Co-Design of a Mixed-Precision Architecture for Long-Context LLM Inference"
source_url: https://arxiv.org/abs/2611.00915
pdf: Coffee_Elastic_Precision_Mixed_Precision_LLM_2026.pdf
retrieved: 2026-11-09
ingested: 2026-11-09
org: Imperial College London / University of Cambridge
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.00915)

Low-bit quantization reduces the data movement and computation costs of large language model (LLM) inference. However, uniform widths can waste precision and degrade model quality because computations differ in quantization sensitivity. Existing mixed-precision methods alleviate this mismatch by assigning widths to channels, tokens, or quantization groups, with some adapting widths to runtime inputs. However, when selecting one input’s width, these methods do not fully account for how the other input of the current GEMM tile affects output error. Combining both inputs of the current GEMM tile to estimate output errors and allocate both input widths can therefore better match precision to the current computation, but introduces additional estimation and selection overheads on conventional GPUs and NPUs. We therefore propose Coffee, a runtime precision allocation architecture for long-context LLM inference. Under a fixed average bit-width budget, Coffee combines information from both input matrices of the current GEMM tile to estimate output errors at candidate widths. These estimates guide online allocation of both input widths across subarrays, directing more bits toward computations with greater estimated error reductions. Its mixed-precision hardware directly supports the selected widths in data access and computation, while overlapping error estimation and width selection with transfers and computation to limit additional stalls. The same read path supports attention-guided KV reads during decoding, reducing traffic and easing bandwidth bottlenecks. Coffee achieves lower perplexity and higher average zero-shot accuracy than the evaluated quantization baselines, and higher long-context retrieval recall than PLENA. For long-context decoding, system modeling projects up to 2.55× the throughput and 2.61× the energy efficiency of the reconfigured PLENA baseline, and up to 4.96× and 12.56×, respectively, compared with the B200 GPU baseline.

# Excerpts / key facts

- Authors: Boyang Chen, Xiao Wu, Haoran Wu, Yiren Zhao (Imperial / Cambridge).
- Coffee: flattened systolic (PLENA-style); both GEMM inputs guide online width selection under offline avg bit budgets; attention-guided KV reads + V skipping.
- Table 1 Llama-3-8B Ours Avg4: WikiText-2 PPL **6.58** vs PLENA **6.95**; Avg acc **72.23** vs **69.63**.
- Table 2: long-context retrieval better than PLENA across models.
- Table 3 system model: up to **2.55×** throughput / **2.61×** energy vs reconfigured PLENA; up to **4.96×** / **12.56×** vs 4×B200 baseline.
- ASAP7 **1 GHz**; max width **INT5**; online decision area **~1.97%** of core.
