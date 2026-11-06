---
type: Raw Source
title: "GC-MoE: Overlapping Expert-Parallel Token Dispatch with FP8/FP4 Grouped GEMM via CUDA Green Contexts"
source_url: https://arxiv.org/abs/2611.04222
pdf: GC_MoE_Green_Context_Expert_Parallel_2026.pdf
retrieved: 2026-11-06
ingested: 2026-11-06
org: Alibaba
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.04222)

Mixture-of-experts (MoE) models are standard for large language model (LLM) serving, and expert parallelism (EP) makes all-to-all token dispatch, grouped GEMMs, and the combine step recurrent costs in every layer… In state-of-the-art fused operators such as DeepGEMM’s Mega MoE, dispatch and computation overlap only by sharing every SM…

This paper presents GC-MoE, an open-source FP8/FP4 MoE inference operator for NVIDIA Hopper and Blackwell GPUs that uses CUDA Green Contexts to split the device at the driver level into a small communication partition and a large compute partition… On eight H20 GPUs GC-MoE accelerates DeepSeek-V4.1-Flash decode by 1.188× on average… (peaks 1.296× and 1.353×, respectively); on eight B300 GPUs it accelerates GLM-5.2 and DeepSeek-V4.1-Flash by 1.106× on average without shared experts and 1.123× with fused shared experts (peak 1.209×), outperforming DeepGEMM’s Mega MoE at all 54 measured points at matched numerical accuracy… GC-MoE reserves only 20 of 148 SMs on B300 for dispatch.

# Excerpts / key facts

- Authors: Yong Li, Kan Liu, Tao Lan (Alibaba). github.com/Bruce-Lee-LY/gc-moe
- Green Contexts：小通信分区 + 大计算分区。
- B300：**20 of 148 SMs** for dispatch。
- 8×H20：均值 **1.188×**；峰 **1.296×** / **1.353×**。
- 8×B300：无 SE **1.106×**，融合 SE **1.123×**（峰 **1.209×**）。
- 全面优于 Mega MoE 的 **54** 测点；精度对齐。
