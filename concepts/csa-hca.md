---
type: Concept
title: CSA and HCA (Hybrid Attention)
description: 两级压缩注意力：CSA 温和压缩+稀疏选择，HCA 激进压缩+dense attention
tags:
- attention
- compression
- sparse
- architecture
timestamp: '2026-04-28T00:00:00Z'
created: 2026-04-28
sources:
- DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
---

# CSA and HCA (Compressed Sparse Attention / Heavily Compressed Attention)

DeepSeek-V4 的核心注意力创新，用于解决长上下文的计算和存储瓶颈。

## Motivation
标准注意力 O(n²) 复杂度在 1M token 上下文下不可行。需要同时降低：
1. **计算量**（attention FLOPs）
2. **KV cache 存储量**

## CSA (Compressed Sparse Attention)

**流程**：Compress → Index → Select → Attend

1. **KV 压缩**：每 m 个 token 的 KV entry 压缩成 1 个
   - 生成两组 KV entries (Ca, Cb) 和对应权重 (Za, Zb)
   - 重叠压缩：每个 compressed entry 来自 2m 个 KV entries（相邻窗口重叠）
   - 实际压缩率：1/m
   - V4-Pro: m=4, V4-Flash: m=4

2. **Lightning Indexer**：为每个 query 选出 top-k 个 compressed entries
   - 生成 indexer queries（低秩分解：h → d_c → n_hI × c_I）
   - 计算 index scores：I(t,s) = Σ w_h · ReLU(q_h · K_s)
   - 选出 top-k entries

3. **Shared KV MQA**：选中的 compressed entries 同时作为 key 和 value
   - 多 query head，单 KV head

4. **Grouped Output Projection**：将 n_h 个输出分组投影，降低计算量

## HCA (Heavily Compressed Attention)

- 更激进的压缩：m'=128 个 token 压成 1 个
- **不做 sparse selection**，直接 dense attention
- 不做重叠压缩
- 用途：极远距离的粗粒度记忆

## 通用组件

### Sliding Window Attention
- 保留最近 n_win=128 个 token 的未压缩 KV entries
- 解决两个问题：因果性约束（同一压缩块内的 token 互相看不到）、局部依赖

### Attention Sink
- 可学习的 sink logits，允许 attention scores 不等于 1
- 避免注意力过度分散

### Partial RoPE
- 只对 query 和 KV entry 的最后 64 维用 RoPE
- KV entry 同时作为 key 和 value，输出会携带绝对位置信息
- 反制措施：对 attention output 的最后 64 维应用 position=-i 的 RoPE

### 混合精度存储
- RoPE 维度：BF16
- 其余维度：FP8
- 近乎减半 KV cache

## 效率分析

以 BF16 GQA8 (head dim 128) 为基线：
- V4 的 KV cache 降至基线的 **~2%**（1M context）
- Lightning indexer 用 **FP4** 计算（加速长上下文 score 计算）
- Index scores 从 FP32 量化到 BF16：top-k selector 2× 加速，99.7% recall

## Trade-offs

| 方面 | CSA | HCA |
|------|-----|-----|
| 压缩率 | 温和 (1/4) | 激进 (1/128) |
| 精度 | 较好 | 较粗 |
| 计算量 | 中等（sparse selection） | 极低（dense on compressed） |
| 适用 | 中距离精确检索 | 极远距离粗粒度记忆 |

## Relations
- Used in: [Deepseek V4](#DeepSeek-V4)
- Related: [Fp4 Qat](#FP4-QAT), [Megamoe Kernel](#MegaMoE-kernel)

# Citations

[1] [DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf](DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf)
