---
type: Raw Source
title: "CHARM+: Cross-Hardware Attention with Re-Merge Multistream Mechanism"
source_url: https://arxiv.org/abs/2611.05906
pdf: CHARM_Plus_Cross_Hardware_Attention_2026.pdf
retrieved: 2026-11-09
ingested: 2026-11-09
org: Lenovo Research
venue: NeurIPS 2026
---

# Abstract (verbatim gist, arXiv:2611.05906)

As sequence lengths continue to grow, distributed attention based on sequence parallelism (e.g., Ring-Attention) has become a mainstream solution for large language models (LLMs). Nevertheless, inherent communication dependencies limit computation–communication overlap, reducing GPU utilization. Moreover, in cross-hardware (NUMA or node) architectures, due to imbalanced communication bandwidth, frequent communication synchronization will limit overall performance. Based on these insights, we propose CHARM+, Cross-Hardware Attention with Re-Merge Multistream Mechanism. We reorganize sequential communications into several levels and achieve intra-level parallelism and computation overlap. Furthermore, we decouple cross-hardware communication from intra-hardware communication, eliminating synchronization overhead caused by bandwidth imbalance. Forward and backward algorithms were evaluated on multiple hardware architectures and consistently outperformed state-of-the-art methods. Compared to Ring-Attention, our forward and backward algorithms achieve average speedups of 1.3× and 1.7× on a dual-NUMA PCIe architecture, and 2.8× and 3.9× on a dual-node NVLink architecture, respectively.

# Excerpts / key facts

- Authors: Xinhang Zhang, Boning Zhang, Chengchun Liu, Chunpu Li, Lei Sun, Weifeng Zhang, Limin Xiao (Lenovo Research). NeurIPS 2026.
- Method: Re-Merge Multistream (RM+) + Cross-Hardware Query Parallelism.
- Abstract avg vs Ring: fwd/bwd **1.3×**/**1.7×** dual-NUMA PCIe; **2.8×**/**3.9×** dual-node NVLink.
- Contributions max: **1.4×**/**1.9×** PCIe; **3.2×**/**4.3×** NVLink.
- H100 Table 5: e.g. 4×8 forward up to ~**2.72×**, backward up to ~**4.21×** vs Ring.
- Megatron end-to-end Table 7: up to **2.17×** (H100).
