---
type: Summary
title: 'Multi-Branch Self-Drafting for LLM Inference Acceleration'
description: AAAI-25 Self-Draft — multi-branch in-model drafting without extra draft model; 2.0–3.2 tokens/step and ~2× throughput vs AR decode
tags:
- inference
- decode
- llm
- optimization
- serving
- transformer
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Multi_Branch_Self_Drafting_LLM_Inference_2025.pdf
---

# Multi-Branch Self-Drafting for LLM Inference Acceleration

**Authors:** Zipeng Gao, Qingrong Xia, Tong Xu, et al. | **Affiliations:** USTC, Huawei Cloud | **PDF:** [raw/papers/Multi_Branch_Self_Drafting_LLM_Inference_2025.pdf](raw/papers/Multi_Branch_Self_Drafting_LLM_Inference_2025.pdf)

## 一句话总结

Self-Draft 将自回归解码扩展为 **multi-branch drafting**：同一 LLM 用 attention mask 并行生成分支 draft 并 verify，无需额外 draft 模型或训练，实现 **2.0–3.2 tokens/step**、端到端吞吐约 **2×**。

## 核心贡献

1. **Training-free self-drafting**：额外 draft branch 与主路径并行，保持 LLM 参数不变
2. **In-context draft cache**：分支 draft + 语料 common expression 联合维护，缓解静态 cache 域偏移
3. **Padding 鲁棒性观察**：噪声 padding 下仍 **>20%** n-gram 与 vanilla 重叠 — 支撑分支 draft 质量
4. **vs 外部 draft model**：避免 serial draft 开销与对齐训练；vs Medusa 类架构修改无需 fine-tune
5. **Huawei Cloud 部署语境**：与 serving 侧 draft-and-verify 生态衔接

## 关键数字

| 设置 | 结果 |
|------|------|
| Accepted tokens / forward | **2.0–3.2** |
| End-to-end throughput vs AR | **~2×** |
| PIA cache mismatch penalty | **>30%** throughput drop (GSM-8K → Dolly-15K) |
| Padding overlap (BLEU/ROUGE) | **>0.2** even with noise |

## 与 wiki 交叉引用

- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — draft-and-verify 谱系与 accepted length 优化
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — decode 步主导延迟，speculative 直接优化 decode
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — 单 token decode 的 memory-bound 特征
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — serving 内存管理与 batch verify
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 更高 tokens/step 对 batch 占用的影响

# Citations

[1] [raw/papers/Multi_Branch_Self_Drafting_LLM_Inference_2025.pdf](raw/papers/Multi_Branch_Self_Drafting_LLM_Inference_2025.pdf) — Gao et al. (AAAI-25)
[2] [raw/papers/multi-branch-self-drafting-llm-inference.md](raw/papers/multi-branch-self-drafting-llm-inference.md) — 结构化摘录
