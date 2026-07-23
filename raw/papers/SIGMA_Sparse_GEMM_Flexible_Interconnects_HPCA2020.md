---
type: Raw Source
title: 'SIGMA: A Sparse and Irregular GEMM Accelerator with Flexible Interconnects for DNN Training'
source_path: /home/luke/wiki/raw/papers/SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf
arxiv: ''
ingested: 2026-07-22
---

# SIGMA (Source)

**Authors:** Eric Qin, Ananda Samajdar, Hyoukjun Kwon, Vineet Nadella, Sudarshan Srinivasan, Dipankar Das, Bharat Kaul, Tushar Krishna (Georgia Tech + Intel) | **Venue:** HPCA 2020 | **PDF:** [raw/papers/SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf](SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf)

## Abstract (verbatim)

> "This paper proposes SIGMA, a flexible and scalable architecture that offers high utilization of all its processing elements (PEs) regardless of kernel shape and sparsity. Within SIGMA includes a novel reduction tree microarchitecture named Forwarding Adder Network (FAN). SIGMA performs **5.7× better than systolic array architectures** for irregular sparse matrices, and roughly 3× better than state-of-the-art sparse accelerators."

## Three trends motivating SIGMA

1. **Irregular (non-square) GEMM dimensions** (from minibatch, factorization)
2. **Weight sparsity** (pruning) + **activation sparsity** (ReLU, pooling, dropout), varies 10-90%
3. **Rapid model evolution** → fixed systolic arrays fall behind

## Key innovation: Flex-DPE + FAN

**Flex-DPE (Flexible Dot Product Engine)** = **basic compute tile** with rich interconnect
- Each Flex-DPE is a tree of MACs
- Inter-Flex-DPEs via **global NoC** → cluster into **Flex-DPU** of arbitrary shape
- **SIGMA can morph**: one large Flex-DPU running one GEMM, **OR** multiple small Flex-DPUs running parallel GEMMs

**FAN (Forwarding Adder Network)** = **partial-sum forwarding** across clusters
- Avoids fixed hierarchical reduction
- Adaptable to **sparse / dynamic patterns**

## Results

- **5.7× speedup** vs systolic arrays on irregular sparse matrices
- **3× speedup** vs SOTA sparse accelerators
- **10.8 TFLOPS efficiency** across arbitrary sparsity levels
- 65.10 mm², 22.33 W at **28 nm**
- Layout capability: arbitrary GEMM shape + arbitrary sparsity distribution

## Significance

**Extends MAERI to sparse + training** — proves flexible NoC is critical not just for inference, but for **sparse + training workloads** that are even more irregular.