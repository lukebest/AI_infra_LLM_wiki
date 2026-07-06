---
type: Concept
title: Topology Optimization Variants
description: 拓扑变体与优化：Folding、Concentrated/Collapsed Mesh、Express Cube、Dally 1990 最优维度定律、高基数路由器；Compression vs Expansion 权衡
tags:
- interconnect
- noc
- topology
- mesh
- torus
- hypercube
- wse
timestamp: '2026-07-06T00:00:00Z'
created: 2026-07-06
sources:
- raw/articles/interconn-study-21d-day-09.md
---

# Topology Optimization Variants（拓扑优化与变体）

教科书拓扑（[Mesh and Torus Topology](/concepts/mesh-torus-topology.md)、[Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)、[Butterfly and MIN Topology](/concepts/butterfly-min-topology.md)）很少「纯净」部署——真实系统通过**折叠、浓缩、长链跳跃**在端口数、线延迟、二分带宽三轴上找局部最优。Kim & Chien 1994 将两类变换形式化为 **Compression vs Expansion**。

**Source:** [raw/articles/interconn-study-21d-day-09.md](raw/articles/interconn-study-21d-day-09.md)（Day 9；Dally 1990 IEEE TC + Kim & Chien 1994）

## Compression vs Expansion

| | Compression（浓缩） | Expansion（扩展） |
|--|---------------------|-------------------|
| **做法** | c 个 PE 共享一个路由器 | 长链路跳过中间节点 |
| **代表** | Concentrated Mesh (CMesh) | Express Cube / Express Mesh |
| **收益** | 端口预算↓、有效基数↑ | 直径/平均距离↓ |
| **代价** | 局部端口争用 | 端口数↑、布线复杂 |

[Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) 的 **concentration** 同属 Compression 思路。

## Folding（折叠）

**问题**：1-D Torus / 3-D Torus 的 wrap-around 链路横跨整片芯片 → 线长与延迟方差大。

**方案**：把长链物理折叠到对侧邻居 → 各 hop 线长近似均匀。

Blue Gene/L 的 3-D Torus 采用 folded torus，便于精确性能建模与时钟分配。

## Concentrated / Collapsed Mesh

**c 个相邻 PE 绑定同一路由器**（concentration ratio = c）：

```
普通 Mesh (c=1)          CMesh (c=2)
R - R - R                R(2PE) - R(2PE)
|       |                |           |
R - R - R                R(2PE) - R(2PE)
```

| 效果 | 说明 |
|------|------|
| 路由器数 | ÷ c |
| 有效基数 | 5 → 5c 可指向更多邻居 |
| 代价 | 共享端口 → 本地 PE 间争用 |

## Express Cube / Express Mesh

在 k-ary n-cube 上每 **e** 个节点加一条**长链**（跳过中间 router）：

| 参数 e | 效果 |
|--------|------|
| e↑ | 平均距离↓ |
| e↑ | 端口数↑ |

4×4 Mesh 平均距离 ~2；Express Mesh (e=2) 可降至 ~1.33。链路足够便宜时，长链是「免费」的延迟优化。

## Dally 1990 最优维度定律

William J. Dally, *Performance Analysis of k-ary n-cube Interconnection Networks* (IEEE TC 1990)：

- 固定链路带宽与节点基数下，存在最优 **(k, n)** 使单位带宽延迟最优
- **低维**（n=2）：链路本地化、度低 → 片上 wire delay 小时占优
- **高维**（n=log N）：直径短 → wire delay 占主导（跨板/机柜）时占优
- **反直觉结论**：wire delay 主导时 **n=2 往往最优** → 奠定 2-D Mesh 在 NoC 的地位

与 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) 中 d_opt ≈ 2√N 吞吐量峰值一致；**理论最优 ≠ 工程最优**（见 Day 10 [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) 综合表）。

| 域 | 典型选型 | wire delay 占比 |
|----|----------|-----------------|
| 片上 NoC | 2-D Mesh | 低 → n=2 |
| 机柜内 HPC | 3-D Torus | 中 → n=3 |
| 早期超算机柜间 | Hypercube | 高 → 高维 |

**N=1024 手算**（Mesh 无环绕，B_b = N/k）：

| (k, n) | 直径 | 度 | 直觉 |
|--------|------|-----|------|
| (2, 10) | 10 | 10 | 度太大，片上不可行 |
| (32, 2) | 62 | 4 | **片上首选**（WSE 方向） |
| (1024, 1) | 1023 | 2 | 线性阵列，直径爆炸 |

## 高基数（High-Radix）路由器

端口数 k 增大 → 单级可承担更多 [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) / [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) 功能：

| 场景 | 典型 k |
|------|--------|
| 片上 NoC | 8–16 |
| InfiniBand 交换机 | ~64 |
| 数据中心 Spine (Tomahawk) | ~256 |

片上高基数仍贵；**CMesh** 是把 PE「虚拟基数」转给路由器的常用手段。

## WSE-3 为何纯 2-D Mesh

[Cerebras WSE](/entities/cerebras-wse.md) ~949×949、~900K PE：

| 变体 | 效果 | 未采用原因 |
|------|------|-----------|
| CMesh c=4 | 路由器 ÷4 | 局部争用；PE 流量已高度局部 |
| Express e=4 | 平均距离↓ | 额外端口与布线 |
| **纯 Mesh + XY** | 4 端口可制造 | 片上 wire 便宜；局部通信为主 |

直径 ~1896、平均距离 ~632（见 [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md)）；collective 见 [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)。

## 相关页面

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — k-ary n-cube 基线与 Dally 维度权衡
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 六拓扑统一比较（Day 10）
- [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) — concentration + bypass
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — Mesh 上 XY 路由（Day 11）
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 拓扑/路由/流控四层
- [Cerebras WSE](/entities/cerebras-wse.md) — 2-D Mesh 实例

# Citations

[1] [raw/articles/interconn-study-21d-day-09.md](raw/articles/interconn-study-21d-day-09.md) — D&T Ch.3 变体 + Dally 1990 / Kim & Chien（Day 9）
