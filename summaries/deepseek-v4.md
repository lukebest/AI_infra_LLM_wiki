---
title: "DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence"
created: 2026-04-28
updated: 2026-04-28
type: summary
tags: [model, architecture, attention, moe, compression, training, inference, quantization]
sources:
  - DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
---

# DeepSeek-V4 Technical Report Summary

**作者**: DeepSeek-AI | **时间**: 2026-04 | **类型**: Preview Technical Report

## 一句话总结
通过 Hybrid Attention (CSA+HCA) + mHC + Muon 三大架构创新，DeepSeek-V4 将百万 token 上下文的推理 FLOPs 降至 V3.2 的 27%，KV Cache 降至 10%，同时推理能力匹配或超越 GPT-5.2 / Gemini-3.0-Pro。

## 关键数字
- V4-Pro: 1.6T 参数 / 49B 激活 / 33T 训练 tokens / 原生 1M context
- V4-Flash: 284B 参数 / 13B 激活 / 32T 训练 tokens
- Codeforces 3206 (首次开源匹配闭源), MRCR 1M 83.5 (超越 Gemini-3.1-Pro)
- Putnam-2025 hybrid formal-informal: 120/120 满分

## 架构创新
1. [[csa-hca]] — 两级压缩注意力，KV cache 降至基线 2%
2. [[mhc]] — 流形约束超连接，残差映射非扩张，6.7% 额外训练开销
3. [[muon-optimizer]] — 矩阵正交化优化器，Hybrid Newton-Schulz 迭代

## 系统工程
- [[megamoe-kernel]] — EP 通信-计算全重叠，1.5-1.96× 加速
- [[tilelang]] — DSL kernel 开发，Z3 形式化分析，bitwise reproducibility
- [[fp4-qat]] — 无损 FP4→FP8 反量化，MoE expert 权重 + indexer QK path
- [[dsec-sandbox]] — 4 种执行基板，数十万并发沙箱
- 确定性训练：end-to-end batch-invariant + deterministic kernels

## 后训练
- Specialist Training → On-Policy Distillation (全词表 logit 蒸馏)
- Generative Reward Model 替代标量奖励
- Interleaved Thinking, Quick Instruction

## 局限
架构复杂、训练稳定性理论不清、缺多模态、长上下文延迟待优化

## Wiki Pages Created
- [[deepseek-v4]] (entity)
- [[csa-hca]] (concept)
- [[mhc]] (concept)
- [[muon-optimizer]] (concept)
- [[fp4-qat]] (concept)
- [[megamoe-kernel]] (concept)
- [[tilelang]] (concept)
- [[dsec-sandbox]] (concept)
