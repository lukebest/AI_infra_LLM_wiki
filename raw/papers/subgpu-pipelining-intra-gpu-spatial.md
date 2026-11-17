---
type: Raw Source
title: "SubGPU Pipelining: Intra-GPU Fine-Grained Spatial Parallelism for LLM Inference"
source_url: https://arxiv.org/abs/2611.14904
pdf: SubGPU_Pipelining_LLM_Inference_2026.pdf
retrieved: 2026-11-17
ingested: 2026-11-17
org: NVIDIA
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.14904)

Large language model (LLM) decode is dominated by short, predominantly memory-bound kernels that make bursty use of on-chip execution resources and memory bandwidth. This paper introduces SubGPU Pipelining, a fine-grained, intra-GPU spatial execution model that cuts an operator graph into ordered contiguous segments, binds those segments to spatial stages backed by disjoint streaming-multiprocessor (SM) pools, and streams microbatches through the resulting schedule. Selecting the graph cuts, segment-to-stage binding, per-stage SM allocation, and microbatch size is a coupled optimization problem: each choice changes the overlap pattern, shared-resource contention, cache state, and execution times of the others. We evaluate SubGPU Pipelining through both simulation and silicon experiment using the GPT-OSS 120B workload with 32-GPU B200 deployment settings. The analytical shared-resource simulator searches across SubGPU pipeline structures and batch sizes to map the per-user/per-GPU throughput Pareto frontier. At matched per-GPU throughput, the modeled SubGPU frontier provides up to 2.2x higher per-user throughput than temporal execution, and at matched per-user throughput it provides up to 1.9x higher per-GPU throughput. To test physical feasibility and further validate the simulation results, silicon experiments are performed, using one B200 GPU to emulate a 32-GPU B200 deployment. The experiment evaluates one selected two-stage pipeline configuration at global batch 2,048 using CUDA Green Contexts and TensorRT-LLM kernels. Results show that SubGPU Pipelining improves mean DRAM read-plus-write throughput from 71.8% to 83.6% of peak, and reduces the 36-layer decoder iteration time by 10.33%.
