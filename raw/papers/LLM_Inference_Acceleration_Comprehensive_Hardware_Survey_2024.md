---
type: Raw Source
title: 'Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective'
source_path: /home/luke/wiki/raw/papers/LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf
arxiv: '2410.04466'
ingested: 2026-07-07
---

# Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective (Source)

**arXiv:** [2410.04466v4](https://arxiv.org/abs/2410.04466) (2024) | **PDF:** [raw/papers/LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf](LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf)

## Scope

目前最完整的 **LLM 推理加速硬件综述**。系统梳理 HBM-assisted / SRAM-based 两大路线，覆盖 GPU/TPU/ASIC/FPGA/wafer-scale，包含典型数据点：

| 平台 | 工艺 | 模型 | 吞吐 | 功耗 |
|------|------|------|------|------|
| HBM-assisted FPGA (Alveo U280) | 16nm | Llama-7B / 2.7B | 290 / 727 tok/s | 46 W |
| Zynq KV260 SoC | - | 4-bit LLaMA2-7B | 4.9 tok/s | 6.57 W |
| MEADOW (TPHS dataflow + mixed precision) | - | LLaMA | - | - |

## 关键技术专题

1. **Quantization** (INT8/INT4/FP8/MXFP4) 与 tensor parallelism 协同
2. **Sparse attention** (long context) — 减少 KV cache 与 attention FLOPs
3. **Speculative decoding** (Medusa、EAGLE、Lookahead)
4. **PagedAttention** (vLLM)、Continuous batching、Chunked prefill
5. **Hardware-software co-design** — 量化/稀疏/数据流的编译器融合

## 与 wiki 已有内容的关联

- [WaferLLM System](/concepts/waferllm-system.md) — WSE 上的 LLM 推理代表
- [FlashAttention 系列](/concepts/flashattention.md) — IO-aware attention
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — MoE 推理 kernel
- [PagedAttention (vLLM)](/concepts/pagedattention.md) — KV cache 内存管理
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 投机解码
- [Cerebras WSE](/entities/cerebras-wse.md) — SRAM-based 路线代表
- [Groq LPU](/entities/nvidia-groq-3-lpx.md) — Deterministic pipeline 路线
