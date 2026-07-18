---
type: Summary
title: 'HCache: Fast State Restoration in LLM Serving'
description: EuroSys '25 HCache — restore conversational state from hidden activations; 6× less compute than recompute, 2× less I/O than KV offload; up to 5.73× TTFT gain
tags:
- inference
- serving
- kv-cache
- cache
- storage
- latency
- serving-system
- llm
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/HCache_Fast_State_Restoration_LLM_Serving_2025.pdf
---

# HCache: Fast State Restoration in LLM Serving

**Authors:** Shiwei Gao, Youmin Chen, Jiwu Shu | **Affiliation:** Tsinghua University | **PDF:** [raw/papers/HCache_Fast_State_Restoration_LLM_Serving_2025.pdf](raw/papers/HCache_Fast_State_Restoration_LLM_Serving_2025.pdf)

## 一句话总结

HCache 在 **stateful serving**（多轮对话/RAG）中从 **hidden state**（约为 KV 一半）恢复上下文：并行 I/O + 轻量 GEMM 重建 KV，相对全量 recompute **6×** 省算力、相对 KV offload **2×** 省 I/O，TTFT 最高 **5.73×** 加速。

## 核心贡献

1. **Hidden-state restoration**：介于 recompute 与 KV offload 之间的 Pareto 点，同时利用 GPU 算力与 IO
2. **Bubble-free restoration scheduler**：硬件上 recompute/IO 完成时间不匹配时组合互补方法消 pipeline bubble
3. **Chunk-based storage manager**：解决 layer-before-token 写入 vs token-before-layer 读取的布局冲突
4. **Stateful trace 动机**：A100-40GB 仅缓存 **7–20** 路多轮或 **1–3** 个长上下文
5. **Serving 集成**：相对 AttentionStore、DeepSpeed-MII 等 SOTA 的 TTFT 优势

## 关键数字

| 设置 | 结果 |
|------|------|
| Compute vs recompute | **6×** reduction |
| I/O vs KV offload | **2×** reduction |
| TTFT vs KV offload | Up to **1.93×** faster |
| TTFT vs recomputation | Up to **5.73×** faster |
| Storage vs KV offload | **1.92–2.40×** less |
| TBT overhead | **<4%** |

## 与 wiki 交叉引用

- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — GPU KV cache 管理与 eviction
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 跨请求/state 的 serving 架构
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 有限 GPU memory 下的上下文复用压力
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — TTFT 与 history prefill/recompute 成本
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — host storage + GPU 混合 state 路径

# Citations

[1] [raw/papers/HCache_Fast_State_Restoration_LLM_Serving_2025.pdf](raw/papers/HCache_Fast_State_Restoration_LLM_Serving_2025.pdf) — Gao et al. (EuroSys '25)
[2] [raw/papers/hcache-fast-state-restoration.md](raw/papers/hcache-fast-state-restoration.md) — 结构化摘录
