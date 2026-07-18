---
type: Summary
title: 'CODE PLAN: Scaling Code-Form Planning for LLM Reasoning'
description: Wen et al. — code-form pseudocode plans auto-mined at scale; 2M-example training; 25.1% relative gain on 13 multi-step reasoning benchmarks
tags:
- reasoning
- llm
- training
- model
- optimization
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Code_Form_Planning_Scaling_LLM_Reasoning_2024.pdf
---

# CODE PLAN: Scaling Code-Form Planning for LLM Reasoning

**Authors:** Jiaxin Wen, Jian Guan, Hongning Wang, Wei Wu, Minlie Huang | **Affiliations:** Tsinghua University, Ant Group | **PDF:** [raw/papers/Code_Form_Planning_Scaling_LLM_Reasoning_2024.pdf](raw/papers/Code_Form_Planning_Scaling_LLM_Reasoning_2024.pdf)

## 一句话总结

CODE PLAN 让 LLM 先生成并遵循 **code-form 伪代码计划**再作答；从海量语料自动抽取 **2M** ⟨prompt, plan, response⟩ 训练，在 **13** 个多步推理基准上相对直接生成平均 **+25.1%**，复杂任务增益更大。

## 核心贡献

1. **Code-form plan IR**：函数调用、循环、条件分支显式编码推理结构 — 可解释且跨域通用
2. **Scalable auto-mining**：无需任务专用标注，从开放语料提取 planning signal
3. **2M 规模数据集**：prompt + code plan + response 三元组监督
4. **vs CoT / Plan-and-Solve / latent plans**：兼顾 expressiveness（结构+通用+可解释）与 learning efficiency
5. **Complexity scaling**：任务越复杂，plan 中间表示收益越显著

## 关键数字

| 设置 | 结果 |
|------|------|
| Training examples | **2M** |
| Benchmarks | **13** (math, symbolic, IF, multi-hop QA, decision) |
| Relative improvement vs no plan | **25.1%** avg |
| Backbone scale | **7B–13B** (Mistral, Llama) |

## 与 wiki 交叉引用

- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — 长 chain-of-thought/plan 拉长 prefill 与 decode
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 多步 reasoning 增加 token 与 KV 占用
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — agent/reasoning 工作负载 placement
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 长上下文 plan+response 的 KV 管理
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — reasoning-heavy 流量与 serving 架构

# Citations

[1] [raw/papers/Code_Form_Planning_Scaling_LLM_Reasoning_2024.pdf](raw/papers/Code_Form_Planning_Scaling_LLM_Reasoning_2024.pdf) — Wen et al. (2024)
[2] [raw/papers/code-form-planning-llm-reasoning.md](raw/papers/code-form-planning-llm-reasoning.md) — 结构化摘录
