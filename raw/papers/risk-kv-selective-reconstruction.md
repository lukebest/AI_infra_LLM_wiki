---
type: Raw Source
title: "RISK-KV: Quality-Aware Selective KV Cache Reconstruction for Distributed LLM Inference"
source_url: https://arxiv.org/abs/2610.29544
pdf: RISK-KV_Selective_KV_Reconstruction_2026.pdf
retrieved: 2026-11-03
ingested: 2026-11-03
org: Harbin Institute of Technology
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2610.29544)

Request migration and interruption recovery in distributed LLM inference rely on historical KV caches. Retaining or transferring a complete cache incurs substantial state overhead, whereas replaying historical tokens requires additional computation. This paper proposes RISK-KV, a quality-aware method for selective historical KV reconstruction in pretrained models. RISK-KV uses exact KV states on both sides of a target layer and cross-layer ridge regression to predict the missing layer's attention-projection input; it then folds in the original model's KV projection matrices to reduce predictor storage. Reconstruction risk is measured by the change in negative log-likelihood (NLL) caused by actual reconstruction, and low-overhead topology search with quality gating selects the layer groups to reconstruct. Independent tests on three language models show that representative recovery configurations omit 18.2%–33.3% of historical KV, with perplexity changes below 0.5%. In a local request-recovery experiment with a 512-token history, RISK-KV achieves a 1.51–3.31× speedup over full Token Replay.

# Excerpts / key facts (from PDF)

- Author: Wang Yuekai (Harbin Institute of Technology).
- Exact KV anchors on both sides of target layer; ridge regression for missing attention-projection input; fold original KV projection matrices for online mapping.
- Risk = NLL delta under teacher-forced inference; topology search along ranked groups + bootstrap quality gate.
- Models: Qwen2.5-0.5B/1.5B-Instruct, TinyLlama-1.1B-Chat-v1.0.
- Omit **18.2%–33.3%** historical KV; perplexity change **<0.5%**; local recovery 512-token history **1.51–3.31×** vs full Token Replay.
