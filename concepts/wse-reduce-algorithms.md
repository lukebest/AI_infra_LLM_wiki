---
type: Concept
title: WSE Reduce Algorithms
description: WSE Reduce/AllReduce 算法族：Star/Chain/Tree/Two-Phase/Auto-Gen，模型驱动选择，Auto-Gen
  ≤1.4× 下界
tags:
- cerebras
- wse
- reduce
- allreduce
- collective
- communication
- mesh
- multicast
- routing
timestamp: '2026-06-20T00:00:00Z'
created: 2026-06-20
sources:
- raw/papers/Near-optimal_wafer-scale_reduce.pdf
confidence: high
---

# WSE Reduce / AllReduce 算法族

Luczynski et al. (HPDC 2024) 系统性设计和分析的 Cerebras WSE 通信 collective 算法。每种算法在不同 (向量长度 B, PE 数 P) 区间有最优区间。

## 1D Reduce 算法

### Star Reduce
- **策略**: 所有 PE 直接发向量到 root PE
- **Depth=1, Contention=B(P-1)**
- T = B(P-1) + 2TR + 1
- **最优区间**: B=1（标量归约），runtime 接近距离下界 P-1
- **弱点**: 大 B 时 root contention 爆炸

### Chain Reduce
- **策略**: PE 依次向左邻居传递部分结果，pipelined
- **Depth=P-1, Contention=B**（每 PE 仅收 B 个）
- T = B + (2TR+2)(P-1)
- **最优区间**: B ≫ TR·P（大向量），runtime 接近 contention 下界 B
- **弱点**: 小 B 时 P-1 的 depth 主导
- 使用 2 个 color（红接收/蓝发送），避免单 color 的方向歧义

### Tree Reduce（新）
- **策略**: 二叉树归约，每轮减半活跃 PE
- **Depth=log2(P)**，contention=B·log2(P)
- **最优区间**: 小到中等 B
- **弱点**: 大 B 时 root contention 线性增长

### Two-Phase Reduce（新）
- **策略**: √P 个 PE 一组做 Chain Reduce → 剩余 √P 个 PE 再 Chain Reduce
- **Depth=2√P−2**（vs Chain 的 P−1），**Contention=2B**（仅比 Chain 差 2×）
- 兼顾低 depth 和低 contention
- **最优区间**: 中间范围 B ≈ P
- **距下界**: ≤2.4×，固定算法中全范围最优

### Auto-Gen Reduce（新）
- **策略**: 性能模型驱动自动搜索最优 reduction tree（pre-order 遍历）
- 递归计算 min energy for given (P, B, D, C)，O(P⁴) backtracking
- Python 离线计算 → 自动生成 CSL 代码（routing + PE code）
- **距下界**: ≤1.4×，**严格优于所有固定算法**
- 泛化所有上述算法（Star=星图, Chain=路径, ...）

## 1D AllReduce 算法

### Reduce-then-Broadcast
- 先 Reduce 到 root → flooding Broadcast 到所有 PE
- Broadcast 利用 multicast: T_Bcast = B + P + 2TR（与单播相同！）
- **反直觉**: 在 WSE 上因 multicast，常优于 Ring AllReduce

### Ring AllReduce
- reduce-scatter (P−1 轮) → allgather (P−1 轮)
- 两种 mesh 映射: simple（最长 link = P−1）vs distance-preserving（≤2 hop）
- 预测性能相同（因 bidirectional links: 2(P−1) links）
- T = 2(P−1)B/P + 4P − 6 + 2(P−1)(2TR+1)
- **最优区间**: 大 B（带宽受限区）

## 2D Collectives (M×N=P)

### 2D Broadcast
- x 轴 broadcast + y 轴 multicast 同时执行
- T = B + M + N − 2 + 2TR + 1
- √P×√P grid: 仅 2√P 距离（vs 1D 的 P）
- **显著收益**: 但受限于单 port（processor↔router），两维不能完全并行

### 2D Reduce
- **X-Y Reduce**: 先 x 轴 reduce → y 轴 reduce
- **Snake Reduce**: Chain 沿 snake 路径映射 2D grid
- Snake 的 runtime ≈ 1D Chain（忽略转弯开销）
- 下界: T* ≥ max(B, BP/8 + M+N−1 + 2TR+1)

### 2D AllReduce
- 2D Reduce + 2D Broadcast
- 不同 (B,P) 区域最优算法不同，类似 1D 的 heatmap

## Color 使用约束

| 实现 | Color 数 |
|---|---|
| 1D 各算法 | ≤ 3 |
| 2D 各算法 | ≤ 5 |
| WSE 总共 | 24 |

剩余 color 留给应用使用。Color 是 [ Color 机制](/concepts/cerebras-color-mechanism.md)的虚拟通道。

## 算法选择决策图

```
B=1?        → Star (距下界 1×)
B 小?       → Tree
B ≈ P?      → Two-Phase (≤2.4× 下界)
B ≫ TR·P?  → Chain
任意 B?     → Auto-Gen (≤1.4× 下界，自动选择)
```

## 相关页面
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — Chain/Tree/Two-Phase 的 SpaDA 实现（1.04× HPDC'24 CSL）
- [Near Optimal Wafer Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md) — 原始论文
- [Wse Performance Model](/concepts/wse-performance-model.md) — 指导算法设计的性能模型
- [Cerebras Wse](/entities/cerebras-wse.md) — 目标硬件
- [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) — Color 路由机制
- [Noc Router Microarchitecture](/concepts/noc-router-microarchitecture.md) — NoC Router 微架构
- [Switching Networks](/concepts/switching-networks.md) — mesh 网络与 collective 算法的关系
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性数据流使精确模型预测成为可能

# Citations

[1] [raw/papers/Near-optimal_wafer-scale_reduce.pdf](raw/papers/Near-optimal_wafer-scale_reduce.pdf)
