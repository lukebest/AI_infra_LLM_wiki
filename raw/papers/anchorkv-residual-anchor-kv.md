---
type: Raw Source
title: "AnchorKV: Lossless Key-Value Cache Reconstruction from Layer-Sparse Residual Anchors"
source_url: https://arxiv.org/abs/2611.00117
pdf: AnchorKV_Residual_Anchor_KV_Reconstruction_2026.pdf
retrieved: 2026-11-05
ingested: 2026-11-05
org: Southwest Jiaotong University
venue: arXiv / Elsevier preprint
---

# Abstract (verbatim gist, arXiv:2611.00117)

Residual-stream caching can reconstruct transformer key–value (KV) caches losslessly, but its memory advantage depends on architecture. We present AnchorKV, a storage–replay spectrum connecting per-layer residual caching and full recomputation through configurable residual anchors. An architecture-dependent break-even rule identifies the first storage-saving spacing, while deployment selects an operating point from the spectrum and cascade replay reduces reconstruction from 𝑂(𝐿𝑠) to 𝑂(𝐿), with 𝐿 the model depth and 𝑠 the anchor spacing. For interleaved sliding-window architectures, exact dynamic programming places anchors under non-uniform reconstruction demand. Across CPU, CUDA, and Ascend NPU backends, six architecture families, and fp32/bf16 arithmetic, evaluations verify bit-exact KV reconstruction and unchanged continuation logits and tokens. At 4k context, cascade reconstruction is up to 16.3 times faster than naive replay; across eight applicable global-attention checkpoints at 32k context, deepest spacing yields 5.78–54.0 times full-KV reactivatable session capacity. Compared with seven external cache methods on a common model, AnchorKV preserves full-cache retrieval and question-answering scores, whereas lossy methods change output fidelity and task scores. The break-even spacing is computable from a model’s configuration file alone.

# Excerpts / key facts

- Authors: Hao Li, Jiashu Zhang, Kaleem Ullah Qasim, Heying Zhang (西南交通大学).
- 𝜌layer = 𝑑/(2𝑛𝑘𝑣 𝑑head) 跨族约 **0.50–3.50**；首个省存间距 𝑠⋆=⌊𝜌layer⌋+1。
- Cascade：24 层 Qwen2.5 上 **276→23** 块执行；4k 上下文相对 naive 最高 **16.3×**（正文另报九模型 **7.17–16.25×**）。
- 32k 最深间距：八模型可再激活会话容量 **5.78–54.0×** full-KV；bit-exact（max |ΔK|=max|ΔV|=0）。
- Gemma-3-1B 交错滑窗：DP 放置把重放 18→0，中位延迟 **60.64→5.52 ms**。
