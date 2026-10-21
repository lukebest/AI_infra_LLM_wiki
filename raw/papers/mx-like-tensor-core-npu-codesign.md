---
type: Raw Source
title: "MX-Like Tensor Core for LLM Inference with NPU Integration via Hardware-Software Co-Design Exploration"
source_url: https://arxiv.org/abs/2610.26083
pdf: MX_Like_Tensor_Core_NPU_CoDesign_2026.pdf
retrieved: 2026-10-21
org: KU Leuven MICAS et al. (SNAX NPU platform)
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.26083)

Block-scaled quantization formats such as OCP Microscaling (MX) and NVFP4 have been widely adopted as efficient data formats for LLM inference. However, the design space of these formats spanned by shared scale, weight, and activation format combinations has not been systematically explored, and the joint accuracy-silicon tradeoff across this space remains uncharacterized, leaving the true Pareto-optimal configurations for NPU-based edge LLM deployment an open question. To bridge this gap, we conduct a joint hardware-software (HW-SW) co-design exploration of the above underexplored MX-like design space with three innovations. 1) We define and systematically characterize the full 8-bit scale format family within the MX-like design space, jointly with asymmetric weight-activation precision, identifying configurations that outperform the MX and NVFP4-like (without per-tensor scaling, PTS) baselines. 2) We build a per-format specialized MAC datapath template that enables fair hardware cost evaluation across the space. 3) We develop an automated co-design flow, integrated into the open-source SNAX NPU platform, that enables joint HW-SW analysis across the design space. Overall, our co-design exploration reveals that scale format matters only under aggressive FP4 quantization, yielding a case-oriented design guideline for both scale format and asymmetric weight-activation precision. We further identify UE5M3 as a favorable accuracy-hardware tradeoff for the FP4 regime, reducing perplexity degradation by up to 25.3% relative to the NVFP4-like baseline, at a cost of only +0.06% area and +0.49% power overhead.

# Excerpts / key facts (from arXiv HTML v1)

- Setup: TSMC 28 nm, 400 MHz, 0.8 V TT; 4x16 PE array in SNAX cluster; models Qwen2.5-3B, Qwen3-1.7B, Llama-3.2-1B, Gemma-3-1B on WikiText-2 / C4.
- Accumulator holds 39-66% of MAC area; fractional-scale multiplier up to 36%.
- Above A6W6, UE8M0 is Pareto-optimal; fractional scale adds up to +22% system power and +17% area with no accuracy gain.
- FP4 regime: UE4M4 scale lowers mean dPPL from 45.0% (UE8M0) to 17.9%; overhead there +4.6% area, +20.8% power.
- Of 126 configurations, 60 draw both less area and power (system level, Sec 4.3).
