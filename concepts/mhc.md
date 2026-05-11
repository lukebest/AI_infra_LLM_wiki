---
title: Manifold-Constrained Hyper-Connections (mHC)
created: 2026-04-28
updated: 2026-04-28
type: concept
tags: [architecture, optimization, training]
sources:
  - DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
---

# Manifold-Constrained Hyper-Connections (mHC)

DeepSeek-V4 对残差连接的升级，源自 Xie et al. (2026)。

## Motivation
标准 Hyper-Connections (HC) 扩展残差流维度 (d → n_hc × d)，提供独立于 hidden size 的缩放轴。但多层堆叠时**数值不稳定**。

## Core Idea
约束残差映射矩阵 B_l 到**双随机矩阵流形**（Birkhoff polytope）：

```
M = { M ∈ R^{n×n} | M·1 = 1, 1^T·M = 1^T, M ≥ 0 }
```

这保证：
- **谱范数 ≤ 1**：残差变换是非扩张的
- **流形对乘法封闭**：深层堆叠时稳定性有保证

## 实现

### 三组参数
- A_l ∈ R^{1×n_hc}: 输入映射 → Sigmoid 约束
- B_l ∈ R^{n_hc×n_hc}: 残差映射 → Sinkhorn-Knopp 投影到 Birkhoff polytope
- C_l ∈ R^{n_hc×1}: 输出映射 → 2·Sigmoid 约束

### 动态参数化
参数分解为动态（依赖输入）和静态（独立于输入）两部分：
- 输入 X_l → flatten → RMSNorm → 线性投影生成 raw parameters
- 加入可学习的 static biases 和 gating factors

### Sinkhorn-Knopp 算法
- exp(B̃_l) → 20 次迭代行列归一化 → 双随机矩阵 B_l

## 配置
- n_hc = 4（扩展因子）
- t_max = 20（Sinkhorn-Knopp 迭代次数）

## Cost
- 训练 wall-time 开销：仅 **6.7%**（通过 fused kernel + recomputation 优化）
- 实现策略：
  - 选择性 checkpoint 中间 tensor
  - 调整 DualPipe 1F1B 重叠方案
  - Recompute 大部分隐藏状态和所有 normalized layer inputs

## Relations
- Used in: [[deepseek-v4]]
- Enhances: residual connections in Transformer
