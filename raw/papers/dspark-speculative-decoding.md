---
type: Raw Source
title: DSpark Speculative Decoding
source_path: /home/luke/snap/zotero-snap/common/Zotero/storage/4ML6ZY7S/Cheng 等 - DSpark Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation.pdf
ingested: 2026-06-24
sha256: 9e1a1e9dadd51537dd02dc8dcec6a25a5bb0417f9835a719dfe05d9dfcba3c19
---

# DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation

**Authors:** Xin Cheng, Xingkai Yu, Chenze Shao, Jiashi Li, Yunfan Xiong, et al.  
**Affiliations:** Peking University; DeepSeek-AI  
**PDF:** [DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf](DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf)

## 核心问题

并行 speculative drafter（如 DFlash）单 forward 生成整块 draft，但块内 token 无依赖 → **suffix acceptance decay**；固定长度 verify 在高并发下浪费 target batch 容量。

## 架构

1. **Semi-autoregressive generation**：DFlash 并行 backbone + 轻量 sequential head（默认 Markov，可选 RNN）→ 块内依赖、缓解 suffix decay；T_draft 仍 ≈ O(1)。
2. **Confidence-scheduled verification**：confidence head 估计 per-position prefix survival；**Hardware-Aware Prefix Scheduler** 最大化 Θ = τ·SPS(B)，按负载动态截断 verify 长度。

## 训练

L = α_ce L_ce + α_tv L_tv + α_conf L_conf；position weight w_k = exp(−(k−1)/γ)；STS 校准 cumulative survival。

## 离线结果（Table 1，Qwen3/Gemma4）

相对 Eagle3 macro-average τ：+30.9% / +26.7% / +30.0%（4B/8B/14B）；相对 DFlash：+16.3% / +18.4% / +18.3%。

## 生产部署（DeepSeek-V4-Flash/Pro vs MTP-1）

- 匹配吞吐：per-user 生成 **+60–85%**（Flash）、**+57–78%**（Pro）
- 严格 SLA 下维持非退化吞吐（Flash 120 tok/s/user、Pro 50 tok/s/user）
- DSpark-5：γ=5，Markov head；异步 scheduler 兼容 ZOS + CUDA graph

## 开源

DeepSpec 训练/评测代码；Hugging Face checkpoints（dspark_qwen3_*、V4 DSpark 部署权重）。
