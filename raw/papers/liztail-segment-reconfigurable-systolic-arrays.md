---
type: Raw Source
title: "LizTail: Unifying Shape Adaptation and Spatial Parallelism with Segment-Reconfigurable Systolic Arrays"
source_url: https://arxiv.org/abs/2610.16159
pdf: LizTail_Segment_Reconfigurable_Systolic_Arrays_2026.pdf
retrieved: 2026-10-16
org: UESTC / Xi'an University of Posts and Telecommunications / Sun Yat-sen University
venue: arXiv cs.AR
---

# Abstract (verbatim, arXiv:2610.16159)

Systolic arrays are widely used to accelerate neural-network inference, yet fixed two-dimensional arrays struggle with the substantial diversity in both matrix geometry and available parallelism across CNNs and Transformer-based large language models. This mismatch is particularly severe for skinny matrices, small-batch autoregressive decoding, and operators containing multiple independent partitions, leading to low processing-element (PE) utilization and repeated spatial folding. Existing reconfigurable arrays typically improve either shape adaptation or distributed execution, whereas supporting both through fine-grained routing incurs considerable interconnect, buffering, and control overheads. We present LizTail, a multi-mode systolic array that enables constrained segment-level reconfiguration by partitioning a 128×128 array into 32 regular 128×4 segments and adding connectivity only at predefined endpoints. The resulting substrate supports trimming, long-path extension through 180° turn-back connections, and distributed execution in which each subarray can itself be trimmed or extended. Differentiated PE datapaths and segment-aware CEB/SIB buffers provide the required compute and data-delivery flexibility without unrestricted PE-level routing. A hardware-constrained mapper selects the execution organization, dataflow, task partition, and tiling. Across representative workloads, LizTail achieves geometric-mean speedups of 5.02× on CNN inference and 25.67× on LLM decoding over a TPU-like array, while reducing EDP by up to 38.23×. LizTail is open-sourced at https://github.com/kmjbwxa/LizTail.

# Excerpts (from arXiv HTML/PDF)

- §1: 128×128 PE array → 32×(128×4) segments; T-Mode trim, E-Mode 180° turn-back extension, P-Mode distributed subarrays with local trim/extend.
- §5.2 / Fig.9: vs TPU-like — GPT-2 XL 27.39×, LLaMA3 8B 27.04×, Qwen3-30B-A3B 22.58×; LLM decode geomean 25.67×. CNN: ResNet-50 2.60×, MobileNetV3-L 8.74×, EfficientNet-B0 3.70×; geomean 5.02×.
- vs ReDas on LLMs: 3.14× / 2.72× / 3.07× faster.
- EDP vs TPU-like: CNN 3.13–11.43× reduction; LLM 38.23× / 37.50× / 31.37×.
- ADP vs TPU-like on LLM decode: 10.67–12.94× reduction.
- Area (28 nm): TPU-like 15.5, Gemmini 16.7, ReDas 20.8, SARA 77.3, LizTail 31.7 mm².
- Default config: 700 MHz, 2 MB CEB + 2 MB SIB, 819 GB/s off-chip BW; TSMC 28 nm.
- PE utilization LLM decode: LizTail 14.91–24.51% vs fixed-array low-single-digit.
- Sensitivity: bs 1→32 speedup 25.57×→7.86×; ctx 1K→128K 25.57×→14.09×.
