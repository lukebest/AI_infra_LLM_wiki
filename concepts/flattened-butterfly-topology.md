---
type: Concept
title: Flattened Butterfly 拓扑
description: Flattened Butterfly 片上拓扑：高基数路由器降低直径，concentration + bypass channel，2-hop
  直径，38% 功耗降低
tags:
- topology
- noc
- high-radix
- on-chip
- butterfly
- mesh
- routing
- switch
timestamp: '2026-06-12T00:00:00Z'
created: 2026-06-12
sources:
- raw/papers/micro-fbfly-flattened-butterfly.md
---

# Flattened Butterfly 拓扑

Flattened butterfly（FBFLY）是一种利用**高基数路由器**降低网络直径的拓扑结构，最初为 off-chip 高基数网络提出（Kim et al., ISCA 2007），后被适配到片上网络（NoC）场景（Kim, Balfour, Dally, MICRO 2007）。从 k-ary n-fly [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) 出发压扁合并行路由器。

## 拓扑构造

从 k-ary n-fly butterfly 出发：
1. 将每行的所有路由器合并为一个高基数路由器
2. 保留所有行间连接 → 每维度路由器全互连
3. 每个路由器挂多个终端节点（concentration）

**64 节点示例**（4-ary 3-fly → 2D FBFLY）：
- 16 个 radix-10 路由器，排成 4×4
- Concentration factor = 4（每路由器挂 4 节点）
- 行内全连接（dim-1）+ 列内全连接（dim-2）
- **直径仅 2 hop**（vs mesh 14 hop, CMESH 6 hop）

## 与其他拓扑的关系

| 特性 | 2D Mesh | CMESH | FBFLY | Generalized Hypercube |
|------|---------|-------|-------|-----------------------|
| 路由器基数 | 低 (5) | 中 (8) | 高 (10) | 高 |
| 直径 | 大 | 中 | **小 (2)** | 小 |
| 跨 bisection 通道 | 基准 | +4× | +4× (concentration → 带宽仅减半) | +16× |
| 通道宽度 | 宽 | 中 | 窄 | 很窄 |
| 布线复杂度 | 低 | 中 | 中 | **高** |

- 与 [CLOS](/concepts/switching-networks.md) 的区别：FBFLY 是 flat 全互连（每维度），CLOS 是多级交换
- 与 [NoC Router](/concepts/noc-router-microarchitecture.md) 的关系：FBFLY 的高基数路由器需要更复杂的 switch 和仲裁器
- 与 [交换原理](/concepts/switching-principles.md) 的联系：体现了"减少中间级"→ 降低延迟和功耗的原则

## 路由

### Minimal: DOR
维度序路由（先 dim-1 再 dim-2），天然无死锁，不需额外 VC。

### Non-minimal: UGAL
- 判断当前负载决定走最小/非最小路径
- 非最小路径分两阶段，每阶段内 DOR → 仅需 2 VC
- 负载均衡效果好，尤其在 adversarial 流量（tornado、bit complement）

## Bypass Channel 机制

FBFLY 行/列内全互连产生大量 bypass channel（跨过中间路由器的长线）。非最小路由可能让包经过非最小物理距离，bypass channel 机制通过 input/output mux 解决：

- **Input mux**: 让本应 bypass 的包提前下"高速"进入本地路由器
- **Output mux**: 让本应绕远的包提前上"高速"跳过中间路由器
- **Yield arbiter**: primary input 优先，idle 时才授权 non-primary；通过沿非最小路径发 control packet 防止饥饿
- 不增加 switch 尺寸，仅增加 mux

**效果**：非最小路由的物理距离接近最小路径 → 延迟和能耗接近最小路由。

## 性能（64 节点，65nm）

| 指标 | vs MESH | vs CMESH |
|------|---------|----------|
| Throughput (tornado) | — | **+50%** |
| Latency | **−28%** | −28% |
| Power | **−38%** | 额外节省 |
| Area | **1/4** | 1/2.5 |

## 扩展方式

1. **增加 concentration**: 64→128 节点（基数 10→14）
2. **增加维度**: 2D→3D（最多 256 节点）
3. **混合**: 局部 FBFLY + 顶层 mesh（减少 bisection 通道数）

## 开放问题

- 片上长线信号完整性（需 repeater/pipeline register）
- 新技术（片上光互连、高速信号）可能更适合 FBFLY 的长短混合线长
- 大规模（>256 节点）时 bisection 带宽与 serialization 的权衡

## 相关概念

- [Switching Networks](/concepts/switching-networks.md) — 交换网络基础（CLOS、Banyan）
- [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) — 经典 k-ary n-fly MIN 与自路由
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — Compression（concentration）理论
- [Switching Elements](/concepts/switching-elements.md) — 交换单元（crossbar、共享存储器）
- [Noc Router Microarchitecture](/concepts/noc-router-microarchitecture.md) — NoC Router 微架构（VC、仲裁器、流水线）
- [Switching Principles](/concepts/switching-principles.md) — 交换原理基础
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性执行与拓扑选择

# Citations

[1] [raw/papers/micro-fbfly-flattened-butterfly.md](raw/papers/micro-fbfly-flattened-butterfly.md)
