---
type: Raw Source
title: "A Runtime System for Mitigating Crossbar Port Contention on SM-Partitioned GPUs"
source_url: https://arxiv.org/abs/2611.24458
pdf: GPCPlace_SM_Partitioned_GPU_2026.pdf
retrieved: 2026-11-25
ingested: 2026-11-25
org: The Hong Kong University of Science and Technology (Guangzhou); Tsinghua University
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.24458)

To avoid scheduling delays when running concurrent workloads on a GPU, Streaming Multiprocessor (SM) partitioning mechanisms such as CUDA Green Contexts restrict each workload to separate SMs. Despite this partitioning, concurrent workloads still significantly slow down latency-critical workloads, which recent studies attribute to shared L2 cache and memory contention. However, contention also occurs at the crossbar ports connecting each Graphics Processing Cluster (GPC) of SMs to the L2 cache, as all SMs in a GPC share one port. Green Contexts spread workloads across GPCs, placing concurrent workloads in the same GPCs and forcing latency-critical memory requests to queue behind background requests. Packing workloads into separate GPCs avoids this contention, but forces latency-critical memory requests through fewer ports, limiting memory bandwidth. Consequently, neither spreading nor packing is always faster across workloads and GPUs. Based on these observations, we present GPCPlace, a runtime system that dynamically selects between spreading and packing by profiling workloads on the target GPU to estimate both slowdowns, and hooks kernel launches in the CUDA driver to set SM masks without application modifications. Across 14 GPUs and 112 workload cases, GPCPlace speeds up latency-critical workloads by up to 1.15× on average and 2.38× maximum over Green Contexts without degrading throughput.

# Excerpts / key facts

- Authors: Ziwen Wang, Qi Luo, Kunlin Li, Changxi Liu, Yun Chen（HKUST Guangzhou）；Dongsheng Wang（Tsinghua）。arXiv:2611.24458，cs.DC，提交标注 18 Nov 2026。
- 14 张 NVIDIA GPU，覆盖 Ampere / Ada / Hopper / Blackwell：A800、RTX 3060/3090、RTX A6000、A40、RTX 4080/4090、L4、RTX 5000 Ada、H20、RTX 5070/5090、RTX PRO 6000、DGX Spark。每张卡 112 个并发用例，结果为五次中位数。
- 时延关键负载四种：Llama-3-8B 的 8 层 Triton / cuBLAS GEMM，以及 FlashAttention 仅注意力 decode，均为 batch 16、上下文 2048；再加上 embedding + FFN。后台 12 种，含 LLM prefill、AdamW、GEMV、vector add、encoder、vector search 等。
- 相对 CUDA Green Contexts：各卡平均加速最高 1.15×（Ada 四卡 1.11×–1.15×；Blackwell 最高 1.07×；GDDR Ampere 1.02×–1.04×；A800 / H20 为 1.00×–1.01×），单用例最高 2.38×；中位 STP 为 1.00×。
- All Packed 在 RTX 4090 上可慢到 Green Contexts 的 0.58×；GPCPlace 相对 All Packed 在 4090 上最高 1.68×。
- 一次性开销：TPC→GPC 映射在 14 张卡上均在 3 秒内完成；I/X 每个后台约 2–3 秒，L/D 每个时延关键负载不到 1.5 秒；运行时改 QMD TPC mask 给 kernel launch 增加不到 1 µs。
