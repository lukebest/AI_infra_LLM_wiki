---
type: Raw Source
title: 'DynaX: sparse attention acceleration with dynamic X:M fine-grained structured pruning'
source_path: /home/luke/wiki/raw/papers/DynaX_Sparse_Attention_Dynamic_XM_Pruning_2025.pdf
arxiv: ''
doi: '10.1145/3676641.3715991'
zotero: 3HWY3YF7
ingested: 2026-07-17
sha256: c90393f1f55392540968f3f51c865d85454d9a6a8e108ac3c41aaaf5e2435e13
---

# DynaX: sparse attention acceleration with dynamic X:M fine-grained structured pruning

Authors: Xiao Xiong, Zhaorui Chen, Yue Liang, Minghao Tian, Jiaxing Shang, Jiang Zhong, Dajiang Liu (Chongqing University)
Year: 2025 (ASPLOS '25)

Structured notes / key excerpts:

- **Problem**: Self-attention is O(n²); dynamic sparsity helps but faces irregular patterns and heavy prediction overhead.
- **DynaX**: Algorithm-hardware co-design — **dynamic X:M** structured pruning (variable X per group, not fixed N:M).
- **2-step pruning**: Low-bit Q/K precompute score matrix → N:M pruning → X:N pruning; high sparsity with lower prediction memory than fixed N:M.
- **Block scheduling**: Reorganizes score blocks to match PEA (processing element array) for SDDMM + SpMM.
- **Sparsity/accuracy**: **89.54%** (short-seq) and **91.77%** (long-seq) average sparsity with **<1%** accuracy loss.
- **vs Sanger/SALO2 (BERT-base)**: **1.99×** / **1.50×** speedup; **5.16×** / **4.20×** energy efficiency.
- **GPU baseline**: **35.14×** avg speedup vs GPU; **299.23×** energy efficiency improvement on accelerator.
- **Energy**: **25.55 TOPS/W** average on DynaX accelerator.
- **Context**: Attention blocks are **47.1%–93.4%** of compute on long-seq BERT/ViT workloads.
