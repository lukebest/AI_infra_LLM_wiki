---
type: Paper
title: "Budgeted Express-Mesh: Traffic-Aware Link Placement and Deadlock-Free Routing"
description: 清华 — 固定线预算 traffic-aware express mesh；Greedy ASPL+SA；Garnet；高负载 Tornado Greedy vs Random 吞吐最高 +50.7%
tags:
- noc
- mesh
- interconnect
- topology
- routing
- fabric
- architecture
- switch
- chiplet
timestamp: '2026-09-17T00:00:00Z'
created: 2026-09-17
updated: 2026-09-17
sources:
- raw/papers/Budgeted_Express_Mesh_NoC_2026.pdf
- raw/papers/budgeted-express-mesh-noc.md
---

# Budgeted Express-Mesh: Traffic-Aware Link Placement and Deadlock-Free Adaptive Routing

**Authors:** Li Cao, Jingyuan Ma
**Affiliation:** Tsinghua University（课设/课程论文；Instructor: Prof. Kaisheng Ma）
**arXiv:** [2609.17057](https://arxiv.org/abs/2609.17057)（2026-09-15，cs.AR/cs.NI；Wed 9/16 列表 v2）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.17057)

在固定 **wire budget** 下，向 2D mesh 加入少量 **traffic-aware express links**，并用 ASPL greedy + simulation-guided annealing 放置；运行时 committed top-K 路由 + 死锁 escape。补 [Topology Optimization Variants](/concepts/topology-optimization-variants.md) 里 Express Mesh 的现代仿真证据。

## 动机

少量长距离链路可决定整网饱和吞吐，而其余容量闲置；只比 Mesh、或随机放置，无法回答「预算内如何放」。

## 方案

- **放置**：traffic-aware ASPL Greedy（单位线成本最大降 ASPL）；再 SA 以仿真吞吐/延迟目标 refining。
- **路由**：committed top-K；延迟量化的 express 拥塞与 reservation；escape timeout。
- **仿真**：gem5 **Garnet**；默认 8×8、B=32、1 flit/cycle；扩展 **16×16 异构 SoC** 流量。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| Mesh → Greedy 静态 | ASPL **5.333→3.837**，Diam **14→8**（8 links / wire cost 31） |
| 注入率 0.80 Tornado | Greedy vs Random 吞吐 **+50.7%**；SA vs Greedy **+3.7%** |
| 注入率 0.70 Tornado / CutStress | Greedy vs Random **+45.7%** / **+33.2%** |
| SA vs Greedy（高负载多流量） | 吞吐再 **+1.3–7.1%** |

低负载（0.40）增益很小；高负载才拉开。合成流量，非 LLM 应用迹。

## 与 wiki 的关系

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 基拓扑
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — Express Mesh / Expansion 变体
- [Adaptive Routing NoC](/concepts/adaptive-routing-noc.md) — 自适应与 escape
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — ASPL/直径
- [NoC Router Microarchitecture](/concepts/noc-router-microarchitecture.md) — Garnet 路由器语境
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — LLM 集体通信 NoC 对照（本文无集体原语）

## 开放问题

1. 真实 LLM all-reduce / MoE dispatch 迹下预算放置是否同序。
2. Express 延迟 τ(e) 与封装线长模型耦合后，SA 目标是否翻转。
3. 与 wafer-scale / chiplet 长边链路的端口度约束。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.17057) — Cao & Ma, arXiv:2609.17057
[2] [raw/papers/budgeted-express-mesh-noc.md](raw/papers/budgeted-express-mesh-noc.md) — ingest stub
