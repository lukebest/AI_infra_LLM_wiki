---
type: Concept
title: Attention Residuals
description: 深度方向上的选择性残差检索；每层可学习地"挑出"对自己有用的旧表示；缓解残差稀释 + 给训练稳定性；K3 报告 +2% latency 但 1.25× 计算优势
tags:
- attention
- llm
- architecture
- moonshot
- residual
- optimization
created: 2026-07-30
updated: 2026-07-30
sources:
- raw/articles/22580 From GPT2 to Kimi3, Explained.md
- raw/articles/02-kimi-k3-from-gpt2.md
timestamp: 2026-07-30T03:23:23Z
---

# Attention Residuals (AttnRes)

## TL;DR
AttnRes 是 Kimi K3 引入的**深度方向选择性检索**机制。标准 Transformer 的残差流是"无差别累加所有层输出"——后面的层想调取某个旧表示，只能"出奇大"地压过前面总和。AttnRes 把这个**加权**操作改成可学习：每层学一个 query，和前面每个状态做点积 → softmax → 加权组合。

**与 KDA 正交**：KDA 是序列方向（一维）检索，AttnRes 是深度方向（一维）检索。两者结合 = 二维选择性检索。

## 数学定义

**标准 Transformer 残差流**：

$$h_l = h_1 + \sum_{i=1}^{l-1} f_i(h_i)$$

所有层的输出被无差别累加。

**AttnRes 残差流**：

$$h_l = \alpha_0 \cdot h_1 + \sum_{i=1}^{l-1} \alpha_i \cdot f_i(h_i)$$

每个 α_i 是当前层学出的一个 query 和前面每个状态作为 key 做点积得到的。

**与标准 attention 的类比**：
- 标准 attention：query 是当前 token 状态，key/value 是历史 token 状态，**沿序列方向**
- AttnRes：query 是当前层参数，key/value 是历史层残差状态，**沿深度方向**

**每个权重 α_i 的计算**：
1. 归一化所有历史残差状态作为 K
2. 当前层学一个投影向量作为 Q
3. logits = einsum(Q, K) → softmax → 加权 V

## 实现：block granularity

AttnRes 不在每层做（太贵），而是**每 12 层一个边界**——把 12 层的 attention + MLP 输出累加成一个 block representation，存下来等后续 AttnRes 调取。

```python
V = torch.stack(blocks + [partial_block])   # [N+1, B, T, D]
K = norm(V)
logits = torch.einsum('d, n b t d -> n b t', proj.weight.squeeze(), K)
h = torch.einsum('n b t, n b t d -> b t d', logits.softmax(0), V)
return h
```

## K3 的具体配置

K3 backbone = **23 macrocycles × 4 layers = 92 层**。

每个 AttnRes 边界 = 12 层。

**92 / 12 = 7.67 → 8 个 AttnRes block**（含最后 partial block）。

**延迟成本**：推理时 **+2%**。

**计算收益**：官方报告 **1.25×**。

**两个具体收益**：
1. **缓解残差稀释（residual dilution）**：后面层不再需要"出奇大"的输出来压过累积残差——这降低了训练不稳定性
2. **1.25× 计算优势**：可选择的信息流减少无用工作

## 与其他机制的关系

| 机制 | 方向 | 选择性 | 适用 |
|------|------|--------|------|
| **Standard residual** | 深度 | 无（全累加）| 所有 Transformer |
| **KDA** | 序列 | 学得的 α 衰减 | K3 / Gated DeltaNet |
| **MLA** | 序列 | softmax attention | K3 周期 reset |
| **AttnRes** | 深度 | 学得的 softmax α | K3 |

**AttnRes 和 MLA 解决同构问题**：两者都做"在容量有限时选择性调取"。MLA 调取历史 token 信息（O(N)），AttnRes 调取历史层表示（O(92)）。

## 开放问题

1. **AttnRes 和 KDA 是否冗余**：两者都做"选择性调取"，但一个序列方向、一个深度方向。**直觉上正交**，但 K3 报告 AttnRes 1.25× 计算优势——为什么深度方向的"旧表示调取"能减少序列方向的工作量？想不清楚。
2. **每 12 层是最优的吗**：boundary 频率直接影响 capacity vs compute trade-off。K3 选 12 是经验值还是 scaling law 推导？公开材料无 ablation。
3. **AttnRes 在 decoder-only 模型上效果**：目前只在 K3 上验证。encoder-decoder 模型、multimodal 模型的 transferability 未知。

## 相关页面

- [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md) — K3 模型
- [Linear Attention Evolution](/concepts/linear-attention-evolution.md) — attention 演化主线
- [Stable Latent MoE](/concepts/stable-latent-moe.md) — MoE 容量设计

# Citations

[1] [raw/articles/22580 From GPT2 to Kimi3, Explained.md](raw/articles/22580 From GPT2 to Kimi3, Explained.md) — Ali 原文 §AttnRes
[2] Moonshot AI Kimi K3 技术报告（公开材料未见完整 AttnRes ablation）
[3] [raw/articles/02-kimi-k3-from-gpt2.md](raw/articles/02-kimi-k3-from-gpt2.md) — 本地中文译注