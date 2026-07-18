---
type: Summary
title: 'pHost: Distributed Near-Optimal Datacenter Transport Over Commodity Network Fabric'
description: UC Berkeley CoNEXT 2015 — 主机端 RTS/token 分布式调度，商品交换机上接近 pFabric FCT（±4%），比 Fastpass 快 3.8×
tags:
- transport
- flow-control
- scheduling
- congestion-control
- infrastructure
- networking
- protocol
- communication
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/pHost_Coflow_Aware_Packet_Scheduling_2015.pdf
---

# pHost: Distributed Near-Optimal Datacenter Transport Over Commodity Network Fabric

**ACM CoNEXT 2015** | DOI [10.1145/2716281.2836086](https://doi.org/10.1145/2716281.2836086)  
Gao, Narayan, Kumar, Agarwal, Ratnasamy, Shenker（UC Berkeley）

在**商品 datacenter fabric** 上实现接近 pFabric 的流完成时间（FCT），同时保留 Fastpass 式**可编程调度策略**，无需交换机内嵌调度逻辑。

## 核心贡献

1. **主机端 per-packet 调度**：RTS → 目的端发 token → 源端选 token 发数据包；控制包最高优先级
2. **完全分布式**：无全局调度器、无 per-flow 交换机状态、无显式网络反馈
3. **利用现代 DC 特性**：小包喷洒 + 全二分带宽 → 核心几乎无拥塞；商品交换机 8–10 级 priority 保护信令
4. **策略可配**：目的端选流、源端选 token、数据优先级、free token 预算均可调（slowdown / deadline / 多租户公平）

## 关键数字

| 对比 | 结果 |
|------|------|
| vs pFabric | 典型条件下 **±4%** FCT |
| vs Fastpass | **3.8×** 更快 |
| Token 过期 | **1.5×** MTU 传输时间 |

## 与 wiki 交叉

- [Clos / Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 全二分带宽前提
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 传输 vs 调度解耦
- [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md) — token/credit 类机制对照

# Citations

[1] [raw/papers/pHost_Coflow_Aware_Packet_Scheduling_2015.pdf](raw/papers/pHost_Coflow_Aware_Packet_Scheduling_2015.pdf)
[2] [raw/papers/phost-coflow-aware-packet-scheduling.md](raw/papers/phost-coflow-aware-packet-scheduling.md) — 结构化摘录
