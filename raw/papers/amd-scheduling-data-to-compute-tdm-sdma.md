---
type: Raw Source
title: "Scheduling Data to Compute: Hierarchical Data Pipelining for LLM Training on AMD GPUs"
source_url: https://arxiv.org/abs/2611.05751
pdf: AMD_Scheduling_Data_to_Compute_TDM_SDMA_2026.pdf
retrieved: 2026-11-09
ingested: 2026-11-09
org: Advanced Micro Devices, Inc.
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.05751)

Large language models (LLM) have been the key focus of recent machine learning breakthroughs. As the model size grows exponentially, the computation needed for training is astronomical. A GPU can do a huge amount of arithmetic. However, the data its compute units need is not always available when they are ready. This data may still be in slow memory or on another GPU. While the chip waits, expensive compute sits idle, and at scale even a small drop in utilization translates into substantial cost. In this paper, we treat this waiting time as the primary bottleneck. We focus on hardware features designed for explicit data movement. These features load data from off-chip memory onto the chip, rearrange it into the layout the computation requires as it is loaded, and transfer it between GPUs. By orchestrating them, we keep a steady pipeline of data flowing to the compute units so that they remain busy.

We present kernel and framework implementations that address this bottleneck using three key data-movement instructions and hardware features. The Tensor Data Mover (TDM) moves tensor data from high-bandwidth memory (HBM) into on-chip memory. Transpose-load instructions transpose tensor data into the layout that LLM computations require as it is loaded on-chip. Finally, System DMA (SDMA) and Remote DMA (RDMA) move data between GPUs over the scale-up and scale-out networks, respectively. Our results show that TDM and transpose-load provide on average 1.88× and 1.19× speedup at the kernel level, respectively. The SDMA and RDMA lead to on average 1.16× and 1.33× speedup for computation overlapped with communication. This is the first AMD LLM training system to utilize all the GPU data pipelining features. Our implementation has been integrated into open source framework and library for AMD GPUs. https://github.com/AMD-AGI/Primus-Turbo https://github.com/AMD-AGI/Primus

# Excerpts / key facts

- Contact: lorrirao@amd.com (AMD Primus / Primus-Turbo).
- First AMD LLM training system using all GPU data-pipelining features: TDM (MI455), transpose-load, SDMA, RDMA.
- TDM CSA kernels geometric mean **1.88×** step (up to **2.74×**); transpose-load avg **1.19×** (up to **1.21×**, excluding spill cases).
- SDMA overlapped region avg **1.16×**; hierarchical SDMA+RDMA makes overlapped GEMM avg **1.33×** faster than CU-based on 16/32 GPU.
- CSA = Compressed Sparse Attention (DeepSeek V4 style).
