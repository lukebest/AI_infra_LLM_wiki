---
type: Paper
title: "22580: From GPT-2 to Kimi K3, Explained"
description: Ali (@waterloo_intern, Baseten) 2026-07-27 X 长文；从 GPT-2 注意力机制一路演化到 Kimi K3；核心论点"过去七年 LLM 真正的变化不是规模 22,580×，而是 attention 状态空间从 O(N) 到 O(1) 的选择/衰减/reset 范式"
tags:
- attention
- moonshot
- llm
- transformer
- architecture
- model
- inference
created: 2026-07-30
updated: 2026-07-30
sources:
- raw/articles/22580 From GPT2 to Kimi3, Explained.md
- raw/articles/02-kimi-k3-from-gpt2.md
timestamp: 2026-07-30T03:25:46Z
---

# 22580: From GPT-2 to Kimi K3, Explained

## Citation
**Author**: Ali (@waterloo_intern, Baseten inference engineer)
**Published**: 2026-07-27
**Source**: https://x.com/waterloo_intern/article/2081762065392541951
**Local**: `raw/articles/22580 From GPT2 to Kimi3, Explained.md`
**Length**: 551 行，28KB
**Format**: X 长文 (long-form article)

## 核心论点

> **过去七年 LLM 真正的变化，不是规模（22,580× 参数放大），而是模型"保存/更新/找回信息"的方式。**

具体来说，attention 机制从 **O(N) 全存（GPT-2）→ O(1) 固定状态（Linear Attention）→ O(1) 精确替换（DeltaNet）→ O(1) + 衰减（Gated DeltaNet）→ O(1) per-channel α + 周期 reset（KDA）→ 完整混合（Kimi K3）**。

**22,580 这个数字的来源**：Kimi K3 (2.8T) / GPT-2 (124M) ≈ 22,580。

## 章节结构

| # | 章节 | 关键技术 |
|---|------|---------|
| 1 | GPT-2 | O(N) KV cache, decoder-only Transformer |
| 2 | Linear Attention | φ(q)·φ(k)ᵀv = q·(φ(k)ᵀv)，associative → O(1) 状态 |
| 3 | DeltaNet (Fast Weight Programmers) | delta rule：v - k@S，精确替换 |
| 4 | DeltaNet (Parallelizing Linear Transformers with Delta Rule) | chunk-wise forward substitution，并行 prefill |
| 5 | Gated Delta Net | Mamba α + Delta β，Gated Delta rule |
| 6 | KDA / Kimi Linear | per-channel α + 周期 MLA 混合 |
| 7 | Kimi K3 | 23 macrocycle × 4 layer (3 KDA + 1 MLA) + MoE + AttnRes |
| 8 | AttnRes | 深度方向选择性残差检索 |

## 关键代码与公式

### Delta rule
```python
v_old = k @ S                  # 先查旧值
u = beta * (v - v_old)         # 计算差值
S = S + k.transpose(-1, -2) @ u  # 等价于"先减再加"
```

### Chunk-wise parallel forward
```python
def chunk_delta_rule_forward(Q, K, V, beta, C):
    Q, K, V = map(lambda x: x.reshape(-1,C,d), [Q, K, V])
    K_beta = K * beta.unsqueeze(-1)
    V_beta = V * beta.unsqueeze(-1)
    
    T = -(K_beta @ K.t()).tril(-1)
    for i in range(1, C):
        T[i, :i] = T[i, :i] + (T[i, :, None] * T[:, :i]).sum(-2)
    T += torch.eye(C)
    W = T @ K_beta; U = T @ V_beta
    
    S = torch.zeros(d, d)
    O = torch.empty_like(V)
    for i in range(L // C):
        u_i = U[i] - W[i] @ S
        o_inter = q_i @ S
        A_i = (q_i @ k_i.t()).tril()
        o_intra = A_i @ u_i
        S += k_i.t() @ u_i
        O[i] = o_intra + o_inter
    return O.reshape(L, d)
```

### Gated Delta rule
$$S_t = \alpha_t \cdot S_{t-1} \cdot (I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top$$

### KDA (per-channel α)
```python
log_alpha = self.alpha_proj(x)
alpha = torch.exp(-torch.exp(log_alpha))    # ∈ (0, 1)
alpha = alpha.reshape(nb, C, d)             # per-channel
```

### AttnRes
```python
V = torch.stack(blocks + [partial_block])
K = norm(V)
logits = torch.einsum('d, n b t d -> n b t', proj.weight.squeeze(), K)
h = torch.einsum('n b t, n b t d -> b t d', logits.softmax(0), V)
return h
```

### SiTU
```python
d = x.shape[-1] // 2
gate = x[..., :d].to(torch.float32)
up = x[..., d:].to(torch.float32)
situ_a = self.beta * torch.tanh(gate / self.beta) * torch.sigmoid(gate)
if self.linear_beta is not None:
    up = self.linear_beta * torch.tanh(up / self.linear_beta)
return (situ_a * up).to(x.dtype)
```

## 关键事实

| 事实 | 来源 |
|------|------|
| GPT-2 124M 参数（12 层，12 head，768 dim）| Ali §"GPT-2" |
| Linear Attention 用 ELU+1 feature map | Katharopoulos 2020 |
| Delta rule 思想来自 Schlag "Fast Weight Programmers" (AISTATS 2022) | Ali §"DeltaNet" |
| Chunk-wise parallel 来自 Yang et al. ICLR 2024 | Ali §"Parallelizing Linear Transformers" |
| Mamba forget gate α ∈ (0,1) | Gu & Dao 2023 |
| Kimi Linear 6× decode throughput claim | Kimi Linear 论文 |
| Kimi K3 = 2.8T 参数 | Kimi 官方技术博客 |
| 898 expert = 2 shared + 896 routed | Kimi 官方 + Ali §"Kimi K3" |
| 23 macrocycle × 4 layer = 92 层 | Ali §"Kimi K3" |
| 3 KDA + 1 MLA per macrocycle | Ali §"Kimi K3" |
| AttnRes 每 12 层 / 8 blocks（92/12 = 7.67）| Ali §"AttnRes" |
| K3 vs K2 scaling efficiency ~2.5× | Kimi 官方 |

## 本文的中文翻译与扩展

本仓库另存有 `raw/articles/02-kimi-k3-from-gpt2.md` ——稼先社区草稿 v1.1，~7000 字中文译注与扩展。

**主要扩展**：
1. 加上"困惑驱动"开篇（α 在 1M 上下文数值稳定性问题）
2. §6.1 补充 per-channel α 的隐藏代价（梯度饱和、interpretability 失效、训练成本 1.5-2×）
3. §8 一句话观察：模型层 vs 硬件层的同构淘汰机制（呼应 WaferLLM §7.5/§8）
4. §9 "几个我没想明白的事" + "如果你自己要做点什么" 实操建议

## 作者背景

Ali 不是某个"水牛实习生"——根据 X 账号自述，在 **Baseten 做 inference engineering**。

文章风格明显是**工程师视角**：关心 HBM 带宽、tensor core 利用率、KV cache 实际尺寸、prefill 能否并行、训练稳定性等。**不是学术派的数学推导**。

## 与其他 paper 摘要的关系

| 类型 | 已存 papers |
|------|------------|
| Attention IO-aware 优化 | [FlashAttention](/papers/flashattention-io-aware-exact-attention.md), [FlashAttention-2](/papers/flashattention-2-faster-attention.md), [FlashAttention-3](/papers/flashattention-3-asynchrony-low-precision.md) |
| Decode 优化 | [FlashDecoding++](/papers/flashdecoding-plus-plus-llm-gpu-inference.md) |
| Sparse attention | [DynaX](/papers/dynax-sparse-attention-acceleration.md) |
| 跨架构综述 | [LLM Inference Hardware Survey](/papers/llm-inference-acceleration-comprehensive-hardware-survey.md), [AI Accelerators Cross-Architecture](/papers/ai-accelerators-llm-inference.md) |
| 注意力机制演化（本文覆盖）| **新增** |

**本文在 paper 库中的独特位置**：其他 paper 摘要都是 softmax attention 优化方向；**本文是 attention 机制"放弃 softmax attention"的方向**（线性化、delta、gating）。

## 相关页面

- [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md) — K3 模型
- [Linear Attention Evolution](/concepts/linear-attention-evolution.md) — attention 七年演化主线
- [Attention Residuals](/concepts/attention-residuals.md) — AttnRes
- [Stable Latent MoE](/concepts/stable-latent-moe.md) — MoE 设计
- [WaferLLM System](/concepts/waferllm-system.md) — 硬件层同构淘汰机制
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode bandwidth 主导
- [FlashAttention 2](/concepts/flashattention-2.md) — softmax attention IO-aware（与 linear attention 正交）

# Citations

[1] Ali (@waterloo_intern), "22580: From GPT2 to Kimi3, Explained", 2026-07-27, https://x.com/waterloo_intern/article/2081762065392541951
[2] Moonshot AI, "Kimi K3 Tech Blog", https://www.kimi.com/blog/kimi-k3
[3] [raw/articles/02-kimi-k3-from-gpt2.md](raw/articles/02-kimi-k3-from-gpt2.md) — 本地中文译注 v1.1