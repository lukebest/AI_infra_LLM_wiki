---
type: Concept
title: High-Radix Clos Adaptive Routing
description: Kim/Dally/Abts SC 2006 — high-radix Clos + DisPERoute 自适应；挑战 mesh+DOR 普适最优；负载均衡与死锁自由
tags:
- noc
- clos
- high-radix
- adaptive-routing
- hpc
- topology
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- raw/articles/paper-deepdive-day-06.md
---

# High-Radix Clos Adaptive Routing（高基数 Clos 自适应路由）

Kim, Dally, Abts, **SC 2006**。paper-deepdive **Day 6**：[raw/articles/paper-deepdive-day-06.md](raw/articles/paper-deepdive-day-06.md)。摘要：[papers/kim-adaptive-routing-high-radix-clos.md](/papers/kim-adaptive-routing-high-radix-clos.md)。

相对 [Balfour CMP Mesh Pareto](/concepts/cmp-noc-pareto-design-tradeoffs.md)：**假设级**跃迁——在 radix≥64 工艺下，indirect Clos + 自适应可 Pareto-dominate mesh + DOR。

## 核心论断

| | Mesh + DOR（CMP 默认） | High-radix Clos + adaptive |
|--|----------------------|----------------------------|
| 路由器基数 | 5–7 | **64–128** |
| 跳数 | O(√N) | **O(log N)** |
| 吞吐（文中） | ~50%（DOR on Clos）| **62–95%**（DisPERoute） |
| 负载 | 路径少、易热点 | 多路径 + 拥塞感知 |

## DisPERoute（要点）

- **Deadlock-free Path-diverse Routing**：保留 path diversity，同时保证无死锁  
- 局部拥塞感知选路（vs 纯确定性）  
- 与 [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md)、[Duato Escape VC](/concepts/duato-escape-vc-deadlock-free-routing.md) 同一工具箱（逃逸/VC 纪律）  

拓扑底座：[Clos and Fat-Tree](/concepts/clos-fat-tree-topology.md)。工业延伸：Cray BlackWidow → 现代 [NVLink/NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md) 高基数交换。

## 与 WSE / LLM fabric

- Mesh 上 FRED 步数 ~O(√N)；若逻辑拓扑 Clos-like，集体通信直径可压到 O(log N)——研究假设，非 WSE 现状  
- WSE 仍偏低基数 Mesh（可制造性）；高基数思想出现在 **边缘交换机 / rack fabric** 与 [TPU v4 OCS](/concepts/tpu-v4-ocs-reconfigurable-fabric.md)  

## 相关页面

- [CMP NoC Pareto Design Tradeoffs](/concepts/cmp-noc-pareto-design-tradeoffs.md) — 被挑战的 Mesh 假设
- [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md)
- [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) — 高基数另一拓扑
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md)
- [Paper Deep-Dive Map](/summaries/paper-deepdive.md)

# Citations

[1] [raw/articles/paper-deepdive-day-06.md](raw/articles/paper-deepdive-day-06.md) — Kim SC'06 精读（Day 6）
