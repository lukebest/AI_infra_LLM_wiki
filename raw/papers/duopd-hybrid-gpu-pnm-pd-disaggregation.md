---
type: Raw Source
title: "A Hybrid GPU and Processing-Near-Memory Architecture with Shared DRAM for Efficient Prefill-Decode Disaggregation"
source_url: https://arxiv.org/abs/2610.26131
pdf: DuoPD_Hybrid_GPU_PNM_PD_Disaggregation_2026.pdf
retrieved: 2026-10-21
org: Seoul National University (SNU VLSI/DRAM group)
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.26131)

The growing adoption of large language models (LLMs) has significantly increased the compute and memory demands of inference serving. A key challenge arises from the mismatch between compute-bound prefill and memory-bound decoding: when executed together, the two phases interfere, while separating them via prefill-decode (PD) disaggregation leads to substantial resource underutilization. Specifically, prefill leaves memory bandwidth underutilized, whereas decoding underutilizes compute resources. Prior approaches, such as GPU Streaming Multiprocessor (SM) partitioning, attempt to improve utilization by spatially dividing GPU resources. However, these approaches remain fundamentally limited, as memory-bound decoding still requires a large number of SMs to saturate bandwidth, reducing the compute resources available for prefill and resulting in an inherent trade-off. To address this limitation, we propose DuoPD, a hybrid PD-disaggregation architecture that integrates lightweight Processing-Near-Memory (PNM) units into the HBM logic die. Unlike prior PIM/PNM designs that rely on costly internal bandwidth scaling and offload only partial decoding operations, DuoPD enables full decoding execution on PNM by leveraging bandwidth sharing with the GPU over a shared HBM interface. This allows compute-bound prefill and memory-bound decoding to execute concurrently with minimal interference, improving both compute and memory utilization. To realize this design, we develop a compact PNM microarchitecture, a TSV-level bandwidth sharing mechanism, and a hierarchical data mapping scheme tailored for hybrid GPU-PNM execution. Evaluations on server-scale LLMs demonstrate that DuoPD achieves up to 2.23x higher end-to-end throughput than conventional PD-disaggregation.

# Excerpts / key facts (from arXiv HTML v1)

- Setup: eight GPU chips, each with eight HBM4 stacks (2 TB/s, 48 GB per stack); GPU 2.5 PFLOPS FP16 (GB300-like); PD instances linked by NVLink5 900 GB/s.
- PNM: SIMD PEs at 1 GHz, 16 lanes x 1,024 FP16 multipliers, 32 TFLOPS peak, 1 MB SRAM buffer.
- Throughput: average 1.46-2.23x on GPT3-175B, 1.29-1.61x on LLaMA2-70B, 1.45-1.78x on Qwen3-235B-A22B.
- SM partitioning: 5:5 matches DuoPD TPOT but TTFT 1.93x/1.66x worse; 9:1 matches TTFT but >5x higher TPOT.
- Area: HBM4 logic die ~140.8 mm2, 38.6 mm2 free after TSV/PHY; PNM total 6.51 mm2 (7 nm scaled; SIMD 3.64, buffer 1.25, vector 1.56).
