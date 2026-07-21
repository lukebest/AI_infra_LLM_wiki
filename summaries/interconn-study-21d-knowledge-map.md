---
type: Summary
title: Interconn-Study 21d Knowledge Map
description: 互连网络 21 天收束：四层金字塔、六块速查、三大洞察、与 WSE/NPU 研究衔接
tags:
- noc
- interconnection
- summary
- methodology
- mesh
- wse
- routing
- flow-control
timestamp: '2026-07-21T00:00:00Z'
created: 2026-07-21
sources:
- raw/articles/interconn-study-21d-day-21.md
---

# Interconn-Study 21d Knowledge Map（互连 21 天知识地图）

interconn-study **Day 21 收官**：不读新章——把 Day 1–20 **压成地图与研究衔接**。完整笔记：[raw/articles/interconn-study-21d-day-21.md](raw/articles/interconn-study-21d-day-21.md)。

## 四层脉络

```
性能与评估 ← Day 4, 20
        ↑
路由器微架构 / 流水线 ← Day 17–18
        ↑
流控（WH / VC / Credit） ← Day 15–16
        ↑
死锁 ← Day 13–14 | 路由 ← Day 11–12 | 拓扑 ← Day 5–10
        ↑
基础 + NI / 系统 ← Day 1–4, 19
```

| 阶段 | Days | 锚点概念 |
|------|------|----------|
| 基础 | 1–4 | [Design Space](/concepts/interconnection-network-design-space.md), [Cost Model](/concepts/interconnection-network-cost-model.md) |
| 拓扑 | 5–10 | [Mesh/Torus](/concepts/mesh-torus-topology.md), [Clos/Fat-Tree](/concepts/clos-fat-tree-topology.md), [Butterfly](/concepts/butterfly-min-topology.md), [Topology Metrics](/concepts/interconnection-topology-metrics.md), [Variants](/concepts/topology-optimization-variants.md) |
| 路由 | 11–14 | [DOR](/concepts/deterministic-routing-dor.md), [Adaptive](/concepts/adaptive-routing-noc.md), [CDG/Dally](/concepts/deadlock-free-routing-cdg-dally.md), [Duato](/concepts/duato-escape-vc-deadlock-free-routing.md) |
| 流控/微架构 | 15–18 | [Flow Control](/concepts/flow-control-fundamentals.md), [VC](/concepts/virtual-channel-flow-control.md), [Pipeline/Allocators](/concepts/noc-router-pipeline-allocators.md), [Optimizations](/concepts/noc-router-pipeline-optimizations.md) |
| 系统/研究 | 19–21 | [NI & System](/concepts/network-interface-and-system-design.md), [Research Cases](/concepts/noc-research-methodology-case-studies.md), 本页 |

## 六块速查

| 块 | 一句 |
|----|------|
| **拓扑** | 二分带宽 = 吞吐硬上界；直连最优度 ~O(log N)；拓扑→基数→物理成本级联 |
| **路由** | Mesh+DOR 黄金；Turn Model 加转向；Duato = escape + adaptive 双 VC |
| **流控** | SAF→WH→VCT；WH+VC 解 HoL；Credit = 链路反向压力 |
| **微架构** | RC→VA→SA→ST/LT；speculative / look-ahead / bypass 压跳延迟 |
| **死锁** | CDG 无环（Dally）充分；Duato 放宽完全自适应 |
| **性能** | 零负载延迟 vs 最大吞吐；曲线由拓扑×路由×流控共决 |

## 三个根洞察

1. **先选拓扑**（Cut Theorem）——路由/流控优化抬不过二分带宽天花板  
2. **死锁是图论问题**——运行时挂死 ↔ CDG/逃逸子网设计  
3. **End-to-End**——网络尽力而为；可靠语义在端点 → 简化片上网络面积/延迟  

## 与 WSE / NPU 研究

| 方向 | 地图位置 |
|------|----------|
| WSE 极简路由器 | Mesh + WH + 少 VC + 编译时调度（砍功能优先于加功能） |
| 集体通信 | [WSE Reduce](/concepts/wse-reduce-algorithms.md)、[LLM Collectives](/concepts/llm-distributed-training-collectives.md) |
| 确定性通道 | [Color](/concepts/cerebras-color-mechanism.md) vs [Æthereal TDM GS](/concepts/aethereal-noc.md) |
| 后摩尔 NoC | [Post-Moore Frontiers](/concepts/post-moore-architecture-frontiers.md)：可重构 / 光 / 3D |

## 收官自测题型（笔记）

1. 16×16 Torus：**Duato 双 VC** 完全自适应无死锁  
2. Torus vs Fat-Tree vs Dragonfly：零负载延迟 vs 最大吞吐  
3. 256 核 NPU：拓扑/路由/流控选型 + AllReduce 瓶颈  

## 相关页面

- [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md)
- [Network Interface and System-Level Design](/concepts/network-interface-and-system-design.md)
- [Arch-Study 30d Knowledge Map](/summaries/arch-study-30d-knowledge-map.md) — 体系结构侧收束
- [Cerebras WSE](/entities/cerebras-wse.md)

# Citations

[1] [raw/articles/interconn-study-21d-day-21.md](raw/articles/interconn-study-21d-day-21.md) — 21 天总复习（Day 21）
