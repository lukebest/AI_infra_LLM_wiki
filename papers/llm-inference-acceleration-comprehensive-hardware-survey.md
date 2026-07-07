---
type: Summary
title: 'Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective'
description: LLM 推理加速硬件最完整综述：HBM-assisted vs SRAM-based 双路线、Quantization/Sparse/Speculative/Paged 关键专题、典型 FPGA/SoC 数据点
tags:
- survey
- llm
- inference
- hardware
- quantization
- speculative-decoding
- sparse-attention
- fpga
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/papers/LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf
---

# LLM Inference Acceleration: A Comprehensive Hardware Perspective

**arXiv:** [2410.04466v4](https://arxiv.org/abs/2410.04466) (2024) | **PDF:** [raw/papers/LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf](LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf)

## 一句话总结

目前最完整的 **LLM 推理加速硬件综述**。系统梳理 HBM-assisted / SRAM-based 两大路线，覆盖 GPU/TPU/ASIC/FPGA/wafer-scale，并按 **quantization / sparse attention / speculative decoding / paged attention / batching / HW-SW co-design** 六大专题组织。

## 典型平台数据

| 平台 | 工艺 | 模型 | 吞吐 | 功耗 |
|------|------|------|------|------|
| HBM-assisted FPGA (Alveo U280) | 16nm | Llama-7B | 290 tok/s | 46W |
| HBM-assisted FPGA (Alveo U280) | 16nm | Llama-2.7B | 727 tok/s | 46W |
| SoC FPGA (Zynq KV260) | - | 4-bit LLaMA2-7B | 4.9 tok/s | 6.57W |
| MEADOW (TPHS dataflow) | - | LLaMA | - | - |

**HBM-assisted 与 SRAM-based 的能耗差距 1-2 个数量级**（HBM 64-256 GB/s/W vs SRAM 100s TB/s/W）。

## 六大专题要点

1. **Quantization**（INT8/INT4/FP8/MXFP4）：与 tensor parallelism 协同，W4A8 是 LLM 推理 sweet spot
2. **Sparse attention**（long context）：减少 KV cache 内存 + attention FLOPs，是长 context 关键
3. **Speculative decoding**：Medusa、EAGLE、Lookahead —— 通过并行验证实现 2-4× 加速
4. **PagedAttention**（vLLM）、Continuous batching、Chunked prefill —— GPU serving 系统层面
5. **Hardware-software co-design** — 量化/稀疏/数据流的编译器融合
6. **Disaggregated inference** — prefill/decode 分离部署

## 与 wiki 已有内容关联

- [WaferLLM System](/concepts/waferllm-system.md) — WSE 上的 LLM 推理代表
- [FlashAttention 系列](/concepts/flashattention.md) — IO-aware attention
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — MoE 推理 kernel
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — KV cache 内存管理（计划补）
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 投机解码
- [Cerebras WSE](/entities/cerebras-wse.md) — SRAM-based 路线代表
- [Groq LPU](/entities/nvidia-groq-3-lpx.md) — Deterministic pipeline 路线
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — prefill/decode 分离
- [FP4 QAT](/concepts/fp4-qat.md) — 量化专题

# Citations

[1] [raw/papers/LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf](raw/papers/LLM_Inference_Acceleration_Comprehensive_Hardware_Survey_2024.pdf) — (2024)
