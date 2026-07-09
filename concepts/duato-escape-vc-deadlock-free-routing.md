---
type: Concept
title: Duato Escape VC Deadlock-Free Routing
description: D&T Ch.8.5-8.8：Duato 定理（逃逸子网）、自适应+逃逸 VC、避免 vs 恢复、协议层 Request/Response 死锁；Dally 的推广
tags:
- interconnect
- noc
- routing
- deadlock
- duato
- escape-vc
- adaptive
- virtual-channel
- protocol
timestamp: '2026-07-09T00:00:00Z'
created: 2026-07-09
sources:
- raw/articles/interconn-study-21d-day-14.md
---

# Duato Escape VC Deadlock-Free Routing（无死锁路由 II）

interconn-study **路由篇 Day 14**：Dally & Towles **Ch.8.5–8.8**——突破 [Dally CDG 定理](/concepts/deadlock-free-routing-cdg-dally.md) 的工程极限：**CDG 有环仍可无死锁**，代价是保留一条**逃逸子网**。

**Source:** [raw/articles/interconn-study-21d-day-14.md](raw/articles/interconn-study-21d-day-14.md)  
**奠基论文：** Duato, *A New Theory of Deadlock-Free Adaptive Routing*, IEEE TPDS 1993

## Dally 的极限：充分而非必要

[Dally & Seitz](/concepts/deadlock-free-routing-cdg-dally.md)：**CDG 无环 ⇒ 无死锁**（充分）。但 **CDG 有环 ⇏ 必死锁**——存在大量「有环但安全」的路由；严格要求无环会**禁止大量最短路径**、削弱自适应。

关系：**Duato 推广 Dally；Dally = Duato 在「整网即逃逸子网」时的特例**。

## Duato 定理（工程表述）

路由 R 在通道集 C 上无死锁，当存在子集 **C₁ ⊆ C** 使得：

1. **R 限制在 C₁ 上的 CDG 无环**（**逃逸子网络**）  
2. 从 **C\C₁** 总能进入 C₁（阻塞时可「降级」进逃逸层）

```
自适应层 (C\C₁)：激进最短/绕路路径（CDG 可有环）
逃逸层   (C₁)  ：保守子集（常为 DOR），保证无环
报文需要时：Adaptive VC → Escape VC
```

## 逃逸虚通道（Escape VC）

| 类别 | 路由 | 角色 |
|------|------|------|
| **Adaptive VC** | 任意最短（或 turn-model 允许）路径 | C\C₁ |
| **Escape VC** | 必须 DOR（或其它无环子集） | C₁ |

**设计规则**：
1. ≥1 条 VC 专作 escape  
2. Escape 上遵守无环路由  
3. Adaptive 可自由选路  
4. **VC 分配**：任意状态须能降级到 escape（满载 / 下游无 credit / 超时）

**Mesh 典型**：3 adaptive + 1 escape（4 端口 degree−1）。**Torus 完全自适应**常需更多 VC（Day 13：DOR 已 ≥2）。

```
[Input] → VC Allocator → Adaptive VCs ↘
                                    Crossbar
[Input] → VC Allocator → Escape VC  ↗
```

## 避免 vs 恢复（再对照）

| | 避免 | 恢复 |
|--|------|------|
| 机制 | CDG/逃逸约束 | 检测 + kill/regress |
| 峰值吞吐 | 路径受限 | 常更高（全自适应） |
| 尾延迟 | **更稳** | 死锁尖刺 |
| LLM 推理 (p99) | **倾向避免** | 抖动伤吞吐 |
| HPC 平均吞吐 | — | 可考虑恢复 |

NoC 上恢复渐多（资源紧、重传相对便宜），但 **WSE/短报文/强同步** 仍宜避免。

## 协议层死锁

网络层无死锁 ≠ 端到端安全。典型 **Request–Response** 共享 VC：

```
A ──Request──→ B
  ←──Response──
双方都等对方释放同一 VC 类 → 死锁
```

**解法**：Request / Response **分 VC 类**或独立 **Virtual Network**；网络层 + 协议层双无死锁。Barrier、fetch-and-add 等同理。

## WSE / 大规模 Mesh 工程估算

~900K PE Mesh：

- **DOR + 单/少 VC**：实现简单、可预测——流量局部时自适应收益有限（见 [Adaptive Routing](/concepts/adaptive-routing-noc.md)）  
- 若上自适应：典型 **3–4 VC = 1 escape + 2–3 adaptive**；escape 过少 → 自适应层满则「假死锁」；过多 → 浪费缓冲  
- 同步原语：**双向分离 VC**（Req/Rsp）防协议层死锁  

## 路由篇自测（Day 11–14）

1. CDG 无环 ⇒ 无死锁？（反证：死锁 ⇒ 循环等待 ⇒ CDG 环）  
2. Torus DOR 至少几 VC？（**≥2**，环绕环）  
3. Duato vs Dally？（推广 / 特例）  
4. Escape VC 作用？（任意自适应状态可退出到无环子网）  

## 相关页面

- [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md) — Day 13 基础
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md) — 最小/完全自适应
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — 逃逸层常用基线
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — VC allocator
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Mesh vs Torus VC 代价
- [Cerebras WSE](/entities/cerebras-wse.md) — 工业选型（倾向避免 + DOR）
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 路由/流控耦合

# Citations

[1] [raw/articles/interconn-study-21d-day-14.md](raw/articles/interconn-study-21d-day-14.md) — D&T Ch.8.5–8.8（Day 14）
