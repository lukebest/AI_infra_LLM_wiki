---
type: Summary
title: 'Cache-Resident LLM Inference in GB-Scale LLCs'
description: KAUST cache-resident CPU inference — weight/attention domain split + sub-operator sync; 2.04–11.51× TPOT vs llama.cpp on Llama-3.2-3B/2-7B
tags:
- inference
- cache
- cpu
- memory
- llm
- kv-cache
- parallelism
- optimization
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Cache_Resident_LLM_Inference_GB_LLC_2026.pdf
---

# Cache-Resident LLM Inference in GB-Scale LLCs

**Authors:** Wanning Zhang, Tongzhou Gu, Marco Canini, et al. | **Affiliations:** KAUST, HKUST | **PDF:** [raw/papers/Cache_Resident_LLM_Inference_GB_LLC_2026.pdf](raw/papers/Cache_Resident_LLM_Inference_GB_LLC_2026.pdf)

## 一句话总结

在 **GB-scale 3D-stacked LLC** 的 server CPU 上，将 **weight-centric** 与 **attention/KV** 解耦到独立资源域，并把同步从 operator 边界细化到 sub-operator 依赖，相对 llama.cpp 实测 **2.04–11.51×** TPOT，模型外推最高 **13.9×**。

## 核心贡献

1. **Cache-residency 瓶颈刻画**：PP 加深 → in-flight KV 与 weight 争用同一 LLC — fundamental scalability limit
2. **Weight–attention 解耦架构**：静态 weight 复用 vs per-query KV state 分域放置
3. **Sub-operator scheduling**：attention head 等语义独立子计算减少 LLC 下无谓 barrier
4. **Multi-socket CPU 原型**：locality-aware placement + specialized static runtime
5. **Commodity CPU 可行性**：GB LLC + 依赖感知协调可高效 serving memory-dominated LLM

## 关键数字

| 设置 | 结果 |
|------|------|
| TPOT vs llama.cpp (Llama-3.2-3B, 2-7B) | **2.04×–11.51×** |
| Extrapolated TPOT | Up to **13.9×** |
| Extrapolated throughput | Up to **12.5×** |
| Platform | Multi-socket server CPU, GB-scale LLC |

## 与 wiki 交叉引用

- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — KV 管理 vs CPU cache-resident 路径
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — decode memory-bound 算子特征
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — weight residency 主要优化 decode 数据移动
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — weight/attention 分域与 disagg 动机对照
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — CPU vs GPU 推理 placement

# Citations

[1] [raw/papers/Cache_Resident_LLM_Inference_GB_LLC_2026.pdf](raw/papers/Cache_Resident_LLM_Inference_GB_LLC_2026.pdf) — Zhang et al. (2026)
[2] [raw/papers/cache-resident-llm-inference-llc.md](raw/papers/cache-resident-llm-inference-llc.md) — 结构化摘录
