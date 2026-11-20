---
type: Raw Source
title: "HETEROVLM: Edge Multi-Request Vision-Language Model Serving on a Heterogeneous Versal SoC with AI Engines and Programmable Logic"
source_url: https://arxiv.org/abs/2611.23878
pdf: HETEROVLM_Versal_AIE_VLM_Serving_2026.pdf
retrieved: 2026-11-20
ingested: 2026-11-20
org: University of California, Irvine
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.23878)

Edge devices in vehicles and robots serve concurrent requests with different deadlines to a vision-language model (VLM), each mixing a compute-bound encoder and prefill with a memory-bound decode. GPU serving targets datacenter throughput with per-iteration host scheduling: an urgent request waits for the running iteration, and small-batch decode costs much energy per token. Prior accelerators on Versal AI Engine (AIE) SoCs map one model onto a fixed AIE dataflow graph for one input stream, without decode or request scheduling. HETEROVLM keeps the AIE graph static and makes it schedulable. The AIE array runs the encoder, prefill and attention, and the programmable logic (PL) holds GEMV engines for small decode steps and a scheduler that orders short work units by class and deadline. Concurrent requests share one decode step that reads the weights once. An urgent request preempts at a work-unit boundary, and the paused request resumes from its results in DDR. On an AMD Versal VC1902, text and camera questions get their first tokens in 140 and 303 ms. HETEROVLM decodes a single request 1.3× and 4.0× faster than NVIDIA Tesla T4 and Jetson Orin Nano GPUs, with 61% and 73% of their energy per token, and uses 51% of the energy per token of an NVIDIA GeForce RTX 3090 Ti. The same bitstream serves multiple VLMs by loading their own instruction programs and weights.

# Excerpts / key facts

- Authors: Zhiheng Chen, Yu-An Chou（共同一作），Yifan Zhang, Ye Qiao, Saptarshi Mitra, Sitao Huang（University of California, Irvine）。arXiv:2611.23878，cs.AR，提交标注 18 Nov 2026。
- 平台：Versal VC1902，Vitis 2022.1 + TAPA，PL 240 MHz、AIE 1.25 GHz；DDR4 约 50 GB/s。主模型 LFM2.5-VL-3B。对照 T4 / Orin Nano / 3090 Ti（320 / 102 / 1,008 GB/s），同一模型与 int8 权重。
- Table IV 单请求 decode：66.5 ms/tok、15.0 tok/s、3.56 J/tok、53.6 W。八请求共享步 104.8 tok/s。抢占下紧急镜头首 token 为闲时的 1.00–1.04×。
