---
type: Concept
title: AIC Folded Multi-Ring NoC
description: 6×8 AIC 折叠多环片上网络：真比例 reticle、RBRG 转弯服务、相位约束最短路径与角到角时延分解
tags:
- noc
- interconnect
- routing
- topology
- mesh
- fabric
- latency
- accelerator
- deterministic
timestamp: '2026-08-13T00:00:00Z'
created: 2026-08-13
updated: 2026-08-13
sources:
- raw/articles/corner-to-corner-route.html
- raw/articles/corner-to-corner-route.md
---

# AIC Folded Multi-Ring NoC（折叠多环角到角路由）

6×8 AIC 的片上织物不是纯 2-D mesh hop 计数，而是 **水平折叠多环 + 竖直跨距 + RBRG 站** 的几何图。来源可视化按 **26 mm × 33 mm 真比例 reticle** 标注每类物理段，并对任意源/目的核求 **最小周期最短路径**。

**Source:** [raw/articles/corner-to-corner-route.html](/raw/articles/corner-to-corner-route.html) · 摘录 [raw/articles/corner-to-corner-route.md](/raw/articles/corner-to-corner-route.md)

与教科书 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) 对照：逻辑上仍是行列可寻址的 48 核阵列，物理上却是 **沿行的双向环（含左右折叠）叠在竖直轨道上**，更接近 [Linear and Ring Topology](/concepts/linear-ring-topology.md) 的 multi-ring + [Topology Optimization Variants](/concepts/topology-optimization-variants.md) 的 Folding，而不是 WSE 式邻居 mesh。

## Floorplan 常量

| 量 | 值 |
|----|----|
| Reticle | 26,000 × 33,000 µm |
| Core field | 25,000 × 32,000 µm（边沿 E=500 µm） |
| 阵列 | 6 行 × 8 列 = 48 核，`eid = r*8+c` |
| Pitch | X 3130 µm，Y 5340 µm |
| 线延迟 | **400 µm / cycle**，`cyc = ceil(ℓ / 400)`（转弯服务除外） |
| 水平轨 | 12 条（每行一对，`hi = 2r` 与 `2r+1`） |
| 竖直轨 | 16 条（每列一对） |

核 `eid` 注入到水平轨 `hi = 2r + (c mod 2)` 上、列 `c` 的 **CS/PIPE 中站**（`hi%2 == c%2` → CS，否则 PIPE）。同核通信不进网。

## 站与微边

图规模（从 viz 构图还原）：**288 站、1920 端口节点、3456 条有向微边**。

| 微边 kind | 典型几何 | 基周期 | 角色 |
|-----------|----------|--------|------|
| inject / eject | 105 µm | 1 | Core ↔ 中站 |
| harm | 1125 µm | 3 | 水平臂 |
| gap | 40 µm | 1 | 站间缝 |
| vspan | 4460 µm | 12 | 竖直跨距 |
| straight RBRG | 420 µm | 2 | 同轴穿站 |
| near / far turn | 315 / 525 µm（几何） | **10** | 5 in + 5 out，几何含在服务里 |
| hfold | 5180 µm | 13 | 行对左右折叠 |
| vfold | 405 µm | 2 | 列顶底折叠 |
| cs / pipe | 0 | 0 | 中站穿过；Advanced extra 可加 |

RBRG 是 420×420 µm 站。转弯不是 `ceil(ℓ/400)`：固定 **ingress 5 + egress 5 = 10 cyc**。Advanced 参数（straight/near/far extra、CS/PIPE extra、inject/eject extra、near/far FIFO wait）默认全 0，加在基周期之上。

## 路由：相位约束最短路

不是任意自适应。合法路径是一台小状态机，目标字典序最小 `(total_cyc, µm, turns, steps, edge-id)`：

| 情形 | 合法相位 |
|------|----------|
| 同行 `sr == dr` | **只走水平**；禁止 `trans`（H↔V 转弯） |
| 跨行 | 源行 H（phase 0）→ 第一次 `H2V`（phase 1）→ 仅当 `⌊hi/2⌋ == dest_row` 才允许 `V2H`（phase 2）→ 目的行 H → eject |

这是 **维序思想的几何版**：先水平、再竖直、再水平，且竖直必须打在目的行的轨对上。保序、路径集合受限，接近 [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md)，但代价函数是 **周期+几何**，不是 hop 数。同行最短路可以走 **hfold** 绕到对侧，而不强行转弯进竖直轨。

## 角到角与其它对（extras = 0）

默认 UI：Core 00 → Core 47。用同一构图与同一 Dijkstra 复现：

| 对 | 总周期 | 几何 | turns | folds | 备注 |
|----|--------|------|-------|-------|------|
| 00 → 47（对角） | **194 cyc** | 53,700 µm | 2 | 0 | 1 near + 1 far；无折叠 |
| 00 → 07（同行最远） | 102 cyc | 30,390 µm | 0 | 1 | H-only + 一次 hfold |
| 00 → 08（下行邻核） | 43 cyc | 8,010 µm | 2 | 0 | 两 near + 一段 vspan |
| 00 → 01（邻列） | 36 cyc | 11,610 µm | 0 | 1 | 短 H + hfold 竞速直臂 |
| 23 → 24 | 98 cyc | 22,580 µm | 2 | 0 | 跨行中部 |

对角 194 cyc 分解（基线、无 extra）：

- 非转弯运输：174 cyc（inject/eject、H 臂、gap、vspan、straight RBRG、CS/PIPE 0）
- 2 × (5 in + 5 out) = 20 cyc 转弯服务
- **194 = 174 + 20**

相对 WSE 式「对角 hops × 单跳周期」：这里对角只有 **两次转弯**，延迟预算被 **长竖直跨距（12 cyc）和大量 2 cyc straight RBRG** 吃掉，而不是 48 核 mesh 的 hop 直径。

## 与既有拓扑页的关系

- vs [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)：核阵列是 6×8，但链路不是四邻居 mesh；竖直是稀疏轨道，水平是折叠环。
- vs [Linear and Ring Topology](/concepts/linear-ring-topology.md)：每行一对水平环，左右 hfold 把 wrap 折到邻轨（Folding 均匀线长）。
- vs [Topology Optimization Variants](/concepts/topology-optimization-variants.md)：hfold/vfold 是教科书 Folding 的 reticle 实例。
- vs [NoC Router 微架构](/concepts/noc-router-microarchitecture.md)：RBRG 把「直通 2 cyc / 转弯 10 cyc」做成站级服务，而不是通用 VA/SA 五级流水的抽象 hop。
- vs [Collective-Capable NoC](/concepts/collective-capable-noc.md)：本页只覆盖 **单播最短路时延**；集合通信如何映射到多环未在该 viz 中给出。

## 开放问题

- 动态随机流量下，相位约束最短路的 **P99** 与 FIFO wait extra 如何标定（viz 把 wait 留作旋钮，默认 0）。
- 多播/all-reduce 是否复用同一 RBRG 树，还是另铺 color/TDM。
- CS vs PIPE 中站在时序上除 extra 外是否还有协议差异（构图里基周期同为 0）。

## 相关页面

- [Linear and Ring Topology](/concepts/linear-ring-topology.md)
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md)
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md)
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md)
- [Collective-Capable NoC](/concepts/collective-capable-noc.md)
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md)

# Citations

[1] [raw/articles/corner-to-corner-route.html](/raw/articles/corner-to-corner-route.html) — interactive 6×8 AIC folded multi-ring viz
[2] [raw/articles/corner-to-corner-route.md](/raw/articles/corner-to-corner-route.md) — extracted constants and routing legality
