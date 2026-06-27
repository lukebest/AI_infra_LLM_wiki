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
| **片上互连 (NoC)** | 4–1000+ 节点 | 面积 + 功耗 + 延迟 | [Cerebras WSE](/entities/cerebras-wse.md) Mesh、TileLink Ring |

**拓扑选择约束**：全连接 N 节点需 C(N,2) 条链路与 N−1 端口/节点——1024 节点全连接约 52 万条链路，不可制造。Mesh 以多跳换低端口数：WSE-3 ~949×949 Mesh，度=4，直径≈1896，相对全连接节省约 **145×** 链路，代价是平均 ~500 跳路由深度。

## Mesh vs Fat Tree 的域差异

| | NoC / HPC 机柜 | 数据中心 scale-out |
|--|----------------|-------------------|
| 约束 | 端口数、片上面积、布线密度 | 机架规模、bisection BW、成本 |
| 常见拓扑 | Mesh、Torus、k-ary n-cube | Fat Tree、CLOS（见 [Switching Networks](/concepts/switching-networks.md)） |
| 原因 | 固定端口预算下 Mesh 可单片实现 | 高基数交换 + 多级结构提供可扩展 bisection BW |

## 性能瓶颈三视角

互连成为系统瓶颈时，可从三方面诊断：

1. **物理上限**：光速传播、SerDes 功耗、pin 密度
2. **拓扑上限**：bisection bandwidth、热点、contention（见 [WSE Performance Model](/concepts/wse-performance-model.md)）
3. **协议开销**：序列化延迟、包头、流控 bubble

## 相关页面

- [Switching Principles](/concepts/switching-principles.md) — 电路/分组/虫孔交换演进
- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — 物理→传输四层接口
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — 微架构层实现
- [Cerebras WSE](/entities/cerebras-wse.md) — 晶圆级 Mesh NoC 实例
- [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md) — 数据中心 Fat Tree 变体

# Citations

[1] [raw/articles/interconn-study-21d-day-01.md](raw/articles/interconn-study-21d-day-01.md) — Dally & Towles Ch.1 学习笔记（21 天互连研究 Day 1）
