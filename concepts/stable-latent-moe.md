---
type: Concept
title: Stable Latent MoE
description: Kimi K3 的 MoE 框架：latent-space experts（输入先 down-project）+ Quantile Balancing（router-score quantile 分配容量）+ 898 experts (2 shared + 896 routed, 16+2 active)；FLOPs 减半
tags:
- moe
- llm
- moonshot
- architecture
- routing
- optimization
- kernel
created: 2026-07-30
updated: 2026-07-30
sources:
- raw/articles/22580 From GPT2 to Kimi3, Explained.md
- raw/articles/02-kimi-k3-from-gpt2.md
timestamp: 2026-07-30T03:24:31Z
---

# Stable Latent MoE

## TL;DR
Kimi K3 的 MoE 设计解决三个问题：
1. **专家容量**：898 experts（2 shared + 896 routed），每个 token 激活 16 routed + 2 shared = **18 个**
2. **训练稳定性**：Quantile Balancing（用 router score 的 quantile 分配 expert 容量，消除手工调平衡超参）
3. **计算效率**：Latent-space MoE（输入 down-project 到压缩空间，专家内部计算，最后 up-project）——**FLOPs 几乎减半**

## K3 专家配置

| 维度 | 值 |
|------|-----|
| **总 expert 数** | 898 |
| **Shared expert** | 2（每个 token 都过）|
| **Routed expert** | 896（router 选 16）|
| **激活 expert per token** | 16 routed + 2 shared = **18** |

**算术校验**：
- 路由选择：每个 token 路由到 16 个 routed expert
- shared expert 总是激活
- 总激活 = 16 + 2 = 18 个 expert per token

**路由机制**：
- 经典 MoE 路由：router = softmax(x · W_gate) → top-K 选择
- 平衡问题：某些 expert 可能被频繁选中（"明星 expert"），导致其他 expert 欠训练

## Quantile Balancing

**传统方法**：auxiliary loss 惩罚负载不均 + 手工调平衡超参 λ。

**K3 的方法**：用 router-score 的 **quantile** 直接分配 expert 容量——**消除手工平衡超参**。

直觉：
- 每个 expert 的 router score 分布看作一个分布
- 用这个分布的 quantile 决定这个 expert 的目标容量
- 训练时用 quantile balancing 作为约束，不需要手调 λ

**优势**：
- **少一个超参数**（少一份工程债）
- **稳定**：quantile 是数据驱动的，不依赖手工调参
- 与 Per-Head Muon optimizer + MXFP4 QAT 共同保证 2.8T 规模训练稳定性

## Latent-Space MoE

**传统 MoE FFN**（LLaMA 风格）：
```
gate = SiLU(x @ W_gate)
up = x @ W_up
out = (gate * up) @ W_down
```
3 个矩阵乘，dim 始终是 d_model。

**Latent-space MoE（K3 风格）**：
```
# 输入先 down-project
x_latent = x @ W_down_in    # d_model → d_latent, d_latent << d_model
# 专家在 latent 空间内计算
gate = SiTU(x_latent @ W_gate_latent)
up = x_latent @ W_up_latent
hidden = gate * up
# 最后 up-project 回原维度
out = hidden @ W_up_out      # d_latent → d_model
```

**FLOPs 节省**：d_latent < d_model 时，专家内部计算量减少 **~d_model/d_latent 倍**。K3 报告"**FLOPs 几乎减半**"——意味着 d_latent ≈ d_model / 2。

## SiTU 激活

**SiTU (Sigmoid Tanh Unit)** 替换 SwiGLU 的 SiLU：

```python
d = x.shape[-1] // 2
gate = x[..., :d].to(torch.float32)
up = x[..., d:].to(torch.float32)
situ_a = self.beta * torch.tanh(gate / self.beta) * torch.sigmoid(gate)
if self.linear_beta is not None:
    up = self.linear_beta * torch.tanh(up / self.linear_beta)
return (situ_a * up).to(x.dtype)
```

**问题**：SiTU 比 SiLU **复杂**——非 fused kernel 时**慢 3×**。**必须 fused**。

**架构 vs 系统的冲突**：模型架构创新带来 kernel 实现挑战——又一个"硬件/系统跟不上模型"的例子。

## SiLU vs SiTU 对比

| | SiLU (SwiGLU) | SiTU |
|---|---|---|
| 公式 | `x * sigmoid(x)` | `β · tanh(x/β) · sigmoid(x)` |
| 计算 | 单 sigmoid | sigmoid + tanh + 乘 |
| Fused kernel | 成熟 | **必须 fused**（否则慢 3×）|
| 表达力 | 基线 | 略好 |

## 训练基础设施（K3 配套）

- **Per-Head Muon optimizer**：attention head 独立优化，更自适应学习率
- **MXFP4 QAT**：从 SFT 阶段开始量化感知训练，MXFP4 权重 + MXFP8 激活
- **Fully balanced EP training**：专家并行训练，**静态 shape + 关键路径无 host sync**——避免 EP 训练中的 host bottleneck

## 推理部署挑战

- **共享 expert 也需要计算**：2 个 shared expert 每个 token 都过——和 routed expert 总共 18 个 expert 在 decode 步的负载不均
- **Latent space 的访存模式**：down-project 输入 → latent 计算 → up-project 输出——访存路径和传统 MoE 不同
- **推荐 supernode**：Kimi 官方建议 **64+ accelerator supernode** 部署
- **Prefix caching 与 KDA 不兼容**：vLLM 社区已开 PR，Kimi 会贡献 KDA-aware prefix cache

## 与已有 MoE 实现的关系

| 实现 | 重点 | 关系 |
|------|------|------|
| [FlashMoE Kernel](/concepts/flashmoe-kernel.md) | 单 persistent kernel 融合分布式 MoE | **kernel 层**：底层算子优化 |
| [MegaMoE Kernel](/concepts/megamoe-kernel.md) | DeepSeek wave EP overlap | **调度层**：wave pipeline |
| Stable Latent MoE (K3) | latent-space 专家 + 容量平衡 | **架构层**：模型设计 |
| [Disaggregated Inference](/concepts/disaggregated-inference.md) | attention↔expert 分部署 | **系统层**：推理系统 |

**这四层正交互补**：架构设计（K3）→ kernel 实现（FlashMoE/MegaMoE）→ 系统部署（disaggregated）→ 硬件后端。

## 开放问题

1. **Quantile Balancing 的理论性质**：quantile 比 auxiliary loss 强在哪？是否在大规模（>1T 参数）下还稳定？
2. **Latent-space MoE 的容量代价**：down-project + up-project 增加了 2 个矩阵乘，但 FLOPs 减半——是否在所有 model dim 下都最优？d_latent = d_model/2 是经验值吗？
3. **898 expert 是不是过度**：active 16/898 ≈ 1.8% 激活率。是不是稀疏到一定程度后路由精度不够？K3 报告模型稳定，但 ablation 数据未见。

## 相关页面

- [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md) — K3 模型
- [Linear Attention Evolution](/concepts/linear-attention-evolution.md) — attention 演化主线
- [Attention Residuals](/concepts/attention-residuals.md) — AttnRes
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — 分布式 MoE 单 kernel
- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — DeepSeek wave EP
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — attention/expert 解耦推理

# Citations

[1] [raw/articles/22580 From GPT2 to Kimi3, Explained.md](raw/articles/22580 From GPT2 to Kimi3, Explained.md) — Ali 原文 §Kimi K3
[2] [Kimi K3 Tech Blog](https://www.kimi.com/blog/kimi-k3) — Moonshot AI 官方 §Stable LatentMoE
[3] [raw/articles/02-kimi-k3-from-gpt2.md](raw/articles/02-kimi-k3-from-gpt2.md) — 本地中文译注