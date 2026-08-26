---
type: Summary
title: 'Cu-Cu Hybrid Bonding: A New 3D Integration Technology (Multiple 2019–2025 Sources)'
description: Hybrid bonding 是 monolithic 与 TSV-based 的中间路线：Cu-Cu 直接键合 (~1 μm pitch) + 固相扩散；近年 HBM4、3D-DRAM、AMD Instinct MI300、Samsung X-Cube、TSMC SoIC 全部以它量产；与 3D NoC 关系：KOZ 接近 zero，垂直 port 数不再是瓶颈
tags:
- 3d
- hybrid-bonding
- cu-cu
- microbump
- tsv
- interconnect
- architecture
- commercial
timestamp: '2026-08-26T00:00:00Z'
created: '2026-07-31'
sources:
- raw/articles/3d-noc-study-03-hybrid-bonding.md
---

# Cu-Cu Hybrid Bonding: A New 3D Integration Technology

**Authors:** 多源（综述型 layer 1 论文）— Shie, J.-S. (ITRI) 等多年 IEDM/ECTC 报告；商业代表：TSMC (SoIC)、Samsung (X-Cube)、Intel (Foveros)、SK hynix (HBM4)

**Venue:** IEEE ECTC 2017–2025 / IEDM 2018–2024

## 一句话总结

Hybrid bonding 是过去七年最重要的 3D 集成技术：Cu-Cu 直接扩散键合 + 隐藏微凸点，**pitch 从 10 μm 缩到 1 μm 以下**（TSMC SoIC-X 当前 3 μm 量产；Samsung 1 μm 试验），**KOZ 显著缩小、密度接近 monolithic**。3D NoC 的物理层约束随之被根本改变——从"TSV KOZ + 良率"主导变成"端口数 + 物理对齐"主导。

## 核心贡献（综述层）

### 1. 与微凸点 / 微凸点（μ-bump）+ 锡基对比

| 维度 | 微凸点 (μ-bump with Sn) | Hybrid Bonding (Cu-Cu) |
|------|---------------------------|------------------------|
| 典型 pitch | 10–40 μm | 0.5–3 μm |
| 直径/间距比 | 1:1 ~ 1:3 | 1:1 ~ 1:2 |
| IO/mm² 密度 | ~2500–10000 | ~10⁵–10⁶ |
| 凸点高度 | ~5 μm（高、需 cap）| ~100–500 nm（实质不可见）|
| 对准容差 | ±2 μm | ±100 nm |
| 电气特性 | Sn 合金 → 高 R | Cu-Cu → 接近于 Cu wire |
| 工艺温度 | ~250 °C（回流）| < 400 °C（扩散键合）|

**演化**：μ-bump 已成为 interconnect 领域瓶颈；hybrid bonding 几乎全部接替。

### 2. Hybrid Bonding 关键工艺步骤

1. **CMP（化学机械抛光）** — Cu pad 暴露至 < 1 nm 表面粗糙度
2. **Cleaning** — 等离子体去氧化层
3. **Bonding** — 常温初对准 → 退火 < 400 °C 形成 Cu-Cu 扩散键合
4. **Anneal** — 形成金属间化合物 + 残余应力释放

**对准容差**：对准必须 **< 200 nm 精度**（一般需 ≤ 50 nm），这对 particle control、wafer warpage 提出极严苛要求。

### 3. 3D NoC 物理层影响

| 3D NoC 假设 (传统 TSV) | Hybrid Bonding 现状（2024）|
|------------------------|-----------------------------|
| TSV 1–5 μm 间距，KOZ 0.2–0.6 μm，每 mm² ~100K TSVs | pitch 1–3 μm，无 KOZ，每 mm² ~M count |
| 5–7 端口路由器（含 1–2 垂直 port）受 TSV limit | 5–7 端口不再受限；可加到 8–10 不牺牲面积 |
| 垂直链路带宽瓶颈 | 接近水平链路带宽→可以构造 dense 3D Mesh |
| 良率主导 worry | 良率仍关键，但靠 redundancy 而非 physical limit |

### 4. 商业用例（2024 视角）

| 产品 | 集成技术 | 设计动机 |
|------|----------|----------|
| **TSMC SoIC** | TSV + Hybrid Bonding；多代 SoIC-X/L | Apple M-Ultra、AMD Instinct MI300 互连 |
| **AMD 3D V-Cache** | μ-bump via-stack | CPU cache stacking (Zen3+ → Zen4) |
| **AMD MI300** | SoIC + 4 die；hybrid bonding interposer | CPU+GPU+IO + HBM chiplet 集成 |
| **Samsung X-Cube** | Hybrid Bonding | Samsung Exynos / 3D-NAND controller |
| **SK hynix HBM3/HBM4** | TSV + μ-bump + 部分 hybrid | 12-Hi 24 GB HBM3, 12-Hi 36 GB HBM4；2026 看 16-Hi / HBM5 |
| **Intel Foveros** | Hybrid Bonding + active interposer | Meteor Lake / Lunar Lake tile-based chiplet |

**3D-DRAM 趋势**：HBM 与 3D-DRAM 路线已开始整合 HBM4 之 hybrid-bonding base die；2026 后 SK hynix/Cadence 标准 16-Hi die + hybrid bonding 之 HBM5。

Hot Chips 2026 校正：[SK hynix](/papers/hc2026-skhynix-hbm-advanced-packaging.md) 公开说 HBM4 **12Hi 量产、16Hi under Qual**（Adv. MR-MUF），**HyB 对准 ≥20Hi**、pitch **<18 μm**、同限高下 core die 可厚最多 **24%**。Samsung [zHBM](/papers/hc2026-samsung-hbm-base-die.md) 用 **WoW + HCB** 取消 2.5D interposer；HPB 覆盖 >50% PHY 时峰值温度降 >35%。d-Matrix [Raptor](/papers/hc2026-dmatrix-raptor-3d-dram.md) 今天仍是 36 μm F2F，HB 是 <2 μm / 8-high 路线图。

### 5. 3D NoC 研究的关键启示

1. **垂直链路不再是稀薄资源** → 经典 3-D Mesh 的 "minimum-port" 假设已被打破。可以构造 **richly-connected vertical topology** (every tile has 4–6 vertical ports)
2. **热约束反而成为新瓶颈** — 越密的 3D 集成 = 越高的功率密度 = 越热的路由器/缓存
3. **bufferless 路由器** 在 hybrid-bonding 时代反而失去优势 — 因为 TSV 资源不再稀缺
4. **3D NoC + LLM serving**：HBM4 + hybrid bonded logic die 是 LLM serving 的事实路径（Apple M-Ultra、AMD MI300、Hopper+ NVL72 都依赖）。

## 与 wiki 既有页面关联

- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — hybrid bonding 是 TSV 的当代延伸
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 三路线对比
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Hybrid bonding 产品（V-Cache、MI300）正是 3D AI 芯片基础
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Packaging / 3D 路线的商业现实
- [Multi-Frame Architecture Memory Hierarchy](/concepts/cxl-tiered-memory.md) — HBM/CXL tiering 与 hybrid-bonding 内存层的差异
- [SK hynix HBM packaging](/papers/hc2026-skhynix-hbm-advanced-packaging.md) — HyB vs MR-MUF
- [Samsung HBM Base Die](/papers/hc2026-samsung-hbm-base-die.md) — HCB / zHBM

## 关键开放问题

1. **wafer-level alignment**：hybrid bonding 失效率仍 depend on wafer scale
2. **BMG (Bulk Metallic Glass) 压降**：键合后的 copper recrystallization 影响 long-term reliability
3. **chip-to-wafer 与 wafer-to-wafer**：KGD/KGS 测试策略成熟度差异（chip-to-wafer 较成熟；wafer-to-wafer 仍需 KGD）
4. **3D NoC 拓扑再设计**：hybrid-bonding 时代是否需要新 3D Mesh 拓扑？port 数扩到 8+ 时 area/energy 折减
5. **DDL（Direct-to-Die Link）相关**：TSMC/IPL level DDLC/d2d 与 UCIe/BoW 对 3D NoC 的影响 — 是另一主题，应分开

# Citations

[1] [raw/articles/3d-noc-study-03-hybrid-bonding.md](raw/articles/3d-noc-study-03-hybrid-bonding.md) — Layer 1 学习笔记
[2] IEEE ECTC 2017–2025 历年 proceedings
[3] TSMC SoIC, Samsung X-Cube, Intel Foveros 公开白皮书
