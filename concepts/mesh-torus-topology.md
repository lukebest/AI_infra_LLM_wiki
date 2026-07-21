---
type: Concept
title: Mesh and Torus Topology
description: 2-D Mesh/Torus 与 k-ary n-cube：度/直径/二分带宽、Dally 维度-延迟-吞吐量权衡、XY 维序路由，及 WSE/Blue Gene 选型
tags:
- interconnect
- noc
- topology
- mesh
- fabric
- wse
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/interconn-study-21d-day-06.md
- raw/articles/interconn-study-21d-day-09.md
- raw/articles/interconn-study-21d-day-10.md
---

# Mesh and Torus Topology（网格与环面拓扑）

将 [Linear and Ring Topology](/concepts/linear-ring-topology.md) 从一维「卷」到二维，直径从 O(N) 降为 O(√N)——**2-D Mesh/Torus 是 NoC 最主流拓扑**，也是 [Cerebras WSE](/entities/cerebras-wse.md) 的骨架。度量公式见 [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md)。

## 1-D → 2-D 演进

```
Ring (1-D) ──卷→ Mesh (2-D) ──+wrap→ Torus (2-D)
         直径 O(N)    O(√N)              O(√N/2)
```

同一总「距离」被更多方向分摊 → 单跳平均进展更大；Torus 再加 wrap-around，最远距离从 k−1 降到 ⌊k/2⌋。

## 2-D Mesh（k×k 网格）

```
         列  0   1   2   3
        ┌──┬──┬──┬──┐
  行 0  │角 │边 │边 │角 │  角度=2，边度=3，内部度=4
        ├──┼──┼──┼──┤
  行 1  │边 │内 │内 │边 │
        └──┴──┴──┴──┘
```

| 指标 | 公式（k×k） | 例：8×8 |
|------|-------------|---------|
| 节点数 N | k² | 64 |
| 链路数 | 2k(k−1) | 112 |
| 直径 D | **2(k−1)** | 14 |
| 平均距离 d̄ | ≈ 2k/3 | ≈ 5.33 |
| 二分带宽 B_b | **k** 链路 | 8 |

**节点非对称**——角/边/内部度不同，路由需处理边缘 case（WSE 论文常见讨论点）。

## 2-D Torus（Mesh + wrap-around）

每行、每列首尾相连 → **全部节点度 = 4**，路由更简单。

| 指标 | 公式（k×k） | 例：8×8 |
|------|-------------|---------|
| 直径 D | **2⌊k/2⌋** | 8 (−43%) |
| 平均距离 d̄ | ≈ k/2 | ≈ 4 |
| 二分带宽 B_b | **2k** 链路 | 16 (+100%) |
| 链路数 | 2k² | 128 (+14%) |

Torus 用 **+14% 链路**（8×8）换直径↓、B_b↑；代价是 chip 边到边的 **wrap-around 长连线**（延迟+功耗）。

### Mesh vs Torus 小结

| | Mesh | Torus |
|--|------|-------|
| 对称性 | 否 | 是 |
| 直径 | 2(k−1) | 2⌊k/2⌋ |
| B_b | k | 2k |
| 制造 | 全局部短连线 | 需长环绕线 |

Blue Gene/L 等 HPC 选 Torus；片上 NoC 常选 Mesh（物理可制造性优先）。

## k-ary n-cube 统一表达

Dally 用 **k（基数）× n（维度）** 表达所有直连网络（N = kⁿ）：

| 拓扑 | k | n | N |
|------|---|---|---|
| 1-D Torus（双向环） | k | 1 | k |
| 2-D Mesh / Torus | k | 2 | k² |
| 3-D Torus | k | 3 | k³ |
| Hypercube | 2 | n | 2ⁿ |

| 指标 | Torus（有环绕） |
|------|-----------------|
| 度 d | 2n |
| 直径 D | n⌊k/2⌋ |
| 二分带宽 B_b | 2N/k = 4k^{n−1} |

## Dally 维度-延迟-吞吐量权衡

固定节点度 d = 2n（成本不变），**提高维度 n、降低基数 k**：

- **延迟 ↓**——跳数减少
- **吞吐量先升后降**——每条链路被更多 bisection 切分，瓶颈链路流量 ↑

**最优维度**：d_opt ≈ **2√N** 时吞吐量最大——Dally 1990 严格证明与 wire-delay 主导下 **n=2 片上最优**见 [Topology Optimization Variants](/concepts/topology-optimization-variants.md)。

| N | 典型选型 |
|---|----------|
| 64 (8×8) | 2-D Torus (n=2, k=8) |
| 64k | 3-D Torus（Blue Gene/L 64×32×32） |
| ~900K (WSE-3) | **2-D Mesh** (k≈949) — 高维需 TSV/堆叠，硅片物理限制 |

N=64k 若用 256×256 Mesh：D=510 跳；3-D Torus 直径 ~64 跳——**8× 延迟差距**是 HPC 弃 Mesh 的根因。维度加不上去时 → [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)（间接网络）。片上 tile mesh 的 collective 加速见 [Collective-Capable NoC](/concepts/collective-capable-noc.md)。

## XY 维序路由

**先 X 后 Y**（或反之）：(0,0)→(3,3) 先右到 (3,0) 再上到 (3,3)。

**无死锁直觉**：强制资源使用顺序（X 先于 Y），打破 Y→X 依赖环——严格证明、源/分布式实现、e-cube 对偶见 [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md)（Day 11）。

## 系统选型实例

| 系统 | N | 拓扑 | 原因 |
|------|---|------|------|
| WSE-3 | ~900K | 2-D Mesh | 单 die 无法 3-D；4 端口可造；无长 wrap 线 |
| Blue Gene/L | 64k | 3-D Torus | 直径 ~64 vs Mesh ~510 |
| Intel Paragon | ~1k | 2-D Mesh | 小规模 Mesh 足够 |
| Aurora | >1M | Dragonfly | 间接网络（Day 7） |

WSE-3 ~949×949 Mesh：D≈1896 跳；T_r=1 ns + T_w=0.5 ns → 最坏 **~2.8 μs**；d̄≈632 → 平均 **~1.4 μs**（见 [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md)）。

## 相关页面

- [Linear and Ring Topology](/concepts/linear-ring-topology.md) — 1-D 基线
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 公式与 WSE 估算
- [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 延迟/注入带宽
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — NoC 域拓扑选择
- [Cerebras WSE](/entities/cerebras-wse.md) — ~949×949 Mesh 实例
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — Mesh 上 collective
- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — Cannon/SUMMA 在 2D 处理器 mesh 上的经典 GEMM
- [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md) — MIN 自路由 vs Mesh 多路径（WSE 选型）
- [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — Folding/CMesh/Express、Dally 1990
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — XY 维序路由
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md) — Mesh 最小/非最小自适应（Day 12）
- [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md) — Mesh 单 VC vs Torus≥2 VC / dateline（Day 13）
- [Duato Escape VC Deadlock-Free Routing](/concepts/duato-escape-vc-deadlock-free-routing.md) — 完全自适应逃逸层（Day 14）
- [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md) — Mesh vs Fat-Tree / Polaris（Day 20）
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 六拓扑统一比较（Day 10）

# Citations

[1] [raw/articles/interconn-study-21d-day-06.md](raw/articles/interconn-study-21d-day-06.md) — D&T Ch.3 Mesh & Torus（Day 6）
[2] [raw/articles/interconn-study-21d-day-09.md](raw/articles/interconn-study-21d-day-09.md) — 拓扑变体与 Dally 1990（Day 9）
[3] [raw/articles/interconn-study-21d-day-10.md](raw/articles/interconn-study-21d-day-10.md) — 拓扑大综合（Day 10）
