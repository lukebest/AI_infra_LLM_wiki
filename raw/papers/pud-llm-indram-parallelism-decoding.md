---
type: Raw Source
title: "Accelerating LLM Decoding with In-DRAM Parallelism (PUD-LLM)"
source_url: https://arxiv.org/abs/2611.02401
pdf: PUD_LLM_InDRAM_Parallelism_Decoding_2026.pdf
retrieved: 2026-11-05
ingested: 2026-11-05
org: The University of Tokyo / RIKEN AIP
venue: arXiv
---

# Abstract (verbatim gist, arXiv:2611.02401)

Autoregressive decoding of large language models (LLMs) on edge devices is dominated by memory-bound general matrix–vector multiplication (GeMV) operations. Processing-using-DRAM (PUD) is a promising computing paradigm that can alleviate this bottleneck by reducing processor–memory data transfers and enabling massively parallel computation within DRAM (e.g., across 65,536 columns). However, weight matrices in individual LLM layers (e.g., a QKV matrix in Llama 3 8B with 6,144 rows) are typically too small to fully utilize parallelism in PUD. To address this challenge, we propose PUD-LLM, an algorithm–system co-design for PUD-based LLM inference. At the algorithm level, we enable a subsequent projection to be packed with the current projection by reformulating it as a computation on the current residual state plus a correction for the residual update. Layer redundancy allows this correction to be approximated using fewer bit-serial steps. At the system level, we tailor data mapping and execution to improve utilization of either columns within DRAM subarrays (SIMD) or independently controlled banks (MIMD). Overall, PUD-LLM achieves up to 1.41× end-to-end decoding speedup over the PUD baseline, corresponding to a 2.45× speedup over processor-based execution.

# Excerpts / key facts

- Authors: Kevin Xu, Tatsuya Kubo, Daichi Tokuda, Shinya Takamaeda-Yamazaki, Issei Sato (UTokyo / RIKEN AIP).
- PUD 列并行示例：跨 **65,536** 列；Llama 3 8B QKV 仅 6,144 行 → 利用率不足。
- 算法：后继投影打包为「当前 residual + 残差更新校正」；系统：SIMD 列打包 / MIMD bank 流水。
- 端到端 decode：相对 PUD 基线最高 **1.41×**，相对处理器执行 **2.45×**。
