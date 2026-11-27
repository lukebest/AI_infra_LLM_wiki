---
type: Raw Source
title: "Gossamer: A Utility-Driven Architecture for Constant-Budget KV Cache Compression in Reasoning LLMs"
source_url: https://arxiv.org/abs/2611.29497
pdf: Gossamer_Constant_Budget_KV_Compression_2026.pdf
retrieved: 2026-11-27
ingested: 2026-11-27
org: Duke / Intel
venue: MICRO 2026
---

# Abstract (verbatim gist, arXiv:2611.29497)

Transformer-based large language models (LLMs) are increasingly applied to complex reasoning tasks, yet their inference efficiency is fundamentally constrained by the rapid growth of the KV cache. Existing compression methods, such as quantization and eviction, alleviate capacity pressure but remain purely algorithmic, often introducing additional passes and compute overhead. This paper presents Gossamer, a KV cache compression architecture for reasoning LLMs that bridges the algorithm–system–hardware gap. Gossamer introduces a unified utility-based action framework that dynamically selects compression operations, quantization, merging, or eviction, under a constant KV cache budget. Through cross-domain co-design, we fuse cosine-similarity estimation directly into the attention computation, exploiting idle compute cycles to perform similarity evaluation without latency or bandwidth cost. We call this mechanism Free-Lunch Utilization. Under tight memory constraints, Gossamer sustains reasoning quality comparable to uncompressed inference while improving end-to-end throughput by up to 16.7× over uncompressed baselines, 5.5× and 4.9× over the quantization-based Oaken and Ecco, and 1.8× over the eviction-based R-KV.

# Excerpts / key facts

- Authors: Feng Cheng, Cong Guo, Junyao Zhang, Haoxuan Shan, Chiyue Wei, Hong Wang, Hai Li, Yiran Chen。Duke University、Intel Corporation。arXiv:2611.29497，cs.AR，MICRO 2026，Sun/Mon 窗口公告后于本轮深读。
- 质量：DeepSeek-R1-Distill-Llama-8B / Qwen-14B，MATH-500（最长 8192）与 AIME 2024（16384），pass@1、k=16、温度 0.6、top-p 0.95；码本在 GSM8K 上剖析。
- 架构仿真：SCALEsim-v2，128×128 PE，输出驻留，FP16 乘 / FP32 累加，片上 64 MB（16/16/32），HBM2 512 GB/s。SystemVerilog，商用 28 nm、500 MHz。定制模块 1.46 mm²、811 mW，相对基线系统 213.74 mm² / 123.97 W 为 0.68% / 0.65%。
- 8192 token 端到端吞吐：相对 FullKV 最高 16.7×，相对 Oaken / Ecco / R-KV 为 5.5× / 4.9× / 1.8×。QwQ-32B 50% 全精度变体在 8192 token 时超过 10× FP16。LongBench v2 上 DS-Llama-8B 总体准确率 30.4%，与 FullKV 相差 0.4 个百分点。
