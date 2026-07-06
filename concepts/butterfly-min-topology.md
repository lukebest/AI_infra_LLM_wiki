---
type: Concept
title: Butterfly and MIN Topology
description: 多级互连网络（MIN）：k-ary n-fly Butterfly、完美洗牌、自路由；Omega/Banyan/Delta 同构；Batcher-Banyan 无阻塞；与 Clos 路径多样性对比
tags:
- interconnect
- noc
- topology
- butterfly
- banyan
- fabric
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/articles/interconn-study-21d-day-08.md
---

# Butterfly and MIN Topology（蝶形与多级互连网络）

**多级互连网络 (MIN)** 用 **log_k(N) 级** k×k 交换节点 + **洗牌 (shuffle) 互连**，以 **自路由 (self-routing)** 把全局路径决策下放到每级局部——与 [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)「靠充足中间级吸收冲突」的哲学相对。Dally & Towles **Ch.3.10–3.13**。

**Source:** [raw/articles/interconn-study-21d-day-08.md](raw/articles/interconn-study-21d-day-08.md)（Day 8）

## k-ary n-fly Butterfly

连接 **N = kⁿ** 端点，**n 级**交换，每级 **N/k** 个 k×k 节点。

| 指标 | 2-ary n-fly |
|------|-------------|
| **直径** | **n** = log_k(N)（源到目的恰 n 级） |
| **链路数** | N · n · k / 2 |
| **与超立方体** | 2-ary n-fly = n 维 Boolean cube 的「时间展开」 |

## 自路由 (Self-Routing)

目的地址 d 的 **k 进制 n 位**逐位决定每级输出端口（2-ary 即每级看 1 bit）：

```
源 0 (000) → 目的 5 (101):
  级0: bit=1 → down
  级1: bit=0 → up
  级2: bit=1 → down
```

- **优点**：无全局路由表，O(log N) 局部决策
- **代价**：**路径唯一** → 易冲突、**阻塞 (blocking)**

## 完美洗牌 (Perfect Shuffle)

节点 i → **k·i mod (kⁿ−1)**；2-ary 8 节点 = 编号 **循环左移 1 位**。洗牌使相邻级交换节点看到**分散的路由位**——MIN 的几何骨架。

## MIN 变体（拓扑同构）

| 网络 | 洗牌 | 备注 |
|------|------|------|
| **Omega** | perfect shuffle | 直角连接 |
| **Butterfly** | 等价形式 | 最常物理实现 |
| **Baseline** | 逆洗牌 | 与 Butterfly 同构 |
| **Delta** | 洗牌族抽象 | 最一般描述 |
| **Banyan** | 自递归 | **有自路由性质即 Banyan 类** |

**关键洞察**：自路由 MIN 仅**绘制方式**不同，本质均为 N/k × log_k(N) 级结构。

## 阻塞与 Batcher-Banyan

**Banyan 阻塞**：多 packet 路径在同一交换节点冲突 → head-of-line blocking。

| 缓解 | 机制 |
|------|------|
| 内部缓冲 / speedup | 成本↑ |
| **Batcher-Banyan** | Batcher **排序网络**（O(log²N) 级）按目的排序 → Banyan **对排序流无阻塞** |

```
源 → [Batcher sort] → [Banyan route] → 目的
```

历史：AT&T No.1 ESS、IBM 3081；今日 **硅光交换**、片上异构 NoC 复兴。

## vs Clos / Fat-Tree

| | Butterfly MIN | Clos C(n,m,r) |
|--|---------------|---------------|
| 级数 | **log N** | 常 3 级（但 m 大） |
| 路径数 (0→63, N=64) | **1 条** | **最多 8 条**（RNB） |
| 硬件成本 | **低** | **高**（中间级多） |
| 阻塞 | 默认 blocking | SNB/RNB 设计目标 |

**硅光 Banyan**：级数少 → **插入损耗最小**；代价需 Batcher 前置。

## vs 片上 Mesh（WSE）

[Cerebras WSE](/entities/cerebras-wse.md) 选 **2-D Mesh** 而非 Butterfly：

- 每 **PE 自带 router**，无专用 MIN 交换节点
- 直径 O(√N) ~950 跳 vs log₂(900K)≈20，但 **多路径 + 自适应路由**
- MIN 片上优势主要在 **光互连 / 专用 NoC**

[Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) 为 off-chip/片上 **高基数压扁 butterfly** 变体（Kim et al.）。

## 相关页面

- [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 间接网络「多路径」侧
- [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) — k-ary n-fly 压扁 + concentration
- [Switching Networks](/concepts/switching-networks.md) — CLOS、TST、Banyan 电信视角
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 直连 vs MIN 选型
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 拓扑设计空间
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 直径、度、B_b

# Citations

[1] [raw/articles/interconn-study-21d-day-08.md](raw/articles/interconn-study-21d-day-08.md) — D&T Ch.3 Butterfly & MINs（Day 8）
