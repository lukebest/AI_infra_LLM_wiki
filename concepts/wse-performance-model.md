---
title: WSE Performance Model
created: 2026-06-20
updated: 2026-06-20
type: concept
tags: [cerebras, wse, performance-model, communication, mesh, noc]
sources: [raw/papers/Near-optimal_wafer-scale_reduce.pdf]
confidence: high
---

# WSE 性能模型（Spatial Computer Model for WSE）

Luczynski et al. (HPDC 2024) 提出的 WSE 通信 collective 性能预测模型。基于 spatial computer model [17]，参数化为 WSE 硬件属性。

## 核心公式

```
T = max(C, E/N) + L + (2·TR + 1)·D
```

### 四个瓶颈项

| 项 | 符号 | 含义 | 主导场景 |
|---|---|---|---|
| **Contention** | C | 单 PE 最大收发次数 | 大向量、PE 成 pipeline 瓶颈 |
| **Energy/Links** | E/N | 总跳数 / 可用链路数 | 网络拥塞 |
| **Distance** | L | 最大单 wavelet 跳数 | 小向量、长距离 |
| **Depth** | D | 最长串行依赖链 | 多轮算法（tree/chain） |

### 硬件参数

- **TR** (ramp latency) ≈ 2 cycles (WSE-2)。之前文献误报为 7。
- 每 link 32 bits/cycle/direction
- 每 cycle: 128-bit read, 64-bit write, 8×16-bit ops
- 波特率: 32-bit wavelet, 1 cycle/hop

## 设计洞察

1. **C 主导 → pipeline 行为**: 当 PE contention 远大于网络拥塞时，系统接近 pipeline，每个 cycle 一个 element 到达 PE，网络延迟可忽略
2. **E/N 主导 → 网络拥塞**: 总流量超过网络容量
3. **L 主导 → 延迟敏感**: 小数据长距离，类似传统 α-β 模型的 α 项
4. **D 主导 → 串行瓶颈**: 依赖链过长，类似传统模型中 β 项受 P 限制

## 与传统 α-β 模型的区别

| 维度 | α-β 模型 | WSE 模型 |
|---|---|---|
| 拓扑 | 抽象（任意全连接） | 具体（2D mesh） |
| 多播 | 不考虑 | 核心特性（免费复制） |
| 流水线 | 不考虑 | 内建于 E/N 项 |
| 预测精度 | 粗粒度 | < 4% 误差（CS-2 实测） |

## 应用

此模型不仅用于 Reduce/AllReduce，也可指导 WSE 上任何通信密集型 kernel 的算法设计：
- 通过计算候选算法的 (C, E, L, D) 四元组即可比较性能
- Auto-Gen Reduce 用此模型在 O(P⁴) 内搜索最优 reduction tree
- 证明了 1D 场景下模型预测可达到 ≤1.4× 最优

## 相关页面
- [[near-optimal-wafer-scale-reduce]] — 提出此模型的论文
- [[wse-reduce-algorithms]] — 用此模型分析的算法族
- [[cerebras-wse]] — 目标硬件
- [[cerebras-color-mechanism]] — Color 路由是模型有效的基础（确定性路由）
- [[noc-router-microarchitecture]] — NoC 路由器微架构理论基础
