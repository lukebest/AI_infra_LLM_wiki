---
type: Raw Source
title: 'Heterogeneous computing: the key to powering the future of AI agent inference'
source_path: /home/luke/wiki/raw/papers/Heterogeneous_Computing_AI_Agent_Inference_2026.pdf
arxiv: '2601.22001'
doi: '10.48550/arXiv.2601.22001'
zotero: 4PYXN5A8
ingested: 2026-07-17
sha256: be571dce0cc71fa471ab79efa5bf5a59ecabbe10aa06da22b9592c78b100be16
---

# Heterogeneous computing: the key to powering the future of AI agent inference

Authors: Aaron Zhao (Imperial College London), Junyi Liu (Microsoft Research)
Year: 2026

Structured notes / key excerpts:

- **Thesis**: AI agent inference (not chatbot-only) needs **system-level heterogeneity** across compute, networking, and memory — beyond GPU-centric stacks; Nvidia Rubin CPX cited as inference-specialization trend.
- **Operational Intensity (OI)**: FLOPs per byte moved from DRAM — classic roofline metric; decode often memory-bandwidth bound.
- **Capacity Footprint (CF)**: Bytes per agent request in DRAM (batch × CF = total capacity need); KV cache dominates CF at long context.
- **Memory capacity wall**: Both MFU and MBU can be low simultaneously — existing roofline/MFU/MBU miss capacity limits (blue/yellow quadrants in their Figure 1).
- **Agent diversity**: Chatbot, coding, web-use (WUA), computer-use (CUA) agents on LLaMA-70B show very different token profiles; coding/WUA/CUA exhibit **snowballing context** (20–30 env interactions/task; coding contexts to **300K–1M** tokens).
- **CF exceeds single B200** for most agent workloads at modest batch; decode OI extremely low due to KV loading — dilemma: need more cards for CF but OI stays low (inefficient scale-out).
- **Attention variants**: MHA vs GQA vs MLA (DeepSeek) drastically change CF vs context length; MLA latent dims 64–1024 shift capacity curves.
- **MoE**: Reduces OI (sparse activation) but CF still sensitive to weights + long-context KV.
- **Optimizations affecting placement**: Quantization, prefill-decode disaggregation, sparse/linear attention — each shifts OI/CF quadrant.
