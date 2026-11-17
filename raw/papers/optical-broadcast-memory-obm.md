---
type: Raw Source
title: "Broadcast, Don't Replicate: Eliminating Weight HBM in Datacenter LLM Serving"
source_url: https://arxiv.org/abs/2611.17097
pdf: Broadcast_Dont_Replicate_OBM_2026.pdf
retrieved: 2026-11-17
ingested: 2026-11-17
org: Uppsala University
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.17097)

Large language model (LLM) inference at datacenter scale is fundamentally bottlenecked by memory capacity and bandwidth limits. Because model weights are read-only and identical across instances, conventional architectures that replicate these parameters across the local DRAM of tens of thousands of accelerators incur massive capital expenditures, significant static power dissipation, and redundant memory-fetch energy. A recent proposal to use optical fiber loops as delay-line memory alleviates these issues, but its recirculating loop must hold the whole model: loop length grows with model size, slack is fixed when the ring is built, and the layouts that serve modern Mixture of Experts (MoE) models efficiently do not fit in it. We propose Optical Broadcast Memory (OBM), an open-ended hierarchical Tap-and-Amplify fiber architecture that generalizes and replaces the optical ring paradigm. A centralized memory server continuously broadcasts weights to distributed inference nodes that passively tap the data stream using receive-only co-packaged optics, delivering parameters directly to compute units without intermediate buffering. To overcome the limitations of continuous weight streaming, we use dynamically-sized slack to accommodate large and variable context lengths. We show how removing the restrictions of the optical ring allows OBM to efficiently serve MoE models. Evaluated at a datacenter scale of 80,000 accelerators, OBM eliminates petabytes of HBM while being competitive or better in throughput and energy per token than an HBM-based system.
