---
type: Raw Source
title: "Zero-SM NCCL: A Systematic Guide to Designing and Deploying SM-Free GPU Communication"
source_url: https://arxiv.org/abs/2611.18075
pdf: Zero_SM_NCCL_2026.pdf
retrieved: 2026-11-18
ingested: 2026-11-18
org: ETH Zurich / NVIDIA
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.18075)

GPU communication libraries such as NCCL use Streaming Multiprocessors (SMs) for data movement and synchronization, slowing overlapped computation at a cost that grows with interconnect bandwidth. We present Zero-SM NCCL, which communicates within and across scale-up domains without launching any SM kernel. It synchronizes through CUDA stream memory operations, moves data asynchronously with copy engines within a scale-up domain, and drives network RDMA from a stream-ordered CPU proxy. It supports data-movement collectives such as AllGather and AlltoAll, plus one-sided ncclPutSignal and ncclWaitSignal APIs. On GB200 NVL72 and B200 NVL8 systems, Zero-SM collectives reach up to 1.36x higher AllGather bandwidth than NCCL's legacy SM-based kernels and cut the median slowdown of overlapped GEMMs from 33% to 4%, at a higher latency per operation. In Megatron-LM training, they accelerate FSDP by up to 3.5%, and one-sided puts accelerate pipeline parallelism by up to 15%. Zero-SM communication is not a universal win, however. Through an end-to-end study across models and parallelism strategies, we show that it pays off for large transfers in GPU-bound workloads and for deep pipelines with large bubbles, but loses on small messages and host-bound workloads. We distill these findings into guidelines for enabling zero-SM communication in NCCL and building it into other libraries.
