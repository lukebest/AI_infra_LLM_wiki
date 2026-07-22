---
type: Concept
title: Clos and Fat-Tree Topology
description: 间接网络：终端/交换分离、Clos C(n,m,r) 无阻塞条件、Fat-Tree 代价等价与 Beneš RNB，及 InfiniBand/Jupiter 与 WSE 规模分界
tags:
- interconnect
- noc
- topology
- fabric
- infrastructure
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/interconn-study-21d-day-07.md
---

# Clos and Fat-Tree Topology（Clos 与 Fat-Tree 间接网络）

[Mesh and Torus Topology](/concepts/mesh-torus-topology.md) 等**直连网络**中每个节点既是终端又是路由器，受 pin/度约束；当 N 大到「每终端 d 端口」不可承受时，切换到**间接网络（Indirect Network）**——终端只发收，交换节点专职转发。形式化 CLOS 与电信 TST 见 [Switching Networks](/concepts/switching-networks.md)。

## 直连 vs 间接

| 维度 | 直连（Mesh/Torus） | 间接（Clos/Fat-Tree） |
|------|-------------------|----------------------|
| 节点角色 | 终端 + 路由器 | 终端 / 交换分离 |
| 终端度 | 受 pin 限制（NoC 常 ≤8） | 终端度低（常 1） |
| 扩展 | 受 d 约束 | 交换级联 → 线性/对数扩展 |
| 典型 N | 数十–数千 PE | 数千–数十万 server |
| 代表 | [Cerebras WSE](/entities/cerebras-wse.md) Mesh | InfiniBand Fat-Tree、Google Jupiter |

**规模分界**：WSE ~900K PE 仍在 Mesh 可制造范围内；**90 万节点集群**互连需间接拓扑（Fat-Tree / Clos / Dragonfly）。

## Clos 网络 C(n, m, r)

```
输入级 (r 个 n×m)  →  中间级 (m 个 m×m)  →  输出级 (r 个 m×n)
```

| 参数 | 含义 |
|------|------|
| **n** | 每个输入模块的源端数 |
| **m** | 中间模块数 |
| **r** | 每个输入/输出模块端口数 |

**无阻塞定理（Clos）**：

| 类型 | 条件 |
|------|------|
| **严格无阻塞 (SNB)** | **m ≥ 2r − 1** |
| **可重排无阻塞 (RNB)** | **m ≥ r** |

直觉：无阻塞不是消除冲突，而是给冲突留足够**中间路径**。例 C(3,5,3)：m=5 ≥ 2×3−1 → SNB；总交叉点 55，9 端节点。

路由：主要在 input stage 选 middle switch；无两端空闲时需迭代重选（见 [Switching Networks](/concepts/switching-networks.md)）。

## Fat-Tree — 代价等价

Leiserson 思想：**向上链路带宽 = 子树总带宽** → 任意 bisection cut 无瓶颈。

```
Core (1) → Aggregation (k²/4) → Edge (k²/2) → k³/4 端节点
```

k-port Fat-Tree 容纳 **N = k³/4** 终端；总链路 **O(N log N)**，**每终端成本 O(1)**。

4-ary 例：16 端点，8 个 L1（各 2 端），4 个 L2；向上链路带宽逐层翻倍。

与 Clos 关系：大规模 Fat-Tree 实为 Clos 的带宽对称实现；10 万+ 节点常需**三级** Clos 而非二级 Fat-Tree。

## Beneš 与其他 MIN

- **Beneš**：log₂(N) 级 2×2 交换 + perfect shuffle 互连
- **RNB**：可重排后建立任意新连接
- 应用：电信交换、洗牌网络；详见 [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md)（Omega/Banyan/Batcher-Banyan，Day 8）

## 系统实例

| 系统 | 拓扑 | 规模 | 特点 |
|------|------|------|------|
| InfiniBand HDR | 2 层 Fat-Tree | ~4096/子网 | Subnet Manager、自适应路由 |
| Google Jupiter | 6 阶段 Clos | 数十万端口 | 集中式流量工程 |
| Azure (Sonic) | Fat-Tree | 数十万 | 端到端无损 |
| Tofino | 多级 Clos | 64–256 端口 | P4 可编程 |
| Intel Omni-Path | Fat-Tree | 数千 | 链路级流控 |
| [Multi-plane Clos](/concepts/multi-plane-clos-topology.md) | 多平面 Clos | 131K GPU | MRC + SRv6 |

## 与 WSE / 研究

| 场景 | 推荐 | 原因 |
|------|------|------|
| 单片 WSE | 2-D Mesh | 4 端口可造，见 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) |
| 16× WSE 集群 | **Dragonfly**（Day 9） | 非数据中心级 Fat-Tree 过重；非 Torus 直径过长 |
| 100K GPU 训练 | 多平面 Clos | 见 [Multi-plane Clos Topology](/concepts/multi-plane-clos-topology.md) |

InfiniBand 4096 端扩展至 10 万：二级 Fat-Tree 不足 → 三级 Clos、分层 SM、ECMP/自适应路由。

## 相关页面

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 直连网络、维度极限 → 间接网络
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 直连 vs 间接、B_b
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 百万节点需间接 + 高基数 switch
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 处理器互连 vs 数据中心域
- [Switching Networks](/concepts/switching-networks.md) — CLOS 路由、TST、Banyan
- [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) — k-ary n-fly、自路由、Batcher-Banyan
- [Switching Principles](/concepts/switching-principles.md) — Clos 历史里程碑
- [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md) — Mesh vs Fat-Tree 哲学（Day 20）
- [High-Radix Clos Adaptive Routing](/concepts/high-radix-clos-adaptive-routing.md) — DisPERoute（SC'06 / paper-deepdive Day 6）
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 工业高基数 Clos

# Citations

[1] [raw/articles/interconn-study-21d-day-07.md](raw/articles/interconn-study-21d-day-07.md) — D&T Ch.3.6–3.9 间接网络（Day 7）
