---
type: Raw Source
title: "A Differential Computing Accelerator for LLM Inference Leveraging Bit-Slice Transition Sparsity"
source_url: https://arxiv.org/abs/2611.34630
pdf: ISTS_Bit_Slice_Steiner_LLM_Accelerator_2026.pdf
retrieved: 2026-11-27
ingested: 2026-11-27
org: University of Science and Technology of China
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.34630)

To accelerate the GEMM operations that dominate LLM computation, bit-slice architectures decompose quantized operands along the bit dimension, exposing slice-level sparsity and redundancy. Existing bit-slice designs primarily exploit sparsity in high-order slices, while dense low-order slices still offer substantial untapped reuse opportunities. We observe that bit-slice vectors (BSVs) are highly clustered in Hamming space, with many BSVs lying only a few bit flips away from a small set of representative patterns. We propose ISTS, an algorithm-hardware co-designed accelerator that leverages representative BSV patterns as shared Steiner points to reuse partial sums across slices. The partial sum of each target BSV can be reconstructed from that of its assigned Steiner point using only a few additions or subtractions. On the algorithmic side, Steiner Absorption Table Construction (SATC) selects a compact set of Steiner points, while FlipPrune selectively prunes flips. On the hardware side, a lightweight accelerator supports Steiner reuse for static linear layer weights and runtime-generated attention K/V tensors. Comprehensive evaluations show that ISTS achieves average speedups of 3.09×, 2.41×, 2.18×, 1.27×, and 1.41× over ANT, BBS, LUT Tensor Core, Transitive Array, and MCBP-BRCR, respectively.

# Excerpts / key facts

- Authors: Yifan Wang, Zetao Guo, You Xiao, Wendi Sun, Song Chen。中国科学技术大学。arXiv:2611.34630，cs.AR，Thu 26 Nov 2026 公告。方法名 ISTS。
- 评估：28 nm、500 MHz RTL 综合；CACTI 7.0 SRAM；DRAMSim3 DDR4；基于 ANT 的周期精确仿真并与 RTL 对时。32×32 PE，Bw=10、K=16、G=128；Steiner 缓冲 40 KB。负载为 prompt + 128 token decode，batch 8。
- 平均加速 3.09× / 2.41× / 2.18× / 1.27× / 1.41×，能效 1.67× / 1.52× / 1.41× / 1.17× / 1.22×，对照 ANT / BBS / LUTA / TA-D / MCBP-BRCR。
- PPL 上升：ISTS(C,8)/(A,8) 低于 0.04 / 0.07，ISTS(C,4)/(A,4) 低于 0.05 / 0.08；下游准确率变化在 3.5% 以内。Qwen2.5-7B / LLaMA-2-7B 上 1-bit 修改占权重 1.92% / 2.05%。低位切片处理占总功耗 50.5%–70.2%。
