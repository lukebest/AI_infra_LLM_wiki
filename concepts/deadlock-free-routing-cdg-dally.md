---
type: Concept
title: Deadlock-Free Routing CDG and Dally Theorem
description: D&T Ch.8.1-8.4：通道依赖图 CDG、Dally & Seitz 无死锁定理、虫孔易死锁、Torus dateline/≥2 VC、Mesh 单 VC；WSE 选型
tags:
- interconnect
- noc
- routing
- deadlock
- cdg
- virtual-channel
- torus
- mesh
- dally
timestamp: '2026-07-09T00:00:00Z'
created: 2026-07-09
sources:
- raw/articles/interconn-study-21d-day-13.md
---

# Deadlock-Free Routing: CDG and Dally Theorem（无死锁路由 I）

interconn-study **路由篇 Day 13**：Dally & Towles **Ch.8.1–8.4**——把「会不会卡死」从工程直觉变成**可机械验证的图论问题**。进阶（CDG 有环仍可安全）见 [Duato Escape VC](/concepts/duato-escape-vc-deadlock-free-routing.md)（Day 14）。

**Source:** [raw/articles/interconn-study-21d-day-13.md](raw/articles/interconn-study-21d-day-13.md)

## 死锁直觉

报文**持有**一条通道、**等待**另一条 → 循环等待 → 网络阻塞但每报文都在「正常等」。虫孔下尤其严重：一个报文可**横跨多跳**，每跳只占 1 flit buffer → 分布式占用，死锁概率上升。

| 流控 | 缓冲占用 | 死锁易感性 |
|------|----------|------------|
| Store-and-Forward / VCT | 整 packet | 较低（到节点才换链路） |
| **Wormhole** | **单 flit** | **高**（几乎必须无死锁路由） |

## 通道依赖图 (CDG)

| 元素 | 含义 |
|------|------|
| **顶点** | **通道**（物理链路或 VC）——不是路由器节点 |
| **边** c₁→c₂ | 存在合法报文：先占 c₁，接着请求 c₂ |

```
CDG 有环  ⇔  可能死锁
CDG 无环  ⇔  无死锁
```

**构造 checklist**：列通道 → 对每对 (c₁,c₂) 问是否存在先后占用 → 查环。

## Dally & Seitz 定理（1987）

> 路由函数 **R 无死锁** ⟺ 其通道依赖图 **D 无环**。

**证明骨架**：
- (⇒) D 有环 → 构造 k 个报文分别占 cᵢ 等 cᵢ₊₁ → 循环等待 → 死锁  
- (⇐) 死锁 → 循环等待报文组 → 相邻占用构成 D 的边 → D 有环  

**推论**：证无死锁 = 画 CDG 查环；所有 cycle 须用 dateline / VC 维序等打断。

## Mesh XY：CDG 为 DAG

维序：**先走完 X 通道再进 Y** → 依赖边只从 X 维指向 Y 维，**无回边**。

2×2 / 3×3 Mesh 上 XY：X+ 节点 → Y+ 节点，Y+ **无出边**（到目标）→ **树状 DAG** → 无死锁。**Mesh 上 DOR 单 VC 即可**。

## Torus：环绕带来依赖环

Torus 同维 X+（含 wrap-around）**首尾相连** → CDG 中 X+ 子图成环 → **DOR + 1 VC 必死锁**。

| 方案 | VC | 要点 |
|------|-----|------|
| **Dateline** | 1 | 切断环绕依赖边（强制绕远）；早期 Cray T3D/T3E |
| **DOR + 2 VC** | ≥2 | 按跨 dateline 次数升 VC；VC₁ 不可再跨 → DAG |
| Duato 完全自适应 | ≥4（典型） | Day 14 |

**k 维 Torus DOR**：每维一环 → 常需 **~k VC**（dateline 方案）——高维 Torus 缓冲代价之一。

## 避免 vs 恢复

| | 避免 (Avoidance) | 恢复 (Recovery) |
|--|------------------|-----------------|
| 思想 | CDG 无环 / 逃逸子网 | 允许死锁，检测后 kill/重传 |
| 代表 | DOR、dateline、escape VC | Progressive kill、draining |
| HPC / WSE NoC | **避免**（延迟确定、短报文难重传） | 少用 |
| 部分 DC / TCP | — | 可容忍重传 |

LLM 推理强同步：丢包 → 整批卡住；片上重传缓冲/协议代价高 → **WSE 必须避免**。

## 为何 WSE 选 Mesh 而非 Torus

[Cerebras WSE](/entities/cerebras-wse.md) ~949×949 **2-D Mesh**，非 Torus：

1. 环绕 = wafer **最长线**（延迟/功耗/良率差）  
2. Torus ≥2 VC → 同预算下 **VC 变浅**、HOL 风险  
3. LLM 流量 **~80% 邻 PE**，极少需 wrap  
4. Mesh CDG = 简单 DAG → **验证易**  

对照：TPU v4 用 **3D Torus + OCS** 重开 Torus 价值，但硬件更复杂。

## 相关页面

- [Duato Escape VC Deadlock-Free Routing](/concepts/duato-escape-vc-deadlock-free-routing.md) — Day 14：有环仍可安全
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — XY / e-cube
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md) — 自适应与死锁张力
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 拓扑与维序
- [Switching Principles](/concepts/switching-principles.md) — 虫孔 vs VCT
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — VC / wormhole
- [Cerebras WSE](/entities/cerebras-wse.md) — Mesh + DOR 工业实例

# Citations

[1] [raw/articles/interconn-study-21d-day-13.md](raw/articles/interconn-study-21d-day-13.md) — D&T Ch.8.1–8.4（Day 13）
