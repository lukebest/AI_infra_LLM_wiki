---
type: Concept
title: Linear Attention Evolution
description: GPT-2 → Linear Attention → DeltaNet → Gated DeltaNet → KDA 的七年演化主线；核心是 attention 状态空间从 O(N) → O(1) + 选择性衰减 + 周期 reset
tags:
- attention
- llm
- transformer
- architecture
- model
- moonshot
- inference
- optimization
created: 2026-07-30
updated: 2026-07-30
sources:
- raw/articles/22580 From GPT2 to Kimi3, Explained.md
- raw/articles/02-kimi-k3-from-gpt2.md
timestamp: 2026-07-30T03:22:43Z
---

# Linear Attention Evolution

## TL;DR
2019–2026 七年里，LLM 的 attention 机制经历了**完整的状态空间压缩演化**：从 O(N) 全存（GPT-2）→ O(1) 固定状态（Linear Attention）→ O(1) 精确替换（DeltaNet）→ O(1) 加选择性衰减（Gated DeltaNet）→ O(1) per-channel α + 周期 reset（KDA / Kimi Linear / Kimi K3）。**每一步都在解决同一个数学下界**："固定容量的关联记忆，必须有淘汰策略"。

> **核心论点**（来自 Ali, @waterloo_intern）：过去七年 LLM 真正的变化不是规模（22,580× 参数），而是**模型保存/更新/找回信息的方式**。

## 时间线

```
2019  GPT-2              O(N) KV cache, softmax attention
2020  Linear Attention   O(1) state, φ(q)·φ(k)ᵀv = q·(φ(k)ᵀv)
2024  DeltaNet           O(1) state + delta rule (替换机制)
2024  Parallelizing Δ    chunk-wise forward substitution（并行 prefill）
2024  Gated DeltaNet     + Mamba 的 α 衰减（遗忘机制）
2025  Kimi Linear (KDA)  per-channel α + 周期 MLA（混合）
2026  Kimi K3            + Stable LatentMoE + AttnRes + Quantile Balancing
```

## 1. GPT-2：O(N) 全存 = "保存一切"

**核心机制**：每个新生成的 token 都要和**所有历史 token** 做 QK 点积（O(N²)），softmax 归一化后对所有 V 加权平均。

**KV cache 优化**：存下历史的 K 和 V，避免每步重投影。但 cache 大小**随序列长度线性增长**：

| 上下文长度 | 7B 模型 FP16 KV cache |
|-----------|---------------------|
| 4K | ~1.5 GB |
| 200K | ~75 GB |

**带宽瓶颈**：长上下文的 cache 访存成为 decode step 的瓶颈——H100 FP16 989 TFLOPS，但 decode 实际算力利用率 <1%。

**GPT-2 的隐含假设**：**所有历史都重要，所以全部保留**。这是个容量无限的假设。

详见 [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md) §"Attention 演化主线"。

## 2. Linear Attention：O(1) 状态 = "把所有历史压成一块黑板"

**核心观察**（Katharopoulos et al. 2020）：如果对 Q 和 K **分别**应用 feature map φ（如 ELU+1），则：

$$\varphi(Q) \cdot \varphi(K)^\top V = Q \cdot (\varphi(K)^\top V)$$

**乘法对加法可结合**——所有历史的 K·V 累加可以折叠成 D×D 状态矩阵 S。

```python
# 线性注意力核心改动
k = F.elu(k) + 1
q = F.elu(q) + 1
S = cache if cache else 0
S = S + k @ v          # 状态 = 历史 K·V 的累加
o = q @ S              # 读：用当前 Q 查状态
```

**代价**：信息会互相干扰。所有 K·V 都累加到同一块"小黑板"——一旦序列长度 N 远超 D（head dim），**精确找回某个早期 token 的信息几乎不可能**。

Schlag (Fast Weight Programmers) 论文原话：

> "当序列长度超过存储容量，模型进入过载区。纯粹的加法策略不适合这个区。**不停地往有限记忆里塞新关联，必然会撞上限**。"

**这是 LLM 记忆问题的正式提出**——从这一步开始，"淘汰策略"成为显式的研究问题。

## 3. DeltaNet：delta rule = "先减再加 = 精确替换"

**核心想法**（Schlag et al. ICLR 2024）：与其"加"，不如"先减再加"——在写入新关联前，先查一下黑板上"键 k 这个位置"现在存着什么，把它擦掉，再写新的。

```python
v_old = k @ S                  # 先查旧值
u = beta * (v - v_old)         # 计算差值：要写的新值减去旧的
S = S + k.transpose(-1, -2) @ u  # 等价于"先减旧值再加新值"
```

**数学性质**：S = S + k⊤·(v - kS) = (I - kk⊤)S + kv⊤。这是 **Householder-like transition matrix**——保证精确替换旧关联而不引入新干扰。

**对比**：

| | 线性 attention | DeltaNet |
|--|---------------|----------|
| 更新 | S = S + k⊤·v | S = (I - βkk⊤)S + βkv⊤ |
| 干扰 | 累积 | 局部（被替换） |
| prefill | 可并行 | **必须串行**（需要 v_old） |

## 4. Parallelizing Linear Transformers with Delta Rule：把"顺序"重新代数化 = "chunk-wise forward substitution"

**核心问题**：DeltaNet 的 prefill 必须串行——但 GPU 的强项是矩阵乘。这是个根本对立。

**解法**（Yang et al. ICLR 2024）：**chunk-wise 分块**。

```
Within chunk C:  score-first  (Q·K⊤)·V  → 矩阵乘，可并行
Across chunks:   state-first   K⊤·V 累加到 S → 无依赖
```

复杂度分两块：
- **块间状态**：2Ld²，**与 chunk size C 无关**
- **块内 score**：2LCd，L 增长时随 C 线性增长

```python
T = -(K_beta @ K.t()).tril(-1)         # 三角因果掩码
for i in range(1, C):
    T[i, :i] = T[i, :i] + (T[i, :, None] * T[:, :i]).sum(-2)
T += torch.eye(C)
W = T @ K_beta; U = T @ V_beta
# 块间可并行
for i in range(L // C):
    u_i = U[i] - W[i] @ S
    o_inter = q_i @ S
    A_i = (q_i @ k_i.t()).tril()
    o_intra = A_i @ u_i
    S += k_i.t() @ u_i
    O[i] = o_intra + o_inter
```

**C 的甜蜜点**：
- C = 1：纯线性注意力（最便宜 FLOP，但 GPU 不友好）
- C = L：标准 O(N²) attention（GPU 最友好，但最贵）
- **C = 64 / 128**：tensor core / UMMA 的天然颗粒度

## 5. Gated DeltaNet：加 Mamba 的 α = "会替换 + 会遗忘"

**核心观察**：DeltaNet 能"换"但不能"忘"。Mamba（Gu & Dao 2023）独立给出了**整体衰减**机制：

```python
S_new = alpha * S_old + k @ v
```

α ∈ (0, 1) 数据依赖，控制"上一刻状态保留比例"。α = 1 → 纯 Delta 规则；α = 0 → 清空记忆。

**Gated DeltaNet 的优雅结合**：

$$S_t = \alpha_t \cdot S_{t-1} \cdot (I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top$$

| 项 | 角色 |
|---|---|
| **α 衰减项** | 整体遗忘（受 Mamba 启发）|
| **β delta 项** | 精确替换某个具体键（受 DeltaNet 启发）|
| **βk⊤v** | 写入新关联 |

**关键性质**：一个 token 在时刻 x 写入、时刻 x+t 读到时，它的状态被乘以 α_x · α_{x+1} · ... · α_{x+t}——**这是一个 multiplicative prefix sum**，所有 α 的连乘决定了"经过 t 步后还剩多少"。

**工程上**：α 的 log-space 重参数化（避免梯度饱和）+ chunk-wise 重新代数化（保持并行 prefill）。

## 6. Kimi Linear / KDA：per-channel α = "每个通道单独衰减"

**Kimi Linear 2025 年的核心升级**：把 scalar α 拆成 per-channel——**每个 head、每个通道单独学一个衰减率**。

```python
log_alpha = self.alpha_proj(x)             # 任意实数
alpha = torch.exp(-torch.exp(log_alpha))    # ∈ (0, 1)，梯度稳定
alpha = alpha.reshape(nb, C, d)             # per-channel
```

**直觉**：高语义层（主旨）保留得久，低语义层（具体名字）忘得快。**per-channel α 让模型按通道类型做精细遗忘**——比 scalar α 信息利用率高。

**架构上的关键决策**：Kimi Linear 不再是"纯线性"——**每隔几层插一个标准 MLA 层**，让模型能在需要时做精确 softmax 检索。

**报告数字**：相比全 attention，**质量持平或更好，decode 吞吐最高 6×**——这是 KDA 把 KV cache 从 O(N) 降到 O(1) 带来的访存量解耦收益。

## 7. Kimi K3：完整混合

K3 在 Kimi Linear 之上加的东西（详见 [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md)）：

| 改动 | 来源 | 目的 |
|---|---|---|
| **KDA + 周期 MLA (3:1)** | Kimi Linear | 用常数状态 + 周期性 softmax 检索替代全 attention |
| **Blockwise AttnRes（每 12 层）** | K3 新增 | 让每层选择性调取旧表示（深度方向）|
| **Gated MLA** | K3 | 控制 MLA 检索结果的输出比例 |
| **Stable LatentMoE (898 expert, 16+2 active)** | K3 | FLOPs 减半 + 容量翻倍 + Quantile Balancing |
| **SiTU 激活** | K3 | 表达力小幅提升 |
| **Per-Head Muon 优化器** | K3 | attention head 独立优化 |
| **MXFP4 量化感知训练** | K3 | 部署成本 |

## 数学下界："固定容量必须有淘汰策略"

Ali 文章最后一节的总结：

> "固定容量的关联记忆（维度固定）必须有淘汰策略，因为纯加性线性运算到容量上限后必然引入干扰。为此，**学到的选择性（gating、routing、decay）是必要的**，而 attention 是最高效的选择性读取机制。"

**这不只是 attention 的故事**——是所有有限存储系统的故事：

| 层级 | "记忆" | "淘汰策略" |
|------|--------|-----------|
| 模型层 | D×D attention 状态矩阵 | Δ-rule + α 衰减 + MLA 周期 reset |
| 系统层 | KV cache（O(N) 历史）| GQA/MQA 压缩 + paged attention |
| 硬件层 | 片上 SRAM (WSE 44 GB / NPU MB 级) | weight streaming + color 路由 + K-tree reduce |
| 网络层 | 网络缓存 (router linecard) | LRU + 多级 tier + aging |

**两边都在和同一个幽灵打仗：固定容量。** 详见 [WaferLLM System](/concepts/waferllm-system.md) §"与 Kimi K3 的同构关系"。

## 开放问题

1. **α 在 1M 上下文里数值稳定性**：FP16 精度上限 ~10⁻⁴，α = 0.99 连乘 1M 次后精确为 0。Kimi 团队怎么救？公开材料里没看到。
2. **per-channel α 的 interpretability**：训练后哪个通道装"事实"、哪个装"上下文"？**完全黑盒**——传统 attention pattern 可视化直接失效。
3. **3:1 (KDA:MLA) macrocycle 比例怎么选**：scaling law 实验？理论推导？公开材料无 ablation。
4. **AttnRes 和 KDA 是否冗余**：两者都做"选择性调取"，但一个序列方向、一个深度方向。**是否真的正交**？K3 报告 AttnRes 1.25× 计算优势，但直觉上说不清为什么。

## 相关页面

- [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md) — K3 模型实体
- [Attention Residuals](/concepts/attention-residuals.md) — AttnRes 专页
- [Stable Latent MoE](/concepts/stable-latent-moe.md) — MoE 容量设计
- [FlashAttention](/concepts/flashattention.md) — softmax attention 的 IO-aware 优化（与 linear attention 正交）
- [FlashAttention 2](/concepts/flashattention-2.md) — block-wise softmax attention
- [FlashAttention 3](/concepts/flashattention-3.md) — Hopper async + low-precision softmax attention
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — 长上下文 decode 优化
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — KV cache 分页管理
- [WaferLLM System](/concepts/waferllm-system.md) — 硬件层（WSE）的同构淘汰机制
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode bandwidth 由 KV cache 主导
- [KV Cache](/concepts/kv-cache.md) — KV cache 访存分析（如果存在）

# Citations

[1] [raw/articles/22580 From GPT2 to Kimi3, Explained.md](raw/articles/22580 From GPT2 to Kimi3, Explained.md) — Ali (@waterloo_intern), 2026-07-27
[2] Katharopoulos et al., "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention" (2020) — Linear Attention 原始论文
[3] Schlag et al., "Fast Weight Programmers" (AISTATS 2022) — delta rule 思想来源
[4] Schlag et al., "Linear Transformers with Delta Rule" (ICLR 2024) — DeltaNet
[5] Yang et al., "Parallelizing Linear Transformers with Delta Rule" (ICLR 2024) — chunk-wise forward substitution
[6] Gu & Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces" (2023) — Mamba / forget gate
[7] Moonshot AI, "Kimi Linear: Extending Parallelism Window with Kimi Delta Attention" (2025) — KDA
[8] [Kimi K3 Tech Blog](https://www.kimi.com/blog/kimi-k3) — Moonshot AI 官方
[9] [raw/articles/02-kimi-k3-from-gpt2.md](raw/articles/02-kimi-k3-from-gpt2.md) — 本地中文译注