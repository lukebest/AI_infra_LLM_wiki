---
type: Concept
title: NoC Fundamentals (H&P Appendix F)
description: H&P 附录 F 互连网络五问：拓扑/路由/流控/路由器/性能；直连 vs 间接、虫孔+VC、饱和吞吐与 WSE-scale 扩展指标
tags:
- architecture
- interconnect
- noc
- topology
- routing
- flow-control
- wse
- hp
timestamp: '2026-07-06T00:00:00Z'
created: 2026-07-06
sources:
- raw/articles/arch-study-30d-day-21.md
---

# NoC Fundamentals (H&P Appendix F)（互连网络基础）

H&P 第 6 版 **Appendix F** 把 NoC 归纳为**五个层层依赖的问题**——与 Dally & Towles 四层设计空间（见 [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)）互补。本页为 arch-study Day 21  digest；拓扑/路由细节见 interconn-study 系列概念页。

**Source:** [raw/articles/arch-study-30d-day-21.md](raw/articles/arch-study-30d-day-21.md)（H&P App.F + D&T 补充，Day 21）

## 五个核心问题

```
Q1 拓扑     → 节点怎么连？          [Mesh/Torus/Fat Tree/Dragonfly…]
Q2 路由     → 包走哪条路径？        [DOR / Turn Model / Adaptive]
Q3 流控     → buffer/credit 如何管？ [Wormhole + VC + Credit]
Q4 路由器   → 物理如何实现交换？    [5-stage pipeline]
Q5 性能     → latency / throughput / energy
```

拓扑决定可达性 → 路由决定路径集 → 流控分配路径资源 → 路由器是物理实现 → 性能是结果。

## 直连 vs 间接

| | 直连 (Direct) | 间接 (Indirect) |
|--|---------------|-----------------|
| 节点 | 计算 + 路由器合一 | 计算与交换分离 |
| 例 | Mesh、Torus、Ring | Crossbar、Butterfly、Fat Tree、Clos |
| 优势 | 可扩展、短链路 | 高 bisection BW |
| WSE | **2-D Mesh 直连** | 集群级用 Dragonfly/Fat Tree |

## 主流拓扑速查（n×n 或 N 节点）

| 拓扑 | 直径 | B_b | 度 | 典型规模 |
|------|------|-----|-----|----------|
| Ring | ⌊N/2⌋ | 1 | 2 | 几十–几百 |
| 2-D Mesh | 2(√N−1) | √N | 2–4 | 10K（片上） |
| 2-D Torus | √N | 2√N | 4 | 10K–100K |
| Hypercube | log₂N | N/2 | log N | ~1K（布线难） |
| Fat Tree | O(log N) | N/2 | k | 10K–1M |
| Dragonfly | ≤3 | 可调 | 高 | 10K–100K |

**N≈10K+ 片上**：Mesh/Torus 是**物理可行**的直连选择——Hypercube 需 log N 端口；Fat Tree 需外部交换。详见 [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md)、[Mesh and Torus Topology](/concepts/mesh-torus-topology.md)。

**Dragonfly**：组内全连接 + 组间少量光口上行；直径 ≤3、链路数少；Cray XC、Omni-Path。集群场景见 [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)。

## 路由（摘要）

| 算法 | 要点 | Wiki |
|------|------|------|
| **DOR / XY** | 先 X 后 Y；CDG 无环 | [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) |
| **Turn Model** | 禁止特定转弯（West-First 等） | 保留无死锁 + 更灵活路径 |
| **Odd-Even 自适应** | 奇偶列禁转弯规则 | 多路径、避热点（Day 12 主题） |
| **e-cube** | Hypercube 维序 DOR | 同页 |

## 流控演进

```
Store-and-Forward → Cut-Through → Wormhole → + Virtual Channel → Credit-Based
     高延迟            HOL 风险        低延迟         消除 HOL          工业标准
```

**虫孔零负载延迟**（cycle 域）：

```
t₀ = t_r × D + P/B

t_r = 单跳 router 延迟；D = 跳数；P = 包长 bits；B = 链路带宽 bits/cycle
```

**饱和吞吐**：注入率 → 1 pkt/cycle/node 时受 **B_bisection** 约束；排队近似 `t(D) = t₀ / (1 − λ/Θ_sat)`。

**VC**：1 物理通道 = k 个独立 buffer + 流控 → 消除 head-of-line blocking；典型 4–8 VC × 4–8 flit 深。详见 [NoC Router 微架构](/concepts/noc-router-microarchitecture.md)、[Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md)。

## 5-stage Router Pipeline

```
RC → VA → SA → ST → LT
(路由计算 → VC 仲裁 → Crossbar 仲裁 → 交换 → 链路传输)
```

Speculative router 重叠 VA/SA → 1 cycle/hop。**t_r 翻倍 → 包延迟 (D×t_r) 翻倍**——NoC 性能第一杠杆。

## WSE Mesh：教科书 + 工业延伸

| | 教科书 Mesh | WSE-3 |
|--|-------------|-------|
| 度 | 4 | 4 |
| 路由 | XY | XY + Color multicast/broadcast |
| 流控 | Wormhole + VC | 确定性 + 硬件 barrier/reduce |
| 规模 | 演示级 | ~900K PE |
| 总带宽 | — | **~21 PB/s**（~5.75 GB/s/port 量级反推） |

**选 Mesh 非 Torus/Hypercube 的根因**（工程 > 理论）：
1. 单片晶圆 wrap-around / 高维布线不可行
2. fail-in-place + route-around 容错简单
3. dataflow placement 匹配二维邻接
4. 4 端口路由器面积可放进 ~225 μm PE

**WSE-scale 扩展指标**（教科书指标不够用时）：

| 指标 | Mesh @ 900K | 含义 |
|------|-------------|------|
| 平均距离 | ~632 hop | 随机 PE 对 |
| B_b / node | ~1/√N | 必须靠 **90%+ 局部流量** |
| 容错 | fail-in-place | 90 万节点 × 万小时 → 必考虑 |
| 单时钟域 | 必须 | 长链路插 pipeline reg |

## 研究切入点（Day 21 映射）

| 方向 | 机会 | 约束 |
|------|------|------|
| 拓扑 | Mesh+bypass / Express Cube | 布线、单时钟域 |
| 路由 | dataflow-aware / locality | 死锁、复杂度 |
| 流控 | predictive / NPU 专用 | buffer 面积 |
| 容错 | 自愈 NoC | 路由表更新 |
| 应用感知 | 编译器协同 | 跨层抽象 |

## 相关页面

- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 四层设计空间
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 统一比较表
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 延迟/吞吐公式
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — XY / e-cube
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — Express / CMesh
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — NoC 在存储路径中的位置（Day 22）
- [Cerebras WSE](/entities/cerebras-wse.md) — Mesh 工业实例

# Citations

[1] [raw/articles/arch-study-30d-day-21.md](raw/articles/arch-study-30d-day-21.md) — H&P App.F NoC（Day 21）
