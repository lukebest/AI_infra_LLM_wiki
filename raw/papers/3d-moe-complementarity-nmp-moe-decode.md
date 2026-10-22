---
type: Raw Source
title: "3D-MoE: Complementarity-Guided Hardware-Software Co-Design for MoE Decode on 3D-Stacked NMP"
source_url: https://arxiv.org/abs/2610.26991
pdf: 3D_MoE_Complementarity_NMP_MoE_Decode_2026.pdf
retrieved: 2026-10-22
org: SKLP, ICT CAS; UCAS; University of Edinburgh
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.26991)

Mixture-of-Experts (MoE) have become a mainstream way to scale Large Language Models (LLMs), because each token activates only a small subset of experts, reducing inference cost. However, MoE decode remains highly memory-bound and exhibits strongly skewed, time-varying expert loads. 3D-stacked DRAM near-memory processing (NMP) provides the bandwidth that decode demands, yet its tiled organization makes load balancing expensive: expert parallelism (EP) preserves locality but suffers from hotspot-induced imbalance, while more distributed strategies weaken locality and increase NoC traffic. To address this locality-balance conflict, we observe that domain-specialized token routing creates offsetting expert-load fluctuations across decode steps, a property we call expert complementarity. Using this insight, we propose 3D-MoE, a hardware--software co-designed system for MoE decode on 3D-stacked NMP. 3D-MoE uses offline, one-time complementarity-guided grouping and locality-aware mapping to establish coarse-grained inter-group balance, handles residual intra-group hotspots through a lightweight Collaborative Memory-Network (CMN) that streams each hot expert's weight tiles once from its host DRAM channel to helper cores over a reconfigured local broadcast path, and uses cost-aware online remapping to remain robust to workload drift. Across MoE models, 3D-MoE achieves an average 4.63x MoE-layer speedup over EP and improves end-to-end throughput by 1.58x-1.86x over the strongest NMP baselines, with 2.11% additional logic-die area.

# Excerpts / key facts (from arXiv PDF v1)

- MoE layers account for 83-92% of end-to-end latency at batch 64; hottest expert can receive over 20x the step-average load; NoC overhead reaches 52% in distributed strategies (authors' analysis).
- Complementarity is prevalent: 82.2%-88.3% of experts have complementary partners; 70.6%-80.5% of partners transfer across datasets; retention over 256-step windows 94.5% / 92.7% / 90.8%.
- System: 4 NMP stacks (2x2), each 16-GB 8-hi DRAM, 16 channels, 16 NMP cores in 4x4 mesh (512-bit links, 2 cycles/hop); core 650 MHz, 1.33 TFLOPS, 166.4 GB/s local DRAM BW, 64-KB buffer; inter-stack 128 GB/s/direction; xPU 0.99 PFLOPS, 2.68 TB/s xPU-stack HBM BW.
- Models: DeepSeek-V2-Lite, Qwen3-30B-A3B, GLM-4.5-Air; datasets ShareGPT, MATH, HumanEval; GPU baselines vLLM 0.8.1 on H100.
- MoE-layer decode: average 5.87x / 4.63x / 1.72x over GPU / EP / HD-MoE; 83% average compute utilization (>4.25x static strategies); 1.93x / 1.59x / 1.84x utilization of best NMP baseline.
- End-to-end: 1.58x-1.86x over strongest NMP baseline; vs GPU 5.54x / 7.88x / 6.95x; DeepSeek-V2-Lite batch 64 p50/p90/p99 TBT -45.3% / -43.7% / -26.0% vs HD-MoE.
- Online remapping: 0.87% exposed end-to-end overhead. Area: +2.11% logic-die area.
