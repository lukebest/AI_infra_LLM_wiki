---
type: Raw Source
title: "EdgeALM: An Efficient and Unified Edge Accelerator for Large Audio Language Models via Full-Stack Hardware-Software Co-Design and Agent-Driven Recursive Optimization"
source_url: https://arxiv.org/abs/2611.30216
pdf: EdgeALM_FPGA_Audio_Language_Model_2026.pdf
retrieved: 2026-11-27
ingested: 2026-11-27
org: Sun Yat-sen University
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.30216)

Edge deployment of audio language models (ALMs) is constrained by large model footprints, heterogeneous workloads, and limited software support. This paper presents EdgeALM, an efficient and unified FPGA accelerator for ALMs that combines full-stack hardware-software co-design with agent-driven recursive optimization. An end-to-end ALM compression flow is developed, combining a unified AWQ-style quantizer with modality-conditioned vocabulary pruning. A Conv-Matmul Disaggregation architecture is proposed, with dedicated matrix and convolution engines that operate concurrently on their respective workloads. An Extra-Coarse-Grained ISA is designed to incorporate regular on-chip data movement and execution sequences into compute instructions. The proposed EdgeALM is implemented on a single Alveo U50 in an ordinary desktop PC and demonstrates inference on more than 20 models, including ALMs with up to 13B parameters within the 8-GB HBM capacity. It achieves high-throughput audio-to-text inference at up to 169.5 tokens/s and sustains real-time streaming audio-to-audio inference, with 94% bandwidth utilization and 26 W power consumption on average.

# Excerpts / key facts

- Authors: Chenglin Yang, Feifan Xu, Xingyuan Li, Xinpeng Xing, Dihu Chen。中山大学集成电路学院。arXiv:2611.30216，cs.AR，周二公告后于本轮深读。
- 板测：Alveo U50 插在 i7-8700 台式主机，自制风扇使 FPGA 低于 60°C；计算 160 MHz，HBM 450 MHz；Vivado / Vitis 2022.2。资源：LUT 587,244，FF 623,683，DSP 1,263，BRAM 567，URAM 204。
- 压缩：Kimi-Audio 25.14→7.35 GB（70.8%），LLaMA-Omni2-3B 9.68→2.75 GB（71.6%）；A2T 分别从 69.90 / 41.61 到 66.68 / 39.95，WER/CER 最多升 1.19 个百分点。
- Mini-Omni 音频到文本 decode 峰值 169.5 token/s；实时门槛写成 12.5 token/s。平均板功耗 26 W（xbutil），带宽利用率 94%。硬件环 158 天、705 版；软件环在 GLM-4-Voice 上 36 分钟 1.79 token/s，19.5 小时、127 版后 12.52 token/s。
