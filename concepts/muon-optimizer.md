---
type: Concept
title: Muon Optimizer
description: 矩阵正交化优化器，Hybrid Newton-Schulz 迭代
tags:
- optimization
- training
timestamp: '2026-04-28T00:00:00Z'
created: 2026-04-28
sources:
- DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
---

# Muon Optimizer

DeepSeek-V4 采用的优化器，基于 Jordan et al. (2024) 和 Liu et al. (2025)，用于大部分参数（embedding、prediction head、RMSNorm 仍用 AdamW）。

## Core Algorithm

```
for each weight W:
  G = ∇L(W)                    # 计算梯度
  M = μ·M + G                  # 动量累积
  O' = HybridNewtonSchulz(μ·M + G)  # Nesterov + 正交化
  O = O' · √max(n,m) · γ      # RMS rescaling
  W = W·(1-ηλ) - η·O           # 权重衰减 + 更新
```

## Hybrid Newton-Schulz Iterations

目标：将动量矩阵近似正交化为 U·V^T（SVD 的左右奇异向量之积）

**两阶段**，共 10 次迭代：
- **前 8 步**（快速收敛）：(a,b,c) = (3.4445, -4.7750, 2.0315)
- **后 2 步**（精确稳定）：(a,b,c) = (2, -1.5, 0.5)

每步操作：M_k = a·M_{k-1} + b·(M_{k-1}·M^T)·M_{k-1} + c·(M·M^T)^2·M

## Key Design Choices

1. **Nesterov 动量**：用 μ·M + G（而不是 M）做正交化
2. **RMS Rescaling**：将更新矩阵的 RMS 调到固定值（0.18），复用 AdamW 学习率
3. **Weight Decay**：应用于 Muon 参数
4. **BF16 通信**：MoE 梯度用 BF16 同步（减半通信量），用 all-to-all + FP32 本地求和代替 reduce-scatter
5. **避免 QK-Clip**：V4 的 attention 架构允许直接在 queries 和 KV entries 上用 RMSNorm，防止 logit 爆炸

## ZeRO 兼容策略

Muon 需要完整梯度矩阵，与传统 ZeRO 冲突：
- **Dense 参数**：限制 ZeRO 并行度上限，用背包算法分配参数矩阵到各 rank
- **MoE 参数**：按 down/up/gate 顺序展平所有专家的所有层，均匀分配
- 连续同形状参数自动合并，批量执行 Newton-Schulz

## Relations
- Used in: [Deepseek V4](#DeepSeek-V4)
- Related: [Fp4 Qat](#FP4-QAT)

# Citations

[1] [DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf](DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf)
