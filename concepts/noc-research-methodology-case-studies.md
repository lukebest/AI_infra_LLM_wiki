---
type: Concept
title: NoC Research Methodology and Case Studies
description: 互连 Day 20 — NoC 论文三层读法；CMP 四原则；Packets not Wires；Polaris 5GHz Mesh；Mesh vs Fat-Tree；WSE 反推
tags:
- noc
- methodology
- research
- mesh
- cmp
- paper
- wse
- polaris
timestamp: '2026-07-21T00:00:00Z'
created: 2026-07-21
sources:
- raw/articles/interconn-study-21d-day-20.md
---

# NoC Research Methodology and Case Studies（NoC 研究读法与案例）

interconn-study **应用篇 Day 20**：教材读完后的**方法论实战**——用四层设计空间反推论文与工业芯片。体系结构通读法见 [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md)；本页偏 **NoC 五决策 + 案例坐标**。

**Source:** [raw/articles/interconn-study-21d-day-20.md](raw/articles/interconn-study-21d-day-20.md)  
扩展精读：paper-deepdive [Day 2](raw/articles/paper-deepdive-day-02.md)（Route Packets）、[Day 3](raw/articles/paper-deepdive-day-03.md)（Polaris）、[Day 4](raw/articles/paper-deepdive-day-04.md)（Balfour）→ [Paper Deep-Dive Map](/summaries/paper-deepdive.md)。

## 论文「读三层」

| 层 | 问什么 |
|----|--------|
| **贡献** | 解决 X，用 Y，得 Z（一句话） |
| **方法** | 拓扑 / 路由 / 流控 / 微架构 / NI 怎么选 |
| **约束** | 面积、功耗、延迟、吞吐、可制造性 |

真贡献 checklist：是否真有新拓扑/流控/微架构/NI？仿真还是硅实测？通常需 **≥2 项新东西 + 可信测量**。

## 奠基：Route Packets, Not Wires（Dally & Towles, DAC 2001）

三层含义：总线→多跳网络；电路→报文统计复用；私有线协议→通用包接口。五个决策（拓扑/路由/流控/微架构/NI）**相互约束**且至今未变——变的是工艺与规模（如 WSE 百万 PE）。

## CMP 四原则（Balfour & Dally, ICS 2006）

| 原则 | 含义 |
|------|------|
| 低基数路由器 | 端口 ≤~8（Crossbar ∝ N²） |
| 规则拓扑 | Mesh/Torus，路由/良率友好 |
| 维度对齐 | k-ary n-cube → DOR 直接可用 |
| 流控极简 | Wormhole + 2–4 VC |

Polaris、Tilera、大量 CMP——以及公开材料下的 **WSE 推测设计**——都落在这四条上。规模放大 ≠ 违反原则：每 PE 仍可是 5-port。

## 案例：Intel Polaris 5 GHz Mesh（Hoskote, IEEE Micro 2007）

| 参数 | 值 |
|------|-----|
| 拓扑 | 10×8 Mesh，80 tile |
| Router | 5-port，virtual bypass |
| 时钟 | tile 5 GHz / **mesh 2 GHz**（半频） |
| 流控 | Wormhole + 2 VC |
| 单跳 | ~2 router + 1 link 拍 |

工程要点：Mesh 是 CMP「最低公分母」；wire delay + skew → mesh 难跟核同频；bypass = Day 18 优化的硅实现；Fat-Tree 高基数片上做不起。

## Mesh vs Fat-Tree 哲学

| | Mesh / NoC | Fat-Tree / HPC |
|--|------------|----------------|
| 口号 | 长度匹配、低基数可堆叠 | 带宽最大、严格无阻塞 |
| 直径 | O(√N) | O(log N) |
| 二分带宽 | 中 | 最高 |
| 面积 | 小 | 大（高基数） |

WSE：**Mesh 哲学 + 规模带宽密度**——链路数×单链路带宽可超过传统 Fat-Tree 集群总带宽，同时保住可制造的 5-port 路由器。见 [Mesh and Torus](/concepts/mesh-torus-topology.md)、[Clos and Fat-Tree](/concepts/clos-fat-tree-topology.md)、[Cerebras WSE](/entities/cerebras-wse.md)。

## WSE 三层反推（笔记框架）

1. **贡献**：单晶圆 ~90 万 PE 片上互连  
2. **方法**：2D Mesh + DOR 变体 + Wormhole + 5-port + 显式消息 NI  
3. **约束**：良率/可制造性、确定性 LLM 流量、极简功耗  

与 [NoC Router Pipeline Optimizations](/concepts/noc-router-pipeline-optimizations.md)、[Network Interface and System-Level Design](/concepts/network-interface-and-system-design.md) 衔接。

## 相关页面

- [Network Interface and System-Level Design](/concepts/network-interface-and-system-design.md) — Day 19
- [Interconn-Study 21d Knowledge Map](/summaries/interconn-study-21d-knowledge-map.md) — Day 21
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)
- [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md)
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md)
- [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) — 高基数另一条路
- [CMP NoC Pareto Design Tradeoffs](/concepts/cmp-noc-pareto-design-tradeoffs.md) — Day 4 展开
- [Paper Deep-Dive Map](/summaries/paper-deepdive.md)

# Citations

[1] [raw/articles/interconn-study-21d-day-20.md](raw/articles/interconn-study-21d-day-20.md) — 论文精读与案例（Day 20）
