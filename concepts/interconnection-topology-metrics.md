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
- raw/articles/interconn-study-21d-day-05.md
- raw/articles/interconn-study-21d-day-06.md
- raw/articles/interconn-study-21d-day-07.md
- raw/articles/interconn-study-21d-day-10.md
---

# Interconnection Topology Metrics（互连拓扑度量）

评估 Mesh、Torus、Fat-Tree、Hypercube 等拓扑不能凭直觉，需用**度量指标**——它们决定性能上界，也决定**能否制造**（端口、布线、功耗）。2-D 结构与 Mesh/Torus 选型见 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)；一维基线见 [Linear and Ring Topology](/concepts/linear-ring-topology.md)。

## 直连 vs 间接网络

| | 直连 (Direct) | 间接 (Indirect) |
|--|---------------|-----------------|
| 节点角色 | 计算 + 路由 | 终端仅计算；路由在 Switch |
| 端口约束 | 度 d = PE 引脚上限 | Switch 可高基数 |
| 例子 | [Cerebras WSE](/entities/cerebras-wse.md) Mesh | [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)、CLOS |

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

Torus 用 **+33% 链路**换直径↓、B_b↑——Blue Gene/L 等 HPC 选 Torus 的原因；代价是环绕**长 wire**。双向环即 **n=1** 的 k-ary n-cube（见 [Linear and Ring Topology](/concepts/linear-ring-topology.md)）。

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

- **最优维度** d_opt ≈ **2√N** 时直连网络吞吐量最大（Dally 1990）——见 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)、[Topology Optimization Variants](/concepts/topology-optimization-variants.md)

## 六大度量（统一比较语）

| 指标 | 反映 |
|------|------|
| **度 d** | 端口成本、可制造性 |
| **直径 D** | 延迟上界 |
| **平均距离 d̄** | 平均延迟 |
| **二分带宽 B_b** | 吞吐量上界（**最关键**） |
| **对称性** | 路由/算法是否简化 |
| **等分线长** | 物理布线成本 |

**Source:** [raw/articles/interconn-study-21d-day-10.md](raw/articles/interconn-study-21d-day-10.md)（拓扑篇收官，Day 10）

## 主流拓扑统一比较

| 拓扑 | 度 | 直径 | 平均距离 | 二分带宽 | 对称 | 典型规模 |
|------|-----|------|----------|----------|------|----------|
| Linear Array | 2 (1) | N−1 | (N+1)/3 | 1 | 否 | 几十 |
| Ring | 2 | ⌊N/2⌋ | ~N/4 | 2 | 是 | 几十–几百 |
| 2-D Mesh (k×k) | 2–4 | 2(k−1) | ~2k/3 | k | 否 | 数十–数百 |
| 2-D Torus | 4 | 2⌊k/2⌋ | k/2 | 2k | 是 | 数百–数千 |
| 3-D Torus / Hypercube | 2n / log₂N | n⌊k/2⌋ / log₂N | ~log N | N/k ~ N/2 | 是 | 数百–数千 |
| k-ary n-fly MIN | k | n | n | N/(2n) | 是 | 数千 |
| Fat Tree | 终端 1 | 2log_k N | ~log N | N/2 | 否 | 数百–数万 |
| Clos C(n,m,r) | m | ~3 | ~3 | r·m | 否 | 数据中心 |

**N=256 手算**（16×16 Mesh/Torus；8-ary 3-fly；8-ary 4-cube）：

| 拓扑 | 直径 | B_b | 备注 |
|------|------|-----|------|
| Mesh 16×16 | 30 | 16 | 度 2–4 |
| Torus 16×16 | 16 | 32 | 度 4 |
| Clos 8-ary 3-fly | ~6 | 64 | 终端度 1 |
| Hyper 8-ary 4-cube | 4 | 128 | 度 4，直径最小 |

## 拓扑选择决策树

```
片上 NoC（端口 4–6）     → 2-D Mesh（+ 变体见 Topology Optimization）
机柜内 HPC（可 3-D 堆叠） → 3-D Torus（Blue Gene/L）
数据中心 scale-out       → Fat Tree / Clos / Dragonfly
特殊流量 / 光互连        → Butterfly MIN、Custom
```

**三轴权衡**：端口成本（度）↔ 直径/延迟 ↔ 二分带宽。**没有最好，只有最匹配**——流量特征 + 物理约束 + 工程成本。

| 对比 | NoC Mesh | HPC Fat Tree |
|------|----------|--------------|
| 端口 | PE 仅 4–6 pin | 机架间光模块，度不受限 |
| 流量 | **局部**（相邻 PE） | **随机/热点**（AllReduce） |
| 布线 | 规则、可制造 | 多级交换、高 B_b |

WSE ~900K 节点若用 20 维 Hypercube：直径 20 但 **每 PE 需 20 端口**——物理不可行；故 [Cerebras WSE](/entities/cerebras-wse.md) 选 2-D Mesh + [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) XY。

LLM 训练 AllReduce/AllToAll 需 B_b ≥ 流量强度；WSE 片上流量局部化（分块 attention）缓解全芯片 bisection 压力。

## 相关页面

- [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 间接网络与 Clos 定理
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 2-D Mesh/Torus 与维度权衡
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 指标→延迟/成本公式
- [Linear and Ring Topology](/concepts/linear-ring-topology.md) — 1-D 基线与 1-D Torus
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 四层设计空间
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — Folding/CMesh/Express（Day 9）
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — Mesh XY 路由（Day 11）
- [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) — k-ary n-fly MIN
- [Cerebras WSE](/entities/cerebras-wse.md) — Mesh 实例
- [WSE Performance Model](/concepts/wse-performance-model.md) — 距离/contention 瓶颈

# Citations

[1] [raw/articles/interconn-study-21d-day-03.md](raw/articles/interconn-study-21d-day-03.md) — D&T Ch.3.1–3.2（Day 3）
[2] [raw/articles/interconn-study-21d-day-05.md](raw/articles/interconn-study-21d-day-05.md) — 1-D Ring 基线（Day 5）
[3] [raw/articles/interconn-study-21d-day-06.md](raw/articles/interconn-study-21d-day-06.md) — 2-D Mesh/Torus（Day 6）
[4] [raw/articles/interconn-study-21d-day-07.md](raw/articles/interconn-study-21d-day-07.md) — Clos/Fat-Tree（Day 7）
[5] [raw/articles/interconn-study-21d-day-10.md](raw/articles/interconn-study-21d-day-10.md) — 拓扑大综合（Day 10）
