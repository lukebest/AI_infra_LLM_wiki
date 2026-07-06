---
type: Concept
title: Interconnection Network Design Space
description: Dally & Towles 互连网络四层设计空间（应用→拓扑/路由/流控→微架构）、基本术语与三大应用域
tags:
- interconnect
- noc
- topology
- routing
- flow-control
- fabric
- mesh
- infrastructure
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/interconn-study-21d-day-01.md
- raw/articles/interconn-study-21d-day-03.md
- raw/articles/interconn-study-21d-day-04.md
- raw/articles/interconn-study-21d-day-05.md
- raw/articles/interconn-study-21d-day-06.md
- raw/articles/interconn-study-21d-day-07.md
---

# Interconnection Network Design Space（互连网络设计空间）

互连网络是多节点系统的**通信骨架**——系统性能上限往往由节点间通信效率决定，而非单节点算力。Dally & Towles 将设计问题组织为**四层强耦合的设计空间**。

## 四层设计空间

```
┌─────────────────────────────┐
│  应用 / 算法 (Algorithms)   │  ← 流量特征（burst、pattern、size）
├─────────────────────────────┤
│  拓扑 (Topology)            │  ← 物理/逻辑布局
│  路由 (Routing)             │  ← 路径选择
│  流控 (Flow Control)        │  ← 资源分配与缓冲
├─────────────────────────────┤
│  微架构 (Microarchitecture) │  ← 路由器/链路硬件实现
└─────────────────────────────┘
```

**耦合示例**（层间不可独立优化）：

| 选择 | 连锁约束 |
|------|----------|
| 2D Mesh | 最短路径集受限 → dimension-ordered / Torus 路由 |
| Wormhole 流控 | 需虚通道 (VC) 打破路由死锁环 |
| 高基数路由器 | 改变最优拓扑（Fat Tree / Flattened Butterfly 优于 Mesh） |

## 基本术语

| 术语 | 定义 | 例子 |
|------|------|------|
| **Node** | 通信端点 | CPU、GPU、Switch、PE |
| **Link** | 两节点间物理连接 | SerDes、光纤、片上 wire |
| **Port** | 节点上一个方向的物理接口 | Mesh PE 的上下左右各一 port |
| **Channel** | 链路 + 缓冲区，端到端资源单元 | 一条物理链路上的多条 VC |
| **Message** | 应用层逻辑数据单元 | AllReduce 一次操作 |
| **Packet / Flit / Phit** | 网络层 / 流控层 / 物理层细分单元 | 见 [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) |

## 三大应用域

| 域 | 典型规模 | 优化目标 | 代表系统 |
|----|----------|----------|----------|
| **处理器互连** | 8–100k 节点 | 延迟 + 吞吐量 | InfiniBand Fat Tree、HPC Torus |
| **I/O 互连** | 数百–数千 | 可靠性 + 延迟 | Fibre Channel、SAS |
| **片上互连 (NoC)** | 4–1000+ 节点 | 面积 + 功耗 + 延迟 | [Cerebras WSE](/entities/cerebras-wse.md) Mesh（[Mesh and Torus Topology](/concepts/mesh-torus-topology.md)）、[Linear and Ring Topology](/concepts/linear-ring-topology.md)（TileLink Ring） |

**拓扑选择约束**：全连接不可制造。WSE-3 为 ~949×949 **2D Mesh**（度=4，直径≈1896，B_b≈949 条链路）——详见 [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) 与 [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md)。

## Mesh vs Fat Tree 的域差异

| | NoC / HPC 机柜 | 数据中心 scale-out |
|--|----------------|-------------------|
| 约束 | 端口数、片上面积、布线密度 | 机架规模、bisection BW、成本 |
| 常见拓扑 | Mesh、Torus、k-ary n-cube | [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)、CLOS（见 [Switching Networks](/concepts/switching-networks.md)） |
| 原因 | 固定端口预算下 Mesh 可单片实现 | 高基数交换 + 多级结构提供可扩展 bisection BW |

## 性能瓶颈三视角

互连成为系统瓶颈时，可从三方面诊断：

1. **物理上限**：光速传播、SerDes 功耗、pin 密度
2. **拓扑上限**：bisection bandwidth、热点、contention（见 [WSE Performance Model](/concepts/wse-performance-model.md)）
3. **协议开销**：序列化延迟、包头、流控 bubble

## 相关页面

- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 度/直径/二分带宽
- [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — Clos 定理与 Fat-Tree 代价等价
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 2-D Mesh/Torus 与 k-ary n-cube
- [Linear and Ring Topology](/concepts/linear-ring-topology.md) — 1-D 基线拓扑
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 延迟与成本公式
- [Switching Principles](/concepts/switching-principles.md) — 电路/分组/虫孔交换演进
- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — 物理→传输四层接口
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — 微架构层实现
- [Cerebras WSE](/entities/cerebras-wse.md) — 晶圆级 Mesh NoC 实例
- [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md) — 数据中心 Fat Tree 变体
- [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) — 自路由 MIN（Day 8）

# Citations

[1] [raw/articles/interconn-study-21d-day-01.md](raw/articles/interconn-study-21d-day-01.md) — Dally & Towles Ch.1（Day 1）
[2] [raw/articles/interconn-study-21d-day-03.md](raw/articles/interconn-study-21d-day-03.md) — Ch.3.1–3.2（Day 3）
[3] [raw/articles/interconn-study-21d-day-04.md](raw/articles/interconn-study-21d-day-04.md) — Ch.3.3–3.5（Day 4）
[4] [raw/articles/interconn-study-21d-day-05.md](raw/articles/interconn-study-21d-day-05.md) — Ch.3 线性/Ring（Day 5）
[5] [raw/articles/interconn-study-21d-day-06.md](raw/articles/interconn-study-21d-day-06.md) — Ch.3 Mesh/Torus（Day 6）
[6] [raw/articles/interconn-study-21d-day-07.md](raw/articles/interconn-study-21d-day-07.md) — Ch.3 间接网络（Day 7）
[7] [raw/articles/interconn-study-21d-day-08.md](raw/articles/interconn-study-21d-day-08.md) — Ch.3 Butterfly/MIN（Day 8）
