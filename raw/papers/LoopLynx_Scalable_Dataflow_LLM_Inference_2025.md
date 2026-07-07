---
type: Raw Source
title: 'LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference'
source_path: /home/luke/wiki/raw/papers/LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf
arxiv: '2504.09561'
ingested: 2026-07-07
---

# LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference (Source)

**Authors:** Jianing Zheng, Gang Chen (Sun Yat-sen University) | **arXiv:** [2504.09561v1](https://arxiv.org/abs/2504.09561) (Apr 2025) | **Venue:** IEEE conference (FPGA-class) | **PDF:** [raw/papers/LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf](LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf)

## Abstract (verbatim)

We propose **LoopLynx**, a scalable dataflow architecture for efficient LLM inference that optimizes FPGA usage through a **hybrid spatial-temporal design**. The design incorporates a hybrid temporal-spatial architecture, where computationally intensive operators are implemented as **large dataflow kernels (Macro Dataflow Kernels, MDK)**. This achieves high throughput similar to spatial architecture, and organizing and reusing these kernels in a temporal way together enhances FPGA peak performance. Furthermore, to overcome the resource limitations of a single device, we provide a **multi-FPGA distributed architecture** that overlaps and hides all data transfers so that the distributed accelerators are fully utilized.

## Why

> "the parallel processing capabilities of such dataflow architectures are largely **underutilized in the decoding phase** due to the sequential processing pattern. Moreover, the limited computational resources of a single FPGA make it difficult to achieve optimal end-to-end inference performance."

**Key insight:** 纯 spatial dataflow 在 LLM decode 上"流水线"不连续（token-by-token 串行依赖），需要 spatial 显式 + temporal 隐式的 hybrid。

## Mechanism

1. **Macro Dataflow Kernels (MDK)**: Fused MP / MHA / LN&Res kernels, scheduler 在时序上复用同一组 MDK
2. **Head-wise pipelining**: 重新排列多头注意力计算，把 head_i 的 softmax 隐入 head_{i+1} 的 attention 计算中
3. **Transmission latency hiding**: 多 FPGA 节点间 ring network 同步开销被 dataflow 计算掩盖

## Results

- **GPT-2 (345M)** + W8A8 + AMD Alveo U50 @ 285 MHz
- **2-node**: **1.67×** A100 latency, **2.3×** A100 energy efficiency
- **4-node**: **2.52×** A100, **2.7×** energy; vs DFX (temporal) **2.11×**, vs [6] (spatial) **1.64×**
- 优势集中在长生成（[32:512]、[64:512]、[128:512]）— prefill 短时 GPU 更强（批处理）

## 资源占用（Xilinx Alveo U50 单 SLR 节点）

| 组件 | DSP | LUT | FF | BRAM |
|------|-----|-----|-----|------|
| Fused MP | 522 | 34K | 56K | 241 |
| Fused MHA | 382 | 38K | 45K | 16 |
| Fused LN | 192 | 23K | 30K | 240 |
| DMA | 0 | 16K | 28K | 97 |
| **总节点** | **1128** | **128K** | **185K** | **595** |

> 注：硬件小（FPGA 级别），与 WSE-2 的 850K core 数量级差 3 个；意义在于 **架构范式** 验证。
