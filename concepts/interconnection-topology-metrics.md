---
type: Concept
title: Interconnection Topology Metrics
description: 互连拓扑度量：度/直径/平均距离/二分带宽/对称性，k-ary n-cube 公式，Mesh vs Torus 对比
tags:
- interconnect
- noc
- topology
- mesh
- fabric
- wse
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/interconn-study-21d-day-03.md
---

# Interconnection Topology Metrics（互连拓扑度量）

评估 Mesh、Torus、Fat-Tree、Hypercube 等拓扑不能凭直觉，需用**度量指标**——它们决定性能上界，也决定**能否制造**（端口、布线、功耗）。

## 直连 vs 间接网络

| | 直连 (Direct) | 间接 (Indirect) |
|--|---------------|-----------------|
| 节点角色 | 计算 + 路由 | 终端仅计算；路由在 Switch |
| 端口约束 | 度 d = PE 引脚上限 | Switch 可高基数 |
| 例子 | [Cerebras WSE](/entities/cerebras-wse.md) Mesh | Fat Tree、CLOS |

WSE：~900K PE **全部参与路由**，每 PE **4 端口**。

## 五个核心指标

| 指标 | 符号 | 含义 |
|------|------|------|
| **度** | d | 每节点链路数 → 端口成本 |
| **直径** | D | 任意两点最短路径的最大值 → 最坏延迟 |
| **平均距离** | d̄ | 所有节点对最短路径均值 → 平均延迟 |
| **二分带宽** | B_b | 将网络切成两半需穿过的**最少链路数** → 聚合吞吐量上界 |
| **节点对称性** | — | 各节点局部结构是否相同 → 路由复杂度 |

**关键**：**二分带宽最关键**——决定最大聚合吞吐量；其他指标在 B_b 约束下被流量模式进一步限制。

## k-ary n-cube（N = kⁿ 节点）

| 指标 | Mesh（无环绕） | Torus（有环绕） |
|------|----------------|-----------------|
| 度 | 2n（内部）；边/角更小 | 2n（全节点） |
| 直径 | **n(k−1)** | **n⌊k/2⌋** |
| 平均距离 | ≈ n(2k−1)/3 | ≈ nk/4 |
| 二分带宽 | **N/k** 条链路 | **2N/k** 条链路 |

Torus 环绕链路穿过 bisection cut → B_b 为 Mesh 的 **2×**。

## 4×4 对比（手算基准）

| | 4×4 Mesh | 4×4 Torus |
|--|----------|-----------|
| 直径 D | 6 | **4** (−33%) |
| 平均距离 d̄ | ~2.67 | **2** |
| 二分带宽 B_b | 4 | **8** (+100%) |
| 总链路 | 24 | 32 (+33%) |
| 对称性 | 否（角/边/内） | 是 |

Torus 用 **+33% 链路**换直径↓、B_b↑——Blue Gene/L 等 HPC 选 Torus 的原因；代价是环绕**长 wire**。

## WSE-3 ~949×949 Mesh（估算）

| 指标 | 值 |
|------|-----|
| N | ~900,000 |
| 度 d | 4（边界略少） |
| 直径 D | ≈ **1896** hops |
| 平均距离 d̄ | ≈ **632** hops（公式 nk/3 − n/6，k≈949） |
| 二分带宽 B_b | ≈ **949** 条链路 |
| 总链路 | ≈ **1.8M** |

典型随机 PE 对通信需经 **~632** 个 router（与 d̄ 一致）。**勿将 d̄ 与网格边长 k≈949 或直径 D≈1896 混为一谈**——早期笔记曾误写 ~949 / ~500。必须优化单跳延迟（见 [NoC Router 微架构](/concepts/noc-router-microarchitecture.md)）。

### 为何 WSE 不用 Torus？

- Torus 需**跨晶圆环绕长连线** → wire delay + 功耗
- Mesh 全是**局部短连线** → 物理可制造
- 教科书最优 ≠ 硅片可实现的最优

## 相关页面

- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 指标→延迟/成本公式
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 四层设计空间
- [Cerebras WSE](/entities/cerebras-wse.md) — Mesh 实例
- [WSE Performance Model](/concepts/wse-performance-model.md) — 距离/contention 瓶颈

# Citations

[1] [raw/articles/interconn-study-21d-day-03.md](raw/articles/interconn-study-21d-day-03.md) — D&T Ch.3.1–3.2（Day 3）
