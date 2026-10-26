---
type: Raw Source
title: "Reorienting the Vector Axis: Restructuring FlashAttention for Long-Vector Processors"
source_url: https://arxiv.org/abs/2610.29489
pdf: FlashAttention_Long_Vector_RISCV_2026.pdf
retrieved: 2026-10-26
org: Barcelona Supercomputing Center; UPC
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.29489, arXiv listing version)

A Transformer is built around attention, whose cost grows with the square of the sequence length and dominates the layer on long sequences. FlashAttention made that cost manageable by tiling the attention matrix and updating the softmax as it goes, but almost all work since has targeted GPUs. On long-vector processors one vector register can hold up to 512 single-precision numbers. The savings of a vector instruction are proportional to how much of the register it uses, so the choice of which loop to vectorize is a first-order decision. We port PyTorch's CPU FlashAttention kernel to a RISC-V CPU with 2KB vector registers and find that it reaches 16.2% of peak floating-point throughput. The kernel walks each tile one query row at a time: the product against V is vectorized along the 64-element head dimension, the softmax's per-row maximum and sum are reductions that collapse a full register to a scalar, and the software exponential's polynomial coefficients compete with tile data for vector registers and cause spilling. We propose two techniques. The first transposes the score tile and the running output so that queries lie along the contiguous axis. The algorithm and its values are unchanged. A single parameter, the number of queries in a tile, now sets the vector length of every part of the kernel and can be matched to the machine. Both reductions also disappear. The second moves the polynomial's coefficients into scalar registers, removing the spills and cutting the softmax's vector memory instructions by 78.7%. On silicon the two together cut whole-kernel cycles by 1.84 to 2.08x at a head dimension of 64, raising floating-point utilization from 16.2% to 29.7% of peak. An FPGA of the same design ranks the changes identically and scores them higher, at 2.71x.

# Excerpts / key facts (from PDF)

- Platform: EPAC (European Processor Initiative) RVV core, 16,384-bit vector registers (32× commercial RVV silicon / A64FX; equal to NEC SX-Aurora); chip 1 GHz, FPGA 50 MHz; chip memory 6–7 B/cycle vs FPGA 32 B/cycle (SerDes link to DDR4).
- Stock kernel = PyTorch CPU FlashAttention-2 forward, ported with RVV intrinsics; exp via polynomial (no hardware exp).
- Stock budget at N=1024, d=64, FP32, best tile Bq=128/Bkv=512: softmax 38%, value product 36% of cycles.
- Per-arm best: scalar coefficients 1.13×, + fused traversal 1.29×, + reorientation instead 1.84×; reoriented vs fused 1.43× (40.23 vs 28.22 Mcyc); reoriented best at Bq=512, Bkv=128.
