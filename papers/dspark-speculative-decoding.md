---
type: Summary
title: 'DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation'
description: DeepSeek 半自回归 speculative decoding + 负载感知 confidence verify；离线 τ +16–31%，V4 生产 per-user +57–85% vs MTP-1，开源 DeepSpec
tags:
- inference
- decode
- serving
- deepseek
- speculative-decoding
- scheduling
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf
---

# DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation

**Authors:** Xin Cheng, Xingkai Yu, Chenze Shao, Jiashi Li, Yunfan Xiong, et al. | **Affiliations:** Peking University + DeepSeek-AI | **PDF:** [raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf](raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf)

## 一句话总结

DSpark 用**半自回归 draft**（并行 DFlash backbone + Markov sequential head）提高 accepted length，用 **confidence + SPS(B) 调度**按负载动态截断 verify，在 DeepSeek-V4 生产流量下相对 MTP-1 将单用户生成速度提升 **57–85%** 且不改变 target 分布。

## 核心贡献

1. **Semi-autoregressive drafter**：保留 O(1) 并行 draft 延迟，块内注入依赖，缓解 parallel suffix decay
2. **Confidence head + STS 校准**：预测 prefix survival，支撑吞吐量公式 Θ = τ·SPS(B)
3. **Hardware-Aware Prefix Scheduler**：全局贪心 admission + 生产异步/ZOS 适配
4. **V4 全栈部署**：训练（hidden-state comm、anchor packing）、变长 verify kernel、live A/B vs MTP-1
5. **开源 DeepSpec**：Eagle3 / DFlash / DSpark 统一训练与评测

## 关键机制

### 延迟分解

```
L = (T_draft + T_verify) / τ
```

- 并行 drafter：T_draft ≈ 常数，但 τ 随块内位置衰减
- 自回归 drafter（Eagle3）：τ 高但 T_draft ∝ γ
- DSpark：T_draft ≈ 常数 + T_sequential ≪ T_parallel；sequential head 对 γ=4→16 仅 +0.2–1.3% 整轮延迟

### Confidence-scheduled verify

- Chat 域 entropy 高 → 静态全块 verify 浪费大；Math/Code 接受率高 → 可 verify 更长
- 高并发：截断低 survival suffix，释放 batch 给 [Inference Capacity Trap](/concepts/inference-capacity-trap.md) 下的其他请求

## 实验摘要

| 设置 | 结果 |
|------|------|
| Offline Qwen3-4B/8B/14B vs Eagle3 | macro τ **+30.9% / +26.7% / +30.0%** |
| Offline vs DFlash | **+16.3% / +18.4% / +18.3%** |
| γ=15 vs γ=7（4B math） | 相对 DFlash 增益 16% → **30%** |
| V4-Flash live vs MTP-1 | 匹配吞吐 **+60–85%** tok/s/user |
| V4-Pro live vs MTP-1 | 匹配吞吐 **+57–78%** tok/s/user |

## 与 wiki 交叉引用

- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 机制与调度细节
- [DeepSeek-V4](/entities/deepseek-v4.md) — 部署模型与 MTP 架构背景
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — decode 主导 wall-clock，speculative 直接优化 decode step
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — kernel 层 decode 加速（与 speculative 正交）
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — draft/MTP 与 LPU 异构部署讨论

# Citations

[1] [raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf](raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf) — Cheng et al. (2026)
