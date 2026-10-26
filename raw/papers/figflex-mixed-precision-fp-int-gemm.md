---
type: Raw Source
title: "FIGFLEX: A Mixed-Precision FP-INT GEMM Accelerator Co-Designed with Low-Bit LLM Quantization"
source_url: https://arxiv.org/abs/2610.30480
pdf: FIGFLEX_Mixed_Precision_FP_INT_GEMM_2026.pdf
retrieved: 2026-10-26
org: University of California, Irvine
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.30480)

Weight-only quantization keeps LLM activations in floating point and stores weights as low-bit integers, turning the dominant workload into floating-point-integer (FP-INT) general matrix multiplication. Recent quantizers reach a 2-3-bit average with mixed precision, but hardware has not kept pace: GPUs dequantize weights to FP16 before the tensor-core multiply-accumulate, and bit-parallel FP-INT accelerators run at a single weight precision, so fewer bits save memory but not computation. In this paper, we present FIGFLEX, an algorithm-hardware co-designed mixed-precision accelerator whose bit-parallel datapath scales throughput as precision falls. FIGFLEX contributes (1) a shift-add, radix-4 reformulation of FP-INT multiplication that fuses the multiply-accumulate into a unified, precision-flexible partial-product reduction and roughly halves the partial products, together with a novel INT3 optimization that reclaims the idle datapath radix-4 leaves at that precision; and (2) a mixed-precision quantizer that assigns each channel group its bit-width according to the error GPTQ cannot compensate, with a per-input-channel column scaling whose power-of-two normalization keeps the scaled activations out of the FP16 subnormal range, so that the quantized model maps directly onto FIGFLEX's datapath with the same accuracy as on a GPU. On LLaMA-2-7B, FIGFLEX attains 5.85 and 8.77 WikiText-2 perplexity at 3- and 2-bit average precision, lower than GPTQ, AWQ, SliM-LLM, AMQ, and QuIP# (without fine-tuning), while delivering 1.56x and 1.42x higher whole-chip throughput per area on the linear GEMMs of a 3-bit mixed-precision model than AxCore and FIGLUT, respectively.

# Excerpts / key facts (from PDF)

- PE runs INT4/INT3/INT2/INT1 weights at increasing throughput (bit-parallel, radix-4 recoding: one partial product per 2-bit digit).
- INT3 high-bit lane fusion: process INT3 weights in pairs, fuse the two single-bit high digits into one 2-bit lane (no idle half lane).
- Baselines FIGNA, FIGLUT, AxCore reimplemented; Synopsys DC, NanGate 15 nm, 1 GHz.
- At INT4, TOPS/W lead remains 1.18–1.50× over FIGNA (Fig. 9 discussion).
