---
type: Entity
title: Moonshot AI Kimi K3
description: 月之暗面 2026-07 发布的 2.8T 参数开源 LLM；KDA + 周期 MLA + AttnRes 混合架构；原生视觉 + 1M context；激活 16 of 896 routed + 2 shared experts
tags:
- model
- moonshot
- architecture
- training
- inference
- attention
- moe
- llm
- quantization
- kernel
created: 2026-07-30
updated: 2026-07-30
sources:
- raw/articles/22580 From GPT2 to Kimi3, Explained.md
- raw/articles/02-kimi-k3-from-gpt2.md
timestamp: '2026-07-30T00:00:00Z'
---

# Moonshot AI Kimi K3

## Overview
**Kimi K3** 是月之暗面 (Moonshot AI) 于 2026-07 发布的世界第一个 **开源 3T 级别** LLM。模型权重 2026-07-27 全量开源，2.8 万亿参数，原生视觉输入，1M token 上下文窗口。"K3" 是 "Kimi 3" 的简称，**与 WSE K-tree 的 K=3 编译器分叉因子毫无关系**——后者属于 Direction 2（mesh-NoC 上的 compiler-aware decode），而 Kimi K3 属于 LLM 模型架构演化主线。

|| 指标 | Kimi K3 |
||------|---------|
|| 总参数 | **2.8T** |
|| 专家数 | **898**（2 shared + 896 routed）|
|| 激活专家 | **18**（16 routed + 2 shared）|
|| 上下文窗口 | **1M** tokens |
|| 模态 | text + native vision |
|| 权重状态 | open-weight（2026-07-27）|

**与 GPT-2 的尺度对照**：GPT-2（2019）124M 参数；K3 / GPT-2 ≈ 2.8T / 124M ≈ **22,580**。这一数字是 Baseten 工程师 Ali (@waterloo_intern) 长文 "22580: From GPT2 to Kimi3, Explained" 的标题来源。

## 架构骨架

### Macrocycle 结构
K3 语言 backbone 由 **23 个 macrocycle** 组成，每个 macrocycle 包含 **4 层**，共 **92 层**。每个 macrocycle 内：
- **3 层 Kimi Delta Attention (KDA)**——常数状态 recurrent memory
- **1 层 Multi-head Latent Attention (MLA)**——全 softmax 检索

**3:1 比例的具体来源未在公开材料里说明**——可能是 scaling law 实验找出的甜蜜点，无完整 ablation 报告。

### Attention 混合
KDA 提供廉价的"长程记忆压缩"（O(1) 状态矩阵），MLA 提供昂贵的"精确全文检索"（O(N) softmax）。**每 4 层就 reset 一次精确检索能力**——这意味着即使是 1M context，"我刚写的那个 token 能不能查回去"这个问题的答案最多是 4 层之前的 KDA 状态。

### MoE：Stable LatentMoE
- **898 experts 总数**：2 个 shared expert（每个 token 都过）+ 896 个 routed expert
- 每个 token 由 router 从 routed 中选 **16 个**激活
- 实际激活 = 16 routed + 2 shared = **18 experts per token**
- **Latent-space MoE**：输入先 down-project 到压缩 latent 空间，专家内部计算，最后 up-project——**FLOPs 几乎减半**
- **Quantile Balancing**：用 router-score 的 quantile 直接分配 expert 容量，消除手工调平衡超参数
- 详见 [Stable Latent MoE](/concepts/stable-latent-moe.md)

### Attention Residuals (AttnRes)
每 12 层一个 AttnRes 边界。**23 macrocycle × 4 layer = 92 层**，92 / 12 = 7.67 → **8 个 AttnRes block**（含最后 partial block）。AttnRes 让每层可学习地"挑出"对自己有用的旧表示，缓解残差稀释。推理延迟 ~+2%，报告 1.25× 计算优势。详见 [Attention Residuals](/concepts/attention-residuals.md)。

### 其他组件
- **Gated MLA**：MLA 检索结果经过 gate（input 投影）后才进入残差流
- **SiTU (Sigmoid Tanh Unit)**：替换 SwiGLU 的 SiLU，性能更好但需要 fused kernel——非 fused 时比原路径慢 **3×**
- **Per-Head Muon optimizer**：attention head 独立优化
- **MXFP4 量化感知训练**：从 SFT 阶段开始，MXFP4 权重 + MXFP8 激活
- **NoPE（无显式位置编码）**：位置信息通过 KDA 的 gating + decay 隐式编码

## Attention 演化主线

K3 是 attention 机制七年演化的**收官节点**。完整路径见 [Linear Attention Evolution](/concepts/linear-attention-evolution.md)：

| 阶段 | 年份 | 关键贡献 | 状态空间 |
|------|------|---------|---------|
| **GPT-2** | 2019 | softmax attention + KV cache | O(N)（token 数）|
| **Linear Attention** | 2020 | φ(q)·φ(k)ᵀv = q·(φ(k)ᵀv)，associative | **O(1)** D×D 矩阵 |
| **DeltaNet** | 2024 | delta rule：v - k@S 替换旧值 | O(1) D×D 矩阵 |
| **DeltaNet Parallel** | 2024 (ICLR) | chunk-wise forward substitution | O(1) 状态 + O(C) chunk |
| **Gated DeltaNet** | 2024 | 加 Mamba 的 α 衰减 | O(1) 状态 + α 控制 |
| **Kimi Linear (KDA)** | 2025 | per-channel α，混合 MLA | O(1) 状态 + 周期 MLA |
| **Kimi K3** | 2026 | + Stable LatentMoE + AttnRes + Quantile Balancing | 完整混合 |

**核心论点**：过去七年 LLM 真正的变化**不是规模**（22,580× 参数），而是**"保存/更新/找回信息"的方式**——从 O(N) 全存，到 O(1) 状态 + 选择性衰减 + 周期性 reset + 深度选择性检索。

## 在推理栈中的位置

```
Model (Kimi K3)
    ↓
Attention — KDA (O(1) state) | MLA (O(N) softmax) | AttnRes (depth-wise retrieval)
    ↓
MoE — Stable LatentMoE (898 expert, 16 routed + 2 shared active)
    ↓
Quantization — MXFP4 weights + MXFP8 activations
    ↓
Serving — 64+ accelerator supernode recommended (Kimi 官方建议)
```

**推理部署挑战**：
- KDA prefix caching 与传统 KV cache 不兼容——vLLM 社区已开相关 PR，Kimi 官方会贡献 KDA-aware prefix cache 实现
- MLA 周期性出现意味着硬件需**双 opset 支持**（MHA + KDA）
- 推荐 64+ accelerator supernode 部署

## 关键事实溯源

- **2.8T 参数**：Kimi 官方技术博客 https://www.kimi.com/blog/kimi-k3 明确给出
- **898 experts = 2 shared + 896 routed**：Kimi 官方技术博客 + Ali 原文 §"Kimi K3" 双源确认
- **16 routed + 2 shared = 18 active**：Ali 原文 §"Kimi K3" 明确给出
- **23 macrocycle × 4 layer**：Ali 原文 §"Kimi K3"
- **3 KDA + 1 MLA per macrocycle**：Ali 原文 §"Kimi K3"
- **AttnRes 每 12 层 / 8 blocks**：Ali 原文 §"AttnRes"（92 / 12 = 7.67 → 8 blocks）
- **vs K2 整体 scaling efficiency ~2.5×**：Kimi 官方技术博客

## 与其他模型/公司的关系

- **vs DeepSeek-V4** ([DeepSeek-V4](/entities/deepseek-v4.md))：同样 2026 年发布的开源 MoE，但 V4 走 CSA + HCA 混合（压缩 + hybrid 注意力），K3 走 KDA + 周期 MLA——**两种不同的"避开 softmax attention O(N) 容量"路线**
- **vs Qwen3** / GPT-5 / Claude Fable 5：K3 性能"整体仍落后最强闭源模型（Claude Fable 5 / GPT 5.6 Sol），但在我们的 evaluation suite 上稳定领先"——Kimi 官方原话
- **vs Anthropic / OpenAI**：K3 是**开源**，Fable 5 / Sol 闭源——这是研究复现优势
- **vs Moonshot K2**：MoE 容量、attention 结构、训练 recipe 都有显著升级

## 相关页面

- [Linear Attention Evolution](/concepts/linear-attention-evolution.md) — attention 七年演化主线（含 KDA）
- [Attention Residuals](/concepts/attention-residuals.md) — AttnRes 深度方向选择性检索
- [Stable Latent MoE](/concepts/stable-latent-moe.md) — MoE 容量与路由
- [WaferLLM System](/concepts/waferllm-system.md) — 硬件层 (WSE) 与 K3 模型层的"同构淘汰机制"
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode bandwidth 由 KV cache 主导，KDA 改变格局
- [papers/ali-22580-from-gpt2-to-kimi3](/papers/ali-22580-from-gpt2-to-kimi3.md) — Ali 长文论文摘要
- [DeepSeek-V4](/entities/deepseek-v4.md) — 同期 CSA+HCA 路线对比

# Citations

[1] [raw/articles/22580 From GPT2 to Kimi3, Explained.md](raw/articles/22580 From GPT2 to Kimi3, Explained.md) — Ali (@waterloo_intern), 2026-07-27, 原文 https://x.com/waterloo_intern/article/2081762065392541951
[2] [Kimi K3 Tech Blog](https://www.kimi.com/blog/kimi-k3) — Moonshot AI 官方
[3] [raw/articles/02-kimi-k3-from-gpt2.md](raw/articles/02-kimi-k3-from-gpt2.md) — 本地中文译注与扩展（稼先社区草稿 v1.1）