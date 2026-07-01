---
type: Concept
title: Linear and Ring Topology
description: 线形阵列与环形拓扑：度/直径/二分带宽度量，双向环即 1-D Torus，NoC/SAN/Die-to-Die 应用与 Chordal Ring 扩展
tags:
- interconnect
- noc
- topology
- mesh
- fabric
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/interconn-study-21d-day-05.md
---

# Linear and Ring Topology（线形与环形拓扑）

线形阵列与 Ring 是 Mesh/Torus 的**一维逻辑起点**：节点成本与链路数最小，直径 O(N) 最大——后续多维拓扑的参照系（见 [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md)）。

## Linear Array（线形阵列）

```
[0] —— [1] —— [2] —— ... —— [N−1]
```

| 指标 | 值 |
|------|-----|
| 度 d | 内部 2，端点 1（非对称） |
| 直径 D | **N−1** |
| 平均距离 d̄ | ≈ **N/3** |
| 二分带宽 B_b | **1** 条链路 |
| 链路数 | N−1 |

N=1000 时平均 ~333 跳——直径 O(N) 使大规模系统几乎不可用；单点断开即网络分裂。

## Ring（环形）

在阵列两端加 **wrap-around** 链路；**双向环 = 1-D Torus = k-ary 1-cube**（n=1）。

| | 单向环 | 双向环 |
|--|--------|--------|
| 度（拓扑意义） | 2 | 2 |
| 直径 D | N−1 | **⌊N/2⌋** |
| 平均距离 d̄ | N/2 | ≈ N/4（N=16 手算 ~5.33） |
| 二分带宽 B_b | 1 | **2** |
| 链路数 | N | N |
| 对称性 | 方向固定 | 节点对称 |

### 仍被使用的原因

| 优势 | 说明 |
|------|------|
| **端口最少** | 每节点 2 链路 → 面积/布线/功耗最低 |
| **规则布线** | 线性物理布局，无跨距长线 |
| **天然广播** | 沿环一圈可达所有节点 |
| **有序 multicast** | 沿环发送保证到达顺序 |
| **故障降级** | 单链路断可退化为 Linear Array |

### 典型应用（N 量级）

| 场景 | N 范围 | 例子 |
|------|--------|------|
| 片上 NoC / 总线 | 4–32 | TileLink RingBus、boot 阶段 |
| Die-to-Die | 4–16 | EDM ring：小 N 下直径可接受，有序 snoop 简化 coherence |
| SAN / 存储环 | 数十 | FC-AL、历史 Token Ring |

数据中心规模（N≫100）因直径与 B_b=1–2 几乎不用纯 Ring；大规模走 Mesh/Torus/Fat Tree（[Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)）。

## Chordal Ring 扩展

直径 O(N) 过长时可加 **chord（弦）** 或 **Multi-Ring**：

- O(log N) 条 chord → 直径 **O(log N)**
- 代价：失去 Ring 的极简性与规则布线

## 与 Mesh 的设计对照

Ring 是 [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) 框架下的**极端解**：

```
节点成本 ↑  链路成本 ↑     直径 ↓  二分带宽 ↑
Ring ────────────────────────────────→  Mesh/Torus/Fat Tree
（度=2，B_b=1–2，D=O(N)）              （度↑，B_b↑，D=O(√N)…）
```

**维度提升**（1-D Ring → 2-D Mesh）将直径从 O(N) 降到 O(√N)——WSE 选 2-D Mesh 而非 Ring 的根因之一（见 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)、[Cerebras WSE](/entities/cerebras-wse.md)）。

## 相关页面

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Ring → Mesh/Torus 演进
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — k-ary n-cube 公式（n=1 即 Ring）
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 延迟/成本权衡
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — NoC 域 TileLink Ring vs WSE Mesh
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — Ring AllReduce（逻辑算法，非物理 Ring 拓扑）

# Citations

[1] [raw/articles/interconn-study-21d-day-05.md](raw/articles/interconn-study-21d-day-05.md) — D&T Ch.3 线性结构（Day 5）
