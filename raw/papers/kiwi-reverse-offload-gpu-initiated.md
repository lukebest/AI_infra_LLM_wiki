---
type: Raw Source
title: "A Fast, Programmable GPU-to-CPU Invocation Layer for GPU-Initiated Communication"
source_url: https://arxiv.org/abs/2611.23848
pdf: KIWI_Reverse_Offload_GPU_Initiated_2026.pdf
retrieved: 2026-11-20
ingested: 2026-11-20
org: Advanced Micro Devices, Inc.
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.23848)

Modern GPU workloads increasingly rely on device-initiated communication to let GPU kernels communicate directly without synchronizing with the host at kernel boundaries. Existing libraries commonly favor placing transport control on GPU threads, an approach known as GPUDirect Async (GDA), and treat reverse offload to host proxy threads as a slower fallback. We argue that reverse offload can outperform GDA and should be a first-class communication path. We further propose exposing reverse offload as a programming interface that lets users define workload-specific communication operations. We present KIWI, a programmable reverse-offload framework that achieves sub-microsecond one-way device-to-host latency and hundreds of millions of operations per second. We address practical challenges of scaling reverse offload, including contention on shared queues, polling overhead, and load imbalance across proxies. KIWI-P2P, a SHMEM-like library built on KIWI, outperforms state-of-the-art GDA implementations in both latency and bandwidth. More importantly, KIWI-EP redesigns low-latency mixture-of-experts dispatch and combine kernels around workload-defined operations, lowering expert-parallel communication latency by up to 2.3× over the best existing backend on AMD GPUs and time per output token in vLLM by up to 29%. The source code of KIWI is available at https://github.com/AMDResearch/kiwi.

# Excerpts / key facts

- Authors: Jiakun Yan, Shiksha Patel, David Sidler, Gengyu Rao, Brandon Potter, Bradford Beckmann（Advanced Micro Devices, Inc.）。arXiv:2611.23848，cs.DC / cs.LG，提交标注 18 Nov 2026。11 pages。
- 平台：每节点 8×MI300X + 8×400 Gb/s ConnectX-7 RoCE，Xeon Platinum 8480+。数据点为至少三次运行的中位数。
- Table III：KIWI 队列 RTT 中位 1.92 µs，与 raw store 相同；256 wave 自有队列 392.0 Mops/s，为最好已有队列的 3.3×。EP 相对最好已有后端最高 2.3×；vLLM 上 GLM-5.3、PD 解耦，八节点 TPOT 最高 −29%。
