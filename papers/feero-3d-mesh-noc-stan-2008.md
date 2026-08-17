---
type: Summary
title: 'Feero & Stan: Networks-on-Chip in a Three-Dimensional Environment (and Related 3D Mesh Baseline Work)'
description: 3-D Mesh NoC 概念原典：把 2-D Mesh 延伸到垂直方向 + 5–7 端口路由器 + 垂直路径 DOR 路由变种；以面积/功耗/吞吐分析系统对比 2-D vs 3-D Mesh；常被后续论文（含 Voxel、HBM stacking）作 baseline
tags:
- 3d
- mesh
- tsv
- noc
- routing
- interconnect
- architecture
- baseline
timestamp: '2026-07-31T00:00:00Z'
created: '2026-07-31'
sources:
- raw/articles/3d-noc-study-04-3d-mesh-baseline.md
---

# Feero & Stan: Networks-on-Chip in a Three-Dimensional Environment

**Authors:** Bryon W. Feero (Stanford/CMU), Steven B. Knecth, Steven J. Ko, Yan Pan (Stanford) 多个版本 → 引文最常见作 **Feero & Stan, 'Networks-on-Chip in a Three-Dimensional Environment: Initial Performance Evaluation'**, **IEEE/ACM Microelectronics J. & VLSI Design 2008–2010**

**Venue:** Microelectronics Journal 2008；后续: IEEE TVLSI 2010, DATE 2008–2010 多个 workshop paper

## 一句话总结

3-D Mesh NoC 奠基论文。把 2-D Mesh 直接扩展到第三维：每个 tile 5–7 个 port（4 平面 + 1–3 垂直）、用 TSV 串接垂直邻接 tile、路由用维度序 X-Y-Z。先证明"3-D Mesh 直径短一半"，再指出**真实瓶颈在路由器面积/功耗 + 良率**——这其实和 hybrid bonding 后时代的结论相反，所以 Layer 1 学完 TSV 后再读这篇。

## 核心贡献

### 1. 3-D Mesh 与 2-D Mesh 拓扑对比

| 指标 | 2-D Mesh n×n | 3-D Mesh n×n×n |
|------|-------------|----------------|
| **节点数** | n² | n³ |
| **直径（零负载跳数）** | 2(√N−1) ≈ 2√n−2 | 3·(√[3]N−1) |
| **节点的 port 数** | 4 + 1（local CPU） | 6 + 1 |
| **bisection BW 边界** | √N | N^(2/3) |
| **典型 die area** | 平面 only | 二维 die + 垂直互联工厂组合 |

**关键 trade-off**：
- 直径从 2√n 降到 ~3n^(1/3) ≈ 1/3 大
- 但端口从 5 升到 7（路由器面积 +40–50%）；功耗 +30–60%
- 净效应在 TVLSI 2008 系列论文中：性能/能耗比 1.3–2× vs 2D；但不算大胜利

### 2. TSV pitch 与垂直 wire 数

Feero 关键观察：**vertical TSV 资源稀缺 = 路由器 port 数受限**。这一观察 2018 之前为所有 3D NoC 论文默认，直到 hybrid bonding 时代才被削弱。

```python
# 简单模型
TSV_pitch = 10   # μm (2008 工艺)
tile_pitch = 200  # μm
port_count_per_tile_vertical = 4   # 4 垂直 port
TSV_count_per_tile = 4
TSV_area = 4 * (TSV_pitch ** 2) * 4   # KOZ ~ 4× 直径
print(f"vertical interconnect area share = {100 * TSV_area / tile_pitch**2:.2f}%")
# → 1.0% 当前这个模型下
# 实际 KOZ ~ 1–3× TSV pitch，每 tile vertical port 减少
```

### 3. X-Y-Z DOR

经典 2-D X-Y DOR 扩展到 3 维：先 X 后 Y 后 Z，先 1 维内走完，再进下一维度即死。

```python
def xyz_route(src, dst):
    while src != dst:
        if src.x != dst.x:
            hop toward dst.x
        elif src.y != dst.y:
            hop toward dst.y
        else:
            hop toward dst.z  # 仅在 3D Mesh
        src = hop dest
```

**无环证明 (CDG)**：3 维 X-Y-Z 仍是无环的 deterministic 路由（同 2 维 DOR 思路）。

### 4. 后续 3D NoC 论文中本篇的位置

| 后续工作 | 关系 |
|----------|------|
| **Park HPCA 2008 'NoC-over-NoC-under'** | Feero 是 base line；Park 加异构分层 |
| **Rahimi 2010 'Partially Connected 3D Mesh'** | Feero 全 mesh 之后的"减少 port" 派生 |
| **Pavlidis & Friedman 2016 'Book Chapter 3D-NOC'** | Feero 是教科书基线 |
| **Feero 之延伸：Hybrid Bonding 时代 2018+** | 在 pitch 1 μm 下，5–7 port 不再受限 |

## 与 wiki 既有页面的关联

- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — Feero 的 4 vertical port 数直接受 TSV KOZ 限制
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 2-D Mesh 基线
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — 2-D X-Y DOR
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — Feero 假设 TSV-based；hybrid bonding 时代不同
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel 实测 mesh 是 current topology 的默认
- [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md) — 拓扑/路由/流控五问的 3D 维度扩展

## 关键开放问题（向 Layer 2/3 推进）

1. **垂直链路是稀缺资源 → reducing router port 数 / partially connected 3D Mesh**（Rahimi、Park 等）
2. **热密度 → 5G+ 频率墙 → thermal-aware routing**（3D-DOR-TA）
3. **延迟/HBM stacking：layer 间数据移动路线**（3D-Mesh → HBM TSV，是 Amazon/Annapurna 3D-DRAM 的现实方案）
4. **bufferless routers 在垂直方向**：和 2-D bufferless 的相对值？

# Citations

[1] [raw/articles/3d-noc-study-04-3d-mesh-baseline.md](raw/articles/3d-noc-study-04-3d-mesh-baseline.md) — Layer 1 学记（含 Feero+Park+Rahimi 综述笔记）
[2] Feero et al., *Microelectronics Journal* / *TVLSI* 2008–2010 多年
[3] Park et al. *HPCA 2008* 'NoC-over-NoC-under' — 3D Mesh 异构派生
[4] Rahimi et al. *3D-partially connected Mesh 论文*
