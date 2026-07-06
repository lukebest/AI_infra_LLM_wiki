---
type: Concept
title: Interconnection Network Cost Model
description: 互连网络开销与性能模型：节点/链路/交换成本、零负载延迟公式、注入带宽与二分带宽上界、直连网络 d≈O(log N)
tags:
- interconnect
- noc
- topology
- latency
- throughput
- mesh
- fabric
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/interconn-study-21d-day-04.md
- raw/articles/interconn-study-21d-day-06.md
- raw/articles/interconn-study-21d-day-07.md
- raw/articles/arch-study-30d-day-21.md
---

# Interconnection Network Cost Model（互连网络成本与性能模型）

拓扑[度量指标](/concepts/interconnection-topology-metrics.md)不是免费的——每个性能优势对应硬件成本。本页把指标映射为**可计算的延迟、吞吐量与制造约束**。

## 三类成本

| 成本 | 度量 | 硬/软 |
|------|------|-------|
| **节点** | 度 d、引脚/SerDes | **硬**（封装限制） |
| **链路** | 链路数 L、线长 | 软（可堆 PCB 层/光模块，但功耗↑） |
| **交换** | Switch 端口、缓冲 | 面积 + 功耗 |

## 零负载延迟模型

```
T = H × (T_r + T_w) + L_packet / B_link
```

| 参数 | 含义 | 典型量级 |
|------|------|----------|
| H | 跳数 | 由拓扑+路由决定 |
| T_r | 单 router 延迟 | 1–10 ns |
| T_w | 单段 wire 延迟 | 片上 1–5 ns（随距离） |
| L_packet / B_link | 序列化延迟 | 64 B @ 16 GB/s ≈ 4 ns |

低负载：H×(T_r+T_w) 主导；高负载另加排队延迟（流控/拥塞，后续主题）。

**虫孔零负载**（H&P App.F / Day 21，cycle 域）：

```
t₀ = t_r × D + P/B
```

**饱和排队近似**：`t(λ) = t₀ / (1 − λ/Θ_sat)`，Θ_sat 受 [二分带宽](/concepts/interconnection-topology-metrics.md) 约束。详见 [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md)。

**例**：8×8 Mesh 对角 14 跳，T_r=2 ns，T_w=1 ns → T_hops=42 ns；64 B 包 +4 ns → **46 ns** 最坏情况。

## 吞吐量约束

```
B_inject ≤ d × B_link                    （单节点注入上界）
B_total ≤ B_bisection = B_b × B_link     （全网聚合上界）
```

8×8 Mesh：64 节点满注入 256 GB/s vs 二分带宽 **8 GB/s** → 差 **32×**——不可能所有节点同时满速注入，需**流量局部性**。

B_b 是**必要条件非充分条件**：热点 all-to-one（如 AllReduce 末段）仍可能受目的节点接收带宽限制。

## 直连网络最优度 d ≈ O(log N)

百万节点直连需 d≈20 端口 → **不可制造**。百万级系统需**间接网络 + 高基数 Switch**（见 [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)、[Switching Networks](/concepts/switching-networks.md)）。

| N | 最优 d（量级） | 典型拓扑 |
|---|----------------|----------|
| 64 | ~6 | 3-D Torus |
| 1024 | ~10 | Hypercube / Fat-Tree |
| 1M | ~20 | 间接 Fat-Tree |

## 低维 vs 高维权衡

| | 低维 Mesh/Torus (d=2–4) | 高维 Hypercube (d≈log N) |
|--|-------------------------|--------------------------|
| 优势 | 少端口、短局部连线 | 小直径、大 B_b |
| 劣势 | 大直径、B_b 受限 | 多端口、长跨维连线 |

**Dally 1990**：固定度 d=2n，最优吞吐量维度 **d_opt ≈ 2√N**——详见 [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)。

**Dally 经验**：NoC → 低维 Mesh；HPC 机柜 → 3-D Torus；超算 → 高维 Torus + 高基数 Switch。

## 设计原则（带宽优先）

1. **二分带宽第一**——所有流量优化目标是打满 B_bisection（在可能范围内）
2. **约束端口**——直连 NoC 通常 ≤ 4–8 端口
3. **局部连线**——避免长 wire（延迟+功耗）
4. **物理约束下的局部最优**——非教科书全局最优

## WSE 物理瓶颈（Day 4 估算）

```
直径 ≈ 1896 跳 × (2+1) ns ≈ 5.7 μs 最坏跨 PE 延迟
B_b ≈ 949 × 4 GB/s ≈ 3.8 TB/s
满注入 ≈ 900K × 4 GB/s ≈ 3.6 PB/s  →  差 ~947×
```

→ **算子融合、kernel 内通信、通信-计算重叠**；跨 PE 流量必须最小化。最坏跨 PE 延迟约为 HBM ~300 ns 的 **~19×**。

WSE 选 2-D Mesh：4 端口可造；3-D Torus 要 6 端口+长环绕；Hypercube 需 ~20 端口——**能造出来的最优**。

## 相关页面

- [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 间接网络规模扩展
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 维度-延迟-吞吐量权衡
- [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 度/直径/B_b 公式
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 四层空间
- [Cerebras WSE](/entities/cerebras-wse.md) — Mesh 设计实例
- [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md) — 间接网络扩展
- [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md) — 虫孔/VC/饱和模型（Day 21）
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — NoC 在存储路径中的角色

# Citations

[1] [raw/articles/interconn-study-21d-day-04.md](raw/articles/interconn-study-21d-day-04.md) — D&T Ch.3.3–3.5（Day 4）
[2] [raw/articles/interconn-study-21d-day-06.md](raw/articles/interconn-study-21d-day-06.md) — D&T Ch.3 Mesh/Torus（Day 6）
[3] [raw/articles/interconn-study-21d-day-07.md](raw/articles/interconn-study-21d-day-07.md) — D&T Ch.3 间接网络（Day 7）
[4] [raw/articles/arch-study-30d-day-21.md](raw/articles/arch-study-30d-day-21.md) — H&P App.F 性能公式（Day 21）
