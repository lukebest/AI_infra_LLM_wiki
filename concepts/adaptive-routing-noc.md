---
type: Concept
title: Adaptive Routing for NoC
description: D&T Ch.6-7 自适应路由：最小/非最小、Valiant VRR、VC 与拥塞感知；Duato 逃逸子网预告；DOR vs 自适应选型与 WSE/AllReduce
tags:
- interconnect
- noc
- routing
- adaptive
- mesh
- virtual-channel
- duato
- wse
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/articles/interconn-study-21d-day-12.md
---

# Adaptive Routing for NoC（自适应路由）

**自适应路由**让报文根据**实时拥塞**在合法路径中选路，缓解 [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md)（XY/e-cube）把流量**钉死**在固定链路上的负载不均。代价：路由器读 VC/credit 状态、**死锁避免变难**（Duato 逃逸子网，Day 13 形式化）。

**Source:** [raw/articles/interconn-study-21d-day-12.md](raw/articles/interconn-study-21d-day-12.md)（D&T Ch.6–7，Day 12）

## 动机：XY 的盲点

4×4 Mesh (0,0)→(3,3) 若全部 X-first，底行 `(0,0)–(1,0)–…–(3,0)` 易饱和；**最小自适应**可在首跳选 Y+（若 X 方向 credit 低）——流量**流向空闲链路**。

| | DOR/XY | 自适应 |
|--|--------|--------|
| 看网络状态 | 否 | 是（VC credit/队列） |
| 负载均衡 | 差（路径固定） | 好 |
| 延迟可预测 | **高** | 低（抖动） |
| 路由器 | 简单 | 复杂 |
| 死锁 | DOR+VC 易证 | 需 Duato / turn 限制 |

## 四轴分类

| 维度 | 选项 |
|------|------|
| **最小 vs 非最小** | 最短 hops vs 绕远 |
| **完全 vs 部分** | 所有最短路径 vs turn model 限制 |
| **局部 vs 全局** | 邻 hop credit vs 端到端（难） |
| **感知 vs 不感知** | 读 VC 状态 vs 随机/轮询 |

常见目标组合：**最小 + 完全 + 局部 + 感知**（完全自适应有死锁，需 Day 13）。

## 最小自适应 (Minimal Adaptive)

每步在**朝向目的**的合法输出端口中，选 **credit/队列长度最优** 者：

```
(0,0)→(3,3): X+ 拥塞 80%, Y+ 20% → 选 Y+ → (0,1)  // 仍是最短路径族
```

4×4 上最短 6 跳 → **C(6,3)=20** 条最短路径；完全最小自适应可走全部 20 条（有环风险）。

## 非最小：Valiant 随机路由 (VRR)

1. 随机中间节点 M  
2. S→M 最短 + M→D 最短  
3. 路径长度 ≤ **2×** 最短

对抗性全局流量下负载均衡强；**AllReduce/强同步**不友好（延迟发散）。数据中心 east-west 热点常用变体。

## 虚通道 (VC) 的角色

1 物理 channel = k 个 **独立 buffer + credit** 的逻辑链路 → 打破 HOL、分配不同转向到不同 VC。

| VC 数 | 能力 | 死锁风险 |
|-------|------|----------|
| **1** | 仅 DOR | 低 |
| **2** | 限制自适应 / Duato escape+adaptive | 中（设计得当可无） |
| **4+** | 完全自适应 | 高（需 Duato） |

典型：**4–8 VC × 4–8 flit** ≈ 32–64 flit/端口（见 [NoC Router 微架构](/concepts/noc-router-microarchitecture.md)）。

**WSE 量级**：4 VC × 8 flit = **32 flits/端口**；固定缓冲下「1 深队列 DOR」vs「4 浅队列自适应」= 延迟确定性 vs 多流并行。

## 拥塞度量与路由伪代码

| 状态 | 用途 |
|------|------|
| VC credit 余量 | **主度量**（越少越忙） |
| 本地队列长度 | 辅助 |
| 链路利用率 | 可选 |

```
candidates = { out | progress(out,dst) && credits(out) > threshold }
return argmin_congestion(candidates)
```

## Duato 理论（预告 — Day 13 展开）

**双子网**：
- **Escape subnetwork**：DOR/XY，保证无死锁
- **Adaptive subnetwork**：可绕路，可能成环

**定理**：逃逸子网无死锁 → **整体无死锁**（阻塞报文可切换到 escape VC）。

Mesh 经典：**degree−1 adaptive VC + 1 escape VC**（4 端口 → 3+1）。Torus DOR 需 **≥2 VC** + dateline（Day 13）。

## DOR vs 自适应：选型决策树

```
流量局部性强（NoC 邻 PE）     → DOR
强同步 collective（AllReduce） → DOR（延迟一致）
延迟抖动敏感 / 保序           → DOR
吞吐优先 + 全局不规则流量      → 自适应（或 VRR）
拓扑已多路径（Clos/Fat Tree）  → 结构均衡，路由器可保持简单
```

| 场景 | 推荐 | 原因 |
|------|------|------|
| WSE LLM 分块 | **DOR/Color** | ~80% 局部；自适应收益小、决策开销大 |
| HPC AllReduce on Mesh | DOR | 集合延迟需一致 |
| 数据中心 east-west | 自适应 | 热点、不规则 |
| NVLink Clos | 结构多样性 | 少需 per-hop 自适应 |

**反直觉**：单一热点（全读同一 embedding）时，自适应可能**全员涌同一路**；DOR 按坐标分散反而缓解雪崩。

## 双 VC QoS（NPU 16×16 例）

VC0 高优先级（barrier/control），VC1 数据；**strict priority** 仲裁 → 避免数据 HoL 阻塞控制。失效：VC0>70% 饿死 VC1；需 weighted RR 保底。

## 相关页面

- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — XY/e-cube 基线（Day 11）
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Mesh 路径多样性
- [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 多路径 vs 自适应
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — VC、wormhole、仲裁
- [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md) — 流控与 VC
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — Mesh AllReduce 与 DOR
- [Cerebras WSE](/entities/cerebras-wse.md) — 静态 Color + XY 推测
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 路由/流控耦合

# Citations

[1] [raw/articles/interconn-study-21d-day-12.md](raw/articles/interconn-study-21d-day-12.md) — D&T Ch.6–7 Adaptive（Day 12）
