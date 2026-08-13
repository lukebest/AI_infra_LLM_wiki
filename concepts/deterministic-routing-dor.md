---
type: Concept
title: Deterministic Routing and DOR
description: 确定性路由与维序路由（DOR）：XY/Y-first、e-cube、源路由 vs 分布式；Mesh/Hypercube 最短路径与 CDG 无死锁直觉；WSE 工业选型
tags:
- interconnect
- noc
- routing
- mesh
- hypercube
- dor
- wse
timestamp: '2026-08-13T00:00:00Z'
created: 2026-07-06
updated: 2026-08-13
sources:
- raw/articles/interconn-study-21d-day-11.md
---

# Deterministic Routing and DOR（确定性路由与维序路由）

**拓扑**是静态骨架；**路由**决定报文从 A 到 B 走哪条路径；**流控**分配链路/缓冲资源——三层解耦但强耦合（见 [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)）。本文聚焦 **确定性路由 (Deterministic Routing)** 与 **维序路由 DOR (Dimension-Order Routing)**：Mesh 上 XY、Hypercube 上 e-cube——WSE、TileLink、多数 NoC 的工业默认。

**Source:** [raw/articles/interconn-study-21d-day-11.md](raw/articles/interconn-study-21d-day-11.md)（D&T Ch.4–5，Day 11）

## 路由设计目标

| 目标 | 含义 |
|------|------|
| **连通性** | 任意节点对可达 |
| **无死锁** | 无资源循环等待（[CDG 无环](/concepts/deadlock-free-routing-cdg-dally.md)） |
| **自适应性** | 能否避让拥塞/故障（确定性路由 **否**） |

附加维度：最小 vs 非最小路径；单播 vs 多播。

## 确定性 vs 自适应

**确定性**：给定 (S, D)，路径唯一，不依赖网络状态。

| 优点 | 缺点 |
|------|------|
| 实现简单（看目的坐标） | 不能避让拥塞 |
| 保序 (order-preserving) | 负载可能不均 |
| 延迟可预测（QoS） | 单点故障即不可达 |

**工程结论**：NoC 流量局部化时，**简单 = 工程最优**；自适应详见 [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md)（Day 12）。

## DOR / XY 路由（2-D Mesh）

**规则**：先在 X（列）维对齐，再在 Y（行）维对齐——**第 i 维到达目的前绝不进入 i+1 维**。

```
(0,0) → (3,3):  (0,0)→(1,0)→(2,0)→(3,0)→(3,1)→(3,2)→(3,3)  // 6 跳，最短
```

**Y-first** 同样合法，但 **XY 与 Y-first 不可混用**（否则破坏维序单调）。

伪代码：

```
while src.x != dst.x: src.x += sign(dst.x - src.x)
while src.y != dst.y: src.y += sign(dst.y - src.y)
```

[Mesh and Torus Topology](/concepts/mesh-torus-topology.md) 简述 XY；[Collective-Capable NoC](/concepts/collective-capable-noc.md) 将 address mask 译为 XY fork 做多播。

### 为何 XY + 合适流控 → 无死锁（直觉）

报文**先单调走完 X 通道，再进入 Y 通道** → 通道依赖分层 → CDG 为 **DAG** → 无环。

**反例**：允许 Y→X→Y 绕回 → 依赖环 → 可能死锁。

**注意**：XY（算法）+ **单 VC Wormhole**（流控不足）仍可能死锁 → 需虚通道 (VC) 打破环（见 [NoC Router 微架构](/concepts/noc-router-microarchitecture.md)）。

## e-cube 路由（Hypercube）

Hypercube 上的 DOR：**从低维到高维**，仅在目的地址该位与当前位不同时走该维。

0000 → 1011：Hamming distance = 3；e-cube 确定路径如 0000 → 0001 → 0011 → 0111 → 1011（逐维修正）。

| 性质 | 说明 |
|------|------|
| 路径长度 | = Hamming distance（最短） |
| 路径数 | e-cube 唯一；其他最短路径共 H! 条但非确定性 |

## 源路由 vs 分布式

| 范式 | 实现 | 优缺点 |
|------|------|--------|
| **源路由** | 路径编码在报文头 | 路由器极简；路径固定 |
| **分布式** | 每跳本地看目的地址 | 可扩展自适应；需死锁逻辑 |

工业 NoC（含 [Cerebras WSE](/entities/cerebras-wse.md) 推测）：**分布式确定性 XY**——每 PE router 看目的坐标局部决策。WSE 另用 [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) 静态 color 路由做 collective，与 XY 坐标路由互补。

## WSE-3 量级

~949×949 Mesh，XY 路由：

| 指标 | 值 |
|------|-----|
| 最远跳数 (0,0)→(948,948) | **1896** |
| 平均跳数 | **~632** |
| 16×16 子 Mesh 对角 | 30 跳 |

LLM 分块后流量局部化，最长路径不频繁；**芯片级 AllReduce** 仍受 ~500–1000 跳约束（~2.5–5 μs @ ~5 ns/hop）——见 [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)、[WSE Performance Model](/concepts/wse-performance-model.md)。

**64 PE 区域 barrier**：朴素 XY 邻居通知最坏 ~直径；树形多播可降至 O(log N) 跳——区域性同步树（如 8×8 子 Mesh）把延迟从 O(diameter) 降到 O(log diameter)。

## NPU 16×16 Mesh 要点

- (0,0)→(15,15)：**30 跳**
- 点对点邻居通信 + XY：**路径利用率高**（最短 + 无环）
- 所需特性：**确定性 + 保序**（层间/batch 依赖）

## 相关页面

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Mesh 拓扑与 XY 简介
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 路由/流控耦合
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — VC、wormhole、仲裁
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — XY mask 组播/归约
- [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) — WSE 静态 color 路由
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — Express/CMesh 变体
- [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) — MIN 自路由（对比 DOR）
- [AIC Folded Multi-Ring NoC](/concepts/aic-folded-multi-ring-noc.md) — 跨行 H→V→H 相位约束最短路（几何 DOR）
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md) — 最小/VRR/VC（Day 12）
- [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md) — CDG / Torus≥2 VC（Day 13）
- [Duato Escape VC Deadlock-Free Routing](/concepts/duato-escape-vc-deadlock-free-routing.md) — 逃逸层常用 DOR（Day 14）

# Citations

[1] [raw/articles/interconn-study-21d-day-11.md](raw/articles/interconn-study-21d-day-11.md) — D&T Ch.4–5 Routing（Day 11）
