---
type: Summary
title: 'PRESERVE: Prefetch Weights and KV-Cache in Distributed LLM Serving'
description: Huawei PRESERVE — overlap HBM→L2 weight/KV prefetch with collective comm; up to 1.6× E2E speedup; optimal L2 104 MB yields 1.25× perf/$ 
tags:
- inference
- serving
- kv-cache
- memory
- hbm
- cache
- communication
- parallelism
- serving-system
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/PRESERVE_Prefetch_Weights_KV_Cache_LLM_Serving_2025.pdf
---

# PRESERVE: Prefetch Weights and KV-Cache in Distributed LLM Serving

**Authors:** Ahmet Caner Yüzügüler, Jiawei Zhuang, Lukas Cavigelli | **Affiliation:** Huawei Zurich Research Center | **PDF:** [raw/papers/PRESERVE_Prefetch_Weights_KV_Cache_LLM_Serving_2025.pdf](raw/papers/PRESERVE_Prefetch_Weights_KV_Cache_LLM_Serving_2025.pdf)

## 一句话总结

PRESERVE 在分布式 decode 中于 **collective communication** 期间从 HBM **prefetch 权重与 KV-cache 至 L2**，overlap 通信与内存读，商业加速器上最高 **1.6×** 端到端加速；考虑 prefetch 的最优 L2 **104 MB** 带来 **1.25×** perf/$。

## 核心贡献

1. **Comm-overlap prefetch**：突破仅 fuse 相邻 GEMM+allreduce 的限制，KV 路径亦可 hide latency
2. **Graph optimization pass**：编译期插入 prefetch 流、跟踪 L2 占用上限防 cache pollution
3. **Weight + KV 联合 prefetch**：长上下文下 KV 读可超过 weight — 二者同等关键
4. **Decode memory-bound 分析**：OI ~16 Op/word vs roofline >100 — HBM BW 主导
5. **Accelerator DSE**：prefetch-aware 最优 on-chip cache 显著大于传统 8 MB 基线

## 关键数字

| 设置 | 结果 |
|------|------|
| End-to-end speedup | Up to **1.6×** |
| Optimal L2 (with prefetch) | **104 MB** (vs **8 MB** baseline) |
| Performance per cost | **1.25×** vs baseline design |
| Decode OI (typical) | **~16 Op/word** |
| Example L2 sizes | GB200 **126 MB**, MI300X **256 MB** L3 |

## 与 wiki 交叉引用

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 多设备 collective 与 serving 拓扑
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — KV-cache 布局与分布式 shard
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — decode 低 OI、memory-bandwidth bound
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 设备 idle 于 comm 阶段的利用率损失
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — decode 阶段 HBM 读主导

# Citations

[1] [raw/papers/PRESERVE_Prefetch_Weights_KV_Cache_LLM_Serving_2025.pdf](raw/papers/PRESERVE_Prefetch_Weights_KV_Cache_LLM_Serving_2025.pdf) — Yüzügüler et al. (2025)
[2] [raw/papers/preserve-prefetch-weights-kv-cache.md](raw/papers/preserve-prefetch-weights-kv-cache.md) — 结构化摘录
