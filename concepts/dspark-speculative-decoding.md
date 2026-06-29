---
type: Concept
title: DSpark Speculative Decoding
description: DeepSeek 半自回归 speculative decoding：并行 DFlash backbone + Markov sequential head、confidence-scheduled 负载感知 verify，V4 生产 +60–85% 单用户速度
tags:
- inference
- decode
- serving
- deepseek
- scheduling
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf
---

# DSpark Speculative Decoding

**DSpark** 是 DeepSeek 的 lossless speculative decoding 框架：draft 模型提议 token 块，target 模型单 forward 验证；接受最长一致前缀 + bonus token。Per-token 延迟 L = (T_draft + T_verify)/τ——DSpark 同时提高 τ 并降低有效 T_verify。

## 两类瓶颈

| 瓶颈 | 原因 | DSpark 对策 |
|------|------|-------------|
| **Draft 质量** | 并行 drafter 块内独立预测 → multi-modal collision、suffix decay | Semi-autoregressive：并行 backbone + 轻量 sequential head |
| **系统效率** | 固定 verify 长度在高并发下 verify 高拒绝率 tail token，占满 batch | Confidence-scheduled verification |

## Semi-Autoregressive Generation

```
Parallel stage (DFlash backbone): 单 forward → h_1..h_γ, base logits U_k
Sequential stage (Markov/RNN head): 采样 x_k ~ p_k(·|x_0, x_<k)
  p_k(v) ∝ exp(U_k(v) + B_k(x_<k, v))
```

- **Markov head（默认）**：B(x_{k−1}, ·) = W1[x_{k−1}]W2，低秩 r=256
- **RNN head**：块内 recurrent state，长块边际收益小
- Position 1 受益于**更深并行 backbone**（vs 浅层 Eagle3）；后续位置靠 sequential head 避免 DFlash 式 decay

离线（γ=7，无 scheduler）：相对 Eagle3 accepted length **+27–31%**；相对 DFlash **+16–18%**（Qwen3 4B/8B/14B）。2-layer DSpark > 5-layer DFlash。

## Confidence-Scheduled Verification

**Confidence head**：c_k ≈ P(位置 k 被 target 接受 | 前缀已接受)；监督标签 c*_k = 1 − ½‖p_d − p_t‖₁。**STS** 逐位校准 cumulative product。

**Hardware-Aware Prefix Scheduler**（Algorithm 1）：最大化 Θ = τ·SPS(B)，SPS(B) 为 engine 预 profile 的 steps/s；按 prefix survival a_{r,j} = ∏_{i≤j} c_{r,i} 贪心扩展 verify 长度。

生产适配：
- **异步**：用两步前 confidence 预测 batch 容量 K，兼容 ZOS + CUDA graph
- **变长 verify**：flatten token + marker tensor 稀疏 attention（V4 index-attention/compress kernel）

## 与 MTP-1 / 并行 drafter 对比

| | MTP-1（V4 旧 baseline） | DFlash | DSpark |
|--|-------------------------|--------|--------|
| Draft | 单 token / 浅 MTP | 全并行块 | 并行 + 块内 sequential |
| Verify | 固定短 | 固定长块 | **负载感知动态截断** |
| 高并发 | 安全但慢 | 吞吐下降 | 维持 Pareto 前沿 |

静态 MTP-3/5 在高并发下 verify 浪费导致吞吐劣化；DSpark 使**大块 draft 在生产环境可部署**。

## DeepSeek-V4 生产结果（live traffic）

| 引擎 | 匹配吞吐时 tok/s/user | 中等 SLA 吞吐提升 |
|------|----------------------|-------------------|
| V4-Flash | **+60–85%** vs MTP-1 | +51% @ 80 tok/s/user |
| V4-Pro | **+57–78%** | +52% @ 35 tok/s/user |

低并发：verify budget ~4–6 tokens（MTP-1 固定 ~2）；高并发：scheduler 自动缩短 verify，保护 batch 容量（与 [Inference Capacity Trap](/concepts/inference-capacity-trap.md) 中 KV/batch 争用同构）。

部署配置 **DSpark-5**：γ=5，3-layer MoE draft + mHC + SWA 128；开源 **DeepSpec** 训练框架与 checkpoints。

## 相关页面

- [DeepSeek-V4](/entities/deepseek-v4.md) — 部署目标模型
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 阶段带宽/算力瓶颈
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 高并发 batch 容量
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — GPU/LPU 上 MTP 与 draft 模型
- [Deterministic Execution](/concepts/deterministic-execution.md) — 对比：编译器调度 vs serving 层 speculative 加速

# Citations

[1] [raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf](raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf) — Cheng et al., DeepSeek-AI / PKU (2026)
