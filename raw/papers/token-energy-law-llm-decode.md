---
type: Raw Source
title: "The Token-Energy Law of LLM Decode: Active Bytes and Realized Time Account for Joules per Token"
source_url: https://arxiv.org/abs/2610.28576
pdf: Token_Energy_Law_LLM_Decode_2026.pdf
retrieved: 2026-10-22
org: NVIDIA; Texas Tech University; TACC
venue: arXiv cs.LG / cs.DC / cs.PF (2026-10)
---

# Abstract (verbatim, arXiv:2610.28576)

Energy-efficient deployment of large language models requires understanding how model architecture, hardware, and serving settings shape energy per generated token. We introduce the Token-Energy Law, a compact, interpretable model of GPU-board energy per output token for dense, full-history decoding. It relates token energy to two core dimensions: active bytes and realized decode time. Active bytes describe logical byte demand per output, separating dense weights shared within a decode iteration from private key--value (KV) histories read and updated for each request. Realized decode time is the elapsed decode duration divided by the number of output tokens produced. We combine the two byte coordinates and time in a common affine form, with coefficients calibrated for each model and hardware/runtime configuration. This formulation explains how batching amortizes shared-weight work, longer attended histories increase private KV demand, and throughput determines the time-associated cost per output. Our experiments cover three models under BF16 decoding on NVIDIA Hopper and Blackwell GPUs, including two-GPU tensor parallelism on Hopper. Using fixed coefficients and observed decode time, held-out condition-mean energy estimates differ from measurements by at most 3.73%.

# Excerpts / key facts (from arXiv PDF v1)

- Law: e_gross = c + alpha*q_w + beta*q_KV + P_tau*tau + u, with q_w = M_w/(1e9*B_eff), q_KV = K_KV*(L_token+1)/1e9, tau = D/T. Weight-KV byte balance batch B* = M_w / [K_KV (L+1)] (logical bytes, not an energy crossover).
- Platforms: GH200 (144-GB HBM3e, 700 W cap, vLLM 25.09; TP=1 and TP=2) and GB300 (1,300 W cap, TP=1). Models Qwen2.5-7B/14B-Instruct, Mistral-7B-Instruct-v0.3; BF16, FlashAttention, full-history attention.
- Validation: 270 held-out static executions over 54 cells, all within 3.73%; zero-refit GPU0->GPU1 transfer median 2.62%, max 3.72%; trace validation adds 40+40+24 runs (374 total).
- GB300 ablation (Table 5, max cell-mean APE): bytes+time 0.887-2.137%; single total-bytes+time 4.381-5.721%; bytes only 28.2-35.5%; time only 10.97-29.4%.
- HBM-read fit MAPE 0.0498% vs measured reads (Qwen2.5-7B, GH200).
- Limitations: dense full-history decode only; MoE, sparse/windowed attention, quantization need further validation.
