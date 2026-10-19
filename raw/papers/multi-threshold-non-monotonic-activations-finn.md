---
type: Raw Source
title: "Compiling Multi-Threshold Operators for Quantized Non-Monotonic and Fine-Granular Activations in Custom-Tailored DNN Accelerators"
source_url: https://arxiv.org/abs/2610.21825
pdf: Multi_Threshold_NonMonotonic_Activations_FINN_2026.pdf
retrieved: 2026-10-19
org: Computer Engineering Group, Paderborn University
venue: arXiv cs.AR (submitted 2026-10-15)
---

# Abstract (verbatim, arXiv:2610.21825)

Aggressive quantization of neural networks can expose activation functions as bottlenecks for efficient hardware acceleration. Implementing quantized activations as multi-threshold operations has been shown to be a promising optimization, allowing for efficient hardware implementation of few-bit activations. However, current implementations are limited to monotonically increasing functions, quantization schemes with one-dimensional (per-channel) granularity and a small set of predefined activation-quantizer combinations. We formalize the multi-threshold representation to extend it to non-monotonic functions and fine-granular parameters, i.e., multi-dimensional thresholds. For automated conversion of quantized function compositions into threshold representation, we propose a systematic approach via algebraic rules integrated into the ONNX-based compiler infrastructure. We experimentally validate our solution on a selection of monotonic and non-monotonic functions by extending the binary search based multi-threshold operator that is integrated into the FINN framework for end-to-end synthesis of custom-tailored FPGA accelerators. The cost of hardware support for non-monotonicity and fine-granularity is characterized in comparison to an alternative approach utilizing existing operators via graph-level decomposition. We compare our method to prior work as well as the approach taken by the hls4ml framework. As an outlook, we demonstrate the prospects of using the multi-threshold representation during the training of a neural network as a form of quantization aware training.

# Excerpts (from arXiv PDF v1)

- Motivation: FINN multi-threshold supports only monotonically increasing functions and predefined activation–quantizer combos (quantized identity, ReLU), granularity limited to the final axis; SIRA relaxes constraints but needs expensive compile-time simulation of the layer tail. Non-monotonic functions such as SiLU are common in modern models.
- Non-monotonic: thresholds with step direction weights (±1); decreasing branches flip comparison with an Ulp-based correction; SiLU inverse via Lambert W principal/secondary branches; x_min = −1 − W(e^−1) ≈ −1.28, y_min ≈ −0.28.
- Setup: FINN+ with PE = 4 along final axis; Vivado 2024.2, Alveo U55C @100 MHz; no DSP/BRAM allowed (LUT-only comparison); RTL simulation; averages over seven random seeds.
- Non-monotonic cost: direct hardware implementation differs by at most a few hundred LUTs vs monotonic; graph-level decomposition total LUT up to 1.5× vs hardware implementation (multi-thresholds 1.6×, dataflow overheads 3.4×; mul+add 4.8k–5.5k LUTs, worst case ~1.05×).
- Fine granularity: per-tensor/per-channel no difference; fine-granular at high bitwidth, graph-level decomposition worst case ~1.9× from per-tensor to 3-channel, direct hardware ~58× (approaching the naive 64× parameter growth); at β = 4 only ~2.2× difference.
- hls4ml (uniform LUT tables, no operator fusion): fewer resources for simple out-of-box functions but higher quantization error at few bits; multi-threshold allocates intervals to steep regions; with streamlining the whole quantized activation datapath can fit in a few hundred LUTs.
- QAT outlook: LeNet/MNIST, baseline ~99%; allowing ≤2 pp drop, models quantize down to 4 steps (~2.32 bit) for both learned thresholds and hand-selected activations.
