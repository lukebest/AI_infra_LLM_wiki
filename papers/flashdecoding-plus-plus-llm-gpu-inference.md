---
type: Summary
title: 'FlashDecoding++: Faster Large Language Model Inference on GPUs'
description: 异步 unified-max softmax + M=8 flat GEMM 双缓冲 + FastGEMV/CUTLASS 启发式 dataflow；decode 相对 HF 最高 4.86×、FlashDecoding 平均 1.37×，NVIDIA/AMD 双平台
tags:
- inference
- llm
- gpu
- decode
- attention
- kernel
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf
---

# FlashDecoding++: Faster Large Language Model Inference on GPUs

**Authors:** Ke Hong, Guohao Dai, Jiaming Xu, Qiuli Mao, et al. (Tsinghua, SJTU, PKU, Infinigence-AI) | **Venue:** arXiv:2311.01282v4, Jan 2024 | **PDF:** [raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf](raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf)

## 一句话总结

针对 LLM **decode** 的三类 kernel 瓶颈——FlashDecoding 式 **partial softmax 同步（~19%）**、cuBLAS **M pad-64 导致 flat GEMM 算力浪费（>50%）**、**静态 Tensor Core dataflow**——FlashDecoding++ 提出 **统一 ϕ 的异步 softmax**、**M pad-8 + 双缓冲 flat GEMM**、以及 **FastGEMV / flat GEMM / CUTLASS 按 M 拐点启发式切换**，在 A100 上相对 FlashDecoding 平均 **1.37×**、相对 Hugging Face 最高 **4.86×**。

## 核心贡献

1. **Asynchronized softmax with unified max value** — 各 partial tile 独立累加，消除跨 tile max 同步；越界回退同步路径
2. **Flat GEMM optimization with double buffering** — M 维仅 pad 到 8；大 N 时 shared memory 双缓冲 hide latency
3. **Heuristic dataflow with hardware resource adaptation** — 每模型 4 种 [N,K]；离线 profile M1/M2，运行时 CUDA Core GEMV ↔ Tensor Core GEMM 查表
4. **跨平台引擎** — PyTorch 前端 + CUDA/ROCm 后端；Llama2/OPT/ChatGLM2；NVIDIA + AMD 验证

## 关键数字

| 指标 | 值 |
|------|-----|
| Attention 同步开销（基线） | **18.8%**（Llama2-7B, A100, seq=1024） |
| M pad-64 算力浪费 | **>50%** |
| 静态 dataflow 损失 | 最高 **50.25%** |
| Decode vs HF（NVIDIA peak） | **4.86×** |
| Decode vs FlashDecoding（A100 avg） | **1.37×** |
| Decode vs HF（AMD MI210 peak） | **3.93×** |
| Prefill vs HF | 最高 **1.40×** |

## 与 wiki 交叉引用

- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — 三项机制与推理栈位置
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode GEMV/flat GEMM 与 BW-bound
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 算法层 decode 加速（正交）
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 系统层 prefill/decode 分硬件
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — decode 吞吐与 KV 饱和

# Citations

[1] [raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf](raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf) — Hong et al. (2024)
