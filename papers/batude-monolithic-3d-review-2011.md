---
type: Summary
title: 'Monolithic 3D: A New Era of Integration (and Earlier Source Lines, e.g., Batude et al. ICCAD 2011)'
description: 2011 前后 3D 集成路线对比原典：Monolithic vs TSV-based 的根本差异在于氧化物隔离层 vs 大 pitch KOZ；Monolithic 优势在密度/KOZ/带宽，劣势在工艺成熟/晶圆级良率/堆叠层数
tags:
- 3d
- monolithic
- tsv
- sequential-integration
- integration
- interconnect
- architecture
timestamp: '2026-07-31T00:00:00Z'
created: '2026-07-31'
sources:
- raw/articles/3d-noc-study-02-monolithic-vs-tsv.md
---

# Monolithic 3D: A New Era of Integration

**Authors:** (综述作者多变；早期代表作) Max M. Batude (CEA-Leti, France) et al., ICCAD 2011（*Demonstration of low temperature 3D sequential integration* 及其系列）

**Venue:** ICCAD 2011 之后多个 IEEE/IEDM 后续，连续代表 2012 (IEDM)、2014 (IEDM)、2017 (IEDM)。综述代表：Batude et al. 2017 IEEE/ACM *More-than-Moore* 节点综述。

## 一句话总结

Monolithic 3D 不是"更密的 TSV"——它**根本不是 TSV**。它是**层间纳米级互连**（微凸点 + 氧化物隔离层 + 常温键合），将堆叠层从"垂直导线 + KOZ"解放到"接近晶体管密度"。代价是工艺成熟度与晶圆级良率均显著逊于 TSV-based HBM/SoIC。

## 核心贡献

### 1. 与 TSV 路线对比

| 维度 | TSV-Based (via-middle) | Monolithic 3D |
|------|------------------------|---------------|
| **互连尺度** | 直径 ~1–10 μm；间距 ~5–20 μm | 微凸点（hybrid bonding Cu-Cu）或 nano-TSV，间距 ~100 nm–1 μm |
| **每 mm² TSV/microbump 数** | ~10K–100K TSVs | ~10M+ 比微凸点（hybrid）|
| **KOZ** | 必要（0.2–5 μm） | 无（层间直接晶体管对晶体管）|
| **工艺成熟** | HBM 现役；SoIC/SolC 出货 | 流片少；工艺不标准化 |
| **堆叠层数（典型）** | 2–8 (HBM3 = 12 层 DRAM) | 实验性 2–4 层；产品多为 2 层 |
| **热预算** | 单层独立 thermal | 顶层制程温度受限 → 低温（< 400 °C）层处理 |
| **功耗密度** | TSV 是"热导管"，上温升高 | 类似，无 KOZ 但堆叠更密 |
| **主要采用者** | TSMC SoIC, Samsung HBM, AMD 3D V-Cache | 实验为主：CEA-Leti, Imec, Tel, IBM Research, MIT |

### 2. Monolithic 关键创新点

- **层间互连密度 +10–100×**：1 μm pitch 的 hybrid-bonding 凸点已商用；micro-TSV 间距 ~200 nm 论文级
- **层间晶体管+互连连续**：上层制程在已制造的底层**顶面**上，且上层只能承受低温 → 必须低温沉积 poly-Si 或 transition metal dichalcogenide
- **KOZ → 0**：层间紧密到晶体管级，**面积利用率接近纯平面 2D** — 是唯一能保住 "3D with same footprint as 2D" 的路线
- **延迟 vs 水平互连**：在同一晶圆上 sequential integration 路径短于传统 2D 全局互连 → **网络直径减半、能耗约减至 1/2**

### 3. 3D NoC 的根本影响

对 3D NoC 而言，monolithic 路线提供：

1. **垂直 port 数不稀缺**：传统 3D Mesh 一个 tile 5–6 个 port 主要瓶颈是 KOZ+水平布线；monolithic 让垂直 port 可达 6–8
2. **partial / sparse 垂直连接的代价降低**：3D Mesh 想"少垂直链路去减小端口" 实际是用 TSV 节省；monolithic 反过来 "能多就多"
3. **3D NoC router 可继续用 2D NoC 路由器 IP 核**：层间互连足够快且密集 → 不必为 3D 重写 router microarchitecture

### 4. 当前 commercial 现实

| 公司 | Monolithic 3D 产品 / 实验 |
|------|-----------------------------|
| **TSMC** | SoIC（SoIC-X vs SoIC-L：L 用 hybrid bonding，等价于 monolithic-style 尺度）|
| **Samsung** | X-Cube（hybrid bonding）|
| **AMD** | 3D V-Cache（via-middle TSV, 不是 monolithic）|
| **Intel** | Foveros（hybrid bonding + active interposer） |
| **MIT/CEA/Imec** | academia 试验纯 monolithic 3D |

**注解**：商业产品严格意义上没"纯 monolithic"——实际是 **hybrid bonding 衔接的 via-middle/micro-bump**。学术 monolithic 主要由 CEA-Leti、Imec、IBM Research、MIT、Stanford 在跑实验。

## 与 wiki 既有页面的关联

- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — 物理层基础
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — TSV / Monolithic / Hybrid 三路线对比
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 在 3D 集成上跑 LLM 的 Voxel 视角
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Packaging 三路之一即此处
- [DRAM Memory System](/concepts/dram-memory-system.md) — HBM 即 TSV-based 现实主流

## 关键开放问题

1. **Monolithic 良率 / 测试策略**：上层堆叠前，下层必须已测（KGD ≠ KGS）
2. **低温工艺的门极等效性**：上层 poly-Si / TMDFET 与底层 Si FinFET 等价吗？
3. **3D NoC 的 tile-to-tile 重叠**：FIB-friendly 时序 vs 物理对齐抖动

# Citations

[1] [raw/articles/3d-noc-study-02-monolithic-vs-tsv.md](raw/articles/3d-noc-study-02-monolithic-vs-tsv.md) — Layer 1 学习笔记
[2] Batude et al., *3D Sequential Integration: A Technology Roadmap*, IEEE/ACM (多年综述)
[3] IEEE/ACM IEDM 历年关于 monolithic 3D 的实验报告
